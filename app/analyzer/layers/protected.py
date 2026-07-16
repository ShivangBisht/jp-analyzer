from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any
import unicodedata

from .morphology import analyze_layered as analyze_alpha21

HONORIFICS={"さん","くん","君","ちゃん","様","さま","氏","先生","先輩","殿","ちゃん"}
CONTENT_POS={"NOUN","VERB","ADJ","ADV","INTJ","PROPN","PRON"}
FUNCTION_DEPS={"fixed","aux","cop"}


def _snapshot(items:list[dict[str,Any]])->str:
    payload=repr([(x.get('id'),x.get('start'),x.get('end'),x.get('surface'),x.get('lemma'),x.get('pos'),x.get('tag')) for x in items])
    return sha256(payload.encode('utf-8')).hexdigest()


def _is_punct(m:dict[str,Any])->bool:
    surface=m['surface']; tag=m.get('tag','')
    return tag.startswith('補助記号') or m.get('pos') in {'PUNCT','SYM'} or (surface and all(unicodedata.category(c).startswith('P') or c in '─—―…⋯〜～' for c in surface))


def orthography(text,ms):
    out=[]; i=0
    while i<len(ms):
        if not _is_punct(ms[i]): i+=1; continue
        start=ms[i]['start']; end=ms[i]['end']; ids=[ms[i]['id']]; j=i+1
        while j<len(ms) and _is_punct(ms[j]) and ms[j]['start']==end:
            # group identical/repeated dash or ellipsis classes; quotes remain independent
            a=text[start:end]; b=ms[j]['surface']
            repeatable=all(c in '─—―…⋯' for c in a+b)
            if not repeatable: break
            end=ms[j]['end']; ids.append(ms[j]['id']); j+=1
        out.append({'id':f'o{len(out)}','start':start,'end':end,'surface':text[start:end],'role':'punctuation','morpheme_ids':ids,'confidence':1.0,'evidence':[{'source':'orthographic-tag','detail':'補助記号/Unicode punctuation'}]})
        i=j
    return out


def person_references(text,ms,base_entities):
    out=[]; consumed=set()
    for i,m in enumerate(ms):
        if '固有名詞-人名' not in m.get('tag',''): continue
        start=m['start']; end=m['end']; ids=[m['id']]; title=None
        if i+1<len(ms) and ms[i+1]['start']==end and (ms[i+1]['surface'] in HONORIFICS or ms[i+1].get('tag','').startswith('接尾辞-名詞的')):
            title=ms[i+1]['surface']; end=ms[i+1]['end']; ids.append(ms[i+1]['id'])
        out.append({'id':f'person{len(out)}','start':start,'end':end,'surface':text[start:end],'base_name':m['surface'],'title':title,'morpheme_ids':ids,'protected':True,'confidence':.96,'evidence':[{'source':'morphology','detail':m['tag']},{'source':'entity-composition','detail':'adjacent honorific' if title else 'person-name tag'}]})
        consumed.update(ids)
    return out


def alpha3_grammar(text,ms,predicates,existing):
    out=deepcopy(existing)
    covered={(g['start'],g['end'],g['grammar_id']) for g in out}
    def add(a,b,gid,canonical,function,conf,priority,ids):
        key=(a,b,gid)
        if key in covered:return
        out.append({'id':f'ag{len(out)}','start':a,'end':b,'surface':text[a:b],'grammar_id':gid,'canonical_form':canonical,'function':function,'host_predicate_id':None,'morpheme_ids':ids,'confidence':conf,'priority':priority,'evidence':[{'source':'alpha3-grammar-pattern','detail':canonical,'confidence':conf}]});covered.add(key)
    # longest licensed surface families first
    surfaces=[
      ('じゃありません','NEGATIVE_COPULA_POLITE','ではありません','polite-negative-copula',.98,120),
      ('ではありません','NEGATIVE_COPULA_POLITE','ではありません','polite-negative-copula',.98,120),
      ('じゃなかった','NEGATIVE_COPULA_PAST','ではなかった','past-negative-copula',.97,115),
      ('ていた','TE_IRU_PAST','Vていた','progressive-resultative-past',.96,110),
      ('でいた','DE_IRU_PAST','Vでいた','progressive-resultative-past',.96,110),
      ('ている','TE_IRU','Vている','progressive-resultative',.96,105),
      ('でいる','DE_IRU','Vでいる','progressive-resultative',.96,105),
      ('ように','YOU_NI','Vように','manner-similarity-purpose',.91,90),
      ('けれど','KEREDO','けれど','concessive-connective',.95,90),
    ]
    for surf,gid,can,fun,conf,pri in surfaces:
        p=0
        while True:
            p=text.find(surf,p)
            if p<0:break
            e=p+len(surf); ids=[m['id'] for m in ms if p<=m['start'] and m['end']<=e]
            add(p,e,gid,can,fun,conf,pri,ids);p=e
    # Remove no evidence: keep old matches, but projection will select longest/highest.
    return out


