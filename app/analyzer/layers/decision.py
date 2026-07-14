from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Iterable

ROLE_ORDER = {
    "punctuation": 90,
    "proper-name": 80,
    "grammar": 70,
    "numeral": 65,
    "discourse": 63,
    "term": 60,
    "particle": 40,
    "speech-fragment": 30,
    "unresolved": 0,
}

SPECIFIC_GRAMMAR_BONUS = {
    "TE_IRU_PAST": 18,
    "DE_IRU_PAST": 18,
    "TE_IRU_NEGATIVE": 18,
    "TE_IRU_POLITE": 18,
    "TE_MORAU_POTENTIAL": 18,
    "TE_SHIMAU_INFLECTED": 16,
    "TE_KURERU_INFLECTED": 16,
    "NAKEREBA_NARANAI": 20,
    "KOTO_GA_DEKIRU": 18,
}
GENERIC_GRAMMAR_IDS = {"TE_IRU_CHAIN", "V_TE"}


def _snapshot_morphology(items: list[dict[str, Any]]) -> str:
    payload = repr([
        (x.get("id"), x.get("start"), x.get("end"), x.get("surface"),
         x.get("lemma"), x.get("normalized"), x.get("pos"), x.get("tag"),
         x.get("dependency"), x.get("head_id"))
        for x in items
    ])
    return sha256(payload.encode("utf-8")).hexdigest()


def _valid_range(text: str, item: dict[str, Any]) -> bool:
    a, b = item.get("start"), item.get("end")
    return (
        isinstance(a, int) and isinstance(b, int) and 0 <= a < b <= len(text)
        and text[a:b] == item.get("surface")
    )


def _dictionary_by_range(dictionary_result: dict[str, Any] | None) -> dict[tuple[int, int], list[dict[str, Any]]]:
    out: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    if not dictionary_result:
        return out
    evidence = dictionary_result.get("evidence") or dictionary_result.get("dictionary_evidence") or []
    for item in evidence:
        a, b = item.get("start"), item.get("end")
        if isinstance(a, int) and isinstance(b, int):
            out[(a, b)].append(item)
    return out


