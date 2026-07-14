from __future__ import annotations
from copy import deepcopy
from hashlib import sha256
from typing import Any
import unicodedata
from .structure import analyze_layered_alpha31

LEXICAL_EXTRA_POS = {"DET", "CCONJ", "NUM"}
DISCOURSE_FORMS = {"そして", "しかし", "また", "それでも", "でも", "だから", "ところで", "それに"}
COUNTER_TAG_HINTS = ("助数詞", "名詞-普通名詞-助数詞可能")
COUNTER_SURFACES = {
    "歳", "才", "年", "月", "日", "回", "階", "週間", "週", "人", "個", "本", "枚", "匹", "台", "冊", "度", "時", "分", "秒", "円", "対"
}
AUX_HEADS = {"いる", "ある", "おく", "いく", "くる", "もらう"}


def _snapshot(items: list[dict[str, Any]]) -> str:
    payload = repr([(x.get("id"), x.get("start"), x.get("end"), x.get("surface"), x.get("lemma"), x.get("pos"), x.get("tag")) for x in items])
    return sha256(payload.encode("utf-8")).hexdigest()


def _add_grammar(out, seen, text, ms, start_i, end_i, gid, canonical, function, confidence, priority, evidence_detail):
    a, b = ms[start_i]["start"], ms[end_i - 1]["end"]
    key = (a, b, gid)
    if key in seen:
        return
    out.append({
        "id": f"a32g{len(out)}",
        "start": a,
        "end": b,
        "surface": text[a:b],
        "grammar_id": gid,
        "canonical_form": canonical,
        "function": function,
        "host_predicate_id": None,
        "morpheme_ids": [m["id"] for m in ms[start_i:end_i]],
        "confidence": confidence,
        "priority": priority,
        "evidence": [{"source": "alpha3.2-compositional-grammar", "detail": evidence_detail, "confidence": confidence}],
    })
    seen.add(key)


def _expand_grammar(text, morphemes, existing):
    """Add grammar families without changing Alpha 3.1 records."""
    out = deepcopy(existing)
    seen = {(g["start"], g["end"], g["grammar_id"]) for g in out}
    ms = sorted(morphemes, key=lambda m: (m["start"], m["end"]))
    n = len(ms)

    for i in range(n):
        # Vて/で + dependent auxiliary (+ inflection chain)
        if ms[i].get("surface") not in {"て", "で"}:
            continue
        if i + 1 >= n:
            continue
        aux = ms[i + 1]
        lemma = aux.get("lemma")
        if lemma not in AUX_HEADS:
            continue
        end = i + 2
        while end < n and ms[end].get("pos") == "AUX" and ms[end]["start"] == ms[end - 1]["end"]:
            end += 1
        gid_map = {
            "いる": "TE_IRU_CHAIN",
            "ある": "TE_ARU",
            "おく": "TE_OKU",
            "いく": "TE_IKU",
            "くる": "TE_KURU",
            "もらう": "TE_MORAU",
        }
        fun_map = {
            "いる": "progressive-resultative",
            "ある": "resultant-state",
            "おく": "preparatory-action",
            "いく": "directional-or-continuative-away",
            "くる": "directional-or-continuative-toward",
            "もらう": "benefactive-reception",
        }
        _add_grammar(out, seen, text, ms, i, end, gid_map[lemma], f"V{ms[i]['surface']} + {lemma}", fun_map[lemma], .95, 116, f"conjunctive + dependent {lemma} chain")

    # Surface families whose pedagogical boundary is larger than one morpheme.
    surface_patterns = [
        ("かもしれない", "KAMOSHIRENAI", "かもしれない", "possibility", .98, 130),
        ("にとって", "NI_TOTTE", "にとって", "perspective-or-relevance", .97, 120),
        ("という間に", "TO_IU_AIDA_NI", "という間に", "during-the-brief-time", .96, 118),
        ("とばかりに", "TO_BAKARI_NI", "とばかりに", "as-if-to-say", .96, 118),
        ("たばかり", "TA_BAKARI", "Vたばかり", "recent-completion", .96, 116),
        ("というか", "TO_IU_KA", "というか", "rephrasing-or-qualification", .94, 108),
        ("ではなかった", "NEGATIVE_COPULA_PAST", "ではなかった", "past-negative-copula", .98, 125),
        ("ではない", "NEGATIVE_COPULA", "ではない", "negative-copula", .98, 122),
        ("ようだった", "YOU_DA_PAST", "ようだった", "appearance-or-similarity-past", .95, 112),
        ("ようだ", "YOU_DA", "ようだ", "appearance-or-similarity", .95, 110),
        ("んです", "NO_DA_POLITE", "のです", "explanatory-polite", .94, 105),
        ("のだ", "NO_DA", "のだ", "explanatory", .93, 102),
    ]
    for surf, gid, canonical, function, conf, pri in surface_patterns:
        p = 0
        while True:
            p = text.find(surf, p)
            if p < 0:
                break
            e = p + len(surf)
            inside = [k for k, m in enumerate(ms) if p <= m["start"] and m["end"] <= e]
            if inside:
                _add_grammar(out, seen, text, ms, min(inside), max(inside) + 1, gid, canonical, function, conf, pri, f"licensed surface family {surf}")
            p = e
    return out


