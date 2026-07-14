from __future__ import annotations

def validate_ranges(text, spans, *, require_partition):
    diagnostics = []
    cursor = 0
    for index, span in enumerate(sorted(spans, key=lambda x: (x.get("start", -1), x.get("end", -1)))):
        start, end = span.get("start"), span.get("end")
        if not isinstance(start, int) or not isinstance(end, int) or not (0 <= start < end <= len(text)):
            diagnostics.append({"severity":"error", "code":"SOURCE_RANGE_INVALID", "index":index})
            continue
        if span.get("surface") != text[start:end]:
            diagnostics.append({"severity":"error", "code":"SOURCE_SURFACE_MISMATCH", "index":index})
        if require_partition and start != cursor:
            diagnostics.append({"severity":"error", "code":"SOURCE_PARTITION_GAP_OR_OVERLAP", "index":index, "expected":cursor, "actual":start})
        if require_partition:
            cursor = end
    if require_partition and cursor != len(text):
        diagnostics.append({"severity":"error", "code":"SOURCE_PARTITION_INCOMPLETE", "expected":len(text), "actual":cursor})
    return diagnostics

def validate_analysis_source(result):
    text = result.get("text", "")
    diagnostics = validate_ranges(text, result.get("resolved_spans_alpha2") or [], require_partition=True)
    diagnostics.extend(validate_ranges(text, result.get("morphemes") or [], require_partition=False))
    return diagnostics
