from .schema import GrammarMatch,Evidence
PATTERNS=[('V_TA_RASHII','Vた + らしい','evidential-inference',('た','らしい'),80),('TE_KURERU','Vて + くれる','benefactive',('て','くれる'),85),('TE_SHIMAU','Vて + しまう','completion-or-regret',('て','しまう'),85),('KOTO_GA_DEKIRU','Vことができる','ability',('こと','が','できる'),95)]
def detect(text,ms,preds):
 out=[]
 def host(start):
  p=[x for x in preds if x.end<=start]; return max(p,key=lambda x:x.end).id if p else None
 for gid,can,fun,seq,pri in PATTERNS:
  for i in range(len(ms)-len(seq)+1):
   w=ms[i:i+len(seq)]
   if tuple(x.lemma for x in w)!=seq: continue
   out.append(GrammarMatch(id=f'g{len(out)}',grammar_id=gid,canonical_form=can,function=fun,host_predicate_id=host(w[0].start),morpheme_ids=[x.id for x in w],start=w[0].start,end=w[-1].end,surface=text[w[0].start:w[-1].end],confidence=.94,priority=pri,evidence=[Evidence(source='grammar-pattern',detail='lemma window',confidence=.94)]))
 for m in ms:
  if m.surface in {'て','で'} and m.pos in {'SCONJ','PART'} and not any(g.start<=m.start and m.end<=g.end for g in out):
   out.append(GrammarMatch(id=f'g{len(out)}',grammar_id='V_TE',canonical_form='Vて',function='conjunctive',host_predicate_id=host(m.start),morpheme_ids=[m.id],start=m.start,end=m.end,surface=m.surface,confidence=.85,priority=40,evidence=[Evidence(source='morphology',detail='conjunctive marker',confidence=.85)]))
 # surface family because analyzers differ on negative morphology
 for surface in ('なければならない','なくてはならない'):
  p=text.find(surface)
  if p>=0:
   mids=[m.id for m in ms if p<=m.start and m.end<=p+len(surface)]
   out.append(GrammarMatch(id=f'g{len(out)}',grammar_id='NAKEREBA_NARANAI',canonical_form='なければならない',function='obligation',host_predicate_id=None,morpheme_ids=mids,start=p,end=p+len(surface),surface=surface,confidence=.98,priority=100,evidence=[Evidence(source='grammar-pattern',detail='licensed full surface',confidence=.98)]))
 return out
