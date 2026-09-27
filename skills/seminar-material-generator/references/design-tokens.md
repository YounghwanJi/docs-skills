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
