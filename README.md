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
| **source-onboarding-generator** | [`skills/source-onboarding-generator/`](./skills/source-onboarding-generator/SKILL.md) | 소스 근거와 검증 상태를 갖춘 개발자 온보딩 문서 생성기. 기본 Markdown, HTML 템플릿·학습 UX·검증 도구를 내장한 독립 배포 패키지 | Claude, Codex, Antigravity |
| **seminar-material-generator** | [`skills/seminar-material-generator/`](./skills/seminar-material-generator/SKILL.md) | 학회, 기술 컨퍼런스, 사내 세미나 발표를 위한 16:9 와이드스크린 반응형 웹 슬라이드 덱(Presentation Deck) 생성기 | Claude, Codex, Antigravity |
| **scroll-deck-generator** | [`skills/scroll-deck-generator/`](./skills/scroll-deck-generator/SKILL.md) | `seminar-material-generator`를 상속받아 6대 모션 문법과 단일 GSAP 연속 타임라인 기반의 고화질 스크롤 발표 덱(Scrolline v2 deck) 및 MP4 영상 추출을 지원하는 프레젠테이션 생성기 | Claude, Codex, Antigravity |
| **eli5** | [`skills/eli5/`](./skills/eli5/SKILL.md) | [DreambigOu/ELI5](https://github.com/DreambigOu/ELI5)를 기반으로 수정한 스킬로, 5세 어린이부터 비기술직 경영진, 전공자까지 청중별 맞춤형 설명(대화형 답변 및 인터랙티브 웹 익스플레이너 `eli5.html`) 생성 | Claude, Codex, Antigravity |

---

### 📖 스킬 상세 안내: `study-material-generator`

- **개요**: 프로토콜, 표준, 알고리즘, 아키텍처 등 기술 주제에 대해 정량적 근거(RFC/논문) 기반의 고품질 단일 `study.html` 문서를 생성합니다.
- **주요 기능**:
  - **Docusaurus 스타일 멀티 프로젝트 아코디언 허브 (Multi-Project Accordion Hub)**: 여러 개의 독립 가이드/프로젝트를 하나의 `study.html`에서 통합 관리할 수 있는 폴더 아코디언(`📁 [아이콘] 프로젝트명`) 지원. 활성 프로젝트 자동 펼침(Auto-expand) 및 접기/펼치기 지원, 단일 프로젝트 시 플랫한 챕터 목록으로 자동 전환 (챕터 내 소제목은 우측 인페이지 TOC로 깔끔하게 분리)
  - **모바일 반응형 완벽 대응 & 토글 단일화**: 중복 햄버거 메뉴를 제거하고 헤더 사이드바 토글 버튼 하나로 데스크톱 집중 모드와 모바일 드로어를 완벽 제어하며, 좁은 화면에서도 가로 스크롤 잘림 없는 최적화된 레이아웃 제공
  - **사이드바 접기/펼치기 (`[` 단축키 & 헤더 토글)**: 데스크톱 화면에서 사이드바를 완전히 접어(Collapse) 본문을 시원하게 넓혀 읽는 집중 모드 지원, 모바일 드로어 연동 및 `localStorage` 상태 보존
  - **키보드 생산성 단축키 체계**:
    - `[` : 사이드바 접기 / 펼치기 (Toggle Sidebar)
    - `t` / `T` : 라이트 / 다크 테마 전환 (Toggle Theme)
    - `Ctrl + K` : 문서 전체 통합 키워드 검색
    - `Shift + /` (`?`) : 약어 및 용어 사전 (Glossary) 열기
    - `←` / `→` : 이전 / 다음 챕터 이동
    - `Esc` : 모달 및 사이드바 드로어 닫기
  - 상단 독립 대시보드 카드(홈/개요) 및 챕터 목록 분리형 사이드바 UX, 반응형 레이아웃
  - 단일 HTML 파일 내 JSON 데이터 기반 자동 렌더링 및 Ctrl+K 검색 색인
  - 기술별 트레이드오프 비교표 및 **고대비 테두리 테이블**(일반 본문 HTML/GFM 마크다운 테이블/비트필드/비교표 전체에 라이트/다크 모드 고대비 경계선 적용), D3.js 기반 시각화 차트, Mermaid 다이어그램 지원
  - 다크/라이트 테마(부드러운 색상 전환 지원), 각주 팝오버(긴 URL 줄바꿈 대응)
  - **UX/UI 가독성 극대화**: 한글 최적화 본문 타이포그래피(16.5px / 420 weight / 1.75 줄간격), 단락 간 명확한 여백, 도표 확대 모달 가시성 개선(클린 화이트/다크 배경), 모바일 1-finger 패닝 및 2-finger 핀치 줌 제스처 지원
  - **코드 블록 원클릭 복사**: 언어 헤더 내 원클릭 클립보드 복사 버튼 내장 및 줄 번호/코드 영역 시각적 구분선 분리
  - **접근성 표준 준수**: `prefers-reduced-motion` 모션 감도 대응, `::selection` 브랜드 컬러 커스텀, 접근성 본문 스킵 링크
  - **프로덕션 및 클라우드(Cloud Native) 인프라 아키텍처 지원**: L4/L7 로드밸런싱, 네트워크 경계/NAT 트래버설, 컨테이너 호스트 네트워킹, 글로벌 엣지 가속 등 실무 배포 인프라 구조 표준화
  - **인라인 마크다운 자동 보정 및 GFM 테이블 렌더링**: 개행(Multiline)을 포함한 `**bold**`, `__bold__`, `` `code` ``(코드 토큰 보호) 자동 치환 및 본문 마크다운 테이블(`| 컬럼 |`)을 가로 스크롤 대응 고대비 테이블로 자동 렌더링
  - **JSON 런타임 오류 오버레이**: 데이터 문법 오류 발생 시 상세 라인과 원인을 화면에 친절히 표시
  - **CLI 검증 도구 내장**: `python skills/study-material-generator/scripts/validate-study.py <파일>`로 문법/스키마/각주 정합성 자동 검증
  - **폐쇄망/보안망 단일 오프라인 번들러**: `python skills/study-material-generator/scripts/bundle-offline.py <파일>`로 외부 CDN 의존성(D3, Mermaid)을 인라인 임베딩한 완전 독립 단일 파일(`study-offline.html`) 즉시 생성
- **사용 방법**:
  - 에이전트에게 주제와 함께 요청:
    > "QUIC 프로토콜에 대해 study-material-generator 스킬을 사용해서 스터디 자료 만들어줘."

---

### 📖 스킬 상세 안내: `source-onboarding-generator`

- **개요**: 소스 저장소를 분석해 프로젝트 이해, 로컬 실행, 기능 추적·변경·테스트, 배포·운영에 필요한 온보딩 문서를 생성하거나 갱신합니다.
- **주요 기능 및 상속 범위**:
  - 실제 소스·설정·테스트·IaC를 근거로 기능 카탈로그, 도메인 용어집, 호출 흐름, API·데이터, 개발·운영 가이드를 작성합니다.
  - 분석 기준 커밋·날짜·범위와 변경된 작업 트리를 기록하고, 확인된 사실·추론·확인 필요와 명령 실행 결과를 구분합니다.
  - `study-material-generator`의 근거 중심 작성, 학습 목표·요약·Q&A, 다이어그램 단계별 해설과 단계별 생성을 재사용합니다. HTML 모드에서는 기존 디자인·검색·용어집·테마·TOC·다이어그램 확대·코드 복사 기능을 사용합니다.
  - RFC 중심 근거, 모든 기술의 대안 비교, 비즈니스 정보 제외, 일괄 클라우드 서술은 소스 온보딩 목적에 맞게 재정의합니다. 필요한 자원을 패키지 내부에 포함하므로 실행 중 부모 스킬을 읽거나 설치할 필요가 없습니다.
- **입력/출력**:
  - 입력: 대상 저장소 경로, 선택적으로 모듈·핵심 기능, 문서 범위(P0~P3), 출력 형식과 경로.
  - 기본 출력: 기존 문서 구조를 우선하는 주제별 Markdown. 새 경로는 대상 저장소의 `docs/onboarding/index.md`와 하위 문서입니다.
  - HTML 요청: 대상 저장소의 `docs/onboarding/onboarding.html`. 두 형식을 요청하면 Markdown과 같은 근거·검증 결과를 반영합니다.
- **사용 방법**:
  > "source-onboarding-generator로 이 저장소의 P0 온보딩 문서를 docs/onboarding/에 Markdown으로 만들어줘."
  > "source-onboarding-generator로 주문 기능의 진입점부터 DB까지 추적하고, 첫 변경과 테스트 가이드를 단일 onboarding.html로 만들어줘."
  > "기존 온보딩 Markdown과 같은 내용으로 HTML도 만들고 폐쇄망용 번들을 제공해줘."
  - HTML 검증·오프라인 번들 예시(이 스킬 저장소 루트 기준, 입력·출력은 실제 파일 경로로 교체):
    ```bash
    python skills/source-onboarding-generator/scripts/validate-onboarding.py <onboarding.html 경로>
    python skills/source-onboarding-generator/scripts/bundle-offline.py <onboarding.html 경로> -o <onboarding-offline.html 경로>
    ```
- **의존성 및 사전 요구사항**:
  - 대상 저장소 읽기 권한과 산출물 경로 쓰기 권한. 빌드·테스트 실행 검증에는 대상 프로젝트의 도구·의존성이 필요하며 미실행 결과는 명시합니다.
  - **단독 설치**: `skills/source-onboarding-generator/` 전체를 대상 도구의 스킬 디렉터리에 복사하거나 링크합니다. `SKILL.md`, `assets/`, `references/`, `scripts/`가 모두 필요하며 `study-material-generator`는 함께 설치하지 않아도 됩니다. 설치된 스킬 폴더에서는 `python scripts/validate-onboarding.py <HTML 경로>`처럼 실행할 수 있습니다.
  - Markdown은 별도 라이브러리·API Key가 필요 없습니다. HTML 템플릿·내용/디자인/인터랙션 참고 문서와 검증·번들 도구는 모두 내장되어 있습니다.
  - HTML 검증·번들: Python 3 표준 라이브러리. 기본 HTML은 Mermaid·D3·폰트 CDN을 사용하며, 오프라인 번들은 포함된 Mermaid 10.9.1·D3 7.9.0 캐시를 인라인으로 넣고 시스템 폰트로 대체합니다. 기본 템플릿 번들에는 다운로드가 필요 없고, 지원 라이브러리를 가져오지 못하면 실패로 종료합니다. 추가 외부 리소스와 소스 근거 링크의 접근 권한은 별도 확인 대상입니다.
  - HTML 검증기는 기본 JSON·스키마를 검사합니다. 소스 설명의 정확성과 UI 동작은 별도로 확인하며, 각주·용어집 관련 경고도 검토합니다.
- **파일 위치**: [SKILL.md](./skills/source-onboarding-generator/SKILL.md), [내용 가이드](./skills/source-onboarding-generator/references/content-structure.md), [디자인 토큰](./skills/source-onboarding-generator/references/design-tokens.md), [인터랙션](./skills/source-onboarding-generator/references/interactions.md), [HTML 템플릿](./skills/source-onboarding-generator/assets/template.html), [검증 도구](./skills/source-onboarding-generator/scripts/validate-onboarding.py), [오프라인 번들러](./skills/source-onboarding-generator/scripts/bundle-offline.py), [Mermaid·D3 캐시](./skills/source-onboarding-generator/assets/vendor/).
- **자원 동기화**: 기반 스킬의 변경은 자동 반영되지 않습니다. 필요한 디자인·인터랙션 변경을 수동으로 반영하고 이 패키지의 문서·템플릿·스크립트를 함께 검증합니다. 내용 가이드는 온보딩에 맞게 수정되어 있으므로 부모 문서로 일괄 덮어쓰지 않습니다.

---

### 📖 스킬 상세 안내: `seminar-material-generator`

- **개요**: 학회, 테크 컨퍼런스, 세미나를 위한 **16:9 와이드스크린 반응형 프레젠테이션 슬라이드 덱(`slides.html`)**을 생성합니다. `study-material-generator`의 디자인 토큰과 UI 스타일을 100% 계승하여 시각적 일관성을 제공합니다.
- **주요 기능**:
  - **16:9 가상 뷰포트 반응형 스케일러**: 어떤 해상도(FHD, 4K, 빔프로젝터 XGA)에서도 비율 왜곡 없이 화면 중앙에 자동 정렬
  - **도표 배치 다형성 (`split` 좌우 vs `stacked` 상하)**: 다이어그램 형태(시퀀스/가로 파이프라인 ➔ 상하, 세로 흐름도 ➔ 좌우)에 맞춰 레이아웃을 자동 지정하고 도표 크기/가독성 극대화
  - **엔지니어링 핸드아웃 문서 뷰 (Docs Mode, `D` 키)**: 목차(TOC) 트리, 서술형 문단(한글 최적 줄간격 및 어절 단위 줄바꿈), 대형 다이어그램 뷰, 상세 엔지니어링 해설 블록으로 구성된 정식 기술 백서 모드 및 라이트/다크 테마 토글 지원
  - **발표자 모드 (Presenter View, `P` 키)**: 듀얼 모니터용 팝업 창 지원 (현재/다음 슬라이드 미리보기, 발표자 대본/스피치 노트, 경과 시간 타이머 동기화)
  - **보안 등급 배지 고정 지원**: `CONFIDENTIAL`, `INTERNAL USE ONLY`, `PUBLIC` 등 슬라이드 상단 및 핸드아웃 헤더에 보안 분류 표기
  - **전문성 타이포그래피 (이모지 배제)**: 학술·기술 세미나의 품격에 맞춰 본문 및 UI 전반에서 이모지를 배제하고 정갈한 뱃지와 타이포그래피 적용
  - **오버뷰 그리드 모드 (`O` 또는 `Esc` 키)**: 전체 슬라이드 썸네일 그리드 조망 및 빠른 점프
  - **무대 제어 인터랙션**: 단축키 도움말(`?` 또는 `Shift + /`), 화면 일시 암전(`B` 키), 전체화면(`F` 키), 다크/라이트 테마(`T` 키)
  - **시각적 요소 및 접근성**: Mermaid 아키텍처 다이어그램(동적 렌더링 및 SVG 다운로드 지원), 다크 모드 가시성이 보강된 패킷 비트필드 표(`.bitfield-table`), Indigo 계열 `::selection` 스타일, `prefers-reduced-motion` 모션 감도 대응
  - **뎁스 앤 블러(Depth & Frosted Blur) 슬라이드 전환**: 슬라이드 이동 시 깊이감 있는 줌스케일(`scale(0.85)`), 퇴장 잔상 보존(`visibility 0.45s`), 가우시안 블러(`filter: blur(16px)`)가 어우러져 테크 키노트 품격의 세련된 트랜지션 제공
  - **스마트 하단 컨트롤 바 마우스 호버 전용 노출**: 슬라이드 몰입도를 위해 평상시(슬라이드 넘김 포함) 화면 하단 밖으로 완벽 숨김되며, 오직 마우스 커서가 화면 맨 아래쪽(하단 90px)으로 접근하거나 포커스될 때만 부드럽게 슬라이드 업되어 노출
  - **마우스 휠 & 터치 스와이프 네비게이션**: 마우스 휠 스크롤(관성 휠 폭주 방지 400ms 쿨다운 락 및 모달/내부 스크롤 보호) 및 모바일 좌우 터치 스와이프로 직관적인 슬라이드 넘김 지원
  - **PDF 인쇄 최적화 (`Ctrl + P`)**: `@media print` 1페이지 1슬라이드 100% 핏팅으로 잘림 없는 16:9 고해상도 PDF 슬라이드 출력
  - **CLI 검증 도구 내장**: `python skills/seminar-material-generator/scripts/validate-slides.py <파일>`로 슬라이드 스키마, 발표자 노트(notes), 예상 발표 시간 자동 검증
  - **오프라인 단일 파일 번들러**: `python skills/seminar-material-generator/scripts/bundle-offline.py <파일>`로 외부망 연결 없는 완전 독립 슬라이드 덱(`slides-offline.html`) 즉시 생성
- **사용 방법**:
  - 에이전트에게 주제와 함께 요청:
    > "WebRTC, gRPC, Zenoh 주제에 대해 seminar-material-generator 스킬로 발표 슬라이드 덱 만들어줘."

---

### 📖 스킬 상세 안내: `eli5`

- **개요**: 복잡한 기술 개념, 아키텍처, 코드, 시스템 장애를 특정 대상(5세 어린이, 중고등학생, 비기술직 경영진, 전공자, 가족 등)의 눈높이에 맞춰 직관적인 현실 비유로 설명합니다.
- **출처 및 기반(Upstream)**: 오픈소스 저장소 [`DreambigOu/ELI5`](https://github.com/DreambigOu/ELI5)의 청중별 프롬프트 지침을 기반으로 도입하였으며, 본 저장소의 `study-material-generator` 디자인 시스템과 결합하여 **독립형 웹 산출물(`eli5.html`) 템플릿, 인터랙티브 청중 탭 전환, CLI 검증 도구**를 추가 구축·수정한 스킬입니다.
- **주요 기능**:
  - **이중 전달 모드(Dual Delivery Modes)**:
    - *대화형 텍스트 모드*: 채팅창 내에서 즉각적이고 명쾌한 비유와 요점 전달
    - *인터랙티브 웹 익스플레이너(`eli5.html`)*: `study-material-generator`의 UI/UX 디자인 표준 100% 상속 (마스터 디자인 토큰, Pretendard 폰트 가독성 스케일, 스마트 캔버스 카드, 라이트/다크 테마 `t` 단축키 전환)이 적용된 단일 독립형 HTML 문서 생성
  - **인터랙티브 청중 눈높이 탭 전환(Multi-Level Switcher)**: 단일 문서 내에서 상단 탭(`[👦 5세 어린이]` ➔ `[💼 경영진]` ➔ `[💻 엔지니어]`) 클릭 또는 키보드 단축키(`←/→`)로 즉각 해당 청중의 설명·비유·다이어그램으로 전환 (URL `#level-N` 딥링크 연동)
  - **사용자 경험(UX) 및 단축키/접근성**: 상단 읽기 진행률 바(`progress-bar`), 테마 토글 단축키(`t`/`T`), 부드러운 테마 전환 애니메이션, 도표 확대 모달(순백색/다크 배경, 모바일 터치 및 핀치 줌 제스처), 본문 스킵 링크
  - **4단계 황금 구조(4-Step Explanation Arc)**:
    1. *본질 한 줄 정의(The Essence)*: 전문용어를 배제한 핵심 직관 요약
    2. *현실 비유 스포트라이트 카드(The Analogy)*: 일상 사물에 빗댄 비유와 Mermaid 다이어그램(줌/다운로드 지원)
    3. *3단계 동작 원리(How It Works)*: 순차적 데이터 흐름 및 메커니즘 분해
    4. *왜 중요한가(The So What)*: 청중 맞춤형 비즈니스/실생활 가치 결론
  - **청중 맞춤형 Q&A 아코디언**: 각 청중 수준에서 가장 궁금해할 질문과 명쾌한 답변 제공
  - **CLI 검증 도구 내장**: `python skills/eli5/scripts/validate-eli5.py <파일>`로 스키마 및 청중 레벨 데이터 정합성 자동 검증
- **사용 방법**:
  - 에이전트에게 눈높이와 함께 요청:
    > "양자 컴퓨터에 대해 5세 어린이와 경영진 눈높이로 eli5 스킬을 써서 HTML 문서로 만들어줘."
    > "쿠버네티스 원리를 비전공자인 내 팀장님한테 설명하듯 쉽게 풀어서 설명해줘."

---

### 📖 스킬 상세 안내: `scroll-deck-generator`

- **개요**: `seminar-material-generator`의 기획 인터뷰와 디자인 시스템을 상속받아, 장면 분할 없이 하나의 연속된 무대 위에서 오브젝트가 변신하며 이어지는 **자급자족형 스크롤 프레젠테이션 웹 덱(`scroll-deck.html`)**, 선언형 소스(`deck.yaml`), 그리고 **MP4 고화질 비디오**를 생성합니다.
- **상속 및 확장 관계**:
  - `seminar-material-generator` 상속: 7대 기획 인터뷰 체크리스트(보안 등급, 행사명, 발표자, 시간, 청중 레벨, 결론 한 줄), 1정지점 1주장 원칙, 이모지 배제 정갈한 타이포그래피, 발표자 노트(Speaker Notes) 필수화, 다크/라이트 디자인 토큰
  - 확장 특화: 단일 HTML 자급자족형 웹 덱(`scroll-deck.html`) 즉시 실행 지원, 단일 무대 및 연속 GSAP 마스터 타임라인(`deck.yaml`), 앞 비트 요소가 다음 비트로 이어지는 Handoff & Link 모션, 6대 모션 콘셉트 팩, 마우스 휠 스크럽 조작, HyperFrames 기반 무손실 MP4 영상 내보내기
- **6대 모션 콘셉트 팩**:
  - `rail` (가로 시간 레일): 회사 연혁, 로드맵, 산업 10년사
  - `data` (데이터 저널리즘): 분기 실적, 통계/시장 분석, 인터랙티브 모핑 차트
  - `launch` (제품 런치): 신제품 발표, 핵심 기능 쇼케이스, 다크/라이트 콘트라스트
  - `zoom` (무한 줌 드릴다운): 장애 근본 원인(Root Cause) 진단, TAM-SAM-SOM, 트리 계층 구조
  - `canvas` (2.5D 공간 비행): 투자 유치 피치덱, 전략 지도, 워크플로 투어
  - `kinetic` (키네틱 타이포그래피): 컨퍼런스 키노트, 선언문, 개념 강의
- **CLI 검증 도구 내장**:
  - `python skills/scroll-deck-generator/scripts/validate-deck.py <deck.yaml>`로 헤더 메타데이터, 콘셉트 유효성, 실데이터 출처, 비트별 발표자 대본 작성률 및 예상 발표 시간 자동 검증
- **의존성 및 사전 요구사항**:
  - 검증: Python 3.7+ (내장 라이브러리 fallback 지원, 추가 설치 불필요)
  - Scrolline 로컬 구동 및 MP4 렌더링 시: Node.js 22+, HyperFrames CLI, ffmpeg
- **사용 방법**:
  - 에이전트에게 주제와 콘셉트와 함께 요청:
    > "차세대 분산 아키텍처 전환 로드맵에 대해 scroll-deck-generator 스킬을 써서 rail 콘셉트의 스크롤 발표 덱으로 만들어줘."
    > "분기 클라우드 인프라 비용 절감 분석 리포트를 data 콘셉트의 스크롤 덱으로 만들어줘."

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
