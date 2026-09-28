# Design Tokens

> **마스터 소스 (Single Source of Truth)**: 이 파일이 `study-material-generator`, `eli5`의 디자인 시스템 기준입니다.  
> `eli5/references/design-tokens.md`는 이 파일과 100% 일치해야 합니다.

Derived from the Mobbin design system, adapted for a technical study document (monochrome base + limited semantic exceptions for diagrams/tables). These are already implemented as CSS variables in `assets/template.html` — this file documents *why*, so edits stay consistent.

## Color

```css
:root {
  --primary: #141414; --accent: #0066ff;
  --canvas: #ffffff; --canvas-soft: #f3f3f3; --field: #f0f0f0;
  --hairline-soft: #e4e4e4; --hairline: #d0d0d0;  /* ↑ 대비 강화: #f0f0f0→#e4e4e4, #e0e0e0→#d0d0d0 */
  --ink: #141414; --ink-soft: #262626; --muted: #5a5a5a; --faint: #adadad; /* --muted 대비 4.95:1 확보 */
  --on-primary: #ffffff;
  --code-bg: #f0f0f0;
}
:root[data-theme="dark"] {
  --primary: #ffffff; --accent: #0066ff;
  --canvas: #0a0a0a; --canvas-soft: #1a1a1a; --field: #1e1e1e; --raised: #2e2e2e;
  --hairline-soft: #303030; --hairline: #404040;  /* ↑ 대비 강화: #262626→#303030, #333→#404040 */
  --ink: #ffffff; --ink-soft: #e2e2e2; --muted: #9a9a9a; --faint: #707070; /* --muted 밝기 조정 */
  --on-primary: #141414;
  --code-bg: #1e1e1e;
}
```

### Semantic exception (diagrams & compare-tables only)
Allowed **only** inside Mermaid diagram state nodes and compare-table support cells — never in body text, headings, or general UI chrome. Always pair color with an icon (colorblind safety):

| Meaning | Light | Dark | Icon |
|---|---|---|---|
| 지원/권장 | `#009E73` | `#3DDC97` | ✓ |
| 부분지원/주의 | `#E69F00` | `#F5B942` | ▲ |
| 미지원 | `#D55E00` | `#E8734A` | ✕ |

Do not add more semantic colors without re-checking contrast + colorblind safety (Okabe-Ito palette family).

