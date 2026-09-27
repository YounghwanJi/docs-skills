#!/usr/bin/env python3
"""
validate-study.py

study-material-generator 스킬로 생성된 HTML 파일 내 #content-data JSON의
문법 유효성 및 스키마 정합성을 검증하는 독립 CLI 스크립트.
(Python 3 표준 라이브러리만 사용)
"""

import sys
import os
import re
import json
from pathlib import Path

# Windows 터미널 한글 깨짐 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def print_err(msg):
    print(f"\033[91m[ERROR]\033[0m {msg}", file=sys.stderr)

def print_warn(msg):
    print(f"\033[93m[WARN]\033[0m {msg}")

def print_ok(msg):
    print(f"\033[92m[OK]\033[0m {msg}")

def validate_study_file(file_path):
    path = Path(file_path)
    if not path.is_file():
        print_err(f"파일을 찾을 수 없습니다: {path.resolve()}")
        return False

    content = path.read_text(encoding="utf-8")

    # 1. <script type="application/json" id="content-data"> 블록 추출
    match = re.search(r'<script\b[^>]*\bid=["\']content-data["\'][^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    if not match:
        print_err(f"{path.name} 내에서 id='content-data' 스크립트 태그를 찾을 수 없습니다.")
        return False

    raw_json = match.group(1).strip()
    if not raw_json:
        print_err(f"{path.name}의 #content-data 블록이 비어 있습니다.")
        return False

    # 2. JSON 문법 파싱 검사
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print_err(f"JSON 문법 오류가 발견되었습니다 (Line {e.lineno}, Col {e.colno}): {e.msg}")
        lines = raw_json.splitlines()
        start = max(0, e.lineno - 4)
        end = min(len(lines), e.lineno + 3)
        print("\n--- [오류 주변 스니펫] ---")
        for i in range(start, end):
            prefix = ">>" if (i + 1) == e.lineno else "  "
            print(f"{prefix} {i+1:4d}: {lines[i]}")
        print("------------------------\n")
        return False

    print_ok(f"JSON 문법 유효성 통과 ({path.name})")

    # 3. 필수 스키마 검증
    errors = []
    warnings = []

    required_top = ["title", "version", "learningGoals", "chapters", "glossary", "references"]
    for key in required_top:
        if key not in data:
            errors.append(f"최상위 필수 필드 누락: '{key}'")

    chapters = data.get("chapters", [])
    if not isinstance(chapters, list) or len(chapters) == 0:
        errors.append("'chapters' 배열이 비어있거나 올바른 형식이 아닙니다.")
    else:
        chapter_ids = set()
        for idx, ch in enumerate(chapters):
            ch_num = idx + 1
            if not isinstance(ch, dict):
                errors.append(f"챕터 {ch_num}: 유효한 객체가 아닙니다.")
                continue

            ch_id = ch.get("id")
            if not ch_id:
                errors.append(f"챕터 {ch_num}: 'id' 필드 누락")
            else:
                chapter_ids.add(ch_id)

            if not ch.get("title"):
                errors.append(f"챕터 {ch_num}: 'title' 필드 누락")
            elif re.match(r'^\s*\d+[\.\s장]', ch.get("title", "")):
                warnings.append(f"챕터 {ch_num} 제목 '{ch.get('title')}': 번호가 수동으로 붙어있습니다. 템플릿이 자동 번호 매김을 지원하므로 번호를 제거하는 것을 권장합니다.")

            if not ch.get("motivation"):
                warnings.append(f"챕터 {ch_num}: 'motivation' (왜 중요한가) 필드가 없습니다.")

            sections = ch.get("sections", [])
            if not isinstance(sections, list) or len(sections) == 0:
                errors.append(f"챕터 {ch_num}: 'sections'가 비어 있습니다.")
            else:
                for s_idx, sec in enumerate(sections):
                    if not sec.get("heading"):
                        errors.append(f"챕터 {ch_num} 섹션 {s_idx+1}: 'heading' 필드 누락")
                    if not sec.get("html"):
                        errors.append(f"챕터 {ch_num} 섹션 {s_idx+1}: 'html' 내용 누락")

            if "compareTables" in ch and ch["compareTables"]:
                for t_idx, tbl in enumerate(ch["compareTables"]):
                    if not tbl.get("verdict"):
                        warnings.append(f"챕터 {ch_num} 비교표 {t_idx+1}: 'verdict' (판정 문장)가 비어 있습니다.")

    # 4. 각주 [data-ref] 와 references id 정합성
    ref_ids = set()
    for ref in data.get("references", []):
        if isinstance(ref, dict) and "id" in ref:
            ref_ids.add(ref["id"])

    # sections 내부의 data-ref 추출
    found_refs = set()
    for ch in chapters:
        for sec in ch.get("sections", []):
            html = sec.get("html", "")
            for ref_val in re.findall(r'data-ref=["\'](\d+)["\']', html):
                found_refs.add(int(ref_val))

    missing_refs = found_refs - ref_ids
    if missing_refs:
        warnings.append(f"본문 각주에서 참조하지만 references에 정의되지 않은 ID: {sorted(list(missing_refs))}")

    # 5. 용어집 seeIn 챕터 ID 정합성
    for g in data.get("glossary", []):
        see_in = g.get("seeIn", [])
        for ch_id in see_in:
            if ch_id not in chapter_ids:
                warnings.append(f"용어집 '{g.get('term')}': 존재하지 않는 챕터 ID '{ch_id}'를 참조하고 있습니다.")

    # 6. 결과 출력
    if warnings:
        print("\n--- [권장 개선 사항 (Warnings)] ---")
        for w in warnings:
            print_warn(w)

    if errors:
        print("\n--- [스키마 오류 (Errors)] ---")
        for err in errors:
            print_err(err)
        return False

    print_ok(f"스키마 검증 성공: 총 {len(chapters)}개 챕터, {len(data.get('glossary', []))}개 용어, {len(data.get('references', []))}개 참고문헌이 정상 구성되었습니다.")
    return True

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # 기본 탐색
        candidates = ["study.html", "skills/study-material-generator/assets/template.html"]
        target = None
        for c in candidates:
            if os.path.exists(c):
                target = c
                break
        if not target:
            print("사용법: python validate-study.py <검사할-html-파일-경로>")
            sys.exit(1)

    print(f"검사 대상 파일: {target}")
    success = validate_study_file(target)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
