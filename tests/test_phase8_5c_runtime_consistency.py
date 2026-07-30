import sqlite3
import pytest
from app.analyzer import teaching_annotation_store as store

S='本電子書籍を示す。'
SPANS=[{'start':0,'end':1,'surface':'本'},{'start':1,'end':3,'surface':'電子'},{'start':3,'end':5,'surface':'書籍'},{'start':5,'end':6,'surface':'を'},{'start':6,'end':8,'surface':'示す'},{'start':8,'end':9,'surface':'。'}]
def compact(spans=SPANS): return {'text':S,'analyzerVersion':'test','engineVersion':'e','schemaVersion':'1','readerSpanSchemaVersion':'1.1','readerCandidateSchemaVersion':'2','correctionRevision':'r','readerSpans':spans,'readerCandidates':[],'readerSelection':{}}
def make(p,cid,start,end,surface,snap): return store.create_annotation(correction_id=cid,sentence=S,start=start,end=end,surface=surface,action='mark-vocabulary',display_role='lexical',split_offsets=[],target_spans=[],raw_snapshot_id=snap,effective_snapshot_id=snap,db_path=p)

def test_preflight_allows_nonoverlap_and_rejects_containment(tmp_path):
 p=tmp_path/'c.sqlite3'; snap=store.save_snapshot({'text':S},compact(),db_path=p); make(p,'c1',1,5,'電子書籍',snap)
 assert store.preflight_annotation_range(S,6,8,db_path=p)['conflicts']==[]
 with pytest.raises(ValueError): store.preflight_annotation_range(S,0,6,db_path=p)

def test_post_outcome_records_colour_and_learning_fields(tmp_path):
 p=tmp_path/'c.sqlite3'; snap=store.save_snapshot({'text':S},compact(),db_path=p); ann=make(p,'c1',1,5,'電子書籍',snap)
 corrected=dict(compact()); corrected['readerSpans']=[{'start':0,'end':1,'surface':'本'},{'start':1,'end':5,'surface':'電子書籍','displayRole':'lexical','knownLookupKey':'電子書籍','frequencyLookupKey':'電子書籍','countsForComprehension':True,'showInNewWords':True,'eligibleForMining':True,'colorPolicy':'known-or-frequency','unknownColorPolicy':'frequency'},{'start':5,'end':6,'surface':'を'},{'start':6,'end':8,'surface':'示す'},{'start':8,'end':9,'surface':'。'}]
 post=store.save_snapshot({'text':S},corrected,kind='post-correction',raw_baseline_snapshot_id=snap,db_path=p)
 result=store.update_derived_outcome(ann['annotation_id'],post,corrected,1,5,db_path=p)['derived_outcome']
 assert result['derivationStatus']=='complete' and result['colourSource']=='known-or-frequency'
 assert result['knownLookupKey']=='電子書籍' and result['eligibleForMining'] is True

def test_integrity_report_is_read_only(tmp_path):
 p=tmp_path/'c.sqlite3'; snap=store.save_snapshot({'text':S},compact(),db_path=p); make(p,'missing-correction',1,5,'電子書籍',snap)
 report=store.integrity_report([],db_path=p)
 assert report['ok'] is False and report['issues'][0]['code']=='ACTIVE_ANNOTATION_MISSING_CORRECTION'
 assert store.corpus_status(p)['activeAnnotationCount']==1
