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


def _lookup_hypothesis(
    text: str,
    hypothesis_type: str,
    *,
    source: str,
    source_predicate_id: str | None = None,
    source_surface: str | None = None,
    source_lemma: str | None = None,
) -> dict[str, Any] | None:
    value = str(text or "").strip()
    if not value or any(char in PUNCTUATION for char in value):
        return None
    return {
        "text": value,
        "type": hypothesis_type,
        "status": "generated",
        "dictionaryStatus": "not-evaluated",
        "generationSource": source,
        "sourcePredicateId": source_predicate_id,
        "sourceSurface": source_surface,
        "sourceLemma": source_lemma,
    }


def _dedupe_lookup_hypotheses(items: list[dict[str, Any] | None]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        if not item:
            continue
        key = (item["text"], item["type"])
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _final_predicate_lookup_hypothesis(
    source_text: str,
    candidate_start: int,
    final_predicate: dict[str, Any],
) -> dict[str, Any] | None:
    pred_start = final_predicate.get("start")
    pred_end = final_predicate.get("end")
    lemma = str(final_predicate.get("headword") or "").strip()
    if not (
        isinstance(candidate_start, int)
        and isinstance(pred_start, int)
        and isinstance(pred_end, int)
        and 0 <= candidate_start <= pred_start < pred_end <= len(source_text)
        and lemma
    ):
        return None
    # Preserve the actual source prefix exactly and normalize only the final
    # predicate. No connective is inserted, no component is reordered, and no
    # earlier source character is rewritten.
    prefix = source_text[candidate_start:pred_start]
    hypothesis = prefix + lemma
    return _lookup_hypothesis(
        hypothesis,
        "complete-final-predicate-normalization",
        source="candidate-final-predicate",
        source_predicate_id=final_predicate.get("id"),
        source_surface=source_text[pred_start:pred_end],
        source_lemma=lemma,
    )


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
    lookup_hypotheses: list[dict[str, Any] | None] | None = None,
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
        "lookupHypotheses": _dedupe_lookup_hypotheses(
            list(lookup_hypotheses or [])
            + [
                _lookup_hypothesis(
                    key,
                    "component-or-lexical-headword",
                    source="candidate-component-headword",
                )
                for key in lookup_keys
                if key
            ]
        ),
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
        if gid in INFLECTION_GRAMMAR_IDS:
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
    """Generate only contiguous verbal compound alternatives.

    This function does not claim that a candidate is a word. It only preserves a
    structurally viable alternative for later evidence ranking. Ambiguous VてV
    sequences retain conflict evidence and remain unselected.
    """
    out = []
    text = result.get("text", "")
    predicates = result.get("predicates") or []
    by_id = {x.get("id"): x for x in predicates if x.get("id")}
    relations = result.get("predicate_relations_alpha31") or result.get("predicate_relations") or []
    morphemes = sorted(result.get("morphemes") or [], key=lambda x: (x.get("start", 0), x.get("end", 0)))

    def predicate_is_verbal(predicate: dict[str, Any]) -> bool:
        ids = set(predicate.get("morpheme_ids") or [])
        heads = [
            item for item in morphemes
            if item.get("id") == predicate.get("head_morpheme_id")
            or item.get("id") in ids
            or (item.get("start") == predicate.get("start") and item.get("end") == predicate.get("end"))
        ]
        return any(item.get("pos") == "VERB" for item in heads)

    for relation in relations:
        left = by_id.get(relation.get("from_predicate_id"))
        right = by_id.get(relation.get("to_predicate_id"))
        if not left or not right or not predicate_is_verbal(left) or not predicate_is_verbal(right):
            continue

        ordered = sorted([left, right], key=lambda x: (x.get("start", 0), x.get("end", 0)))
        first, second = ordered
        start, second_end = first.get("start"), second.get("end")
        if not _range_valid(text, start, second_end):
            continue

        between = [
            item for item in morphemes
            if first.get("end", -1) <= item.get("start", -1)
            and item.get("end", -1) <= second.get("start", -1)
        ]
        gap_surface = text[first.get("end", 0):second.get("start", 0)]
        marker = relation.get("marker_range") or {}
        marker_surface = marker.get("surface")

        # Contiguous lexical compounds may have no gap (読み終わる), or only a
        # visible conjunctive marker (出て行く). Arguments and modifiers block
        # a lexical-compound proposal.
        direct_compound = first.get("end") == second.get("start")
        conjunctive_compound = gap_surface in {"て", "で"} and marker_surface in {"て", "で"}
        if not (direct_compound or conjunctive_compound):
            continue
        if any(item.get("pos") in {"NOUN", "PROPN", "PRON", "NUM", "DET"} for item in between):
            continue
        if _crosses_punctuation(text, start, second_end):
            continue

        end = second_end
        trailing = [item for item in morphemes if item.get("start") == end]
        while trailing and trailing[0].get("pos") == "AUX":
            end = trailing[0]["end"]
            trailing = [item for item in morphemes if item.get("start") == end]
        if _crosses_punctuation(text, start, end):
            continue

        component_keys = list(dict.fromkeys(
            value for value in [first.get("headword"), second.get("headword")] if value
        ))
        conflicts = [{
            "source": "predicate-relation",
            "detail": relation.get("semantic_relation") or relation.get("relation") or "compound-vs-independent-predicates",
            "confidence": relation.get("confidence"),
        }]
        evidence = [{
            "source": "predicate-link",
            "detail": relation.get("id"),
            "confidence": relation.get("confidence"),
        }]
        if marker_surface:
            evidence.append({
                "source": "visible-connective",
                "detail": marker_surface,
                "confidence": relation.get("confidence"),
            })
        if direct_compound:
            evidence.append({
                "source": "contiguous-verbal-predicates",
                "detail": "no intervening source material",
                "confidence": relation.get("confidence"),
            })

        complete_hypothesis = _final_predicate_lookup_hypothesis(text, start, second)
        candidate = _record(
            result,
            "compound-predicate",
            start,
            end,
            "lexical-compound",
            component_keys,
            [first.get("id"), second.get("id"), relation.get("id")],
            evidence,
            conflicts,
            lookup_hypotheses=[complete_hypothesis],
        )
        candidate["features"]["completeLookupHypothesisGenerated"] = bool(complete_hypothesis)
        candidate["features"]["completeLookupHypothesisStatus"] = (
            "not-evaluated" if complete_hypothesis else "not-generated"
        )
        candidate["features"]["completeLookupKeyCorroborated"] = False
        candidate["features"]["containsInterveningArgumentMaterial"] = False
        candidate["features"]["verbalPredicatePair"] = True
        out.append(candidate)
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
    public = []
    for item in deduped.values():
        if item.get("hardRejectionReasons"):
            continue
        item["rankingEligible"] = True
        item["abstentionEligible"] = True
        item["selectionPolicy"] = "evidence-ranking-with-abstention"
        public.append(item)
    return sorted(public, key=lambda x: (x.get("start", 0), x.get("end", 0), x.get("candidateFamily", "")))