def _dict_summary(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    records = list(records)
    matched = [x for x in records if x.get("matched")]
    type_counts: dict[str, int] = defaultdict(int)
    sources: set[str] = set()
    headwords: set[str] = set()
    confidence = 0.0
    pos_compatible = False
    for item in matched:
        confidence = max(confidence, float(item.get("confidence") or 0.0))
        pos_compatible = pos_compatible or (item.get("pos_compatibility") or {}).get("status") == "compatible"
        for key, value in (item.get("dictionary_type_counts") or {}).items():
            type_counts[str(key)] += int(value or 0)
        sources.update(str(x) for x in (item.get("source_names") or []))
        headwords.update(str(x) for x in (item.get("matched_headwords") or []) if x)
    return {
        "matched": bool(matched),
        "evidence_records": len(records),
        "matched_records": len(matched),
        "dictionary_type_counts": dict(type_counts),
        "source_names": sorted(sources),
        "independent_source_count": len(sources),
        "matched_headwords": sorted(headwords),
        "confidence": confidence or None,
        "pos_compatible": pos_compatible,
    }


def _specificity(candidate: dict[str, Any]) -> int:
    family = candidate["candidate_family"]
    if family == "grammar":
        gid = candidate.get("grammar_id") or ""
        if gid in SPECIFIC_GRAMMAR_BONUS:
            return 95
        if gid in GENERIC_GRAMMAR_IDS:
            return 55
        return 78
    if family == "proper-name":
        return 88 if len(candidate.get("morpheme_ids") or []) > 1 else 76
    if family in {"punctuation", "numeral", "discourse"}:
        return 85
    if family == "term":
        return 70
    if family == "particle":
        return 65
    return 30


def _completeness(candidate: dict[str, Any]) -> int:
    family = candidate["candidate_family"]
    length = candidate["end"] - candidate["start"]
    if family in {"grammar", "proper-name", "numeral", "discourse", "punctuation"}:
        return min(100, 70 + length * 3)
    return min(85, 55 + length * 2)


def _candidate_utility(candidate: dict[str, Any]) -> tuple[int, int, int, int, int, int]:
    """Lexicographic evidence dimensions, not newest-rule priority.

    Dimensions: integrity, protected/context family, specificity, completeness,
    dictionary corroboration, confidence. The tuple is serialized for audit.
    """
    family = candidate["candidate_family"]
    dictionary = candidate.get("dictionary_evidence") or {}
    dictionary_support = 0
    if dictionary.get("matched"):
        type_counts = dictionary.get("dictionary_type_counts") or {}
        if family == "term":
            dictionary_support = min(80, 25 + 5 * int(type_counts.get("term", 0)) + 3 * int(type_counts.get("expression", 0)))
        elif family == "proper-name":
            dictionary_support = min(55, 15 + 5 * int(type_counts.get("name", 0)))
        elif family == "grammar":
            dictionary_support = min(45, 10 + 5 * int(type_counts.get("grammar", 0)))
        else:
            dictionary_support = 10
    protected = 100 if family == "punctuation" else (90 if family == "proper-name" else ROLE_ORDER.get(family, 0))
    confidence = int(round(float(candidate.get("confidence") or 0.0) * 100))
    return (100, protected, _specificity(candidate), _completeness(candidate), dictionary_support, confidence)


def _candidate_score(candidate: dict[str, Any]) -> int:
    # Score per covered character so splitting a range cannot manufacture extra
    # "integrity" points. Completeness/specificity then break equal-coverage ties.
    family = candidate["candidate_family"]
    if family == "unresolved":
        return 0
    u = candidate["utility_dimensions"]
    length = candidate["end"] - candidate["start"]
    per_char = u[1] * 1_000_000 + u[2] * 10_000 + u[4] * 100 + u[5]
    whole_span_bonus = u[3] * 1_000 + length
    return per_char * length + whole_span_bonus


def normalize_candidates(
    analysis: dict[str, Any],
    dictionary_result: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    text = analysis["text"]
    by_range = _dictionary_by_range(dictionary_result)
    out: list[dict[str, Any]] = []
    seen: set[tuple[int, int, str, str | None, str | None]] = set()

    def add(item: dict[str, Any], family: str, role: str, *, source_layer: str,
            headword: str | None = None, grammar_id: str | None = None,
            confidence: float | None = None, protected: bool = False,
            component_ids: list[str] | None = None) -> None:
        if not _valid_range(text, item):
            return
        key = (item["start"], item["end"], role, headword, grammar_id)
        if key in seen:
            return
        seen.add(key)
        dsum = _dict_summary(by_range.get((item["start"], item["end"]), []))
        record = {
            "candidate_id": f"a34c{len(out)}",
            "start": item["start"], "end": item["end"], "surface": item["surface"],
            "proposed_role": role, "candidate_family": family,
            "headword": headword, "grammar_id": grammar_id,
            "confidence": float(confidence if confidence is not None else item.get("confidence") or 0.0),
            "protected": protected, "source_layer": source_layer,
            "source_annotation_id": item.get("id"),
            "morpheme_ids": component_ids or item.get("morpheme_ids") or [],
            "dictionary_evidence": dsum,
            "evidence": deepcopy(item.get("evidence") or []),
        }
        record["utility_dimensions"] = _candidate_utility(record)
        record["utility_score"] = _candidate_score(record)
        out.append(record)

    for item in analysis.get("orthographic_spans") or []:
        add(item, "punctuation", "punctuation", source_layer="orthography", confidence=1.0, protected=True)
    for item in analysis.get("person_references") or []:
        add(item, "proper-name", "proper-name", source_layer="person-references", headword=item.get("base_name") or item["surface"], confidence=item.get("confidence", .95), protected=True)
    for item in analysis.get("grammar_matches_alpha321") or analysis.get("grammar_matches_alpha32") or analysis.get("grammar_matches_alpha31") or []:
        add(item, "grammar", "grammar", source_layer="grammar", grammar_id=item.get("grammar_id"), confidence=item.get("confidence", .9))
    for item in analysis.get("numeral_expressions_alpha32") or []:
        add(item, "numeral", "term", source_layer="numeral", headword=item["surface"], confidence=item.get("confidence", .9))
    for item in analysis.get("discourse_connectives_alpha321") or analysis.get("discourse_connectives_alpha32") or []:
        add(item, "discourse", "term", source_layer="discourse", headword=item.get("headword") or item["surface"], confidence=item.get("confidence", .9))
    for item in analysis.get("lexical_items_alpha32") or analysis.get("lexical_items_alpha31") or []:
        family = "proper-name" if item.get("lexical_type") == "proper-name" else "term"
        add(item, family, "proper-name" if family == "proper-name" else "term", source_layer="lexical", headword=item.get("headword"), confidence=item.get("confidence", .8), protected=family == "proper-name")

    # Function/punctuation fallbacks come from immutable morphology and guarantee coverage.
    for m in analysis.get("morphemes") or []:
        if m.get("pos") in {"PUNCT", "SYM"} or str(m.get("tag") or "").startswith("補助記号"):
            add(m, "punctuation", "punctuation", source_layer="morphology-fallback", confidence=1.0, protected=True)
        elif m.get("pos") in {"ADP", "PART", "AUX", "SCONJ"}:
            add(m, "particle", "particle", source_layer="morphology-fallback", confidence=.8)

    return out


@dataclass(frozen=True)
class _Plan:
    score: int
    spans: tuple[dict[str, Any], ...]


def _better(left: _Plan, right: _Plan) -> _Plan:
    if left.score != right.score:
        return left if left.score > right.score else right
    # Stable tie-breakers: fewer fragments, then longer first span.
    if len(left.spans) != len(right.spans):
        return left if len(left.spans) < len(right.spans) else right
    left_lengths = tuple(-(x["end"] - x["start"]) for x in left.spans)
    right_lengths = tuple(-(x["end"] - x["start"]) for x in right.spans)
    return left if left_lengths <= right_lengths else right


def resolve_candidates(text: str, candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_start: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for c in candidates:
        by_start[c["start"]].append(c)

    # Explicit neutral fallback for every code point. It is never mistaken for evidence.
    for i, char in enumerate(text):
        fallback = {
            "candidate_id": f"a34fallback{i}", "start": i, "end": i + 1,
            "surface": char, "proposed_role": "unresolved", "candidate_family": "unresolved",
            "headword": None, "grammar_id": None, "confidence": 0.0, "protected": False,
            "source_layer": "coverage-fallback", "source_annotation_id": None,
            "morpheme_ids": [], "dictionary_evidence": {"matched": False}, "evidence": [],
            "utility_dimensions": (100, 0, 0, 0, 0, 0),
        }
        fallback["utility_score"] = _candidate_score(fallback)
        by_start[i].append(fallback)

    dp: list[_Plan | None] = [None] * (len(text) + 1)
    dp[len(text)] = _Plan(0, tuple())
    for pos in range(len(text) - 1, -1, -1):
        best: _Plan | None = None
        for candidate in by_start.get(pos, []):
            tail = dp[candidate["end"]]
            if tail is None:
                continue
            plan = _Plan(candidate["utility_score"] + tail.score, (candidate,) + tail.spans)
            best = plan if best is None else _better(best, plan)
        dp[pos] = best
    selected = list((dp[0] or _Plan(0, tuple())).spans)

    decisions: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    for selected_candidate in selected:
        overlapping = [
            c for c in candidates
            if c["candidate_id"] != selected_candidate["candidate_id"]
            and c["start"] < selected_candidate["end"] and selected_candidate["start"] < c["end"]
        ]
        rejected = sorted({c["candidate_id"] for c in overlapping})
        policies = []
        if selected_candidate["candidate_family"] == "punctuation":
            policies.append("protected-orthography")
        if selected_candidate["candidate_family"] == "proper-name":
            policies.append("protected-person-reference")
        if selected_candidate["candidate_family"] == "grammar":
            policies.extend(["complete-contextual-construction", "grammar-specificity"])
        if (selected_candidate.get("dictionary_evidence") or {}).get("matched"):
            policies.append("dictionary-corroboration")
        if selected_candidate["candidate_family"] == "unresolved":
            policies.append("abstain-when-evidence-insufficient")
        decision = {
            "decision_id": f"a34d{len(decisions)}",
            "start": selected_candidate["start"], "end": selected_candidate["end"],
            "surface": selected_candidate["surface"],
            "selected_candidate_id": selected_candidate["candidate_id"],
            "selected_role": selected_candidate["proposed_role"],
            "selected_headword": selected_candidate.get("headword"),
            "selected_grammar_id": selected_candidate.get("grammar_id"),
            "rejected_candidate_ids": rejected,
            "decision_policies": policies,
            "utility_dimensions": selected_candidate["utility_dimensions"],
            "reason": _decision_reason(selected_candidate, overlapping),
            "confidence": selected_candidate.get("confidence", 0.0),
        }
        decisions.append(decision)
        if overlapping:
            conflicts.append({
                "conflict_id": f"a34x{len(conflicts)}",
                "start": selected_candidate["start"], "end": selected_candidate["end"],
                "surface": selected_candidate["surface"],
                "selected_candidate_id": selected_candidate["candidate_id"],
                "candidate_ids": [selected_candidate["candidate_id"]] + rejected,
                "resolved": selected_candidate["candidate_family"] != "unresolved",
                "resolution_policy": policies or ["evidence-utility"],
            })
    return selected, decisions, conflicts


def _decision_reason(selected: dict[str, Any], overlapping: list[dict[str, Any]]) -> str:
    family = selected["candidate_family"]
    if family == "punctuation":
        return "Orthographic punctuation is protected and cannot be crossed by lexical or grammar candidates."
    if family == "proper-name":
        return "A structurally supported person reference outranks component lexical proposals."
    if family == "grammar":
        return "The complete licensed contextual grammar construction outranks internal function or dictionary-valid fragments."
    if family == "term" and (selected.get("dictionary_evidence") or {}).get("matched"):
        return "Morphology and contextual lexical evidence are corroborated by independent dictionary evidence."
    if family == "term":
        return "The contextual lexical proposal is valid; dictionary absence is not treated as rejection."
    if family == "particle":
        return "Morphology identifies a contextual function element and no stronger complete construction covers the range."
    if family == "unresolved":
        return "No compatible evidence candidate was strong enough; the resolver abstains instead of guessing."
    return "Selected from compatible evidence using integrity, specificity, completeness, corroboration, and confidence."


def analyze_layered_alpha34(
    text: str,
    nlp,
    dictionary_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from .stabilization import analyze_layered_alpha321

    base = analyze_layered_alpha321(text, nlp)
    result = deepcopy(base)
    before = _snapshot_morphology(result.get("morphemes") or [])
    candidates = normalize_candidates(result, dictionary_result)
    selected, decisions, conflicts = resolve_candidates(text, candidates)
    resolved_spans = [
        {
            "start": c["start"], "end": c["end"], "surface": c["surface"],
            "role": c["proposed_role"], "headword": c.get("headword"),
            "grammar_id": c.get("grammar_id"), "confidence": c.get("confidence", 0.0),
            "selected_candidate_id": c["candidate_id"],
        }
        for c in selected
    ]
    diagnostics: list[dict[str, Any]] = []
    if before != _snapshot_morphology(result.get("morphemes") or []):
        diagnostics.append({"severity": "error", "code": "A34_MORPHOLOGY_MUTATED", "message": "Resolver changed Layer 0 morphology."})
    if "".join(x["surface"] for x in resolved_spans) != text:
        diagnostics.append({"severity": "error", "code": "A34_PROJECTION_INCOMPLETE", "message": "Resolved spans do not reconstruct source text."})
    cursor = 0
    for span in resolved_spans:
        if span["start"] != cursor or text[span["start"]:span["end"]] != span["surface"]:
            diagnostics.append({"severity": "error", "code": "A34_RANGE_INVALID", "message": f"Invalid resolved range at {cursor}."})
            break
        cursor = span["end"]

    result.update({
        "version": "8.0.0-alpha3.4-resolver",
        "dictionary_evidence_alpha34": dictionary_result or {
            "dictionary_ready": False, "evidence": [],
            "contract": {"evidence_only": True, "dictionary_miss_is_not_rejection": True},
        },
        "resolver_candidates_alpha34": candidates,
        "resolver_conflicts_alpha34": conflicts,
        "resolver_decisions_alpha34": decisions,
        "resolved_spans_alpha34": resolved_spans,
        "diagnostics_alpha34": diagnostics,
        "layer0_snapshot_alpha34": before,
        "alpha34_contract": {
            "non_destructive": True,
            "alpha321_preserved": True,
            "dictionary_is_evidence_only": True,
            "dictionary_miss_is_not_rejection": True,
            "only_resolved_spans_are_exclusive": True,
            "every_decision_is_explainable": True,
        },
    })
    return result


analyze = analyze_layered_alpha34
