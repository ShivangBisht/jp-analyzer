from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any

from .alpha321 import analyze_layered_alpha321
from .alpha32 import _project

BOUNDARY_CHARS = {"。", "！", "？", "!", "?", "、", "，", ",", "…", "─", "―", "「", "『", "（", "("}


def _snapshot(items: list[dict[str, Any]]) -> str:
    payload = repr([(x.get("id"), x.get("start"), x.get("end"), x.get("surface"), x.get("lemma"), x.get("pos"), x.get("tag")) for x in items])
    return sha256(payload.encode("utf-8")).hexdigest()


def _add_grammar(out, seen, text, ms, start_i, end_i, gid, canonical, function, confidence=.96, priority=120, detail="alpha3.3 licensed construction"):
    a, b = ms[start_i]["start"], ms[end_i - 1]["end"]
    key = (a, b, gid)
    if key in seen:
        return
    out.append({
        "id": f"a33g{len(out)}", "start": a, "end": b, "surface": text[a:b],
        "grammar_id": gid, "canonical_form": canonical, "function": function,
        "host_predicate_id": None, "morpheme_ids": [m["id"] for m in ms[start_i:end_i]],
        "confidence": confidence, "priority": priority,
        "evidence": [{"source": "alpha3.3-residual-grammar", "detail": detail, "confidence": confidence}],
    })
    seen.add(key)


def _surface_grammar(text, ms, existing):
    out = deepcopy(existing)
    seen = {(g["start"], g["end"], g["grammar_id"]) for g in out}
    patterns = [
        ("という", "TO_IU", "という", "quotation-or-naming-modifier", .96, 118),
        ("でしまう", "DE_SHIMAU", "Vでしまう", "completion-or-regret", .96, 122),
        ("ではあった", "COPULA_AFFIRMATIVE_PAST", "ではあった", "affirmative-past-copular-emphasis", .97, 124),
        ("てもらえる", "TE_MORAU_POTENTIAL", "Vてもらえる", "benefactive-reception-potential", .97, 124),
        ("でもらえる", "DE_MORAU_POTENTIAL", "Vでもらえる", "benefactive-reception-potential", .97, 124),
        ("てそう", "TE_SOU", "Vてそう", "appearance-or-inference-colloquial", .94, 112),
    ]
    for surface, gid, canonical, function, conf, pri in patterns:
        pos = 0
        while True:
            pos = text.find(surface, pos)
            if pos < 0:
                break
            end = pos + len(surface)
            inside = [i for i, m in enumerate(ms) if pos <= m["start"] and m["end"] <= end]
            if inside:
                _add_grammar(out, seen, text, ms, min(inside), max(inside) + 1, gid, canonical, function, conf, pri, f"licensed surface family {surface}")
            pos = end

    # Productive lexical-predicate negative: split lexical host and auxiliary ない.
    for i, m in enumerate(ms):
        if m.get("surface") != "ない" or m.get("pos") != "AUX" or i == 0:
            continue
        prev = ms[i - 1]
        if prev["end"] != m["start"] or prev.get("pos") not in {"VERB", "ADJ"}:
            continue
        if any(g["start"] <= m["start"] and m["end"] <= g["end"] and g["grammar_id"] not in {"V_TE"} for g in out):
            continue
        _add_grammar(out, seen, text, ms, i, i + 1, "NEGATIVE_AUX", "Vない", "negative-inflection", .92, 82, "AUX ない attached to lexical predicate")
    return out


def _lexicalized_negative_adjectives(text, ms):
    out = []
    # This family is lexical, not productive V + negative auxiliary.
    for surface, headword in (("つまらない", "つまらない"),):
        pos = 0
        while True:
            pos = text.find(surface, pos)
            if pos < 0:
                break
            end = pos + len(surface)
            mids = [m["id"] for m in ms if pos <= m["start"] and m["end"] <= end]
            out.append({
                "id": f"a33lex{len(out)}", "start": pos, "end": end, "surface": surface,
                "headword": headword, "normalized_headword": headword, "lexical_type": "term",
                "morpheme_ids": mids, "confidence": .96,
                "evidence": [{"source": "alpha3.3-lexicalized-negative", "detail": "licensed lexical adjective", "confidence": .96}],
            })
            pos = end
    return out


