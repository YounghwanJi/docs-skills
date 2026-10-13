#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate-deck.py
Scrolline v2 deck.yaml 유효성 검사 스크립트.

검증 항목:
1. 필수 헤더 메타데이터 (id, title, concept)
2. 유효한 6대 콘셉트 (rail, data, launch, zoom, canvas, kinetic)
3. 수치 날조 방지 (sample: false 시 sources 필수, 차트/수치 비트의 source 참조)
4. 비트(Beats) 구조 및 필수 필드 (id, type, place)
5. 발표자 노트(notes.script) 작성 여부
6. 정지점(Stop) 수 및 예상 발표 소요 시간 집계
"""

import sys
import os
import re

# Windows 콘솔 인코딩 대응
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VALID_CONCEPTS = {"rail", "data", "launch", "zoom", "canvas", "kinetic"}
VALID_CLASSIFICATIONS = {"CONFIDENTIAL", "INTERNAL USE ONLY", "PUBLIC", None}

def _strip_comment(val_str):
    """문자열 내 인라인 주석(#) 제거 (따옴표 내부 제외)"""
    in_quote = None
    for i, ch in enumerate(val_str):
        if ch in ('"', "'"):
            if in_quote == ch:
                in_quote = None
            elif in_quote is None:
                in_quote = ch
        elif ch == '#' and in_quote is None:
            return val_str[:i].strip()
    return val_str.strip()

def _parse_yaml_fallback(text):
    """PyYAML 미설치 시 작동하는 경량 기본 YAML 파서 (표준 deck.yaml 구조 지원)"""
    data = {"beats": [], "sources": []}
    current_section = None
    current_item = None

    lines = text.splitlines()
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))

        # 1. 루트 키-값
        if indent == 0 and ":" in line:
            parts = line.split(":", 1)
            k = parts[0].strip()
            v = _strip_comment(parts[1])
            if v == "" or v == "[]":
                current_section = k
                if k not in data:
                    data[k] = [] if k in ("beats", "sources") else {}
            else:
                current_section = None
                v = v.strip("\"' ")
                if v.lower() == "true": v = True
                elif v.lower() == "false": v = False
                elif v.lower() == "null": v = None
                data[k] = v
            continue

        # 2. beats / sources 최상위 리스트 아이템 시작 (- ) (indent == 2)
        if indent == 2 and line.startswith("- "):
            item_content = line[2:].strip()
            item = {}
            if ":" in item_content:
                k, v = item_content.split(":", 1)
                k = k.strip()
                v = _strip_comment(v).strip("\"' ")
                item[k] = v
            current_item = item
            if current_section and isinstance(data.get(current_section), list):
                data[current_section].append(item)
            continue

        # 3. 비트 내부 하위 키-값 (indent >= 4)
        if ":" in line and current_item is not None and indent >= 4:
            parts = line.split(":", 1)
            k = parts[0].strip()
            v = _strip_comment(parts[1])
            v_clean = v.strip("\"' ")
            if v == "":
                # 서브 컨테이너 (예: notes:, steps:, place:)
                if k not in current_item:
                    current_item[k] = {}
            else:
                if v_clean.isdigit(): v_val = int(v_clean)
                elif v_clean.lower() == "true": v_val = True
                elif v_clean.lower() == "false": v_val = False
                elif v_clean.lower() == "null": v_val = None
                else: v_val = v_clean
                
                # notes 하위인지 체크
                if "notes" in current_item and isinstance(current_item["notes"], dict) and indent >= 6:
                    current_item["notes"][k] = v_val
                elif "place" in current_item and isinstance(current_item["place"], dict) and indent >= 6:
                    current_item["place"][k] = v_val
                else:
                    current_item[k] = v_val

    return data

def load_yaml(file_path):
    try:
        import yaml
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        # PyYAML이 없는 경우 내장 fallback 파서 사용
        with open(file_path, "r", encoding="utf-8") as f:
            return _parse_yaml_fallback(f.read())
    except Exception as e:
        raise RuntimeError(f"YAML 파일 파싱 실패: {e}")

