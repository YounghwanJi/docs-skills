# Design Tokens

Derived from the Mobbin design system, adapted for a technical study document (monochrome base + limited semantic exceptions for diagrams/tables). These are already implemented as CSS variables in `assets/template.html` — this file documents *why*, so edits stay consistent.

## Color

```css
:root {
  --primary: #141414; --accent: #0066ff;
  --canvas: #ffffff; --canvas-soft: #f3f3f3; --field: #f0f0f0;
  --hairline-soft: #f0f0f0; --hairline: #e0e0e0;
  --ink: #141414; --ink-soft: #262626; --muted: #707070; --faint: #adadad;
  --on-primary: #ffffff;
  --code-bg: #f0f0f0;
}
:root[data-theme="dark"] {
  --primary: #ffffff; --accent: #0066ff;
  --canvas: #0a0a0a; --canvas-soft: #1a1a1a; --field: #1e1e1e; --raised: #2e2e2e;
  --hairline-soft: #262626; --hairline: #333333;
  --ink: #ffffff; --ink-soft: #e2e2e2; --muted: #adadad; --faint: #707070;
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
- `--faint` (#adadad / #707070) is sub-AA for body text by design (it's for placeholders/fine print). Never use it for footnote numbers, glossary labels, or anything the reader must read.
- `--accent` (#0066ff) is a fill/badge color, never a text color on `--canvas` (fails AA as text).

## Typography

Font: **Pretendard Variable** (OFL, free, Korean + Latin). Fallback: `"Pretendard Variable", Pretendard, -apple-system, "Noto Sans KR", "Malgun Gothic", sans-serif`.
Monospace (code/RFC excerpts): `"JetBrains Mono", "D2Coding", "Courier New", monospace`.

Weight mapping from the original Saans spec (652/456/300) → Pretendard Variable axis:

| Token | Size | Weight | Line height | Use |
|---|---|---|---|---|
| display | 48px | 650 | 1.1 | Document title only |
| h1 | 32px | 650 | 1.15 | Chapter title |
| h2 | 24px | 650 | 1.2 | Section heading |
| h3 | 20px | 600 | 1.25 | Sub-section heading |
| body-lg | 18px | 300 | 1.5 | Motivation box lead line |
| body | 16px | 450 | 1.6 | Default body text |
| body-sm | 14px | 450 | 1.5 | Table cells, captions, footnotes |
| label | 12px | 600 | 1.3 | Badges, eyebrow labels |
| mono | 14px | 450 | 1.6 | Code / RFC excerpt blocks |

Line length target: ≤80 characters for body text (per frontend-design skill guidance).

## Reading column width & centering
`main` is a grid item in the 3-column layout (`280px sidebar | 1fr content | 220px TOC`). It must always have `margin: 0 auto` alongside its `max-width` (currently 860px) — without the auto margin it sticks to the left edge of the flexible middle track and leaves a large dead gap before the TOC on wide screens, which reads as "misaligned," not as a deliberate reading column. Paragraph line-length is capped independently via `p{max-width:76ch}`, so widening `main` (e.g. to fit the 900px compare-table / 640px chart width better) does not hurt prose readability — it only gives tables/charts/code more breathing room.

## Footer: thin full-width bar (colophon), mirrors the header
The footer is a **thin, full-width bar** — no rounding, no color inversion — deliberately mirroring the header's full-width sticky bar so the page reads as one consistent frame (thin bar on top, thin bar on bottom) rather than a narrow floating card. Background is the quiet `--canvas-soft` with a 1px top hairline, not `var(--ink)` inversion — a full-bleed element with rounding (or a jarring color flip) reads as a design mistake, not a choice; removing both fixes it in one move. It carries the document's colophon info (title · version · created/reviewed dates) plus the 참고문헌/용어집 links — this is the *only* place that identity block appears now (see sidebar note below).

## Sidebar carries no document title
The sidebar shows only the "개요/표지" link + chapter tree — no book title/version block. That identity information already appears in three other places (the breadcrumb on every chapter page, the cover page's `<h1>`, and now the footer colophon), so a fourth copy in the sidebar was redundant. This also means the mobile off-canvas drawer shows only chapter navigation, nothing else — don't re-add a title block there.

## Spacing & Shape
8px base unit: 4/8/12/16/24/32/48/80px. Border radius: 16px (cards, code blocks), 24px (major containers), full pill (buttons, badges, nav). No drop shadows — elevation via `--canvas-soft` fill + 1px `--hairline` only (an exception is made for the floating search modal backdrop, which uses a semi-transparent scrim since it must visually separate from full page content).

## Components mapped from Mobbin → study doc

| Mobbin component | Study-doc use |
|---|---|
| `compare-table` (highlighted column + inset ring) | Technology comparison table — highlight the chapter's chosen technology's column |
| `nav-pill` | Top header bar |
| `faq-row` | Q&A accordion at end of each chapter |
| `badge-overlay` | Footnote number badges |
| `text-input` + focus ring | Ctrl+K search input |
| `footer` (ink band) | Page footer with references/glossary links |
