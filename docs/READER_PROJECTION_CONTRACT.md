\# JP Analyzer Reader Projection Contract



\## Status



This document defines the ownership boundary between JP Analyzer and Novel Audio Miner.



JP Analyzer is the sole owner of linguistic analysis and learner-facing span decisions.



Novel Audio Miner must not infer linguistic boundaries, merge analyzer spans, construct compound headwords, or reclassify analyzer output.



\## Analyzer responsibilities



JP Analyzer must produce authoritative, exact, non-overlapping reader spans.



For every reader span, JP Analyzer decides:



\- source start offset

\- source end offset

\- surface text

\- display role

\- lexical type

\- canonical headword

\- known-word lookup key

\- frequency lookup key

\- unknown-word colour policy

\- comprehension eligibility

\- New Words eligibility

\- mining eligibility

\- grammar ID, where applicable

\- confidence

\- supporting evidence IDs

\- correction information, where applicable



\## Required reader roles



The reader projection may produce:



\- lexical

\- lexical-compound

\- numeric-lexical

\- name

\- learnable-grammar

\- function

\- punctuation

\- unresolved



\## Reader-span invariants



Every reader span must satisfy:



1\. `start` and `end` are integer offsets.

2\. `0 <= start < end <= len(text)`.

3\. `surface == text\[start:end]`.

4\. Reader spans are ordered.

5\. Reader spans do not overlap.

6\. Reader spans respect protected punctuation boundaries.

7\. Reader spans provide complete source coverage.

8\. Lexical lookup keys are explicit.

9\. Novel Audio Miner is not required to reconstruct a headword.

10\. Novel Audio Miner is not required to merge spans.



\## Display-unit requirement



Inflected words and validated compounds must be emitted as complete learner-facing display units.



Examples:



\- `頷いて` with lookup key `頷く`

\- `出て行った` with lookup key `出て行く`

\- `とばかりに` as one learnable grammar span

\- `二人` as numeric lexical material with lookup key `二人`



Internal morphology remains available separately and must not force fragmented reader colouring.



\## User-specific colour resolution



JP Analyzer supplies:



\- the display role

\- known-word lookup key

\- frequency lookup key

\- unknown-word colour policy



Novel Audio Miner may then consult user-specific known-word and frequency data.



This lookup does not constitute a linguistic decision.



\## Corrections and learning



Saved reader corrections belong to JP Analyzer.



Novel Audio Miner may collect corrections through its interface, but corrections must be stored and applied by JP Analyzer.



A correction is an example or exact constraint. A correction must not automatically become a global handwritten rule.



\## Compatibility



Existing `resolvedSpans` may remain for diagnostics and backward compatibility.



A new `readerSpans` output will become the authoritative Novel Audio Miner display contract.

