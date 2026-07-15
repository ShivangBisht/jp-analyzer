from __future__ import annotations

import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

VERSION = "9.0.0-alpha1-readonly"
_FEATURE_RE = re.compile(r"<([^<>]+)>")
_REL_RE = re.compile(r'^rel type="([^"]+)" target="([^"]*)"(?: sid="([^"]*)")?(?: id="([^"]*)")?/?$')
_HEADER_RE = re.compile(r"^([*+])\s+(-?\d+)([A-Z])?(?:\s+(.*))?$")

# KWJA may normalize source punctuation in the morpheme surface column.
_SURFACE_ALIASES = {
    "~": ("～", "~"),
    "......": ("……", "...", "......"),
    "?": ("？", "?"),
    "!": ("！", "!"),
    ".": ("．", "."),
    "-": ("−", "-"),
}


@dataclass
class _Morpheme:
    surface: str
    reading: str
    lemma: str
    pos: str
    pos_id: str
    subpos: str
    subpos_id: str
    conjugation_type: str
    conjugation_type_id: str
    conjugation_form: str
    conjugation_form_id: str
    semantic: str = ""
    features: list[str] = field(default_factory=list)
    start: int | None = None
    end: int | None = None
    aligned_surface: str | None = None


@dataclass
class _BasicPhrase:
    index: int
    destination: int
    dependency_type: str
    features: list[str]
    morphemes: list[_Morpheme] = field(default_factory=list)


@dataclass
class _Bunsetsu:
    index: int
    destination: int
    dependency_type: str
    features: list[str]
    basic_phrases: list[_BasicPhrase] = field(default_factory=list)


def _extract_features(text: str) -> list[str]:
    return _FEATURE_RE.findall(text or "")


def _parse_morpheme(line: str) -> _Morpheme | None:
    # KNP guarantees 12 fixed whitespace-separated fields; semantic/features follow.
    fields = line.split(maxsplit=11)
    if len(fields) < 11:
        return None
    semantic = fields[11] if len(fields) > 11 else ""
    return _Morpheme(
        surface=fields[0], reading=fields[1], lemma=fields[2], pos=fields[3],
        pos_id=fields[4], subpos=fields[5], subpos_id=fields[6],
        conjugation_type=fields[7], conjugation_type_id=fields[8],
        conjugation_form=fields[9], conjugation_form_id=fields[10],
        semantic=semantic, features=_extract_features(semantic),
    )