def predicate_relations(ms,preds,base_relations,grammar):
    out=deepcopy(base_relations); bym={m['id']:m for m in ms}; byp={p['head_morpheme_id']:p for p in preds}
    for r in out:
        frm=next((p for p in preds if p['id']==r['from_predicate_id']),None)
        if not frm:continue
        m=bym[frm['head_morpheme_id']]
        # Taxonomy is annotation only; the original UD evidence remains.
        if m.get('pos')=='ADJ' and next((p for p in preds if p['id']==r['to_predicate_id'] and p['headword']=='なる'),None):
            r['semantic_relation']='result-state'
        else:
            marker = r.get('marker_range') or {}
            if marker.get('surface') == 'けれど':
                r['semantic_relation'] = 'concessive'
            elif marker.get('surface') in {'て', 'で'}:
                r['semantic_relation'] = 'sequential-or-coordinate'
            else:
                g = next((g for g in grammar if g['start'] == m['end'] and g['grammar_id'] == 'YOU_NI'), None)
                r['semantic_relation'] = 'manner-similarity' if g else 'direct-subordinate'
            r['relation_evidence'] = 'alpha3-taxonomy'
            continue
        r['relation_evidence']='alpha3-taxonomy'
    return out


def lexical_proposals(text,ms,persons,grammar,orth):
    blocked_person=[(x['start'],x['end']) for x in persons]
    blocked_punct=[(x['start'],x['end']) for x in orth]
    grammar_ranges=[(g['start'],g['end']) for g in grammar]
    title_ids={mid for p in persons for mid in p['morpheme_ids'][1:]}
    out=[]
    for p in persons:
        out.append({'id':f'al{len(out)}','start':p['start'],'end':p['end'],'surface':p['surface'],'headword':p['base_name'],'lexical_type':'proper-name','morpheme_ids':p['morpheme_ids'],'confidence':p['confidence'],'evidence':[{'source':'person-reference','detail':p['id']}]})
    for m in ms:
        a,b=m['start'],m['end']
        if m['id'] in title_ids or _is_punct(m):continue
        if any(x<=a and b<=y for x,y in blocked_person):continue
        if m.get('pos') not in CONTENT_POS:continue
        if m.get('dependency') in FUNCTION_DEPS:continue
        if any(x<=a and b<=y for x,y in grammar_ranges):continue
        out.append({'id':f'al{len(out)}','start':a,'end':b,'surface':m['surface'],'headword':m['lemma'],'normalized_headword':m['normalized'],'lexical_type':'term','morpheme_ids':[m['id']],'confidence':.84,'evidence':[{'source':'alpha3-lexical-policy','detail':f"{m['pos']}/{m['dependency']}"}]})
    return out


def dictionary_candidates(ms,lexical):
    byid={m['id']:m for m in ms};out=[]
    for l in lexical:
        if l['lexical_type']!='term':continue
        m=byid[l['morpheme_ids'][0]];forms=[]
        for f in (m['surface'],m['lemma'],m['normalized']):
            if f and f not in forms:forms.append(f)
        out.append({'id':f'adc{len(out)}','start':l['start'],'end':l['end'],'surface':l['surface'],'lookup_forms':forms,'candidate_type':'alpha3-lexical-proposal','protected_boundary_safe':True,'evidence':[{'source':'alpha3-lexical-policy','detail':'content lexeme outside grammar/name/punctuation'}]})
    return out


