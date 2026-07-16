# Analyzer Test Corpora

## Development corpus

Path:

tests/corpora/development/random_sentences.txt

Purpose:

- Existing 200-sentence development regression corpus.
- Used during phased analyzer development.
- Used for semantic regression and compatibility testing.

Count:

200 non-empty Japanese sentences.

## Consolidation parity corpus

Path:

tests/corpora/parity/consolidation_fresh_unseen_200.txt

Purpose:

- Fresh corpus created after the consolidated analyzer implementation.
- Used only for old-versus-consolidated semantic parity.
- Contains original synthetic Japanese novel-style sentences.
- It is not a native-corpus accuracy benchmark.

Composition:

- Adventure: 50
- Action: 50
- Romance: 50
- Slice of life: 50
- Total: 200

Sampling seed:

20260715

Expected SHA-256:

33b32d7297358d2a11ab4eec0d4fce3a6e23f3d326b3d7641d937d8535d1e50b

## Important distinction

These corpora verify behavior preservation and regression stability.

They are not the future linguistic-accuracy corpus. Accuracy tuning will use a separate 500-sentence corpus derived from authentic novel text, with development, validation, and final held-out subsets.
