# Design Tokens for Seminar Slides

`seminar-material-generator`는 `study-material-generator`의 디자인 시스템을 100% 계승하여 시각적 통일성을 유지합니다.

---

## 1. 16:9 슬라이드 가상 캔버스 규격
- **기준 해상도**: `1920px` $\times$ `1080px` (Full HD 16:9 와이드스크린 표준)
- **반응형 뷰포트 스케일러**:
  - 부모 뷰포트 창 크기(`window.innerWidth`, `window.innerHeight`)에 맞춰 비율 왜곡 없이 화면 중앙에 자동 스케일링:
  ```javascript
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  slideCanvas.style.transform = `scale(${scale})`;
  ```

---

## 2. 컬러 팔레트 & 시맨틱 토큰 (CSS Variables)

```css
:root {
  /* Brand Accents (study-material-generator 계승) */
  --accent-primary: #6366f1;      /* Indigo 500 */
  --accent-hover: #4f46e5;        /* Indigo 600 */
  --accent-subtle: rgba(99, 102, 241, 0.12);
  --accent-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);

  /* Light Theme */
  --bg-presentation: #0f172a;     /* 프레젠테이션 기본 배경: 슬레이트 다크 */
  --bg-slide: #ffffff;
  --bg-surface: #f8fafc;
  --bg-surface-elevated: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --border-subtle: #e2e8f0;
  --border-strong: #cbd5e1;
  --shadow-slide: 0 25px 50px -12px rgba(0, 0, 0, 0.35);

  /* Status Tokens */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-info: #0ea5e9;

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace;
}

/* Dark Presentation Theme (기본 권장: 학회 빔프로젝터/대형 디스플레이 최적화) */
[data-theme="dark"] {
  --bg-presentation: #020617;
  --bg-slide: #0b0f19;
  --bg-surface: #111827;
  --bg-surface-elevated: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --border-subtle: #1e293b;
  --border-strong: #334155;
  --shadow-slide: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
}
```

---

## 3. 타이포그래피 스케일 (1920x1080 기준)
- **Cover Slide Main Title**: `56px~64px` (Weight 800, Letter-spacing `-0.03em`)
- **Slide Heading**: `36px~42px` (Weight 700)
- **Slide Subheading / Section Category**: `18px~20px` (Weight 600, All Caps, Accent color)
- **Body Text**: `22px~26px` (Line-height `1.5`, Letter-spacing `-0.01em`)
- **Bullet Text**: `20px~24px`
- **Code / Monospace**: `18px~20px` (JetBrains Mono)
- **Footnotes & Citations**: `14px~16px` (Text-muted)

---

## 4. Docs/Handout 모드 타이포그래피 & 여백
- **본문 (`.docs-prose`)**: `19px` (Line-height `1.8`, `word-break: keep-all; overflow-wrap: break-word;`)
- **단락 여백**: `margin-bottom: 18px; max-width: 78ch;`
- **리스트 아이템**: `18px` (Line-height `1.65`, Gap `12px`)

---

## 5. 텍스트 선택 & 모션 접근성
- **Text Selection**:
  ```css
  ::selection {
    background: rgba(99, 102, 241, 0.25);
    color: var(--text-primary);
  }
  ```
- **Motion Accessibility (`prefers-reduced-motion: reduce`)**:
  - `transform` 및 모든 인터랙션 확장 전환을 비활성화하되, 발표 슬라이드 전환의 급격한 깜빡임을 방지하기 위해 `.slide`의 `opacity` 전환(`0.15s ease`)은 부드럽게 유지.

---

## 6. 테이블 경계선 대비 규격 (Table Contrast)
- 다크 모드 `bitfield-table`:
  - `th`: `border-bottom: 2px solid #4a4a4a; border-right: 1px solid #444;`
  - `td`: `border-right: 1px solid #3a3a3a; border-bottom: 1px solid #3a3a3a;`
  - 하이라이트 셀: `background: var(--accent-subtle); color: var(--accent-primary); font-weight: 800;`

---

## 7. 슬라이드 전환 애니메이션 & 제어 인터랙션 (Transitions & Navigation)
- **뎁스 앤 블러 슬라이드 전환 애니메이션 (Depth & Frosted Blur Transition)**:
  - **전환 메커니즘**: 슬라이드 이동 시 현재 슬라이드는 깊이감 있게 뒤로 축소(`scale(0.85)`)되며 은은한 가우시안 블러(`filter: blur(16px)`)와 함께 페이드아웃되고, 대상 슬라이드는 전면으로 자연스럽게 확대(`scale(1)`)되며 선명하게 포커싱(`filter: blur(0px)`).
  - **퇴장 잔상 보존**: `visibility 0.45s` 트랜지션을 명시하여 퇴장 슬라이드의 블러/스케일 아웃이 씹히지 않고 부드럽게 퇴장.
  - **타이밍 및 이징**: `transition: opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1), transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), filter 0.45s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.45s cubic-bezier(0.16, 1, 0.3, 1);`
  - **방향성 패럴랙스 (Directional Parallax)**:
    - 다음 슬라이드(`.slide.next`): `transform: scale(0.85) translate3d(60px, 0, 0); filter: blur(16px);`
    - 이전 슬라이드(`.slide.prev`): `transform: scale(0.85) translate3d(-60px, 0, 0); filter: blur(16px);`
    - 활성 슬라이드(`.slide.active`): `transform: scale(1) translate3d(0, 0, 0); filter: blur(0);`
  - **모션 접근성 (`prefers-reduced-motion: reduce`)**: `filter: none !important; transform: none !important; transition: opacity 0.15s ease !important;`
- **스마트 하단 가이드 바 마우스 호버 전용 인터랙션 (Hover-Only Bottom Control Bar)**:
  - **기본 상태 (Hidden)**: 슬라이드 몰입도를 위해 평상시 화면 하단 밖으로 완벽 숨김(`transform: translateX(-50%) translateY(calc(100% + 36px)); opacity: 0; pointer-events: none;`). 슬라이드 넘김 시에도 노출되지 않음.
  - **하단 진입 감지 (Bottom Hover Reveal)**: 마우스 커서가 화면 맨 아래쪽(하단 $90\text{px}$ 이내)으로 직접 내려가거나 컨트롤 바 위에 호버/포커스될 때만 부드럽게 위로 슬라이드 업(`transform: translateX(-50%) translateY(0); opacity: 1; pointer-events: auto;`).
  - **이탈 시 자동 숨김**: 마우스가 하단 영역을 벗어나면 즉시 다시 아래로 부드럽게 퇴장(`0.35s cubic-bezier(0.16, 1, 0.3, 1)`).
- **마우스 휠 스크롤 네비게이션 (Wheel Navigation)**:
  - 휠 아래로 스크롤: `nextSlide()`
  - 휠 위로 스크롤: `prevSlide()`
  - **폭주 방지 쿨다운 락 (Wheel Throttle Lock)**: 트랙패드 및 관성 휠 연속 발화를 방지하기 위해 $400\text{ms}$ 쿨다운 및 역치($|\Delta y| \ge 15$) 적용
  - **스마트 스크롤 보호**: Docs 모드, 슬라이드 개요 모달, 도움말 모달 활성화 시 슬라이드 전환을 유예하고 기본 스크롤 동작 보장
- **모바일 터치 스와이프 (Touch Navigation)**:
  - 가로 스와이프($|\Delta x| > 50\text{px}$) 감지하여 모바일/태블릿에서도 직관적인 슬라이드 전환 지원
