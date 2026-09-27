# -*- coding: utf-8 -*-
"""
Seminar Slides Offline Bundler
Inlines vendor JS into a standalone offline HTML file.
Usage: python bundle-offline.py <input-slides.html> [-o <output-slides-offline.html>]
"""
import sys
import os
import re
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
VENDOR_DIR = os.path.join(SKILL_ROOT, "assets", "vendor")

def bundle_offline(input_file, output_file=None):
    if not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}-offline{ext}"

    print(f"오프라인 슬라이드 번들링 시작: {input_file} -> {output_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Read vendor libraries
    d3_path = os.path.join(VENDOR_DIR, "d3.min.js")
    mermaid_path = os.path.join(VENDOR_DIR, "mermaid.min.js")

    with open(d3_path, "r", encoding="utf-8") as f:
        d3_code = f.read()
    with open(mermaid_path, "r", encoding="utf-8") as f:
        mermaid_code = f.read()

    # Safe replacement without regex template escaping issues
    d3_tag = '<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>'
    mermaid_tag = '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>'

    if d3_tag in html:
        html = html.replace(d3_tag, f'<script>\n/* D3.js (Offline Inlined) */\n{d3_code}\n</script>')
    if mermaid_tag in html:
        html = html.replace(mermaid_tag, f'<script>\n/* Mermaid.js (Offline Inlined) */\n{mermaid_code}\n</script>')

    # Remove fallback check blocks in offline mode
    html = re.sub(
        r'<script>\s*// Fallback if CDN blocked.*?</script>',
        '',
        html,
        flags=re.DOTALL
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"[OK] 오프라인 슬라이드 번들 완료: {output_file} ({size_mb:.2f} MB)")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seminar Slides Offline Bundler")
    parser.add_argument("input", help="Path to presentation HTML file")
    parser.add_argument("-o", "--output", help="Output path (default: <name>-offline.html)")
    args = parser.parse_args()

    bundle_offline(args.input, args.output)
