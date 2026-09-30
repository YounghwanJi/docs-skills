# Content Structure Rules

## 1. Document metadata (header/footer)
- Title, version, 작성일, 최종 검토일, 참고 표준 버전 목록 — shown in header/footer per `assets/template.html`.

## 1.5 Multi-Project & Chapter Structure (Docusaurus-style Accordion Hub)
- Do NOT prefix `chapter.title` with a manual number ("1. ...", "2장 ..."). The template auto-numbers chapters from their array position in the sidebar, breadcrumb, and `CHAPTER n` eyebrow.
- **Multi-Project Hub Mode (`projects: [...]`)**:
  - 추후 여러 개의 프로젝트/기술 스터디 문서를 하나의 `study.html` 인덱스에서 통합 관리하고자 할 때 사용합니다.
  - 최상위에 `projects` 배열을 두고 각 프로젝트 객체(`id`, `title`, `icon`, `chapters: [...]`)로 구성합니다.
  - 사이드바에서는 **Docusaurus 스타일의 폴더형 아코디언 (`📁 [아이콘] 프로젝트명`)**으로 렌더링되어, 클릭 시 해당 프로젝트의 챕터 목록이 펼쳐집니다.
- **Single-Project Mode (`chapters: [...]`)**:
  - 단일 기술 주제나 표준을 다루는 기본 모드로, 최상위에 `chapters` 배열을 직접 정의합니다. 사이드바에 번호가 매겨진 챕터 목록이 깔끔하게 렌더링됩니다.
- **Strict In-Page TOC Separation Principle**:
  - 챕터 내부의 소제목(`sections`)은 사이드바에 중첩시키지 않고, **우측 TOC(`#toc-box`)**에서만 전담하여 인페이지 스크롤 앵커로 처리합니다. 이를 통해 사이드바는 프로젝트-챕터 단위의 정갈한 디렉터리 트리 형태를 유지합니다.

## 2. Chapter shape (mandatory, in order)
1. **Motivation box** — "왜 중요한가": 2–4 sentences, why a researcher should care, before any technical detail.
2. **Body**, point escalating: 기초 개념 → 표준/RFC 레벨 상세 → 구현/실무 이슈.
   - **Self-Contained Exposition**: When introducing any technical keyword (e.g. codecs like Opus/AV1, NAT types like Symmetric/Cone, protocol concepts like HPACK/Varint/ZInt), explain its full definition (What), inner mechanics (How), and engineering rationale (Why) so the reader never needs external search.
   - Use Mermaid diagrams for flows/architectures (see §4) and D3 tables/charts for data (see §3).
3. **Technology comparison table** — see §5. Mandatory whenever the chapter introduces a "core technology" (a named protocol, algorithm, architecture pattern, or standard).
4. **핵심 요약** — 3–5 bullet lines, no new information, pure recap.
5. **예상 Q&A** — at least 3 question/answer pairs addressing real-world edge cases, troubleshooting, and architectural defense.

## 3. Quantitative data & citations
- Every number/statistic gets a footnote marker `[n]` linking to an entry on the References page.
- Reference entry format: `[n] Title — Standard/Journal/Org, RFC number or DOI or arXiv ID, Year-Month. [normative|informative]. <link>`
- Only use primary sources: RFC editor (rfc-editor.org), ISO/IEEE/W3C/IETF official pages, peer-reviewed venues, arXiv preprints (label as preprint), or the official spec/vendor documentation for implementation details (not marketing pages).
- If no reliable number exists, write the qualitative statement and skip the footnote rather than inventing a figure.
- Note standard version/revision date explicitly in-line the first time it's introduced, e.g. "TLS 1.3 (RFC 8446, 2018-08)".

## 4. Mermaid diagrams
- Every diagram is followed immediately by one plain-text line: `그림 설명: ...` — a full-sentence summary usable as alt text and indexed by search.
- Complex flows (>8 nodes) should be split into two linked diagrams (e.g., "요청 흐름" then "오류 처리 흐름") rather than one dense graph.
- **Strict Syntax Rules**:
  - Always quote node labels containing special characters (`()`, `/`, `:`, `&`, `#`) using `["..."]` or `{"..."}` to prevent parser syntax errors.
  - Never use HTML entities (`--&gt;`, `&lt;=&gt;&gt;`) for arrows — always use raw Mermaid arrow syntax (`-->`, `->>`, `<-->`).
- Use semantic exception colors (§ design-tokens.md) only for state nodes (지원/부분지원/미지원 등), never for decoration.

## 5. Technology comparison table (compare-table)
Triggered for every "core technology" introduced in a chapter. Structure:

