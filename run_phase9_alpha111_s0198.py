from __future__ import annotations

import json
from pathlib import Path

from app.phase9.kwja_alpha1 import analyze_kwja_alpha1

TEXT = (
    '仕事の確認が済んだ後、軽い相談のつもりでタッくんとのことを'
    '「私じゃなくて友達の話なんですけど～」と始めたら、'
    '一瞬で噓がバレてしまい、あれよあれよという間に'
    '全ての情報を抜き取られてしまった。'
)


def main() -> None:
    layer = analyze_kwja_alpha1(TEXT)
    metadata = layer.get('kwja_metadata_alpha1', {})
    diagnostics = layer.get('kwja_alignment_diagnostics_alpha1', [])

    result = {
        'version': '9.0.0-alpha1.1.1-alignment',
        'text': TEXT,
        'source_alignment_complete': metadata.get('source_alignment_complete'),
        'alignment_diagnostics': diagnostics,
        'kwja_metadata_alpha1': metadata,
        'kwja_morphemes_alpha1': layer.get('kwja_morphemes_alpha1', []),
        'contract': {
            'alignment_only_change': True,
            'source_text_immutable': True,
            'reader_projection_unchanged': True,
        },
    }

    output = Path('phase9_alpha111_s0198_result.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"source alignment complete: {result['source_alignment_complete']}")
    print(f'alignment diagnostics: {len(diagnostics)}')
    print(f'Wrote {output}')

    if result['source_alignment_complete'] is not True or diagnostics:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
