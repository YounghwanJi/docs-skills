#!/usr/bin/env python3
"""
bundle-offline.py

study-material-generator로 생성된 HTML 문서에서 외부 CDN 의존성(Mermaid, D3.js 등)을
인라인으로 직접 임베딩하여, 인터넷이 연결되지 않은 폐쇄망/보안망 환경에서도
완전히 동작하는 단일 오프라인 HTML 파일(study-offline.html)을 생성합니다.
(Python 3 표준 라이브러리만 사용)
"""

import sys
import os
import re
import argparse
import urllib.request
from pathlib import Path

# Windows 터미널 한글 깨짐 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_ROOT = SCRIPT_DIR.parent
CACHE_DIR = SKILL_ROOT / "assets" / "vendor"

def print_err(msg):
    print(f"\033[91m[ERROR]\033[0m {msg}", file=sys.stderr)

def print_ok(msg):
    print(f"\033[92m[OK]\033[0m {msg}")

def print_info(msg):
    print(f"\033[94m[INFO]\033[0m {msg}")

def fetch_resource(url: str, cache_filename: str) -> str:
    """캐시 디렉터리에서 먼저 찾고, 없으면 다운로드하여 캐시 후 내용 반환."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / cache_filename

    if cache_path.is_file() and cache_path.stat().st_size > 0:
        print_info(f"로컬 캐시 사용: {cache_filename}")
        return cache_path.read_text(encoding="utf-8")

    print_info(f"리소스 다운로드 중: {url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = res.read().decode("utf-8")
        cache_path.write_text(data, encoding="utf-8")
        print_ok(f"다운로드 및 캐시 완료: {cache_filename} ({len(data)//1024} KB)")
        return data
    except Exception as e:
        print_err(f"다운로드 실패 ({url}): {e}")
        return None

def bundle_html(input_file: Path, output_file: Path) -> bool:
    if not input_file.is_file():
        print_err(f"입력 파일을 찾을 수 없습니다: {input_file}")
        return False

    content = input_file.read_text(encoding="utf-8")

    # 1. 외부 CDN 스크립트 매핑 (Mermaid, D3)
    cdn_targets = [
        {
            "name": "mermaid",
            "regex": r'<script\b[^>]*\bsrc=["\'][^"\']*mermaid(?:\.min)?\.js[^"\']*["\'][^>]*>\s*</script>',
            "default_url": "https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js",
            "cache_file": "mermaid.min.js"
        },
        {
            "name": "d3",
            "regex": r'<script\b[^>]*\bsrc=["\'][^"\']*d3(?:\.v\d+)?(?:\.min)?\.js[^"\']*["\'][^>]*>\s*</script>',
            "default_url": "https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js",
            "cache_file": "d3.min.js"
        }
    ]

    for target in cdn_targets:
        match = re.search(target["regex"], content, re.IGNORECASE)
        if match:
            # src URL 추출 시도
            src_match = re.search(r'src=["\']([^"\']+)["\']', match.group(0), re.IGNORECASE)
            url = src_match.group(1) if src_match else target["default_url"]
            if url.startswith("//"):
                url = "https:" + url

            js_code = fetch_resource(url, target["cache_file"])
            if js_code:
                # script 태그 내부 인라인 코드로 치환
                inlined_tag = f"<!-- Inlined {target['name']}.js (offline bundle) -->\n<script>\n{js_code}\n</script>"
                content = content[:match.start()] + inlined_tag + content[match.end():]
                print_ok(f"{target['name']}.js 인라인 임베딩 완료")
            else:
                print_err(f"{target['name']}.js 리소스를 가져오지 못해 인라인 처리를 건너뜁니다.")

    # 2. 외부 폰트 CDN 주석 처리 (폐쇄망에서 타임아웃 방지 및 시스템 폰트 폴백 안내)
    # Pretendard CDN
    content = re.sub(
        r'(<link\b[^>]*href=["\'][^"\']*pretendard[^"\']*["\'][^>]*>)',
        r'<!-- \1 (폐쇄망: 시스템 기본 폰트로 폴백됨) -->',
        content,
        flags=re.IGNORECASE
    )
    # Google Fonts
    content = re.sub(
        r'(<link\b[^>]*href=["\'][^"\']*fonts\.googleapis\.com[^"\']*["\'][^>]*>)',
        r'<!-- \1 (폐쇄망: 시스템 고정폭 폰트로 폴백됨) -->',
        content,
        flags=re.IGNORECASE
    )
    # Preconnect links
    content = re.sub(
        r'(<link\b[^>]*rel=["\']preconnect["\'][^>]*>)',
        r'<!-- \1 -->',
        content,
        flags=re.IGNORECASE
    )

    # 3. 오프라인 배지 메타데이터 주석 추가
    offline_notice = (
        "\n<!-- [OFFLINE BUNDLE] 본 문서는 폐쇄망/보안망 환경용 완전 독립 단일 파일로 빌드되었습니다. -->\n"
    )
    content = content.replace("<head>", "<head>" + offline_notice, 1)

    # 4. 결과 파일 저장
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding="utf-8")
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print_ok(f"오프라인 단일 파일 생성 완료: {output_file.resolve()} ({size_mb:.2f} MB)")
    return True

def main():
    parser = argparse.ArgumentParser(description="단일 오프라인 study.html 번들 생성기")
    parser.add_argument("input", nargs="?", default="study.html", help="입력 HTML 파일 (기본값: study.html)")
    parser.add_argument("-o", "--output", help="출력 HTML 파일 (기본값: <input파일명>-offline.html)")

    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.is_file():
        # assets/template.html fallback for testing
        template_candidate = SKILL_ROOT / "assets" / "template.html"
        if args.input == "study.html" and template_candidate.is_file():
            input_path = template_candidate

    if args.output:
        output_path = Path(args.output)
    else:
        stem = input_path.stem if input_path.stem != "template" else "study"
        output_path = input_path.parent / f"{stem}-offline.html"

    print(f"변환 시작: {input_path.name} -> {output_path.name}")
    success = bundle_html(input_path, output_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
