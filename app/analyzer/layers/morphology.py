from __future__ import annotations
from .schema import *
from .grammar import detect
from .invariants import validate
PUNCT={'PUNCT','SYM'}; NOMINAL={'NOUN','PROPN','PRON','NUM'}
PROPER_NER={'Person','PERSON','Character','Company','Organization','ORG','Country','City','Facility','GPE','LOC','Product','Book'}
TEMP_NER_PREFIX=('Date','Time','Period','Duration','Age')

def morphemes(doc):
 out=[]
 for i,t in enumerate(doc):
  try: inf=list(t.morph.get('Inflection')); reading=(list(t.morph.get('Reading')) or [None])[0]
  except Exception: inf=[]; reading=None
  out.append(Morpheme(id=f'm{i}',surface=t.text,start=t.idx,end=t.idx+len(t.text),lemma=t.lemma_,normalized=t.norm_,reading=reading,pos=t.pos_,tag=t.tag_,dependency=t.dep_,head_id=f'm{t.head.i}',conjugation=inf))
 return out

def entities(doc,ms):
 out=[]; occupied=set()
 for m in ms:
  if '固有名詞-人名' in m.tag:
   out.append(EntitySpan(id=f'e{len(out)}',start=m.start,end=m.end,surface=m.surface,entity_type='Person',entity_class='proper-name',protected=True,morpheme_ids=[m.id],evidence=[Evidence(source='morphology',detail=m.tag,confidence=.95)])); occupied.update(range(m.start,m.end))
 for e in doc.ents:
  mids=[m.id for m in ms if e.start_char<=m.start and m.end<=e.end_char]
  cls='proper-name' if e.label_ in PROPER_NER else ('temporal' if e.label_.startswith(TEMP_NER_PREFIX) else 'semantic-category')
  protected=cls in {'proper-name','temporal'}
  if cls=='proper-name' and all(i in occupied for i in range(e.start_char,e.end_char)): continue
  out.append(EntitySpan(id=f'e{len(out)}',start=e.start_char,end=e.end_char,surface=e.text,entity_type=e.label_,entity_class=cls,protected=protected,morpheme_ids=mids,evidence=[Evidence(source='ginza-ner',detail=e.label_,confidence=.75)]))
 return out

def particle_phrases(text,ms):
 out=[]
 for i,m in enumerate(ms):
  if m.pos not in {'ADP','PART'} or '接続助詞' in m.tag or i==0: continue
  head=ms[i-1]
  if head.pos not in NOMINAL: continue
  out.append(ParticlePhrase(id=f'pp{len(out)}',start=head.start,end=m.end,surface=text[head.start:m.end],nominal_morpheme_ids=[head.id],particle_morpheme_ids=[m.id],nominal_head_id=head.id,particle_surface=m.surface,particle_type=m.tag,evidence=[Evidence(source='morphology',detail='nominal case/topic/focus phrase',confidence=.9)]))
 return out

def basic_phrases(text,doc,ms):
 out=[]
 try:
  import ginza
  spans=list(ginza.bunsetu_spans(doc))
  for s in spans:
   mids=[m.id for m in ms if s.start_char<=m.start and m.end<=s.end_char]
   head=next((m.id for m in reversed(ms) if m.id in mids and m.pos not in {'ADP','AUX','SCONJ','PART','PUNCT','SYM'}),None)
   out.append(BasicPhrase(id=f'bp{len(out)}',start=s.start_char,end=s.end_char,surface=s.text,morpheme_ids=mids,head_id=head,evidence=[Evidence(source='ginza-bunsetu',detail='native bunsetsu span',confidence=.85)]))
 except Exception as ex:
  # one morpheme per safe phrase is preferable to inventing large punctuation chunks
  for m in ms:
   if m.pos not in PUNCT: out.append(BasicPhrase(id=f'bp{len(out)}',start=m.start,end=m.end,surface=m.surface,morpheme_ids=[m.id],head_id=m.id,evidence=[Evidence(source='safe-fallback',detail='single morpheme phrase',confidence=.3)]))
 return out

