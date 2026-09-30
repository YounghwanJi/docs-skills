# Interaction Spec

Implemented already in `assets/template.html`. Documented here so edits preserve behavior.

## Ctrl+K search
- Opens a modal with a text input (`text-input-focused` style) + result list.
- Index built at page-load time (not on every keystroke) from the `#content-data` JSON: chapter titles, section headings, body paragraph text, footnote text, glossary terms, compare-table rows.
- Each hit shows: category badge (본문/용어집/참고문헌/비교표) + matched snippet with the query term highlighted.
- Keys inside modal: `↑`/`↓` move selection, `Enter` navigates to it and closes modal, `Esc` closes modal.
- While the search input has focus, global shortcuts (←/→ chapter nav, Shift+/) are suppressed.

## Shift + / (i.e. "?") — Glossary
- Opens the glossary page/modal: alphabetically sorted abbreviation list, each with full term, one-line definition, and links back to every chapter section where it's used.
- Has its own lightweight filter input (not the same index as Ctrl+K, but same data source).

## [ — Sidebar collapse / expand (Toggle)
- Toggles the left sidebar open/closed.
- On desktop (>840px): collapses `#layout` from 3 columns to 2 columns (sidebar width becomes 0), expanding the main reading area for distraction-free reading. Persists state in `localStorage` (`sidebar-collapsed`).
- On mobile/tablet (≤840px): toggles the off-canvas drawer.
- Also accessible via the header's sidebar toggle button (`#sidebar-toggle-btn`).
- Suppressed when focus is inside any text input, search modal, or glossary filter.

## t / T — Theme toggle
- Switches between light and dark themes instantly.
- Triggers smooth CSS transition, switches theme attribute, updates Mermaid diagrams, and persists choice in `localStorage` (`theme`).
- Also accessible via the header theme toggle button (`#theme-toggle`).
- Suppressed when focus is inside text inputs.

## ← / → — Chapter navigation
- Left = previous chapter, Right = next chapter, wraps are disabled (no-op at first/last chapter, not a wraparound).
- Suppressed when focus is inside any text input, the search modal, or the glossary filter.
- Visible chapter position indicator in the header (e.g. "3 / 9") updates on navigation.

## Theme toggle
- Light is default. Toggle button in header sets `data-theme="dark"` on `<html>` and persists the choice in `localStorage` (per-browser only — this is a downloaded file, not a shared hosted page, so this is fine and expected).
- Respects `prefers-color-scheme` only as the *initial* default if the user has never toggled manually in that browser.

## Sidebar / TOC (Docusaurus-style Multi-Project Accordion Hub)
- **Left sidebar**: Project & Chapter directory navigation:
  - **Multi-project Hub Mode (`DATA.projects`)**: When managing multiple projects/guides in a single index document, each project is rendered as a collapsible accordion folder (`📁 [아이콘] 프로젝트명`). Clicking a project header expands/collapses its chapter list. The project containing the active chapter is **auto-expanded** on load and chapter switch.
  - **Single-project Mode (`DATA.chapters`)**: Renders a clean numbered chapter list (`1`, `2`, `3`...).
  - **Strict Separation Principle**: Sidebar displays chapters only — it does NOT clutter the sidebar with child section headings. In-page section navigation lives exclusively in the right TOC (`#toc-box`).
- Breadcrumb (`문서 제목 › 프로젝트명 › 챕터 제목`) and a `CHAPTER n` eyebrow sit above the chapter `<h1>`, reinforcing position in the book.
- Right TOC is a boxed "이 페이지의 내용" card listing the current chapter's section headings; clicking smoothly scrolls to that anchor.
- **Bottom-of-chapter page-turner**: a two-card row (◀ 이전 / 다음 ▶) showing the previous/next chapter's title, clickable — the primary way readers move linearly through the book, with ←/→ keys as the power-user shortcut for the same action.
- Sidebar and TOC both collapse to off-canvas drawers below the `md` breakpoint (840px), matching the Mobbin responsive collapsing strategy (column-by-column, not reflow).
- Main reading column is narrowed to ~760px (book-page width) rather than a wide dashboard layout.

## Reading progress bar
Thin fixed bar at the very top of the viewport, width = scroll progress through the current chapter (resets per chapter, not per document).

## Cover page
The document opens on a cover page (title, learning goals, "이 문서 보는 법", chapter overview, a "시작하기" button) rather than dropping straight into Chapter 1. A left-sidebar "개요 / 표지" item always returns here. If the reader has a previously-read chapter saved (`localStorage`), the cover shows a "이어보기" resume banner rather than auto-redirecting — the cover is always shown first so returning readers aren't skipped past it. Includes shortcut cheat sheet cards for `[`, `t`, `Ctrl+K`, `Shift+/`, and arrow keys.