def parse_knp(text: str) -> dict[str, Any]:
    bunsetsu: list[_Bunsetsu] = []
    current_b: _Bunsetsu | None = None
    current_bp: _BasicPhrase | None = None
    metadata: dict[str, Any] = {}
    diagnostics: list[dict[str, Any]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line == "EOS":
            continue
        if line.startswith("#"):
            metadata["header"] = line
            m = re.search(r"kwja:([^\s]+)", line)
            if m:
                metadata["kwja_version"] = m.group(1)
            continue
        hm = _HEADER_RE.match(line)
        if hm:
            kind, destination, dep_type, remainder = hm.groups()
            features = _extract_features(remainder or "")
            if kind == "*":
                current_b = _Bunsetsu(len(bunsetsu), int(destination), dep_type or "D", features)
                bunsetsu.append(current_b)
                current_bp = None
            else:
                if current_b is None:
                    diagnostics.append({"severity":"error","code":"KWJA_BASIC_PHRASE_WITHOUT_BUNSETSU","line":line})
                    continue
                current_bp = _BasicPhrase(sum(len(x.basic_phrases) for x in bunsetsu), int(destination), dep_type or "D", features)
                current_b.basic_phrases.append(current_bp)
            continue
        if current_bp is None:
            diagnostics.append({"severity":"warning","code":"KWJA_MORPHEME_WITHOUT_BASIC_PHRASE","line":line})
            continue
        morpheme = _parse_morpheme(line)
        if morpheme is None:
            diagnostics.append({"severity":"warning","code":"KWJA_UNPARSED_LINE","line":line})
        else:
            current_bp.morphemes.append(morpheme)
    return {"metadata": metadata, "bunsetsu": bunsetsu, "diagnostics": diagnostics}


def _candidate_surfaces(surface: str) -> tuple[str, ...]:
    return _SURFACE_ALIASES.get(surface, (surface,))


def align_to_source(source: str, bunsetsu: list[_Bunsetsu]) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    cursor = 0
    for b in bunsetsu:
        for bp in b.basic_phrases:
            for m in bp.morphemes:
                candidates = _candidate_surfaces(m.surface)
                matched = None
                for candidate in sorted(candidates, key=len, reverse=True):
                    if source.startswith(candidate, cursor):
                        matched = candidate
                        break
                if matched is None:
                    # Strict monotonic recovery: search only a short forward window and
                    # report skipped source; never align backward or silently guess.
                    hits = [(source.find(x, cursor, min(len(source), cursor + 12)), x) for x in candidates]
                    hits = [(i, x) for i, x in hits if i >= 0]
                    if hits:
                        start, matched = min(hits, key=lambda z: z[0])
                        if start > cursor:
                            diagnostics.append({
                                "severity":"warning", "code":"KWJA_ALIGNMENT_SOURCE_GAP",
                                "start":cursor, "end":start, "surface":source[cursor:start],
                                "kwja_surface":m.surface,
                            })
                        cursor = start
                    else:
                        diagnostics.append({
                            "severity":"error", "code":"KWJA_ALIGNMENT_FAILED",
                            "source_cursor":cursor, "kwja_surface":m.surface,
                        })
                        continue
                m.start = cursor
                m.end = cursor + len(matched)
                m.aligned_surface = source[m.start:m.end]
                cursor = m.end
    if cursor != len(source):
        diagnostics.append({
            "severity":"error", "code":"KWJA_ALIGNMENT_TRAILING_SOURCE",
            "start":cursor, "end":len(source), "surface":source[cursor:],
        })
    return diagnostics


def _span(morphemes: list[_Morpheme], source: str) -> dict[str, Any] | None:
    aligned = [m for m in morphemes if m.start is not None and m.end is not None]
    if not aligned:
        return None
    start, end = min(m.start for m in aligned), max(m.end for m in aligned)
    return {"start":start, "end":end, "surface":source[start:end]}


def _feature_values(features: list[str], prefix: str) -> list[str]:
    return [x.split(":", 1)[1] for x in features if x.startswith(prefix + ":")]


def normalize_kwja(source: str, raw_knp: str, *, model_size: str = "base", elapsed_ms: float | None = None) -> dict[str, Any]:
    parsed = parse_knp(raw_knp)
    bunsetsu: list[_Bunsetsu] = parsed["bunsetsu"]
    alignment_diagnostics = align_to_source(source, bunsetsu)
    morphemes: list[dict[str, Any]] = []
    basic_phrases: list[dict[str, Any]] = []
    bunsetsu_rows: list[dict[str, Any]] = []
    dependencies: list[dict[str, Any]] = []
    predicates: list[dict[str, Any]] = []
    arguments: list[dict[str, Any]] = []
    entities: list[dict[str, Any]] = []
    clauses: list[dict[str, Any]] = []
    modalities: list[dict[str, Any]] = []
    discourse: list[dict[str, Any]] = []

    bp_index = 0
    for b in bunsetsu:
        b_morphs = [m for bp in b.basic_phrases for m in bp.morphemes]
        bspan = _span(b_morphs, source)
        if bspan:
            bunsetsu_rows.append({
                "id":f"kwb{b.index}", **bspan,
                "destination_bunsetsu_id": None if b.destination < 0 else f"kwb{b.destination}",
                "dependency_type":b.dependency_type, "features":b.features,
            })
        for bp in b.basic_phrases:
            span = _span(bp.morphemes, source)
            if not span:
                bp_index += 1
                continue
            bp_id = f"kwbp{bp_index}"
            all_features = list(dict.fromkeys(bp.features + b.features))
            basic_phrases.append({
                "id":bp_id, **span, "bunsetsu_id":f"kwb{b.index}",
                "destination_basic_phrase_id":None if bp.destination < 0 else f"kwbp{bp.destination}",
                "dependency_type":bp.dependency_type, "features":all_features,
            })
            if bp.destination >= 0:
                dependencies.append({
                    "id":f"kwdep{len(dependencies)}", "from_basic_phrase_id":bp_id,
                    "to_basic_phrase_id":f"kwbp{bp.destination}", "dependency_type":bp.dependency_type,
                    **span,
                })
            for m in bp.morphemes:
                if m.start is None:
                    continue
                mid = f"kwm{len(morphemes)}"
                morphemes.append({
                    "id":mid, "start":m.start, "end":m.end, "surface":m.aligned_surface,
                    "kwja_surface":m.surface, "reading":m.reading, "lemma":m.lemma,
                    "pos":m.pos, "pos_id":m.pos_id, "subpos":m.subpos,
                    "subpos_id":m.subpos_id, "conjugation_type":m.conjugation_type,
                    "conjugation_form":m.conjugation_form, "features":m.features,
                    "basic_phrase_id":bp_id,
                    "authority":{"range":True,"reading":False,"lemma_requires_corroboration":True},
                })
            predicate_types = _feature_values(all_features, "用言")
            if predicate_types:
                predicates.append({
                    "id":f"kwp{len(predicates)}", **span, "basic_phrase_id":bp_id,
                    "predicate_types":predicate_types,
                    "state":"state" if "状態述語" in all_features else ("dynamic" if "動態述語" in all_features else None),
                    "tense":_feature_values(all_features,"時制"),
                    "negative":"否定表現" in all_features,
                    "potential":"可能表現" in all_features,
                    "politeness":[x for x in all_features if x.startswith("敬語:")],
                    "evidence_only":True,
                })
            for feature in all_features:
                rm = _REL_RE.match(feature)
                if rm:
                    rel_type, target, sid, target_id = rm.groups()
                    arguments.append({
                        "id":f"kwa{len(arguments)}", **span, "predicate_basic_phrase_id":bp_id,
                        "relation_type":rel_type, "target_surface":target,
                        "target_sentence_id":sid, "target_kwja_id":target_id,
                        "status":"proposal", "requires_corroboration":True,
                    })
                if feature.startswith("NE:"):
                    parts = feature.split(":", 2)
                    named_surface = parts[2] if len(parts) == 3 else span["surface"]
                    loc = source.find(named_surface, span["start"], span["end"])
                    if loc >= 0:
                        entities.append({
                            "id":f"kwe{len(entities)}", "start":loc, "end":loc+len(named_surface),
                            "surface":named_surface, "entity_type":parts[1],
                            "source_basic_phrase_id":bp_id, "evidence_only":True,
                        })
                if feature.startswith("節-"):
                    clauses.append({
                        "id":f"kwc{len(clauses)}", **span, "basic_phrase_id":bp_id,
                        "feature":feature, "evidence_only":True,
                    })
                if feature.startswith("モダリティ-"):
                    modalities.append({
                        "id":f"kwmod{len(modalities)}", **span, "basic_phrase_id":bp_id,
                        "feature":feature, "evidence_only":True,
                    })
                if feature.startswith("談話関係:"):
                    discourse.append({
                        "id":f"kwdis{len(discourse)}", **span, "basic_phrase_id":bp_id,
                        "feature":feature, "evidence_only":True,
                    })
            bp_index += 1

    diagnostics = parsed["diagnostics"] + alignment_diagnostics
    complete = not any(x.get("severity") == "error" for x in diagnostics)
    return {
        "kwja_metadata_alpha1": {
            "available":True, "layer_version":VERSION, "kwja_version":parsed["metadata"].get("kwja_version"),
            "model_size":model_size, "elapsed_ms":elapsed_ms, "source_alignment_complete":complete,
            "read_only":True,
        },
        "kwja_morphemes_alpha1":morphemes,
        "kwja_bunsetsu_alpha1":bunsetsu_rows,
        "kwja_basic_phrases_alpha1":basic_phrases,
        "kwja_dependencies_alpha1":dependencies,
        "kwja_predicate_phrases_alpha1":predicates,
        "kwja_argument_evidence_alpha1":arguments,
        "kwja_entities_alpha1":entities,
        "kwja_clause_features_alpha1":clauses,
        "kwja_modality_features_alpha1":modalities,
        "kwja_discourse_relations_alpha1":discourse,
        "kwja_alignment_diagnostics_alpha1":diagnostics,
        "kwja_contract_alpha1": {
            "evidence_only":True, "source_text_immutable":True, "ginza_layers_immutable":True,
            "existing_resolver_immutable":True, "readings_non_authoritative":True,
            "lemmas_require_corroboration":True, "arguments_require_corroboration":True,
            "orthography_controls_punctuation":True,
        },
    }


def run_kwja(text: str, *, executable: str | None = None, model_size: str = "base", timeout_seconds: int = 300) -> tuple[str, float]:
    exe = executable or os.getenv("KWJA_EXE")
    if not exe:
        raise RuntimeError("Set KWJA_EXE to the isolated KWJA executable path.")
    path = Path(exe)
    if not path.exists():
        raise FileNotFoundError(f"KWJA executable not found: {path}")
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    started = time.perf_counter()
    result = subprocess.run(
        [str(path), "--model-size", model_size, "--text", text],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        timeout=timeout_seconds, env=env,
    )
    elapsed = (time.perf_counter() - started) * 1000
    return result.stdout.decode("utf-8", errors="strict"), elapsed


def analyze_kwja_alpha1(text: str, *, raw_knp: str | None = None, executable: str | None = None) -> dict[str, Any]:
    if raw_knp is None:
        raw_knp, elapsed = run_kwja(text, executable=executable)
    else:
        elapsed = None
    return normalize_kwja(text, raw_knp, model_size="base", elapsed_ms=elapsed)


def attach_kwja_read_only(existing_analysis: dict[str, Any], kwja_layer: dict[str, Any]) -> dict[str, Any]:
    """Return a new object and prove that pre-existing fields are retained unchanged."""
    result = dict(existing_analysis)
    collision = set(result).intersection(kwja_layer)
    if collision:
        raise ValueError(f"KWJA layer would overwrite existing fields: {sorted(collision)}")
    result.update(kwja_layer)
    result["phase9_alpha1_contract"] = {
        "read_only":True, "existing_field_count":len(existing_analysis),
        "kwja_field_count":len(kwja_layer), "overwritten_fields":[],
    }
    return result


analyze = analyze_kwja_alpha1
