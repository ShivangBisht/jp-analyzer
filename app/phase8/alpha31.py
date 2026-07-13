from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any

from .alpha3 import analyze_layered_alpha3, lexical_proposals, dictionary_candidates, project

MOTION_HEADS={"行く","来る","帰る","向かう","戻る"}
LICENSED_TRAILING={"た","ない","なかっ","ます","まし","ません","ぬ"}


def _morph_snapshot(items:list[dict[str,Any]])->str:
    payload=repr([(x.get('id'),x.get('start'),x.get('end'),x.get('surface'),x.get('lemma'),x.get('pos'),x.get('tag')) for x in items])
    return sha256(payload.encode('utf-8')).hexdigest()


def _expand_inflected_grammar(text, morphemes, grammar):
    """Add larger licensed grammar ranges. Existing grammar records remain untouched."""
    out=deepcopy(grammar); seen={(g['start'],g['end'],g['grammar_id']) for g in out}
    ms=sorted(morphemes,key=lambda x:(x['start'],x['end']))
    by_start={m['start']:i for i,m in enumerate(ms)}
    for g in list(grammar):
        idx=by_start.get(g['end'])
        if idx is None: continue
        m=ms[idx]
        if m['start']!=g['end']: continue
        # Extend only grammar families that license inflectional auxiliaries.
        if g['grammar_id'] not in {'TE_SHIMAU','TE_KURERU','TE_IRU','DE_IRU'}: continue
        if m.get('lemma') not in LICENSED_TRAILING and m.get('surface') not in LICENSED_TRAILING: continue
        end=m['end']; suffix=m['surface']; gid=g['grammar_id']+'_INFLECTED'
        key=(g['start'],end,gid)
        if key in seen: continue
        out.append({
          'id':f'a31g{len(out)}','start':g['start'],'end':end,'surface':text[g['start']:end],
          'grammar_id':gid,'canonical_form':g.get('canonical_form',g['surface'])+' + '+m.get('lemma',suffix),
          'function':g.get('function','grammar')+'-inflected','host_predicate_id':g.get('host_predicate_id'),
          'morpheme_ids':list(g.get('morpheme_ids',[]))+[m['id']], 'confidence':min(0.99,g.get('confidence',0.9)+0.02),
          'priority':g.get('priority',80)+8,
          'evidence':list(g.get('evidence',[]))+[{'source':'alpha3.1-inflection-extension','detail':f'licensed trailing auxiliary {suffix}','confidence':0.96}]
        });seen.add(key)
    return out


def _dependency_aware_basic_phrase_heads(morphemes, basic_phrases):
    byid={m['id']:m for m in morphemes}; out=[]
    for bp in basic_phrases:
        x=deepcopy(bp); mids=x.get('morpheme_ids',[]); midset=set(mids)
        candidates=[byid[i] for i in mids if i in byid]
        # Prefer ROOT or token whose syntactic head exits the phrase, then non-dependent content.
        head=next((m for m in candidates if m.get('dependency')=='ROOT'),None)
        if head is None:
            head=next((m for m in candidates if m.get('head_morpheme_id') and m.get('head_morpheme_id') not in midset and m.get('pos') not in {'ADP','AUX','PART','SCONJ','PUNCT','SYM'}),None)
        if head is None:
            head=next((m for m in candidates if m.get('dependency') not in {'fixed','aux','cop'} and m.get('pos') not in {'ADP','AUX','PART','SCONJ','PUNCT','SYM'}),None)
        x['projected_head_id']=head['id'] if head else x.get('head_id')
        x['head_projection_source']='alpha3.1-dependency-aware'
        out.append(x)
    return out


def _person_aware_projections(text, person_refs, particle_phrases, clauses, arguments):
    """Add expanded semantic ranges; never alter parser-native records."""
    pps=[]; cps=[]; aps=[]
    for p in person_refs:
        for ph in particle_phrases:
            # Native phrase may start inside composed person reference and end after it.
            if p['start'] <= ph['start'] < p['end'] and ph['end']>p['end']:
                pps.append({'id':f'a31pp{len(pps)}','start':p['start'],'end':ph['end'],'surface':text[p['start']:ph['end']],
                    'nominal_head_surface':p['surface'],'person_reference_id':p['id'],'source_particle_phrase_id':ph['id'],
                    'particle':ph.get('particle_surface'),'confidence':min(p['confidence'],ph.get('confidence',0.9)),
                    'evidence':[{'source':'alpha3.1-person-range-projection','detail':'expanded native nominal range to composed person reference'}]})
        for c in clauses:
            mr=c.get('modifies_range') or {}
            if mr and p['start']<=mr.get('start',-1)<p['end']:
                y=deepcopy(c);y['id']=f'a31cl{len(cps)}';y['projected_modifies_range']={'start':p['start'],'end':p['end'],'surface':p['surface'],'person_reference_id':p['id']};y['projection_source']='alpha3.1-person-range-projection';cps.append(y)
        for a in arguments:
            ar=a.get('source_range') or {}
            if ar and p['start']<=ar.get('start',-1)<p['end']:
                y=deepcopy(a);y['id']=f'a31arg{len(aps)}';y['projected_argument_range']={'start':p['start'],'end':max(p['end'],ar.get('end',p['end'])),'surface':text[p['start']:max(p['end'],ar.get('end',p['end']))],'person_reference_id':p['id']};y['projection_source']='alpha3.1-person-range-projection';aps.append(y)
    return pps,cps,aps