def _numeral_expressions(text, morphemes):
    out = []
    ms = sorted(morphemes, key=lambda m: (m["start"], m["end"]))
    i = 0
    while i < len(ms):
        m = ms[i]
        if m.get("pos") != "NUM" and "数詞" not in m.get("tag", ""):
            i += 1
            continue
        end_i = i + 1
        # Allow counter/unit chains and numeral ratios such as 一対一.
        while end_i < len(ms) and ms[end_i]["start"] == ms[end_i - 1]["end"]:
            x = ms[end_i]
            if x.get("pos") == "NUM" or any(h in x.get("tag", "") for h in COUNTER_TAG_HINTS) or x.get("surface") in COUNTER_SURFACES:
                end_i += 1
                continue
            break
        # Keep a bare numeral as a useful numeral annotation too.
        a, b = m["start"], ms[end_i - 1]["end"]
        counter = text[m["end"]:b] or None
        out.append({
            "id": f"num{len(out)}", "start": a, "end": b, "surface": text[a:b],
            "role": "numeral-expression", "value_surface": m["surface"], "counter_surface": counter,
            "morpheme_ids": [x["id"] for x in ms[i:end_i]], "confidence": .96 if counter else .9,
            "evidence": [{"source": "alpha3.2-numeral-composition", "detail": "NUM plus contiguous counter/unit"}],
        })
        i = end_i
    return out


def _discourse_connectives(text, morphemes):
    out = []
    for m in morphemes:
        if m["surface"] in DISCOURSE_FORMS or m.get("pos") == "CCONJ":
            out.append({
                "id": f"disc{len(out)}", "start": m["start"], "end": m["end"], "surface": m["surface"],
                "role": "discourse-connective", "headword": m.get("lemma") or m["surface"], "morpheme_ids": [m["id"]],
                "confidence": .94, "evidence": [{"source": "alpha3.2-discourse-policy", "detail": f"{m.get('pos')}/{m.get('tag')}"}],
            })
    return out


def _lexical_items(text, morphemes, base_lexical, grammar, numerals, discourse, persons, orthography):
    """Create Alpha 3.2 lexical proposals; earlier lexical arrays remain untouched."""
    out = deepcopy(base_lexical)
    covered = {(x["start"], x["end"], x.get("lexical_type"), x.get("headword")) for x in out}
    grammar_ranges = [(g["start"], g["end"]) for g in grammar]
    person_ranges = [(p["start"], p["end"]) for p in persons]
    punct_ranges = [(o["start"], o["end"]) for o in orthography]
    numeral_ranges = {(n["start"], n["end"]) for n in numerals}
    discourse_ranges = {(d["start"], d["end"]) for d in discourse}

    # Remove earlier terms fully swallowed by newer grammar; preserve the earlier array separately.
    out = [x for x in out if not any(a <= x["start"] and x["end"] <= b for a, b in grammar_ranges)]

    for m in morphemes:
        a, b = m["start"], m["end"]
        if any(x <= a and b <= y for x, y in person_ranges + punct_ranges + grammar_ranges):
            continue
        if (a, b) in numeral_ranges or (a, b) in discourse_ranges:
            continue
        if m.get("pos") not in LEXICAL_EXTRA_POS:
            continue
        key = (a, b, "term", m.get("lemma") or m["surface"])
        if key in covered:
            continue
        out.append({
            "id": f"a32l{len(out)}", "start": a, "end": b, "surface": m["surface"],
            "headword": m.get("lemma") or m["surface"], "normalized_headword": m.get("normalized") or m["surface"],
            "lexical_type": "term", "morpheme_ids": [m["id"]], "confidence": .88,
            "evidence": [{"source": "alpha3.2-lexical-class", "detail": f"supported POS {m.get('pos')}"}],
        })
        covered.add(key)
    return out


def _name_diagnostics(text, morphemes, persons):
    out = []
    # Roman/katakana yes/no discourse should not become a person just because the parser says PROPN.
    for p in persons:
        if p["surface"] in {"イエス", "ノー"} or p["surface"].startswith("イエスとも"):
            out.append({"severity": "warning", "code": "SUSPICIOUS_PROPER_NAME", "message": p["surface"], "start": p["start"], "end": p["end"]})
    # Adjacent proper-name-like tokens are review candidates for full-name composition.
    ms = sorted(morphemes, key=lambda m: (m["start"], m["end"]))
    for i in range(len(ms) - 1):
        a, b = ms[i], ms[i + 1]
        if a["end"] != b["start"]:
            continue
        if ("固有名詞" in a.get("tag", "") or a.get("pos") == "PROPN") and ("人名" in b.get("tag", "") or b.get("pos") == "PROPN"):
            out.append({"severity": "info", "code": "POSSIBLE_MULTI_TOKEN_NAME", "message": text[a["start"]:b["end"]], "start": a["start"], "end": b["end"]})
    return out


