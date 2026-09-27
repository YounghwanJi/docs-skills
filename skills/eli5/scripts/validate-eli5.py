#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ELI5 Explainer HTML 문서 검증 도구
사용법: python skills/eli5/scripts/validate-eli5.py <path_to_eli5_html>
"""
import sys
import os
import json
import re

def validate_eli5(file_path):
    print(f"검사 대상 파일: {file_path}")
    if not os.path.exists(file_path):
        print(f"[FAIL] 파일을 찾을 수 없습니다: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. content-data 태그 존재 여부 검사
    match = re.search(r'<script\s+type=["\']application/json["\']\s+id=["\']content-data["\']>(.*?)</script>', content, re.DOTALL)
    if not match:
        print("[FAIL] <script type=\"application/json\" id=\"content-data\"> 블록이 존재하지 않습니다.")
        return False

    json_raw = match.group(1).strip()
    try:
        data = json.loads(json_raw)
        print("[OK] JSON 문법 파싱 성공")
    except Exception as e:
        print(f"[FAIL] JSON 파싱 오류: {e}")
        return False

    # 2. 필수 최상위 필드 검증
    if not data.get("topic"):
        print("[FAIL] 'topic' 필드가 누락되었습니다.")
        return False

    levels = data.get("levels")
    if not levels or not isinstance(levels, list) or len(levels) == 0:
        print("[FAIL] 'levels' 배열이 비어 있거나 올바르지 않습니다.")
        return False

    print(f"[INFO] 등록된 청중 레벨 수: {len(levels)}개")

    # 3. 레벨별 필수 필드 검증
    required_level_fields = ["id", "label", "essence", "analogyText", "steps", "whyItMatters", "qa"]
    for idx, lvl in enumerate(levels):
        lvl_name = lvl.get("label") or lvl.get("id") or f"Level {idx}"
        for rf in required_level_fields:
            if rf not in lvl or not lvl[rf]:
                print(f"[FAIL] [{lvl_name}] 레벨에 필수 필드 '{rf}'가 누락되었습니다.")
                return False

        if not isinstance(lvl["steps"], list) or len(lvl["steps"]) == 0:
            print(f"[FAIL] [{lvl_name}] 'steps' 배열에 최소 1개 이상의 스텝이 필요합니다.")
            return False

        if not isinstance(lvl["qa"], list):
            print(f"[FAIL] [{lvl_name}] 'qa' 필드는 배열이어야 합니다.")
            return False

        for q_idx, q_item in enumerate(lvl["qa"]):
            if "q" not in q_item or "a" not in q_item:
                print(f"[FAIL] [{lvl_name}] Q&A 항목 #{q_idx+1}에 'q' 또는 'a'가 누락되었습니다.")
                return False

        print(f"  - [{lvl_name}]: 스텝 {len(lvl['steps'])}개, Q&A {len(lvl['qa'])}개 확인 완료")

    print("[OK] ELI5 산출물 스키마 및 데이터 유효성 검증 완료!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python validate-eli5.py <file.html>")
        sys.exit(1)

    success = validate_eli5(sys.argv[1])
    sys.exit(0 if success else 1)
