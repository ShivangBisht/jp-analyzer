from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from typing import Any

from app.phase8.alpha321 import analyze_layered_alpha321
from app.phase8.dictionary_evidence import evaluate_analysis_candidates
from app.phase8.resolver_alpha34 import analyze_layered_alpha34
from app.phase9.kwja_alpha1 import analyze_kwja_alpha1, attach_kwja_read_only

VERSION = "9.0.0-alpha1.1-integrated-readonly"


def _stable_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(payload.encode("utf-8")).hexdigest()


def _protected_snapshots(analysis: dict[str, Any]) -> dict[str, str]:
    """Snapshot every pre-KWJA field, plus explicit critical fields."""
    return {key: _stable_hash(value) for key, value in analysis.items()}


def analyze_integrated_alpha11(
    text: str,
    nlp,
    *,
    use_dictionary: bool = True,
    raw_knp: str | None = None,
    kwja_executable: str | None = None,
) -> dict[str, Any]:
    # Build the complete existing Alpha 3.4 result first. KWJA is invoked only after
    # the established analyzer and resolver have finished.
    baseline = analyze_layered_alpha321(text, nlp)
    dictionary_result = evaluate_analysis_candidates(baseline) if use_dictionary else None
    alpha34 = analyze_layered_alpha34(text, nlp, dictionary_result)

    before = _protected_snapshots(alpha34)
    existing_keys = set(alpha34)

    kwja_layer = analyze_kwja_alpha1(
        text,
        raw_knp=raw_knp,
        executable=kwja_executable,
    )
    integrated = attach_kwja_read_only(alpha34, kwja_layer)

    after = {key: _stable_hash(integrated[key]) for key in existing_keys}
    changed = sorted(key for key in existing_keys if before[key] != after[key])
    collisions = sorted(existing_keys.intersection(kwja_layer))

    diagnostics: list[dict[str, Any]] = []
    if collisions:
        diagnostics.append({
            "severity": "error",
            "code": "P9A11_FIELD_COLLISION",
            "fields": collisions,
        })
    if changed:
        diagnostics.append({
            "severity": "error",
            "code": "P9A11_EXISTING_FIELD_MUTATED",
            "fields": changed,
        })
    if not (kwja_layer.get("kwja_metadata_alpha1") or {}).get("source_alignment_complete"):
        diagnostics.append({
            "severity": "error",
            "code": "P9A11_KWJA_ALIGNMENT_INCOMPLETE",
        })

    resolved_before = alpha34.get("resolved_spans_alpha34") or []
    resolved_after = integrated.get("resolved_spans_alpha34") or []
    decisions_before = alpha34.get("resolver_decisions_alpha34") or []
    decisions_after = integrated.get("resolver_decisions_alpha34") or []

    integrated.update({
        "version": VERSION,
        "diagnostics_phase9_alpha11": diagnostics,
        "phase9_alpha11_snapshots": {
            "before": before,
            "after": after,
        },
        "phase9_alpha11_contract": {
            "read_only_attachment": True,
            "kwja_evidence_only": True,
            "existing_fields_preserved": not changed,
            "existing_field_collisions": collisions,
            "layer0_preserved": before.get("morphemes") == after.get("morphemes"),
            "alpha34_resolved_spans_preserved": _stable_hash(resolved_before) == _stable_hash(resolved_after),
            "alpha34_resolver_decisions_preserved": _stable_hash(decisions_before) == _stable_hash(decisions_after),
            "dictionary_evidence_preserved": before.get("dictionary_evidence_alpha34") == after.get("dictionary_evidence_alpha34"),
            "kwja_source_alignment_complete": bool((kwja_layer.get("kwja_metadata_alpha1") or {}).get("source_alignment_complete")),
            "kwja_readings_non_authoritative": True,
            "kwja_lemmas_require_corroboration": True,
            "kwja_arguments_require_corroboration": True,
            "final_projection_changed_by_kwja": False,
        },
    })
    return integrated