| 기술명 | 핵심 특징 | 장점 | 단점 | 적합 사용처 | 근거 문서 |
|---|---|---|---|---|---|
| (본 챕터 기술, highlighted column) | ... | ... | ... | ... | [n] |
| 대안 A | ... | ... | ... | ... | [n] |
| 대안 B | ... | ... | ... | ... | [n] |

Rules:
- 2–4 rows total (chosen tech + 1–3 alternatives). Select alternatives that are actually discussed as competing/adjacent approaches in the cited standards/papers — not an arbitrary list.
- **Comprehensive Technical Axes**: When building cross-cutting or summary comparison tables, include deep technical comparison axes:
  - Transport Layer, Serialization/Wire Format, Minimal Header Bytes, Flow Control, Multiplexing mechanism, Connection Handshake RTT, NAT/Firewall Traversal, Browser Native Support, Embedded/MCU Constraints, Supported Topologies.
- Each cell's claims need the same footnote-citation treatment as body text.
- End with **one verdict sentence**: why this document teaches/uses the chosen technology over the alternatives.
- Rendered via D3 (see `assets/template.html` `renderCompareTable()`), not a plain HTML `<table>`, so it exports to SVG at publication quality. Cells wrap (not truncate) — row heights are computed from measured wrapped text, so don't hand-set a fixed row height when editing this function.

## 6. Charts & data tables (D3)
- Always: axis labels + units, legend if >1 series, colorblind-safe palette, Figure/Table numbering.
- Caption placement: **tables** — caption above; **figures/charts** — caption below (academic convention).
- Provide an "SVG로 내보내기" button per chart/table for reuse in papers/slides.

## 7. Abbreviations & Glossary
- First use per chapter: wrap in `<abbr title="...">` with a hover tooltip AND a footnote-style superscript linking to the glossary page.
- Glossary page (opened via Shift+/): alphabetical, searchable, each entry back-links to every chapter location it appears in.

## 8. Cover page (mandatory, auto-generated)
The template always renders a cover page before Chapter 1, built from `title`, `version`, `createdDate`, `reviewedDate`, and a new top-level `learningGoals: [string,...]` array. Populate `learningGoals` with 2–4 concrete, checkable outcomes ("~를 근거를 들어 설명할 수 있다" style), not vague aspirations. The cover also auto-lists all chapters with their `motivation` as a one-line preview — don't duplicate this content elsewhere.

## 9. Code / RFC excerpt blocks
Wrap code or protocol excerpts as:
```html
<div class="code-block" data-lang="JSON"><pre><code>실제 코드/텍스트 (그대로, 이스케이프 불필요)</code></pre></div>
```
The renderer adds the language header and line numbers automatically. Use `data-lang` for the actual language/format name shown (e.g. `JSON`, `text`, `pseudocode`) — don't invent a language that doesn't match the content.

## 9.5 Protocol packet header layouts (Bitfield Tables)
When presenting network packet headers, frame formats, or bit-level field specifications (e.g. HTTP/2 9-byte header, Zenoh minimal header, IPv4/TCP header), do NOT use raw ASCII art (`+---+---+`). Use the built-in `.bitfield-table-wrap` component for responsive, clean rendering:
```html
<div class="bitfield-table-wrap">
  <table class="bitfield-table">
    <thead>
      <tr><th>비트 0~7</th><th>비트 8~15</th><th>비트 16~31</th></tr>
    </thead>
    <tbody>
      <tr><td class="highlight">필드 A</td><td>필드 B</td><td>필드 C</td></tr>
    </tbody>
  </table>
  <div class="bitfield-caption">Table n. 필드 명세 설명</div>
</div>
```

## 10. Charts (D3 bar/line, distinct from compare tables)
Use a `charts` array (sibling to `compareTables`) inside a chapter for **quantitative series data** (benchmarks, latency, throughput) — as opposed to `compareTables`, which is for qualitative technology comparisons. Schema:
```json
{"figureLabel":"Figure 1","caption":"Figure 1. ...","type":"bar","xLabel":"...","yLabel":"...","unit":"ms",
 "series":[{"name":"...", "points":[{"x":"카테고리","y":숫자}, ...]}]}
```
Same citation rule applies: the caption or a footnote in the surrounding text must cite where the numbers came from.