def _speech_fragments(text, ms):
    out = []
    for i, m in enumerate(ms):
        if len(m["surface"]) != 1 or i + 2 >= len(ms):
            continue
        comma, following = ms[i + 1], ms[i + 2]
        if comma["surface"] not in {"、", ","} or m["end"] != comma["start"]:
            continue
        if not following["surface"].startswith(m["surface"]):
            continue
        out.append({
            "id": f"frag{len(out)}", "start": m["start"], "end": m["end"], "surface": m["surface"],
            "role": "speech-fragment", "fragment_type": "repeated-start-hesitation", "morpheme_ids": [m["id"]],
            "confidence": .94, "evidence": [{"source": "alpha3.3-dialogue-fragment", "detail": "single mora repeated after comma", "confidence": .94}],
        })
    return out


def _at_boundary(text, start):
    if start == 0:
        return True
    prefix = text[:start].rstrip()
    return not prefix or prefix[-1] in BOUNDARY_CHARS


def _discourse_compositions(text, ms, existing):
    out = deepcopy(existing)
    seen = {(x["start"], x["end"], x["surface"]) for x in out}
    patterns = {
        ("だ", "から"): ("だから", True),
        ("それ", "とも"): ("それとも", False),
        ("それ", "でも"): ("それでも", True),
        ("それ", "に"): ("それに", True),
    }
    for i in range(len(ms) - 1):
        a, b = ms[i], ms[i + 1]
        if a["end"] != b["start"]:
            continue
        spec = patterns.get((a["surface"], b["surface"]))
        if not spec:
            continue
        surface, needs_boundary = spec
        if text[a["start"]:b["end"]] != surface or (needs_boundary and not _at_boundary(text, a["start"])):
            continue
        key = (a["start"], b["end"], surface)
        if key in seen:
            continue
        out.append({
            "id": f"a33disc{len(out)}", "start": a["start"], "end": b["end"], "surface": surface,
            "role": "discourse-connective", "headword": surface, "morpheme_ids": [a["id"], b["id"]],
            "confidence": .96, "evidence": [{"source": "alpha3.3-discourse-composition", "detail": "licensed adjacent connective window", "confidence": .96}],
        })
        seen.add(key)
    # Remove a shorter CCONJ-derived claim swallowed by an explicitly composed connective.
    composed = [(d["start"], d["end"]) for d in out if d["id"].startswith("a33disc")]
    return [d for d in out if not (not d["id"].startswith("a33disc") and any(a <= d["start"] and d["end"] < b for a, b in composed))]


def _entity_projections(text, ms, persons, name_diags):
    suppressions, full_names = [], []
    for d in name_diags:
        if d["code"] == "SUSPICIOUS_PROPER_NAME":
            a, b = d["start"], d["end"]
            # Project the lexical core only; particles remain morphology-owned.
            core = next((m for m in ms if a <= m["start"] and m["end"] <= b and m["surface"] in {"イエス", "ノー"}), None)
            if core:
                suppressions.append({
                    "id": f"a33sup{len(suppressions)}", "start": a, "end": b, "surface": text[a:b],
                    "replacement_start": core["start"], "replacement_end": core["end"], "replacement_surface": core["surface"],
                    "replacement_role": "term", "confidence": .98,
                    "evidence": [{"source": "alpha3.3-contextual-entity-rejection", "detail": "yes/no parallel expression", "confidence": .98}],
                })
        elif d["code"] == "POSSIBLE_MULTI_TOKEN_NAME":
            a, b = d["start"], d["end"]
            full_names.append({
                "id": f"a33name{len(full_names)}", "start": a, "end": b, "surface": text[a:b],
                "headword": text[a:b], "lexical_type": "proper-name", "morpheme_ids": [m["id"] for m in ms if a <= m["start"] and m["end"] <= b],
                "confidence": .9, "evidence": [{"source": "alpha3.3-name-composition", "detail": "adjacent surname/given-name proposal", "confidence": .9}],
            })
    return suppressions, full_names