def _purpose_motion_relations(text,morphemes,predicates,relations,particle_phrases):
    out=deepcopy(relations); eyebypid={p['id']:p for p in predicates}; bymid={m['id']:m for m in morphemes}
    # Correct accidental variable name support without mutation.
    bypid=eyebypid
    for r in out:
        frm=bypid.get(r.get('from_predicate_id')); to=bypid.get(r.get('to_predicate_id'))
        if not frm or not to or to.get('headword') not in MOTION_HEADS: continue
        fm=bymid.get(frm.get('head_morpheme_id'))
        if not fm: continue
        # V continuative + に + motion predicate.
        between=text[frm['end']:to['start']]
        if fm.get('pos')=='VERB' and between=='に':
            r['semantic_relation']='purpose-motion'
            r['relation_evidence']='alpha3.1-purpose-motion'
            r['construction_surface']=text[frm['start']:to['end']]
            r['purpose_predicate_head']=frm.get('headword')
            r['motion_predicate_head']=to.get('headword')
    return out


def _validate_projection(text, spans):
    issues=[]
    if ''.join(s['surface'] for s in spans)!=text: issues.append({'severity':'error','code':'A31_COLOR_INCOMPLETE','message':'Alpha 3.1 color projection does not reconstruct source text.'})
    cursor=0
    for s in spans:
        if s['start']!=cursor or text[s['start']:s['end']]!=s['surface']:
            issues.append({'severity':'error','code':'A31_COLOR_RANGE','message':f"Invalid color span {s.get('surface')!r} at {s.get('start')}:{s.get('end')}"});break
        cursor=s['end']
    if cursor!=len(text):issues.append({'severity':'error','code':'A31_COLOR_END','message':'Alpha 3.1 projection does not end at source length.'})
    return issues


def analyze_layered_alpha31(text,nlp,dictionary_evidence=None):
    base=analyze_layered_alpha3(text,nlp,dictionary_evidence)
    result=deepcopy(base)
    ms=deepcopy(result['morphemes']); before=_morph_snapshot(ms)
    grammar=_expand_inflected_grammar(text,ms,result['grammar_matches_alpha3'])
    bpheads=_dependency_aware_basic_phrase_heads(ms,result['basic_phrases'])
    pp_proj,cl_proj,arg_proj=_person_aware_projections(text,result['person_references'],result['particle_phrases'],result['clauses'],result['arguments'])
    rels=_purpose_motion_relations(text,ms,result['predicates'],result['predicate_relations_alpha3'],result['particle_phrases'])
    lexical=lexical_proposals(text,ms,result['person_references'],grammar,result['orthographic_spans'])
    dc=dictionary_candidates(ms,lexical)
    colors,decisions=project(text,ms,result['orthographic_spans'],result['person_references'],grammar,lexical)
    after=_morph_snapshot(ms)
    diagnostics=[]
    if before!=after:diagnostics.append({'severity':'error','code':'MORPHOLOGY_MUTATED','message':'A later Alpha 3.1 layer changed Layer 0 morphology.'})
    diagnostics.extend(_validate_projection(text,colors))
    result.update({
      'version':'8.0.0-alpha3.1','grammar_matches_alpha31':grammar,'basic_phrase_head_projections':bpheads,
      'particle_phrase_projections':pp_proj,'clause_target_projections':cl_proj,'argument_range_projections':arg_proj,
      'predicate_relations_alpha31':rels,'lexical_items_alpha31':lexical,'dictionary_candidates_alpha31':dc,
      'reader_decisions_alpha31':decisions,'color_spans_alpha31':colors,'diagnostics_alpha31':diagnostics,
      'layer0_snapshot_alpha31':before,'alpha31_contract':{'non_destructive':True,'alpha3_preserved':True,'only_reader_projection_is_exclusive':True}
    })
    return result
