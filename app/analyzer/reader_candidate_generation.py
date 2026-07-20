from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Any

PUNCTUATION = set("、。！？!?「」『』（）()……─―～")
LEXICAL_ROLES = {"term"}
FUNCTION_ROLES = {"particle", "grammar"}
INFLECTION_GRAMMAR_IDS = {"V_TE"}
TRAILING_AUX_LEMMAS = {
    "れる", "られる", "せる", "させる", "ない", "ぬ", "た", "ます", "です",
}


def _candidate_id(family: str, start: int, end: int, role: str, keys: list[str]) -> str:
    raw = f"{family}|{start}|{end}|{role}|{'|'.join(keys)}"
    return "reader-generated-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _range_valid(text: str, start: Any, end: Any) -> bool:
    return isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(text)


def _crosses_punctuation(text: str, start: int, end: int) -> bool:
    return any(char in PUNCTUATION for char in text[start:end])


def _contained(items: list[dict[str, Any]], start: int, end: int) -> list[dict[str, Any]]:
    return [x for x in items if start <= x.get("start", -1) and x.get("end", -1) <= end]


def _kwja_support(result: dict[str, Any], start: int, end: int) -> dict[str, Any]:
    phrases = result.get("kwja_basic_phrases_alpha1") or []
    predicates = result.get("kwja_predicate_phrases_alpha1") or []
    exact_phrase_ids = [x.get("id") for x in phrases if x.get("start") == start and x.get("end") == end]
    containing_phrase_ids = [x.get("id") for x in phrases if x.get("start", 10**9) <= start and end <= x.get("end", -1)]
    exact_predicate_ids = [x.get("id") for x in predicates if x.get("start") == start and x.get("end") == end]
    containing_predicate_ids = [x.get("id") for x in predicates if x.get("start", 10**9) <= start and end <= x.get("end", -1)]
    return {
        "kwjaExactBasicPhrase": bool(exact_phrase_ids),
        "kwjaContainingBasicPhrase": bool(containing_phrase_ids),
        "kwjaExactPredicatePhrase": bool(exact_predicate_ids),
        "kwjaContainingPredicatePhrase": bool(containing_predicate_ids),
        "kwjaBasicPhraseIds": list(dict.fromkeys(x for x in exact_phrase_ids + containing_phrase_ids if x)),
        "kwjaPredicatePhraseIds": list(dict.fromkeys(x for x in exact_predicate_ids + containing_predicate_ids if x)),
    }


def _dictionary_support(result: dict[str, Any], start: int, end: int) -> dict[str, Any]:
    candidates = result.get("resolver_candidates_alpha2") or []
    exact = [x for x in candidates if x.get("start") == start and x.get("end") == end]
    records = [x.get("dictionary_evidence") or {} for x in exact]
    return {
        "dictionaryMatched": any(x.get("matched") for x in records),
        "dictionaryIndependentSourceCount": max([int(x.get("independent_source_count") or 0) for x in records] or [0]),
        "dictionaryPosCompatible": any(x.get("pos_compatible") for x in records),
        "dictionaryEvidenceStatus": "existing-exact-range" if records else "not-evaluated-for-generated-candidate",
    }


def _record(
    result: dict[str, Any], family: str, start: int, end: int, role: str,
    lookup_keys: list[str], component_ids: list[str], evidence: list[dict[str, Any]],
    conflicts: list[dict[str, Any]], grammar_id: str | None = None,
) -> dict[str, Any]:
    text = result.get("text", "")
    hard: list[str] = []
    if not _range_valid(text, start, end):
        hard.append("invalid-source-range")
        surface = ""
    else:
        surface = text[start:end]
        if _crosses_punctuation(text, start, end):
            hard.append("crosses-protected-punctuation")
    features = {
        **_kwja_support(result, start, end),
        **_dictionary_support(result, start, end),
        "componentCount": len(component_ids),
        "positiveEvidenceCount": len(evidence),
        "conflictingEvidenceCount": len(conflicts),
        "hasLookupKey": bool(lookup_keys),
        "crossesPunctuation": "crosses-protected-punctuation" in hard,
    }
    return {
        "candidateId": _candidate_id(family, start, end, role, lookup_keys),
        "candidateSource": "reader-evidence-generator",
        "candidateFamily": family,
        "start": start,
        "end": end,
        "surface": surface,
        "proposedRole": role,
        "possibleLookupKeys": list(dict.fromkeys(x for x in lookup_keys if x)),
        "preferredLookupKey": None,
        "grammarId": grammar_id,
        "componentIds": list(dict.fromkeys(x for x in component_ids if x)),
        "evidence": evidence,
        "conflictingEvidence": conflicts,
        "features": features,
        "hardRejectionReasons": hard,
        "rankingStatus": "unscored-generated-alternative",
        "selected": False,
        "selectionReason": None,
        "schemaStatus": "phase-2.2B-generated-candidate",
    }