def predicates(ms):
 return [Predicate(id=f'p{j}',start=m.start,end=m.end,surface=m.surface,head_morpheme_id=m.id,headword=m.lemma,morpheme_ids=[m.id],evidence=[Evidence(source='dependency',detail=f'{m.pos}/{m.dependency}',confidence=.8)]) for j,m in enumerate([x for x in ms if x.pos in {'VERB','ADJ'} and x.dependency not in {'aux','cop','fixed'}])]

def structure(text,ms,pps,preds):
 by={m.id:m for m in ms}; pb={p.head_morpheme_id:p for p in preds}; args=[]; rel=[]; clauses=[]
 for pp in pps:
  n=by[pp.nominal_head_id]; target=pb.get(n.head_id or '')
  if not target: continue
  role={'obj':'object','nsubj':'subject','obl':'oblique'}.get(n.dependency,'dependent')
  if role=='oblique': role={'に':'destination-or-target','で':'manner-or-location','から':'source','へ':'destination'}.get(pp.particle_surface,'oblique')
  args.append(Argument(id=f'a{len(args)}',predicate_id=target.id,phrase_id=pp.id,source_range=Range(start=pp.start,end=pp.end,surface=pp.surface),role=role,marker=pp.particle_surface,confidence=.78,evidence=[Evidence(source='ud-dependency',detail=n.dependency or '',confidence=.78)]))
 for p in preds:
  m=by[p.head_morpheme_id]; target=pb.get(m.head_id or '')
  if target and m.dependency in {'advcl','conj'}:
   marker=next((x for x in ms if x.head_id==m.id and x.pos in {'SCONJ','PART'}),None)
   rel.append(PredicateRelation(id=f'pr{len(rel)}',from_predicate_id=p.id,to_predicate_id=target.id,marker_range=Range(start=marker.start,end=marker.end,surface=marker.surface) if marker else None,relation='sequential-or-subordinate',confidence=.82,evidence=[Evidence(source='ud-dependency',detail=m.dependency,confidence=.82)]))
  if m.dependency=='acl':
   modified=by.get(m.head_id or '')
   if modified:
    start=min([x.start for x in ms if x.head_id==m.id]+[m.start]); end=max([x.end for x in ms if x.head_id==m.id]+[m.end])
    clauses.append(Clause(id=f'c{len(clauses)}',start=start,end=end,surface=text[start:end],clause_type='relative-clause',predicate_ids=[p.id],modifies_range=Range(start=modified.start,end=modified.end,surface=modified.surface),evidence=[Evidence(source='ud-acl',detail='predicate modifies nominal',confidence=.88)]))
 # conservative subject propagation from governing predicate to subordinate predicate
 subjects={a.predicate_id:a for a in args if a.role=='subject'}
 for r in rel:
  if r.from_predicate_id not in subjects and r.to_predicate_id in subjects:
   s=subjects[r.to_predicate_id]
   args.append(Argument(id=f'a{len(args)}',predicate_id=r.from_predicate_id,phrase_id=s.phrase_id,source_range=s.source_range,role='subject',marker=s.marker,inherited=True,confidence=.72,evidence=[Evidence(source='subject-propagation',detail='shared subject through predicate relation',confidence=.72)]))
 return args,rel,clauses

def dictionary_candidates(text,ms,ents,grammar):
 blocked=[(e.start,e.end) for e in ents if e.protected]+[(g.start,g.end) for g in grammar]
 out=[]
 for m in ms:
  if m.pos not in {'NOUN','VERB','ADJ','ADV','INTJ','PROPN'}: continue
  if any(e.entity_class=='proper-name' and e.protected and e.start<=m.start and m.end<=e.end for e in ents): continue
  if any(a<m.start<b or a<m.end<b for a,b in blocked): continue
  forms=[]
  for f in (m.surface,m.lemma,m.normalized):
   if f and f not in forms: forms.append(f)
  out.append(DictionaryCandidate(id=f'dc{len(out)}',start=m.start,end=m.end,surface=m.surface,lookup_forms=forms,candidate_type='morphological-lexeme',evidence=[Evidence(source='morphology',detail=m.tag,confidence=.85)]))
 return out