def validate_deck(deck_path):
    print(f"\n[검사 시작] 대상 파일: {deck_path}")
    if not os.path.exists(deck_path):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {deck_path}")
        return False

    errors = []
    warnings = []

    try:
        data = load_yaml(deck_path)
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

    if not isinstance(data, dict):
        print("[ERROR] deck.yaml의 루트는 맵(Dictionary) 형태여야 합니다.")
        return False

    # 1. 필수 헤더 검증
    deck_id = data.get("id")
    title = data.get("title")
    concept = data.get("concept")
    is_sample = data.get("sample", False)
    classification = data.get("classification")

    if not deck_id:
        errors.append("헤더에 'id' 필드가 누락되었습니다.")
    if not title:
        errors.append("헤더에 'title' 필드가 누락되었습니다.")
    if not concept:
        errors.append("헤더에 'concept' 필드가 누락되었습니다.")
    elif concept not in VALID_CONCEPTS:
        errors.append(f"유효하지 않은 콘셉트입니다: '{concept}'. 허용 값: {', '.join(sorted(VALID_CONCEPTS))}")

    if classification and classification not in VALID_CLASSIFICATIONS:
        warnings.append(f"표준 보안 등급(CONFIDENTIAL, INTERNAL USE ONLY, PUBLIC)이 아닙니다: '{classification}'")

    # 2. 수치 날조 방지 검증 (sample: false)
    sources = data.get("sources", [])
    source_ids = {s.get("id") for s in sources if isinstance(s, dict) and "id" in s}

    if not is_sample and not sources:
        warnings.append("실데이터 덱('sample: false')이지만 헤더에 'sources' 목록이 비어 있습니다.")

    # 3. 비트(Beats) 검증
    beats = data.get("beats", [])
    if not beats or not isinstance(beats, list):
        errors.append("'beats' 목록이 비어 있거나 올바른 배열이 아닙니다.")
        total_stops = 0
    else:
        total_stops = len(beats)
        total_seconds = 0
        notes_count = 0

        for idx, beat in enumerate(beats, 1):
            if not isinstance(beat, dict):
                errors.append(f"비트 #{idx}: 딕셔너리 구조가 아닙니다.")
                continue

            b_id = beat.get("id")
            b_type = beat.get("type")
            b_place = beat.get("place")
            b_notes = beat.get("notes", {})
            b_steps = beat.get("steps", [])

            if not b_id:
                errors.append(f"비트 #{idx}: 'id'가 누락되었습니다.")
            if not b_type:
                errors.append(f"비트 #{idx} ({b_id}): 'type'이 누락되었습니다.")
            if not b_place:
                warnings.append(f"비트 #{idx} ({b_id}): 'place' 설정이 없습니다. 기본 슬롯이 적용됩니다.")

            # 차트/수치 비트 출처 체크
            if b_type in ("chart", "number", "metric") and not is_sample:
                b_source = beat.get("source")
                if not b_source:
                    warnings.append(f"비트 #{idx} ({b_id}): {b_type} 타입이지만 'source' 참조가 없습니다.")
                elif b_source not in source_ids:
                    warnings.append(f"비트 #{idx} ({b_id}): 지정된 source '{b_source}'가 상단 sources 목록에 없습니다.")

            # 발표자 노트 확인
            if isinstance(b_notes, dict):
                script = b_notes.get("script", "")
                dur = b_notes.get("duration_sec", 30)
                if script:
                    notes_count += 1
                else:
                    warnings.append(f"비트 #{idx} ({b_id}): 발표자 대본(notes.script)이 비어 있습니다.")
                total_seconds += int(dur)
            elif isinstance(b_notes, str) and b_notes.strip():
                notes_count += 1
                total_seconds += 30
            else:
                warnings.append(f"비트 #{idx} ({b_id}): 발표자 대본(notes.script)이 누락되었습니다.")
                total_seconds += 30

            # Step 추가 정지점 카운트
            if isinstance(b_steps, list):
                total_stops += len(b_steps)

        # 요약 리포트
        min_est = total_seconds // 60
        sec_est = total_seconds % 60
        print("[통계 분석]")
        print(f"   * 콘셉트: {concept}")
        print(f"   * 총 Beat 수: {len(beats)}개")
        print(f"   * 총 정지점(Stops) 수: 약 {total_stops}개")
        print(f"   * 발표자 대본 작성률: {notes_count}/{len(beats)} ({(notes_count/len(beats)*100):.1f}%)")
        print(f"   * 예상 발표 소요 시간: 약 {min_est}분 {sec_est}초")

    # 결과 출력
    if warnings:
        print("\n[WARNING] 권고 사항:")
        for w in warnings:
            print(f"   - {w}")

    if errors:
        print("\n[ERROR] 검증 실패 (수정 필요):")
        for e in errors:
            print(f"   - {e}")
        return False

    print("\n[OK] 검증 성공: deck.yaml 구조와 작성 규범이 Scrolline v2 기준을 만족합니다!\n")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python validate-deck.py <path/to/deck.yaml>")
        sys.exit(1)

    target_file = sys.argv[1]
    success = validate_deck(target_file)
    sys.exit(0 if success else 1)
