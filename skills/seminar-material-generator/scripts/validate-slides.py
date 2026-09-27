# -*- coding: utf-8 -*-
"""
Seminar Slides Validation CLI Tool
Usage: python validate-slides.py <path-to-slides.html>
"""
import sys
import json
import re
import os

def validate_slides(file_path):
    print(f"검사 대상 슬라이드 파일: {file_path}")
    if not os.path.exists(file_path):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. JSON Data Extraction
    pattern = r'<script type="application/json" id="slides-data">(.*?)</script>'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("[ERROR] <script id='slides-data'> 태그를 찾을 수 없습니다.")
        return False

    json_str = match.group(1).strip()
    try:
        data = json.loads(json_str)
        print("[OK] JSON 문법 유효성 통과")
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 파싱 오류: {e}")
        return False

    # 2. Schema Validation
    if not data.get("title"):
        print("[WARNING] 슬라이드 전체 'title'이 정의되지 않았습니다.")
    
    slides = data.get("slides", [])
    if not slides:
        print("[ERROR] 'slides' 배열이 비어 있습니다.")
        return False

    print(f"[INFO] 총 슬라이드 수: {len(slides)}장")

    notes_missing = 0
    diagram_count = 0

    for idx, s in enumerate(slides, 1):
        s_type = s.get("type", "split")
        heading = s.get("heading") or s.get("title") or f"Slide {idx}"

        # Notes Check
        if not s.get("notes") or not s["notes"].strip():
            notes_missing += 1

        # Visual check
        visual = s.get("visual", {})
        if visual.get("type") == "mermaid":
            diagram_count += 1
            m_content = visual.get("content", "").strip()
            # Basic arrow check
            bad_arrows = re.findall(r'--[^-]+?-->', m_content)
            if bad_arrows:
                print(f"  [WARNING] Slide {idx} Mermaid 라벨 문법 주의: {bad_arrows}")

    if notes_missing > 0:
        print(f"[WARNING] 발표자 노트(notes)가 누락된 슬라이드가 {notes_missing}개 있습니다. 학회 발표 준비를 위해 보강을 권장합니다.")
    else:
        print("[OK] 모든 슬라이드에 발표자 노트(notes)가 완벽히 등록되어 있습니다.")

    est_minutes = len(slides) * 1.5
    print(f"[INFO] 다이어그램 슬라이드: {diagram_count}개")
    print(f"[INFO] 예상 발표 소요 시간: 약 {est_minutes:.1f}분 (슬라이드당 1.5분 기준)")
    print("[OK] 슬라이드 검증 완료: 정상적으로 발표에 사용할 수 있습니다.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python validate-slides.py <path-to-slides.html>")
        sys.exit(1)
    success = validate_slides(sys.argv[1])
    sys.exit(0 if success else 1)
