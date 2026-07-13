from .schema import Diagnostic, LayeredAnalysis

FUNCTION_POS = {"ADP", "AUX", "SCONJ", "PART", "PUNCT", "SYM"}


def validate(a: LayeredAnalysis):
    out = []
    cursor = 0

    # Reader projection must form an exact, non-overlapping partition.
    for span in sorted(a.color_spans, key=lambda x: (x.start, x.end)):
        if span.start != cursor:
            out.append(
                Diagnostic(
                    severity="error",
                    code="COLOR_GAP_OR_OVERLAP",
                    message=f"Expected {cursor}, found {span.start}",
                    start=cursor,
                    end=span.start,
                )
            )
        if span.surface != a.text[span.start:span.end] or span.end <= span.start:
            out.append(
                Diagnostic(
                    severity="error",
                    code="COLOR_RANGE_INVALID",
                    message="Color range mismatch",
                    start=span.start,
                    end=span.end,
                )
            )
        cursor = span.end

    if cursor != len(a.text):
        out.append(
            Diagnostic(
                severity="error",
                code="COLOR_INCOMPLETE",
                message="Color partition incomplete",
                start=cursor,
                end=len(a.text),
            )
        )

    morphemes = {m.id: m for m in a.morphemes}
    entities = {e.id: e for e in a.entities}
    predicates = {p.id: p for p in a.predicates}

    for m in a.morphemes:
        if m.surface != a.text[m.start:m.end]:
            out.append(
                Diagnostic(
                    severity="error",
                    code="MORPHEME_RANGE_INVALID",
                    message=m.id,
                    start=m.start,
                    end=m.end,
                )
            )

    # Bunsetsu heads must be content heads, never punctuation/function tokens.
    for phrase in a.basic_phrases:
        head = morphemes.get(phrase.head_id or "")
        if head and head.pos in {"PUNCT", "SYM"}:
            out.append(
                Diagnostic(
                    severity="error",
                    code="BUNSETSU_HEAD_IS_PUNCTUATION",
                    message=f"{phrase.id} points to punctuation head {head.id}",
                    start=phrase.start,
                    end=phrase.end,
                )
            )

    # General dictionary lookup must never target protected person/name spans.
    protected_names = [
        e for e in a.entities if e.protected and e.entity_class == "proper-name"
    ]
    for candidate in a.dictionary_candidates:
        for entity in protected_names:
            if entity.start <= candidate.start and candidate.end <= entity.end:
                out.append(
                    Diagnostic(
                        severity="error",
                        code="DICTIONARY_CANDIDATE_INSIDE_PROTECTED_NAME",
                        message=f"{candidate.id} is inside protected name {entity.surface}",
                        start=candidate.start,
                        end=candidate.end,
                    )
                )

    # Predicate relations should retain their visible connective when available.
    for relation in a.predicate_relations:
        if relation.from_predicate_id not in predicates or relation.to_predicate_id not in predicates:
            out.append(
                Diagnostic(
                    severity="error",
                    code="PREDICATE_RELATION_TARGET_MISSING",
                    message=relation.id,
                )
            )
        if relation.marker_range is None:
            out.append(
                Diagnostic(
                    severity="warning",
                    code="PREDICATE_RELATION_MARKER_MISSING",
                    message=f"{relation.id} has no connective marker",
                )
            )
        elif relation.marker_range.surface != a.text[
            relation.marker_range.start : relation.marker_range.end
        ]:
            out.append(
                Diagnostic(
                    severity="error",
                    code="PREDICATE_RELATION_MARKER_INVALID",
                    message=relation.id,
                    start=relation.marker_range.start,
                    end=relation.marker_range.end,
                )
            )

    # Japanese prenominal relative clauses should finish before the modified noun.
    for clause in a.clauses:
        if clause.clause_type != "relative-clause" or clause.modifies_range is None:
            continue
        if clause.end > clause.modifies_range.start:
            out.append(
                Diagnostic(
                    severity="error",
                    code="RELATIVE_CLAUSE_CROSSES_MODIFIED_NOUN",
                    message=f"{clause.id} extends into {clause.modifies_range.surface}",
                    start=clause.start,
                    end=clause.end,
                )
            )
        if clause.surface != a.text[clause.start:clause.end]:
            out.append(
                Diagnostic(
                    severity="error",
                    code="RELATIVE_CLAUSE_RANGE_INVALID",
                    message=clause.id,
                    start=clause.start,
                    end=clause.end,
                )
            )

    return out