## Mobile navigation (≤840px)
- The left sidebar becomes an off-canvas drawer, opened by the sidebar toggle button in the header and closed by tapping the scrim, a nav item, Escape, or the browser back gesture.
- The right "이 페이지의 내용" TOC is hidden at this width; its content is duplicated into a `<details>` accordion inserted at the top of the chapter body instead, so in-page navigation is never lost on mobile — only relocated.

## Footnotes as popovers
Clicking a footnote marker (`sup.fn`) opens a small floating popover positioned near the marker (not an inline block pushed into the reading flow). It closes on: clicking outside, Escape, or scrolling.

## URL deep-linking
Navigating to a chapter updates the URL to `#ch-{idx}` via `history.replaceState` (no new history entries, so back/forward isn't spammed). Loading the page with a `#ch-N` hash already in the URL jumps straight to that chapter, bypassing the cover — this is what makes a chapter shareable/bookmarkable and survives a refresh.

## Resume position
`localStorage` records the last-viewed chapter index per browser. This does not auto-navigate on load (the cover always shows first); it only powers the resume banner on the cover page.

## Print
A `@media print` stylesheet hides the header, sidebar, TOC, footer, progress bar, chapter-nav cards, modals, and hamburger button, leaving only the current chapter's body content in normal print flow. Note the practical limit: since chapters are rendered one at a time into the DOM (not all at once), printing only captures whichever chapter is currently open — mention this to the reader if they ask for a full-document PDF (they should print each chapter, or you should offer a separate "print all" build if that's explicitly requested).

## Sidebar and TOC Coordination
- **Left sidebar**: Book/Project-level directory navigation (Project folder accordions in multi-project mode, and chapter items). It never duplicates section headings.
- **Right TOC (`#toc-box`)**: Exclusively handles the active chapter's detailed in-page headings (including h3 nesting) with real-time `IntersectionObserver` Scrollspy position tracking.

## TOC scroll-position tracking (scrollspy)
An `IntersectionObserver` watches every heading in the current chapter and marks the matching TOC link `.active` as it enters the reading viewport (trigger band: roughly top-90px to 70%-of-viewport). This means the TOC always shows where the reader currently is, not just a static list.

## Header identity (fixed, not per-page)
`#header-doc-title` is set once from `DATA.title` at load and never changes as the reader navigates — it's the page's stable identity anchor (same idea as a site name in a top bar), not a "current page" label. Per-page position is already covered by `#chapter-pos` ("3 / 9", which does update) and the in-page breadcrumb, so don't wire chapter/cover navigation to rewrite the header title again — that was tried and reverted because it made the header flicker on every navigation and duplicated what the breadcrumb already says. Document title/version/dates otherwise live only in the footer colophon (see design-tokens.md) and the cover page.

## Footer
Kept intentionally light: a small byline (`문서 제목 · 버전`) plus the 참고문헌/용어집 links, not a second large title repeat. Still uses the inverted-color band from the design system, just without competing with the header/sidebar for "the" title placement.

## Theme toggle icon
The button shows a moon icon in light mode (click → switches to dark) and a sun icon in dark mode (click → switches to light) — both are inline SVGs toggled purely by CSS off `[data-theme]`, no icon-swapping JS needed.

## Compare-table cell wrapping
Compare-table cells wrap normally instead of truncating with `…`. Each cell measures its own wrapped text height first (via a hidden probe element) so row height is set to fit the tallest cell in that row, then the cell is drawn as an SVG `foreignObject` containing a normal wrapping HTML `<div>` — this is what makes real line-wrapping possible inside an SVG (plain SVG `<text>` cannot wrap on its own).

## Mermaid diagram zoom
Every rendered Mermaid diagram gets a "🔍 확대 보기" button beneath it. Clicking opens a full-screen lightbox with: mouse-wheel zoom (zooms toward the pointer's general area, clamped 40%–600%), click-and-drag panning, +/− buttons, a reset button, and the usual Esc/backdrop-click/✕ close. The lightbox operates on a clone of the already-rendered SVG, so it works offline with no extra network calls.

## Code block copy button
Every code block header includes a "복사" button. Clicking copies raw code to the clipboard via `navigator.clipboard.writeText`, changes label to "✓ 복사됨", and reverts back to "복사" after 1.5 seconds.

## Diagram zoom & touch gestures
The full-screen diagram lightbox supports:
- Mouse wheel zooming (clamped 40%–600%) and mouse drag panning.
- Mobile/tablet touch: 1-finger drag panning and 2-finger pinch-to-zoom.
- Toolbar buttons (+, −, 초기화, 닫기) and `Esc` key / backdrop click to exit.

## Smooth theme transition
When toggling theme, `html.theme-transitioning` is temporarily applied for 350ms to ensure a smooth, flicker-free color and background transition.

## Accessibility
- A "본문으로 건너뛰기" skip link is the first focusable element on the page.
- All interactive elements get a visible `:focus-visible` outline.
- Compare-table and chart SVGs carry `role="img"`, an `aria-label`, and a `<title>` element for assistive tech.
- `@media (prefers-reduced-motion: reduce)` disables non-essential animations and transitions for motion-sensitive users.
