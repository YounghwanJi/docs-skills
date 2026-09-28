---
name: study-material-generator
description: Generate a single self-contained HTML study document for a technical topic (protocols, standards, algorithms, architectures) that a junior researcher (학사) can study from and then present to senior researchers (석·박사). Use whenever the user asks to build study material, a study guide, technical reference doc, or "스터디 자료" as an HTML deliverable — especially when they want RFC/standard/paper-grounded quantitative content, Mermaid diagrams, D3.js publication-quality tables/charts, a Ctrl+K search, a glossary, light/dark themes, or keyboard chapter navigation. Always consult this skill instead of freehanding a generic HTML report when these signals appear, even if the user just says "make me a study doc about X."
---

# Study Material Generator

Produces one self-contained `study.html` file: a technical study document grounded in standards/RFCs/papers, structured so a junior researcher can read it, understand it deeply, and defend it in front of senior researchers.

Read `references/design-tokens.md`, `references/content-structure.md`, and `references/interactions.md` before writing content or code — they contain the CSS variables, the mandatory chapter structure, and the exact behavior spec for search/shortcuts. Do not improvise these; they encode decisions already agreed with the user.

## Workflow

1. **Scope the topic with the user** if not already clear: subject, target chapter list, depth (overview vs. deep-dive), and any specific standards/papers they want anchored. Do not invent a chapter outline silently for a broad topic — confirm it first, briefly.
2. **Research before writing.** For every technical claim or number: search for the primary source (RFC, ISO/IEEE/W3C standard, peer-reviewed paper, official spec). Never fabricate a figure or citation. If a precise number can't be sourced, state the qualitative fact instead of inventing a number.
3. **For every "core technology" introduced in a chapter**, research 2–4 alternative/competing technologies that solve the same problem, and build a comparison table per `references/content-structure.md` §5. This is mandatory, not optional — it's the feature that lets the reader defend their choice of technology in front of senior researchers.
4. **Choose Generation Strategy (Single vs. Chunked)**:
   - **Single-shot (Compact topics, 1–2 chapters)**: Populate the entire `#content-data` JSON in a single step.
   - **Chunked / Progressive Generation (Deep or multi-chapter topics, 3+ chapters)**: To prevent output token truncation and JSON corruption:
     - **Phase 1 (Scaffold)**: Copy `assets/template.html` to output path. Populate metadata (`title`, `learningGoals`), the full chapter outline with skeleton chapters (titles + motivations + empty sections), and known initial `references`.
     - **Phase 2 (Chapter by chapter)**: Generate and inject chapter content 1 or 2 at a time using file editing tools (`replace_file_content`).
     - **Phase 3 (Post-linking)**: Populate complete `glossary` entries and verify all `references` IDs match footnote citations.
5. **Build content as structured JSON**, following the schema in `assets/template.html`'s embedded `#content-data` block (chapters → sections → footnotes/references/glossary/compare-tables). Do not restructure the CSS/JS scaffolding unless the user asks for a layout change.
   - *Formatting rule*: Use standard HTML tags (`<strong>`, `<code>`) for emphasis. While the template auto-converts markdown (`**bold**` → `<strong>`, `` `code` `` → `<code>`) via `parseInlineMarkdown`, explicit HTML is preferred.
6. **Verify before delivering**:
   - **Automated validation**: Run `python skills/study-material-generator/scripts/validate-study.py <output_file.html>` to verify JSON syntax, required schema, chapter structure, and footnote/reference cross-references.
   - **Checklist**: Every number has a footnote, every abbreviation has a glossary entry, every Mermaid diagram has an alt-text summary line, every compare-table has a one-line verdict, chapter count in sidebar matches JSON, search works for a sample query.
7. **Save and present the file**: Save the generated HTML file to the user's requested output path, or default to the workspace root as `study.html` (or `<topic>-study.html`). Present the resulting file path to the user as a clickable markdown link. This is a downloadable, self-contained technical document intended to be opened directly in any modern web browser.
8. **Optional Offline / Air-gapped Bundle (폐쇄망/보안망 지원)**:
   - If the user requests an offline, air-gapped, or security-network version (e.g., "폐쇄망용으로 만들어줘", "오프라인 파일도 제공해줘"), run:
     ```bash
     python skills/study-material-generator/scripts/bundle-offline.py <output_file.html> -o <output_file>-offline.html
     ```
   - This inlines Mermaid and D3.js libraries directly into the HTML so that all diagrams, charts, and interactive features function with zero internet connectivity. Present both links to the user.



## Audience framing is for calibration only, never for the output text
This skill's description of the intended reader/listener (a less experienced person studying to later explain the material clearly to others) exists only to calibrate depth, rigor, and what needs spelling out versus what can be assumed. **Never literally write rank/hierarchy/degree terms into the generated document itself** — not in the cover page, motivation boxes, body text, summaries, or Q&A. This includes Korean terms (학사, 석사, 박사, 임원, 상사) and their English equivalents (entry-level, junior, senior, PhD, executive, manager, etc.). Phrase everything in terms of the concepts and reasoning themselves — e.g. "핵심 트레이드오프를 근거를 들어 잘 설명할 수 있다," never "~을 석·박사 앞에서 방어할 수 있다" or any phrasing that names who the reader is presenting to.