def _project_alpha33(text, ms, orthography, grammar, lexical, numerals, discourse, speech, suppressions):
    # Remove only copied lexical claims rejected for Alpha 3.3 projection.
    copied_lexical = deepcopy(lexical)
    for s in suppressions:
        copied_lexical = [x for x in copied_lexical if not (s["start"] <= x["start"] and x["end"] <= s["end"] and x.get("lexical_type") == "proper-name")]
        copied_lexical.append({
            "id": s["id"] + "-replacement", "start": s["replacement_start"], "end": s["replacement_end"],
            "surface": s["replacement_surface"], "headword": s["replacement_surface"], "normalized_headword": s["replacement_surface"],
            "lexical_type": "term", "morpheme_ids": [], "confidence": s["confidence"], "evidence": s["evidence"],
        })
    colors, decisions = _project(text, ms, orthography, [], grammar, copied_lexical, numerals, discourse)
    # Speech fragment stays visually neutral/unresolved but is now a recognized category.
    for frag in speech:
        for span in colors:
            if span["start"] == frag["start"] and span["end"] == frag["end"]:
                span["evidence_ids"] = [frag["id"]]
                span["confidence"] = frag["confidence"]
    return colors, decisions


def analyze_layered_alpha33(text, nlp, dictionary_evidence=None):
    base = analyze_layered_alpha321(text, nlp, dictionary_evidence)
    result = deepcopy(base)
    ms = deepcopy(result["morphemes"])
    before = _snapshot(ms)

    grammar = _surface_grammar(text, ms, result["grammar_matches_alpha321"])
    lexicalized = _lexicalized_negative_adjectives(text, ms)
    speech = _speech_fragments(text, ms)
    discourse = _discourse_compositions(text, ms, result["discourse_connectives_alpha321"])
    suppressions, full_names = _entity_projections(text, ms, result["person_references"], result["name_diagnostics_alpha32"])

    lexical = deepcopy(result["lexical_items_alpha32"])
    # Remove copied lexical pieces swallowed by a licensed full lexical adjective.
    for item in lexicalized:
        lexical = [x for x in lexical if not (item["start"] <= x["start"] and x["end"] <= item["end"])]
        lexical.append(item)
    lexical.extend(full_names)

    colors, decisions = _project_alpha33(text, ms, result["orthographic_spans"], grammar, lexical, result["numeral_expressions_alpha32"], discourse, speech, suppressions)

    diagnostics = []
    if before != _snapshot(ms):
        diagnostics.append({"severity": "error", "code": "MORPHOLOGY_MUTATED", "message": "Alpha 3.3 changed Layer 0 morphology."})
    if "".join(s["surface"] for s in colors) != text:
        diagnostics.append({"severity": "error", "code": "A33_COLOR_INCOMPLETE", "message": "Alpha 3.3 projection does not reconstruct source text."})

    result.update({
        "version": "8.0.0-alpha3.3",
        "grammar_matches_alpha33": grammar,
        "lexical_items_alpha33": lexical,
        "speech_fragments_alpha33": speech,
        "discourse_connectives_alpha33": discourse,
        "entity_suppressions_alpha33": suppressions,
        "full_name_projections_alpha33": full_names,
        "reader_decisions_alpha33": decisions,
        "color_spans_alpha33": colors,
        "diagnostics_alpha33": diagnostics,
        "layer0_snapshot_alpha33": before,
        "alpha33_contract": {"non_destructive": True, "alpha321_preserved": True, "only_reader_projection_is_exclusive": True},
    })
    return result
