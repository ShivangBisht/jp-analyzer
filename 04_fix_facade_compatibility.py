from pathlib import Path

path = Path(__file__).resolve().parent / "app" / "analyzer" / "pipeline.py"
text = path.read_text(encoding="utf-8-sig")

import_block = '''from .layers.evidence_gate import (\n    VERSION as CONSOLIDATED_ENGINE_VERSION,\n    analyze_integrated_alpha2 as analyze_layers,\n)\n'''
replacement_block = import_block + '''\n# Temporary compatibility alias for the established facade test and callers\n# that patch this module-level seam. Production still resolves to the\n# consolidated layer engine.\nanalyze_integrated_alpha2 = analyze_layers\n'''

if "analyze_integrated_alpha2 = analyze_layers" not in text:
    if import_block not in text:
        raise RuntimeError("Expected consolidated layer import block was not found")
    text = text.replace(import_block, replacement_block, 1)

text = text.replace(
    "legacy_engine=analyze_layers,",
    "legacy_engine=analyze_integrated_alpha2,",
    1,
)

path.write_text(text, encoding="utf-8", newline="\n")
print(f"Updated: {path}")
