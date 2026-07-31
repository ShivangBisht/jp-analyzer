# Phase 8 Alpha 5 Reimplementation

Alpha 5 connects the Teaching UI to immutable AnalyzerDecisionSnapshot v1 and TeachingDecisionRecord v1 persistence.

- Review judgments: accepted-current, corrected, rejected.
- Records remain test-only, operationally inactive, and export-excluded.
- Saving a review decision does not create or activate a Reader correction.
- Existing correction Preview/Save/Undo remains a separate workflow.
- Sentence history includes active, retracted, and superseded records.
- The analyzer dictionary is read-only and must remain byte-identical through installation tests.