def _from_complete_grammar(result: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    grammar = (
        result.get("grammar_matches_alpha321")
        or result.get("grammar_matches_alpha32")
        or result.get("grammar_matches_alpha31")
        or []
    )
    for item in grammar:
        start, end = item.get("start"), item.get("end")
        gid = item.get("grammar_id")
        if not _range_valid(result.get("text", ""), start, end) or not gid:
            continue
        out.append(_record(
            result, "complete-grammar", start, end, "learnable-grammar", [],
            item.get("morpheme_ids") or [item.get("id")],
            [{"source": "known-grammar-id", "detail": gid, "confidence": item.get("confidence")}],
            [], grammar_id=gid,
        ))
    return out


def _from_numerals(result: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for item in result.get("numeral_expressions_alpha32") or []:
        start, end = item.get("start"), item.get("end")
        if not _range_valid(result.get("text", ""), start, end):
            continue
        surface = result["text"][start:end]
        out.append(_record(
            result, "numeric-lexical", start, end, "numeric-lexical", [surface],
            item.get("morpheme_ids") or [item.get("id")],
            [{"source": "numeral-expression", "detail": "existing numeric/counter composition", "confidence": item.get("confidence")}],
            [],
        ))
    return out


def _from_inflected_predicates(result: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    text = result.get("text", "")
    resolved = result.get("resolved_spans_alpha2") or []
    morphemes = result.get("morphemes") or []
    predicates = result.get("predicates") or []
    predicate_by_range = {(x.get("start"), x.get("end")): x for x in predicates}

    for index, span in enumerate(resolved):
        if span.get("role") not in LEXICAL_ROLES or not span.get("headword"):
            continue
        start, end = span.get("start"), span.get("end")
        components = [span.get("selected_candidate_id")]
        evidence = [{"source": "lexical-headword", "detail": span.get("headword"), "confidence": span.get("confidence")}]
        conflicts = []
        cursor = end
        consumed = 0
        for following in resolved[index + 1:index + 4]:
            if following.get("start") != cursor or following.get("role") not in FUNCTION_ROLES:
                break
            covered = _contained(morphemes, following["start"], following["end"])
            grammar_id = following.get("grammar_id")
            auxiliary = any(
                x.get("pos") == "AUX" or x.get("lemma") in TRAILING_AUX_LEMMAS
                for x in covered
            )
            conjunctive = grammar_id in INFLECTION_GRAMMAR_IDS
            if not (auxiliary or conjunctive):
                break
            cursor = following["end"]
            consumed += 1
            components.append(following.get("selected_candidate_id"))
            evidence.append({
                "source": "attached-function-material",
                "detail": grammar_id or ",".join(str(x.get("lemma") or x.get("surface")) for x in covered),
                "confidence": following.get("confidence"),
            })
        if consumed:
            predicate = predicate_by_range.get((start, end))
            if predicate:
                evidence.append({"source": "predicate-record", "detail": predicate.get("id"), "confidence": 1.0})
            out.append(_record(
                result, "inflected-lexical", start, cursor, "lexical", [span.get("headword")],
                components, evidence, conflicts,
            ))
    return out


def _from_predicate_relations(result: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    text = result.get("text", "")
    predicates = result.get("predicates") or []
    by_id = {x.get("id"): x for x in predicates if x.get("id")}
    relations = result.get("predicate_relations_alpha31") or result.get("predicate_relations") or []
    morphemes = result.get("morphemes") or []

    for relation in relations:
        left = by_id.get(relation.get("from_predicate_id"))
        right = by_id.get(relation.get("to_predicate_id"))
        if not left or not right:
            continue
        ordered = sorted([left, right], key=lambda x: (x.get("start", 0), x.get("end", 0)))
        start = ordered[0].get("start")
        end = ordered[-1].get("end")
        if not _range_valid(text, start, end):
            continue
        # Include contiguous function/inflection material between and immediately after predicates.
        contained = _contained(morphemes, start, end)
        if not contained:
            continue
        cursor = end
        trailing = sorted([x for x in morphemes if x.get("start") == cursor], key=lambda x: x.get("end", 0))
        while trailing and trailing[0].get("pos") == "AUX":
            cursor = trailing[0]["end"]
            trailing = sorted([x for x in morphemes if x.get("start") == cursor], key=lambda x: x.get("end", 0))
        end = cursor
        left_head = ordered[0].get("headword")
        right_head = ordered[1].get("headword")
        possible = []
        if left_head and right_head:
            possible.append(f"{text[ordered[0]['start']:ordered[0]['end']]}て{right_head}")
        possible.extend(x for x in [left_head, right_head] if x)
        conflicts = [{
            "source": "predicate-relation",
            "detail": relation.get("semantic_relation") or relation.get("relation") or "possible independent sequential actions",
            "confidence": relation.get("confidence"),
        }]
        marker = relation.get("marker_range") or {}
        evidence = [{"source": "predicate-link", "detail": relation.get("id"), "confidence": relation.get("confidence")}]
        if marker:
            evidence.append({"source": "visible-connective", "detail": marker.get("surface"), "confidence": relation.get("confidence")})
        out.append(_record(
            result, "compound-predicate", start, end, "lexical-compound", possible,
            [left.get("id"), right.get("id"), relation.get("id")], evidence, conflicts,
        ))
    return out


def generate_reader_candidates(result: dict[str, Any]) -> list[dict[str, Any]]:
    generated = []
    generated.extend(_from_complete_grammar(result))
    generated.extend(_from_numerals(result))
    generated.extend(_from_inflected_predicates(result))
    generated.extend(_from_predicate_relations(result))

    deduped: dict[tuple[Any, ...], dict[str, Any]] = {}
    for item in generated:
        key = (
            item.get("start"), item.get("end"), item.get("proposedRole"),
            tuple(item.get("possibleLookupKeys") or []), item.get("grammarId"),
        )
        if key not in deduped:
            deduped[key] = item
            continue
        existing = deduped[key]
        existing["evidence"] = existing.get("evidence", []) + item.get("evidence", [])
        existing["conflictingEvidence"] = existing.get("conflictingEvidence", []) + item.get("conflictingEvidence", [])
        existing["componentIds"] = list(dict.fromkeys(existing.get("componentIds", []) + item.get("componentIds", [])))
        existing["features"]["positiveEvidenceCount"] = len(existing["evidence"])
        existing["features"]["conflictingEvidenceCount"] = len(existing["conflictingEvidence"])
    return sorted(deduped.values(), key=lambda x: (x.get("start", 0), x.get("end", 0), x.get("candidateFamily", "")))