def resolve_lexical(text,ms,ents,grammar,cands,evidence):
 bycand={e.candidate_id:e for e in evidence}; out=[]
 for e in ents:
  if e.entity_class=='proper-name': out.append(LexicalItem(id=f'l{len(out)}',start=e.start,end=e.end,surface=e.surface,headword=e.surface,normalized_headword=e.surface,lexical_type='proper-name',morpheme_ids=e.morpheme_ids,confidence=.95,evidence=e.evidence))
 for c in cands:
  if any(x.start<=c.start and c.end<=x.end and x.entity_class=='proper-name' for x in ents): continue
  m=next(x for x in ms if x.start==c.start and x.end==c.end); ev=bycand.get(c.id)
  head=ev.matched_headword if ev and ev.matched_headword else m.lemma
  conf=max(.82,ev.confidence) if ev else .82
  out.append(LexicalItem(id=f'l{len(out)}',start=c.start,end=c.end,surface=c.surface,headword=head,normalized_headword=m.normalized,lexical_type='term',morpheme_ids=[m.id],confidence=conf,evidence=[Evidence(source='dictionary' if ev else 'morphology',detail=ev.match_type if ev else m.tag,confidence=conf)]))
 return out

def colors(text,ms,ents,grammar,lex):
 claims=[None]*len(text)
 def put(a,b,role,pri,head=None,gid=None,conf=1,eids=None):
  for i in range(a,b):
   if claims[i] is None or pri>claims[i][0]: claims[i]=(pri,role,head,gid,conf,eids or [])
 for m in ms:
  if m.pos in PUNCT: put(m.start,m.end,'punctuation',100)
  elif m.pos in {'ADP','PART','AUX','SCONJ'}: put(m.start,m.end,'particle',40)
 for l in lex: put(l.start,l.end,'proper-name' if l.lexical_type=='proper-name' else 'term',80 if l.lexical_type=='proper-name' else 60,l.headword,None,l.confidence,[l.id])
 for g in grammar: put(g.start,g.end,'grammar',200+g.priority,None,g.grammar_id,g.confidence,[g.id])
 for i in range(len(text)):
  if claims[i] is None: claims[i]=(0,'unresolved',None,None,0,[])
 out=[]; a=0
 def key(c): return c[1:]
 for i in range(1,len(text)+1):
  if i==len(text) or key(claims[i])!=key(claims[a]):
   _,role,head,gid,conf,eids=claims[a]; out.append(ColorSpan(start=a,end=i,surface=text[a:i],role=role,headword=head,grammar_id=gid,confidence=conf,evidence_ids=eids)); a=i
 return out

def analyze_layered(text,nlp,dictionary_evidence=None):
 doc=nlp(text); ms=morphemes(doc); es=entities(doc,ms); pps=particle_phrases(text,ms); bps=basic_phrases(text,doc,ms); ps=predicates(ms); args,rels,cls=structure(text,ms,pps,ps); gs=detect(text,ms,ps); dcs=dictionary_candidates(text,ms,es,gs); des=dictionary_evidence or []; ls=resolve_lexical(text,ms,es,gs,dcs,des); cs=colors(text,ms,es,gs,ls)
 r=LayeredAnalysis(text=text,morphemes=ms,particle_phrases=pps,basic_phrases=bps,entities=es,predicates=ps,arguments=args,predicate_relations=rels,clauses=cls,grammar_matches=gs,dictionary_candidates=dcs,dictionary_evidence=des,lexical_items=ls,color_spans=cs,diagnostics=[],parser_metadata={'parser':'GiNZA','split_mode':'A','architecture':'immutable-layers','dictionary_policy':'evidence-only'})
 r.diagnostics.extend(validate(r)); return r


analyze = analyze_layered
