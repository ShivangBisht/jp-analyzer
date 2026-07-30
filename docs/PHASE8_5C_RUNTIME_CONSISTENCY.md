# Phase 8.5C Runtime Consistency

Phase 8.5C adds preflight conflict detection before either store mutates, explicit same-range replacement with compensation, distinct raw/effective/post-correction snapshots, post-correction outcome capture for lookup/learning/colour fields, typed lifecycle response metadata, and a read-only integrity report at `/reader-corrections/integrity`. Non-overlapping ranges coexist; overlap and containment are rejected.
