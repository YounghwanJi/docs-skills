# docs-skills

개인적으로 사용하는 **LLM Skills, 프롬프트 지침, 자동화 스크립트 및 도구 모음** 저장소입니다.

---

## 📌 저장소 목적

- 다양한 LLM 및 AI 에이전트(Claude Code, Codex, Antigravity 등)에서 재사용 가능한 맞춤형 스킬과 가이드를 관리합니다.
- 복잡한 워크플로우를 표준화된 스킬 형태로 패키징하여 작업 생산성을 향상시킵니다.
- 단일 표준 위치인 `skills/` 디렉터리를 중심으로 관리하며, 각 AI 도구에서 유연하게 참조 및 연동할 수 있도록 설계되었습니다.

---

## 📂 Skills 및 도구 목록

| 스킬 / 도구명 | 위치 링크 | 설명 | 지원 환경 |
| :--- | :--- | :--- | :--- |
| **study-material-generator** | [`skills/study-material-generator/`](./skills/study-material-generator/SKILL.md) | 표준/논문 기반의 기술 주제를 깊이 있게 학습·발표할 수 있는 자급자족형(Single-file) HTML 스터디 문서 생성기 | Claude, Codex, Antigravity |

---

### 📖 스킬 상세 안내: `study-material-generator`

- **개요**: 프로토콜, 표준, 알고리즘, 아키텍처 등 기술 주제에 대해 정량적 근거(RFC/논문) 기반의 고품질 단일 `study.html` 문서를 생성합니다.
- **주요 기능**:
  - 위키독스(Wikidocs) 스타일 목차 트리 네비게이션 및 반응형 레이아웃
  - 단일 HTML 파일 내 JSON 데이터 기반 자동 렌더링 및 Ctrl+K 검색 색인
  - 기술별 트레이드오프 비교표, D3.js 기반 시각화 차트, Mermaid 다이어그램 지원
  - 다크/라이트 테마, 각주 팝오버, 키보드 단축키(←/→ 챕터 이동, Shift+/ 용어 사전)
  - **프로덕션 및 클라우드(Cloud Native) 인프라 아키텍처 지원**: L4/L7 로드밸런싱, 네트워크 경계/NAT 트래버설, 컨테이너 호스트 네트워킹, 글로벌 엣지 가속 등 실무 배포 인프라 구조 표준화
  - **인라인 마크다운 자동 보정**: `**bold**`, `` `code` `` 혼용 시 브라우저에서 `<strong>`, `<code>`로 자동 치환하여 깨짐 방지
  - **JSON 런타임 오류 오버레이**: 데이터 문법 오류 발생 시 상세 라인과 원인을 화면에 친절히 표시
  - **CLI 검증 도구 내장**: `python skills/study-material-generator/scripts/validate-study.py <파일>`로 문법/스키마/각주 정합성 자동 검증
  - **폐쇄망/보안망 단일 오프라인 번들러**: `python skills/study-material-generator/scripts/bundle-offline.py <파일>`로 외부 CDN 의존성(D3, Mermaid)을 인라인 임베딩한 완전 독립 단일 파일(`study-offline.html`) 즉시 생성
- **사용 방법**:
  - 에이전트에게 주제와 함께 요청:
    > "QUIC 프로토콜에 대해 study-material-generator 스킬을 사용해서 스터디 자료 만들어줘."
  - 폐쇄망/보안망용 결과물이 필요한 경우:
    > "오프라인/폐쇄망용 번들도 같이 만들어줘."
  - 에이전트는 [`SKILL.md`](./skills/study-material-generator/SKILL.md) 및 `references/` 가이드를 먼저 읽고 표준 템플릿(`assets/template.html`)을 기반으로 완성된 `study.html`을 생성합니다.
  - 대규모 주제(3개 이상 챕터)의 경우 토큰 초과 방지를 위해 **골격 생성 → 챕터별 순차 생성(Chunking) → 용어집/각주 최종 연결**의 점진적 워크플로우를 따릅니다.



---

## 🔌 각 AI 에이전트 도구별 연동 가이드

본 저장소의 모든 스킬은 **`skills/<skill_name>/`** 디렉터리에 표준 포맷(YAML frontmatter + `SKILL.md` + 보조 리소스)으로 배치되어 있습니다.  
각 에이전트 도구에서 이 스킬들을 활용하는 방법은 다음과 같습니다:

### 1. Claude Code
- **저장소 내 작업 시**: 루트의 [`CLAUDE.md`](./CLAUDE.md)가 [`AGENTS.md`](./AGENTS.md)를 참조하므로, Claude Code에게 스킬 이름을 언급하면 `skills/` 디렉터리의 지침을 자동으로 로드합니다.
- **다른 프로젝트에 스킬 등록 시**:  
  해당 프로젝트의 `.claude/skills/` 디렉터리에 본 저장소의 스킬 폴더를 심볼릭 링크하거나 복사합니다.
  ```bash
  # 예시 (Linux / macOS / Git Bash)
  mkdir -p .claude/skills
  ln -s /path/to/docs-skills/skills/study-material-generator .claude/skills/study-material-generator
  ```

### 2. Antigravity (AGY / Gemini)
- **저장소 내 작업 시**: [`AGENTS.md`](./AGENTS.md) 및 [`GEMINI.md`](./GEMINI.md)에 명시된 규칙에 따라 `skills/` 폴더를 자동으로 탐색하여 실행합니다.
- **다른 프로젝트에 네이티브 스킬로 등록 시**:  
  해당 프로젝트의 `.agents/skills/`에 스킬 폴더를 링크하거나 복사합니다.
  ```bash
  # Windows PowerShell (디렉터리 Junction 예시)
  New-Item -ItemType Directory -Force -Path ".agents\skills"
  New-Item -ItemType Junction -Path ".agents\skills\study-material-generator" -Target "d:\workspace\git\docs-skills\skills\study-material-generator"
  ```

### 3. Codex (OpenAI Codex / Copilot / Cursor)
- **저장소 내 작업 시**: 루트의 [`CODEX.md`](./CODEX.md) 및 [`AGENTS.md`](./AGENTS.md) 지침을 통해 `skills/` 경로의 `SKILL.md`를 프롬프트 컨텍스트로 읽고 작업을 수행합니다.

---

## 🛠️ 작업 및 기여 규칙

이 저장소에서 작업을 수행하는 LLM 에이전트 및 사용자는 [`AGENTS.md`](./AGENTS.md)에 정의된 규칙을 준수합니다.

1. **명시적 지시 전 Commit/Push 금지**: 사용자의 명시적인 지시가 있을 때만 커밋 및 푸시를 진행합니다.
2. **Conventional Commits & 한국어 커밋 메시지**: 커밋 메시지는 한국어로 상세하게 작성하며 표준 Conventional Commits 형식을 따릅니다.
3. **README.md 동기화**: 신규 스킬, 스크립트, 도구가 추가되거나 변경될 때 본 `README.md`에 설명, 사용법, 요구사항 등을 상세히 업데이트합니다.

---

## 📄 라이선스

이 프로젝트는 [MIT License](./LICENSE)를 따릅니다.
