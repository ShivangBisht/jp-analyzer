from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    source:str; detail:str; confidence:float=1.0
class Range(BaseModel):
    start:int; end:int; surface:str
class Morpheme(Range):
    id:str; lemma:str; normalized:str; reading:str|None=None; pos:str; tag:str
    dependency:str|None=None; head_id:str|None=None; conjugation:list[str]=Field(default_factory=list)
class ParticlePhrase(Range):
    id:str; nominal_morpheme_ids:list[str]; particle_morpheme_ids:list[str]; nominal_head_id:str
    particle_surface:str; particle_type:str; evidence:list[Evidence]=Field(default_factory=list)
class BasicPhrase(Range):
    id:str; morpheme_ids:list[str]; head_id:str|None=None; phrase_type:str='basic-phrase'
    evidence:list[Evidence]=Field(default_factory=list)
class EntitySpan(Range):
    id:str; entity_type:str; entity_class:Literal['proper-name','semantic-category','temporal','other']='other'
    protected:bool=False; morpheme_ids:list[str]=Field(default_factory=list); evidence:list[Evidence]=Field(default_factory=list)
class Predicate(Range):
    id:str; head_morpheme_id:str; headword:str; morpheme_ids:list[str]; predicate_type:str='lexical'
    evidence:list[Evidence]=Field(default_factory=list)
class Argument(BaseModel):
    id:str; predicate_id:str; phrase_id:str|None=None; source_range:Range; role:str; marker:str|None=None
    inherited:bool=False; confidence:float=.7; evidence:list[Evidence]=Field(default_factory=list)
class PredicateRelation(BaseModel):
    id:str; from_predicate_id:str; to_predicate_id:str; marker_range:Range|None=None; relation:str
    confidence:float=.7; evidence:list[Evidence]=Field(default_factory=list)
class Clause(Range):
    id:str; clause_type:str; predicate_ids:list[str]; modifies_range:Range|None=None
    evidence:list[Evidence]=Field(default_factory=list)
class GrammarMatch(Range):
    id:str; grammar_id:str; canonical_form:str; function:str; host_predicate_id:str|None=None
    morpheme_ids:list[str]; confidence:float; priority:int=50; evidence:list[Evidence]=Field(default_factory=list)
class DictionaryCandidate(Range):
    id:str; lookup_forms:list[str]; candidate_type:str; protected_boundary_safe:bool=True
    evidence:list[Evidence]=Field(default_factory=list)
class DictionaryEvidence(Range):
    candidate_id:str; lookup_form:str; matched_headword:str|None=None
    match_type:Literal['exact','lemma','normalized','none']='none'; source_count:int=0; source_names:list[str]=Field(default_factory=list)
    confidence:float=0.0
class LexicalItem(Range):
    id:str; headword:str; normalized_headword:str; lexical_type:Literal['term','proper-name','expression','unknown']='term'
    morpheme_ids:list[str]; confidence:float; evidence:list[Evidence]=Field(default_factory=list)
class ColorSpan(Range):
    role:Literal['term','grammar','particle','proper-name','punctuation','unresolved']; headword:str|None=None
    grammar_id:str|None=None; confidence:float=1.0; evidence_ids:list[str]=Field(default_factory=list)
class Diagnostic(BaseModel):
    severity:Literal['info','warning','error']; code:str; message:str; start:int|None=None; end:int|None=None
class LayeredAnalysis(BaseModel):
    text:str; version:str='8.0.0-alpha2.1'; morphemes:list[Morpheme]; particle_phrases:list[ParticlePhrase]
    basic_phrases:list[BasicPhrase]; entities:list[EntitySpan]; predicates:list[Predicate]; arguments:list[Argument]
    predicate_relations:list[PredicateRelation]; clauses:list[Clause]; grammar_matches:list[GrammarMatch]
    dictionary_candidates:list[DictionaryCandidate]; dictionary_evidence:list[DictionaryEvidence]=Field(default_factory=list)
    lexical_items:list[LexicalItem]; color_spans:list[ColorSpan]; diagnostics:list[Diagnostic]
    parser_metadata:dict[str,Any]=Field(default_factory=dict)