def _project(text, morphemes, orthography, persons, grammar, lexical, numerals, discourse):
    claims = [None] * len(text)
    decisions = []
    def put(a, b, role, priority, source, head=None, gid=None, confidence=1.0):
        for i in range(a, b):
            c = {"priority": priority, "role": role, "headword": head, "grammar_id": gid, "confidence": confidence, "source": source}
            if claims[i] is None or priority > claims[i]["priority"]:
                claims[i] = c
    for m in morphemes:
        if m.get("pos") in {"ADP", "PART", "AUX", "SCONJ"}:
            put(m["start"], m["end"], "particle", 30, "morphology")
    for l in lexical:
        put(l["start"], l["end"], "proper-name" if l.get("lexical_type") == "proper-name" else "term", 80 if l.get("lexical_type") == "proper-name" else 60, l["id"], l.get("headword"), None, l.get("confidence", .8))
    for d in discourse:
        put(d["start"], d["end"], "term", 90, d["id"], d["headword"], None, d["confidence"])
    for n in numerals:
        put(n["start"], n["end"], "term", 92, n["id"], n["surface"], None, n["confidence"])
    for g in sorted(grammar, key=lambda x: (x.get("priority", 0), x["end"] - x["start"])):
        put(g["start"], g["end"], "grammar", 150 + g.get("priority", 0), g["id"], None, g["grammar_id"], g.get("confidence", .9))
    for o in orthography:
        put(o["start"], o["end"], "punctuation", 300, o["id"], None, None, 1.0)
    for i in range(len(text)):
        if claims[i] is None:
            claims[i] = {"priority": 0, "role": "unresolved", "headword": None, "grammar_id": None, "confidence": 0.0, "source": "none"}
    spans = []; a = 0
    def same(x, y):
        return all(x[k] == y[k] for k in ("role", "headword", "grammar_id", "confidence", "source"))
    for i in range(1, len(text) + 1):
        if i == len(text) or not same(claims[a], claims[i]):
            c = claims[a]; rid = f"a32rd{len(decisions)}"
            decisions.append({"id": rid, "start": a, "end": i, "surface": text[a:i], "selected_role": c["role"], "selected_source": c["source"], "reason": "Alpha 3.2 projection priority; all earlier annotations preserved", "confidence": c["confidence"]})
            spans.append({"start": a, "end": i, "surface": text[a:i], "role": c["role"], "headword": c["headword"], "grammar_id": c["grammar_id"], "confidence": c["confidence"], "evidence_ids": [c["source"], rid]})
            a = i
    return spans, decisions


def analyze_layered_alpha32(text, nlp, dictionary_evidence=None):
    base = analyze_layered_alpha31(text, nlp, dictionary_evidence)
    result = deepcopy(base)
    ms = deepcopy(result["morphemes"])
    before = _snapshot(ms)

    grammar = _expand_grammar(text, ms, result["grammar_matches_alpha31"])
    numerals = _numeral_expressions(text, ms)
    discourse = _discourse_connectives(text, ms)
    lexical = _lexical_items(text, ms, result["lexical_items_alpha31"], grammar, numerals, discourse, result["person_references"], result["orthographic_spans"])
    colors, decisions = _project(text, ms, result["orthographic_spans"], result["person_references"], grammar, lexical, numerals, discourse)
    name_diags = _name_diagnostics(text, ms, result["person_references"])

    diagnostics = []
    if before != _snapshot(ms):
        diagnostics.append({"severity": "error", "code": "MORPHOLOGY_MUTATED", "message": "Alpha 3.2 changed Layer 0 morphology."})
    if "".join(s["surface"] for s in colors) != text:
        diagnostics.append({"severity": "error", "code": "A32_COLOR_INCOMPLETE", "message": "Alpha 3.2 projection does not reconstruct source text."})

    result.update({
        "version": "8.0.0-alpha3.2",
        "grammar_matches_alpha32": grammar,
        "numeral_expressions_alpha32": numerals,
        "discourse_connectives_alpha32": discourse,
        "lexical_items_alpha32": lexical,
        "reader_decisions_alpha32": decisions,
        "color_spans_alpha32": colors,
        "name_diagnostics_alpha32": name_diags,
        "diagnostics_alpha32": diagnostics,
        "layer0_snapshot_alpha32": before,
        "alpha32_contract": {"non_destructive": True, "alpha31_preserved": True, "only_reader_projection_is_exclusive": True},
    })
    return result


analyze = analyze_layered_alpha32