def project(text,ms,orth,persons,grammar,lexical):
    claims=[None]*len(text);decisions=[]
    def put(a,b,role,pri,source,head=None,gid=None,conf=1):
        for i in range(a,b):
            claim={'priority':pri,'role':role,'headword':head,'grammar_id':gid,'confidence':conf,'source':source}
            if claims[i] is None or pri>claims[i]['priority']:claims[i]=claim
    for m in ms:
        if m.get('pos') in {'ADP','PART','AUX','SCONJ'}:put(m['start'],m['end'],'particle',30,'morphology')
    for l in lexical:put(l['start'],l['end'],'proper-name' if l['lexical_type']=='proper-name' else 'term',80 if l['lexical_type']=='proper-name' else 60,l['id'],l['headword'],None,l['confidence'])
    # grammar overlaps are resolved longest/highest, not by deleting other matches
    for g in sorted(grammar,key=lambda x:(x['priority'],x['end']-x['start'])):put(g['start'],g['end'],'grammar',150+g['priority'],g['id'],None,g['grammar_id'],g['confidence'])
    for o in orth:put(o['start'],o['end'],'punctuation',300,o['id'],None,None,1)
    for i in range(len(text)):
        if claims[i] is None:claims[i]={'priority':0,'role':'unresolved','headword':None,'grammar_id':None,'confidence':0,'source':'none'}
    out=[];a=0
    def same(x,y):return all(x[k]==y[k] for k in ('role','headword','grammar_id','confidence','source'))
    for i in range(1,len(text)+1):
        if i==len(text) or not same(claims[a],claims[i]):
            c=claims[a];cid=f'rd{len(decisions)}';decisions.append({'id':cid,'start':a,'end':i,'surface':text[a:i],'selected_role':c['role'],'selected_source':c['source'],'reason':'highest applicable projection priority; source annotations preserved','confidence':c['confidence']})
            out.append({'start':a,'end':i,'surface':text[a:i],'role':c['role'],'headword':c['headword'],'grammar_id':c['grammar_id'],'confidence':c['confidence'],'evidence_ids':[c['source'],cid]});a=i
    return out,decisions


def analyze_layered_alpha3(text,nlp,dictionary_evidence=None):
    base=analyze_alpha21(text,nlp,dictionary_evidence)
    result=deepcopy(base.model_dump())
    ms=deepcopy(result['morphemes']); before=_snapshot(ms)
    orth=orthography(text,ms); persons=person_references(text,ms,result['entities']); grammar=alpha3_grammar(text,ms,result['predicates'],result['grammar_matches'])
    relations=predicate_relations(ms,result['predicates'],result['predicate_relations'],grammar)
    lexical=lexical_proposals(text,ms,persons,grammar,orth); dc=dictionary_candidates(ms,lexical); colors,decisions=project(text,ms,orth,persons,grammar,lexical)
    after=_snapshot(ms)
    diagnostics=[]
    if before!=after: diagnostics.append({'severity':'error','code':'MORPHOLOGY_MUTATED','message':'A later layer changed Layer 0 morphology.'})
    if ''.join(x['surface'] for x in colors)!=text:diagnostics.append({'severity':'error','code':'ALPHA3_COLOR_INCOMPLETE','message':'Alpha 3 projection does not reconstruct text.'})
    result.update({'version':'8.0.0-alpha3','orthographic_spans':orth,'person_references':persons,'grammar_matches_alpha3':grammar,'predicate_relations_alpha3':relations,'dictionary_candidates_alpha3':dc,'lexical_items_alpha3':lexical,'reader_decisions':decisions,'color_spans_alpha3':colors,'diagnostics_alpha3':diagnostics,'layer0_snapshot':before,'alpha3_contract':{'non_destructive':True,'earlier_layers_preserved':True,'only_reader_projection_is_exclusive':True}})
    return result