### Contrast notes
- `--muted` (#5a5a5a / #9a9a9a): 본문 보조 텍스트(캡션, 메타)에 사용. 라이트 4.95:1, 다크 모드 대비 AA 확보.
- `--faint` (#adadad / #707070) is sub-AA for body text by design (it's for placeholders/fine print). Never use it for footnote numbers, glossary labels, or anything the reader must read.
- `--accent` (#0066ff) is a fill/badge color, never a text color on `--canvas` (fails AA as text).
- `--hairline` (#d0d0d0 / #404040): 테이블 경계선 및 구분선에 사용. 이전 값 대비 가시성 향상.

## Typography

Font: **Pretendard Variable** (OFL, free, Korean + Latin). Fallback: `"Pretendard Variable", Pretendard, -apple-system, "Noto Sans KR", "Malgun Gothic", sans-serif`.
Monospace (code/RFC excerpts): `"JetBrains Mono", "D2Coding", "Courier New", monospace`.

Weight mapping from the original Saans spec (652/456/300) → Pretendard Variable axis:

| Token | Size | Weight | Line height | Letter-spacing | Use |
|---|---|---|---|---|---|
| display | 48px | 700 | 1.1 | -0.02em | Document title only |
| h1 | 34px | 700 | 1.2 | -0.015em | Chapter title (**34px**: 32→34, 존재감 강화) |
| h2 | 25px | 650 | 1.25 | -0.01em | Section heading (**25px**: 24→25 미세 조정) |
| h3 | 20px | 600 | 1.3 | 0 | Sub-section heading |
| body-lg | 18px | 450 | 1.65 | 0 | Motivation box lead line (**wt 300→450**: 리드문 명확화) |
| body | 16.5px | 420 | 1.75 | -0.01em | Default body text (**한글 황금 비율**: 16→16.5, lh 1.6→1.75) |
| body-sm | 13.5px | 450 | 1.55 | 0 | Table cells, captions, footnotes (**13.5**: 본문과 구분 강화) |
| label | 11.5px | 650 | 1.3 | 0.03em | Badges, eyebrow labels (**작고 단단하게**) |
| mono | 14px | 450 | 1.75 | 0 | Code / RFC excerpt blocks (**lh 1.6→1.75**: 코드 가독성 ↑) |

Line length target: ≤76 characters (`p { max-width: 76ch }`) for body text (한글 기준 최적 행 길이).

### 타이포그래피 설계 근거
- **body 16.5px/lh 1.75**: 한글 자소의 복잡도(복합 자모 구조)로 인해 영문 대비 줄간격 +0.1~0.15 필요. 네이버 블로그, 브런치 등 한글 장문 UX 연구 기반.
- **body-weight 420**: 한글은 디스플레이 렌더링 시 영문 대비 획이 두껍게 보이므로 450→420으로 낮춰 장문 피로감 경감.
- **소수점 폰트 사이즈 금지**: `15.5px` 같은 값은 서브픽셀 렌더링 아티팩트 유발. 정수 또는 `.5px` 단위만 허용.

## Reading column width & centering
`main` is a grid item in the 3-column layout (`280px sidebar | 1fr content | 220px TOC`). It must always have `margin: 0 auto` alongside its `max-width` (currently 860px) — without the auto margin it sticks to the left edge of the flexible middle track and leaves a large dead gap before the TOC on wide screens, which reads as "misaligned," not as a deliberate reading column. Paragraph line-length is capped independently via `p{max-width:76ch}`, so widening `main` (e.g. to fit the 900px compare-table / 640px chart width better) does not hurt prose readability — it only gives tables/charts/code more breathing room.

## Footer: thin full-width bar (colophon), mirrors the header
The footer is a **thin, full-width bar** — no rounding, no color inversion — deliberately mirroring the header's full-width sticky bar so the page reads as one consistent frame (thin bar on top, thin bar on bottom) rather than a narrow floating card. Background is the quiet `--canvas-soft` with a 1px top hairline, not `var(--ink)` inversion — a full-bleed element with rounding (or a jarring color flip) reads as a design mistake, not a choice; removing both fixes it in one move. It carries the document's colophon info (title · version · created/reviewed dates) plus the 참고문헌/용어집 links — this is the *only* place that identity block appears now (see sidebar note below).

## Sidebar carries no document title
The sidebar shows only the "개요/표지" link + chapter tree — no book title/version block. That identity information already appears in three other places (the breadcrumb on every chapter page, the cover page's `<h1>`, and now the footer colophon), so a fourth copy in the sidebar was redundant. This also means the mobile off-canvas drawer shows only chapter navigation, nothing else — don't re-add a title block there.

## Spacing & Shape
8px base unit: 4/8/12/16/24/32/48/80px. Border radius: 16px (cards, code blocks), 24px (major containers), full pill (buttons, badges, nav). No drop shadows — elevation via `--canvas-soft` fill + 1px `--hairline` only (an exception is made for the floating search modal backdrop, which uses a semi-transparent scrim since it must visually separate from full page content).

### 컴포넌트별 여백 기준 (개선 후)

| 컴포넌트 | padding | margin |
|---|---|---|
| `main` | `28px 52px 56px` | (grid layout) |
| `.canvas-card-body` | `24px` | — |
| `.canvas-card-header`, `.canvas-card-footer` | `12px 18px` | — |
| `.motivation`, `.summary-box` | `22px 28px` | `0 0 24px` |
| `.callout` | `16px 20px` | `20px 0` |
| `.canvas-card` | — | `28px 0` |
| `.code-block` | — | `24px 0` |
| `p` | — | `0 0 18px` |

## Components mapped from Mobbin → study doc

| Mobbin component | Study-doc use |
|---|---|
| `compare-table` (highlighted column + inset ring) | Technology comparison table — highlight the chapter's chosen technology's column |
| `nav-pill` | Top header bar |
| `faq-row` | Q&A accordion at end of each chapter |
| `badge-overlay` | Footnote number badges |
| `text-input` + focus ring | Ctrl+K search input |
| `footer` (ink band) | Page footer with references/glossary links |