## 11. Callout boxes
Three types, used sparingly (not every paragraph): `note`(참고), `warning`(주의), `deep`(심화). Markup:
```html
<div class="callout warning" data-label="주의">본문...</div>
```
Use `warning` for correctness/security caveats, `note` for supplementary context, `deep` for optional advanced detail a first-time reader can skip on a first pass (again, a calibration note only — don't write 학사 or similar terms into the callout text).

## 12. Figures / screenshots
```html
<figure class="figure-block"><img src="..." alt="설명"><figcaption>Figure n. 캡션</figcaption></figure>
```
Only use real, sourced images (never fabricate a screenshot). If no image asset is available, prefer a Mermaid diagram or D3 chart instead of skipping the visual.

## 12.5 Mermaid 다이어그램 및 시퀀스/플로우 상세 해설(Walkthrough) 규칙 (CRITICAL)
다이어그램(시퀀스 다이어그램, 아키텍처 토폴로지, 데이터 흐름도 등)은 절대 시각 자료만 덩그러니 배치되어서는 안 됩니다.
1. **1:1 대응 단계별 해설(Step-by-Step Breakdown)**:
   - 다이어그램의 각 노드, 화살표, 상태 전이, 메시지 교환 순서와 1:1로 매핑되는 번호 매겨진 해설 목록(`<ol><li>...</li></ol>`) 또는 상세 단락을 반드시 직전 또는 직후 본문에 제공해야 합니다.
2. **시퀀스 다이어그램 해설 요건**:
   - 메시지 송수신 주체, 전달되는 페이로드/헤더 필드, 연결 상태(State)의 전이(예: Half-closed, Established), 타임아웃 및 폴백 조건을 단계별로 명시해야 합니다.
3. **아키텍처/플로우 다이어그램 해설 요건**:
   - 데이터 인입(Ingress)부터 처리(Processing), 캐싱/영속화(Storage), 최종 사용자 전달(Egress)까지의 패킷 여정(Packet Journey)을 노드별로 추적하여 설명해야 합니다.


## 13. References page
The footer's "참고문헌" link opens a dedicated references view listing every entry in `references`, grouped by `normative`/`informative`. Every reference added to the JSON automatically appears there — don't hand-write a references section in chapter content.

## 14. Right-side TOC now reflects h3
Any `<h3>` used inside a section's `html` is automatically picked up and nested under the page TOC (and the in-page mobile TOC) — no manual registration needed. Use h3 for a genuine sub-point within a section, not for cosmetic emphasis.

## 15. Business-data exclusion
No pricing, licensing cost, market share, vendor revenue, or competitive-positioning-as-a-business content. If a source discusses this, drop that part and keep only the technical substance.

## 16. Text formatting & Inline Markdown
- In JSON fields (`html`, `motivation`, `summary`, `qa`, `verdict`), prefer standard HTML tags: `<strong>...</strong>`, `<em>...</em>`, `<code>...</code>`.
- The template includes an automated inline markdown parser (`parseInlineMarkdown`) that automatically converts `**bold**` to `<strong>`, `*italic*` to `<em>`, and `` `code` `` to `<code>` at render time. This prevents raw asterisks from being displayed to the reader even if markdown shorthand is inadvertently used.

## 17. 프로덕션 인프라 및 클라우드(Cloud Native) 아키텍처 서술 규칙 (CRITICAL)
서버, 네트워킹, 분산 미들웨어, 스트리밍, 대규모 IPC 관련 기술을 다룰 때는 소프트웨어 코드 레벨뿐 아니라 **실제 프로덕션 환경 및 클라우드(AWS/GCP/Azure) 배포 인프라 아키텍처**를 반드시 포함해야 합니다.

1. **로드밸런싱 및 트래픽 분산 전략 (L4 vs L7)**
   - 프로토콜 특성(비연결형 UDP, 연결형 TCP, 단일 연결 다중화 스트리밍 등)에 따른 로드밸런서 선택 기준을 명시합니다.
   - 단일 커넥션 다중화 환경에서의 L4 로드밸런서 커넥션 고착(Connection Sticking) 문제 및 L7 애플리케이션 프록시(Envoy, ALB 등)를 통한 프레임/요청 단위 분산 원리를 설명합니다.
2. **네트워크 경계, NAT 트래버설 및 포트 관리**
   - 방화벽 통과, 대규모 동적 포트(Dynamic Port Range) 할당, 공인 IP 1:1 바인딩, 사내 보안망 차단 우회(표준 443 포트 폴백 및 보안 터널링) 전략을 구체적으로 설명합니다.
3. **클라우드 네이티브 토폴로지 (Cloud Native Infrastructure)**
   - 컨테이너 오케스트레이션(K8s/ECS) 시의 네트워크 모드(`hostNetwork` vs Overlay CNI 오버헤드 비교).
   - Anycast 기반 글로벌 엣지 가속 계층을 통한 인터넷 라우팅 지터 및 패킷 손실 최적화.
   - 하이브리드 WAN 연동(Site-to-Site VPN / Direct Connect) 및 인터넷 데이터 송출(Egress) 비용 방어 전략.
4. **인프라 아키텍처 다이어그램 필수화**
   - 클라이언트 ➔ 엣지/게이트웨이 ➔ 로드밸런서 ➔ 서버 클러스터 ➔ 스토리지/캐시로 이어지는 인프라 토폴로지를 Mermaid 다이어그램으로 시각화합니다.


