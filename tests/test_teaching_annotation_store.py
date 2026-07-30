import json
from pathlib import Path
import pytest
from app.analyzer import teaching_annotation_store as store

S='本電子書籍を示す。'
SPANS=[{'start':0,'end':1,'surface':'本'},{'start':1,'end':3,'surface':'電子'},{'start':3,'end':5,'surface':'書籍'},{'start':5,'end':6,'surface':'を'},{'start':6,'end':8,'surface':'示す'},{'start':8,'end':9,'surface':'。'}]
def compact(rev='r0'): return {'text':S,'analyzerVersion':'test','engineVersion':'e','schemaVersion':'1','readerSpanSchemaVersion':'1.1','readerCandidateSchemaVersion':'2','correctionRevision':rev,'readerSpans':SPANS,'readerCandidates':[],'readerSelection':{}}
def test_snapshot_deduplicates(tmp_path):
 p=tmp_path/'a.sqlite3'; a=store.save_snapshot({'text':S},compact(),db_path=p); b=store.save_snapshot({'text':S},compact(),db_path=p)
 assert a==b and store.corpus_status(p)['snapshotCount']==1

def test_annotation_partial_coverage_and_restart(tmp_path):
 p=tmp_path/'a.sqlite3'; snap=store.save_snapshot({'text':S},compact(),db_path=p)
 ann=store.create_annotation(correction_id='c1',sentence=S,start=1,end=5,surface='電子書籍',action='mark-vocabulary',display_role='lexical',split_offsets=[],target_spans=[{'start':1,'end':5,'surface':'電子書籍'}],raw_snapshot_id=snap,effective_snapshot_id=snap,db_path=p)
 assert [x['state'] for x in ann['coverage']['regions']]==['unreviewed','reviewed-corrected','unreviewed']
 assert store.corpus_status(p)['activeAnnotationCount']==1
 assert store.find_annotation_by_correction('c1',db_path=p)['annotation_id']==ann['annotation_id']

def test_nonoverlap_same_range_supersession_and_overlap_rejection(tmp_path):
 p=tmp_path/'a.sqlite3'; snap=store.save_snapshot({'text':S},compact(),db_path=p)
 kw=dict(sentence=S,display_role='lexical',split_offsets=[],target_spans=[],raw_snapshot_id=snap,effective_snapshot_id=snap,db_path=p)
 a=store.create_annotation(correction_id='c1',start=1,end=5,surface='電子書籍',action='mark-vocabulary',**kw)
 b=store.create_annotation(correction_id='c2',start=6,end=8,surface='示す',action='mark-vocabulary',**kw)
 c=store.create_annotation(correction_id='c3',start=1,end=5,surface='電子書籍',action='show-as-one-unit',**kw)
 assert store.get_annotation(a['annotation_id'],db_path=p)['status']=='superseded'
 assert len(store.list_annotations(db_path=p))==2
 with pytest.raises(ValueError): store.create_annotation(correction_id='c4',start=3,end=6,surface='書籍を',action='show-as-one-unit',**kw)

def test_retraction_preserves_history(tmp_path):
 p=tmp_path/'a.sqlite3'; snap=store.save_snapshot({'text':S},compact(),db_path=p)
 ann=store.create_annotation(correction_id='c1',sentence=S,start=1,end=5,surface='電子書籍',action='mark-vocabulary',display_role='lexical',split_offsets=[],target_spans=[],raw_snapshot_id=snap,effective_snapshot_id=snap,db_path=p)
 result=store.retract_for_correction('c1',db_path=p)
 assert result['status']=='retracted' and result['history'][-1]['event_type']=='retracted'
 assert store.corpus_status(p)['snapshotCount']==1