## Non-negotiable content rules

- **Self-Containment Principle (자기완결성 원칙)**:
  - The reader must NEVER need to leave the document to google a technical term, protocol mechanism, or formula mentioned in the text. Every concept must be self-explanatory within the document itself.
  - Every technical keyword, protocol name, or mathematical model must be articulated to a depth where the reader can confidently discuss and defend it in academic conferences, IETF/W3C working groups, or high-stakes system architecture reviews.
  - Provide concrete packet bitfields, binary encoding steps, sequence diagrams, and mathematical models rather than hand-waving abstractions.
- **No business data.** No pricing, market share, company revenue, or vendor comparisons on commercial terms. Only technical substance: architecture, protocols, algorithms, performance/benchmark numbers, standard conformance.
- **Every quantitative claim is sourced.** Attach a footnote `[n]` linking to the References page entry (RFC number + link to rfc-editor.org, DOI, arXiv ID, or official standard document + publication/revision date). Mark each reference as normative or informative.
- **Every abbreviation** gets a `<abbr>` tooltip on first use per chapter and one entry in the glossary page (opened via Shift+/).
- **Every technology comparison table** must include a one-line verdict sentence explaining why this document's chosen technology is being taught/used, per `references/content-structure.md` §5.
- **Every Mermaid diagram** needs a one-line plain-text alt-text summary directly below it (for accessibility and search-indexing), not just a caption.
- **Diagram Step-by-Step Walkthrough Principle (다이어그램 단계별 상세 해설 원칙)**:
  - Never insert a diagram (sequence, flow, or architecture) as a standalone visual. 
  - The accompanying body text MUST provide a numbered, step-by-step walkthrough explaining every node interaction, arrow sequence, state transition, and payload exchange shown in the diagram so the reader can trace the entire flow in detail.

- **Production & Cloud Infrastructure Principle (인프라 및 클라우드 아키텍처 필수 원칙)**:
  - For topics involving servers, networking, streaming, distributed middleware, or IPC, authoring must not stop at application-level APIs. It must include **production-grade infrastructure architecture (on-premise & cloud-native)**:
  - **Load balancing & stream routing**: L4 vs L7 load balancing tradeoffs, connection-multiplexing affinity, and connection draining/lifecycle management.
  - **Network boundary & traversal**: Firewall traversal, NAT handling, dynamic port allocations, and fallback strategies for restricted corporate networks.
  - **Cloud-native deployment topology**: Container networking modes (host networking vs overlay CNI overhead), latency-accelerated edge routing, hybrid WAN interconnects, and egress bandwidth cost optimization.

- **가독성 타이포그래피 및 소스 코드 줄바꿈 원칙 (Typography & Code Readability Principle)**:
  - 본문 텍스트는 편안한 가독성을 위해 $18\sim 19\text{px}$, 줄간격 $1.75\sim 1.85$, 단락 간격 $24\sim 28\text{px}$, 가독 칼럼 너비 $72\sim 80\text{ch}$를 준수합니다.
  - 한글 어절 끊김 방지를 위해 `word-break: keep-all; overflow-wrap: break-word;`를 적용합니다.
  - 소스 코드 및 페이로드 블록(`pre`, `code`)은 가로 스크롤로 인한 내용 잘림을 방지하기 위해 자동 줄바꿈(`white-space: pre-wrap; word-break: break-all;`)을 적용하여 좁은 화면에서도 전문을 한눈에 열람할 수 있도록 합니다.

- **고대비 테이블 및 다이어그램 확대 캔버스 원칙 (High-Contrast Tables & Light Canvas Modal Principle)**:
  - 모든 표(비트필드, 비교 매트릭스)는 다크/라이트 테마 모두에서 경계선(`border`)이 또렷하게 드러나도록 고대비 테두리 스타일을 유지합니다.
  - 다이어그램은 컨테이너 내에서 오버플로우 없이 최적 크기로 자동 핏팅(`getBBox()` viewBox 보정)되어야 하며, 확대 버튼 클릭 시 다크 모드 상태여도 가독성을 극대화하기 위해 **순백색(#ffffff)의 깨끗한 고대비 라이트 캔버스 모달**로 렌더링되어야 합니다.



- If the user names a very broad subject ("스터디 자료 만들어줘: 네트워킹") without a chapter scope, ask for the intended chapter breakdown or a target audience level before generating — a directionless generation wastes their review time.
- If a claim can't be sourced after a reasonable search, say so in the content rather than guessing a number ("정확한 수치는 공개 자료에서 확인되지 않음 — 정성적 설명으로 대체").
