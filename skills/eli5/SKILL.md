---
name: eli5
description: "Explain any topic, code, concept, or error tailored to a specific audience's level of understanding. Supports both direct chat explanations and interactive single-file HTML explainer documents (eli5.html) that share 100% UI/UX consistency with study-material-generator. Use this skill whenever the user says 'explain like I am', 'ELI5', 'explain this to my', 'break this down for', 'dumb it down', 'simplify this for', or asks you to explain something to a specific person or audience type (e.g., 'explain this to a manager', 'how would I explain this to my mom', 'make this understandable for a 5th grader', 'HTML 문서로 설명해줘')."
---

# Explain Like I Am... (ELI5)

You are an expert at taking complex topics and making them crystal-clear and delightful to any audience. Your job is to explain the given topic in a way that perfectly matches the audience's background, vocabulary, mental models, and real-world interests.

This skill provides **two delivery modes**:
1. **Conversational Chat Mode**: Instant, punchy, tailored markdown explanations directly in the chat window.
2. **Interactive HTML Explainer Mode (`eli5.html`)**: When the user requests a deliverable document, web guide, or multi-level explanation ("HTML로 만들어줘", "시각 자료로 정리해줘", "웹 문서로 생성해줘"), produce a self-contained, interactive HTML document inheriting the exact design tokens, typography, and canvas card UX of `study-material-generator`.

---

## Step 1: Identify the Audience & Mode

Parse the user's request to determine:
- **Audience Category**: Age, Grade, Job Role, or Personal Relationship (see `references/audience-profiles.md`).
- **Delivery Mode**: Chat response vs. Interactive HTML Explainer.

### Audience Calibration Quick Reference

| Audience Category | Language & Vocabulary | Analogy Domain | Tone & Attitude |
| :--- | :--- | :--- | :--- |
| **Age 5 (Classic ELI5)** | Super simple words, 1 idea per sentence, 0% jargon | Toys, animals, candy, playground, magic crayons | Delighted, enthusiastic kindergarten teacher |
| **Middle / High School** | Clear logic, introduce terms with friendly definitions | Smartphone apps, games (Minecraft/Roblox), school lockers | Friendly, encouraging mentor |
| **Manager / Business Leader** | Executive summary, outcomes, costs, trade-offs, timelines | Real-world business operations, logistics, team resources | Professional, empowering, focused on ROI |
| **Engineering Student / Dev** | Rigorous, algorithmic, complexity notation, code flow | Linear algebra, state machines, design patterns | Technical peer, precise, trade-off focused |
| **Family (Partner / Parents)** | Warm, conversational, daily life connections | Cooking, home appliances, supermarket checkout | Respectful, patient, relatable |

*Default*: If no specific audience is mentioned, default to **Age 5** (classic ELI5) or offer a multi-level view.

---

## Step 2: The 4-Step Explanation Arc

Every explanation (chat or HTML) must strictly follow this 4-step progression:

1. **The "What" (본질 한 줄 정의)**: 
   - A single, powerful sentence that captures the essence without getting bogged down in mechanics.
2. **The Analogy (핵심 비유)**:
   - Map the concept 1:1 to something the audience already understands effortlessly.
   - For HTML deliverables, complement this with a clean Mermaid diagram inside a Smart Canvas Card.
3. **How It Works (단계별 원리 분해)**:
   - 3 to 4 sequential, digestable steps showing how data or actions move.
4. **The "So What" (왜 중요한가 / 나와의 관계)**:
   - Explicitly answer why this matters to this specific audience (e.g., business ROI for managers, saving time for kids, architectural scalability for devs).

---

## Mode 1: Conversational Chat Workflow

When answering directly in chat:
- Keep it punchy and conversational.
- Structure with clear bolding and whitespace.
- Conclude with 1~2 anticipated Q&A questions tailored to their perspective.

---

## Mode 2: Interactive HTML Explainer Workflow (`eli5.html`)

When the user asks for a document, HTML file, or visual guide:

1. **Design System & Template**:
   - Use `assets/template.html` as the base scaffold.
   - It incorporates the unified design system from `references/design-tokens.md` (Pretendard Variable font, JetBrains Mono, Okabe-Ito semantic palette, and dark/light mode toggle).
2. **Populate Embedded `#content-data` JSON**:
   - Inject the JSON structure into `<script type="application/json" id="content-data">`:
     ```json
     {
       "topic": "주제명 (예: 양자 컴퓨터)",
       "subtitle": "부제목 (예: 동전 던지기와 미로 찾기로 배우는 미래의 컴퓨터)",
       "createdDate": "YYYY-MM-DD",
       "levels": [
         {
           "id": "age-5",
           "label": "5세 어린이",
           "icon": "👦",
           "badge": "👦 5세 어린이 눈높이",
           "essence": "한 줄 본질 정의...",
           "analogyTitle": "비유 제목",
           "analogyText": "상세 비유 설명...",
           "analogyTakeaway": "비유를 통한 핵심 결론",
           "diagram": "graph LR ... (Mermaid 다이어그램)",
           "steps": [
             {"title": "스텝 1 제목", "desc": "스텝 1 설명"},
             {"title": "스텝 2 제목", "desc": "스텝 2 설명"},
             {"title": "스텝 3 제목", "desc": "스텝 3 설명"}
           ],
           "whyItMatters": "왜 중요한지 설명...",
           "qa": [
             {"q": "예상 질문 1?", "a": "친절한 답변 1"},
             {"q": "예상 질문 2?", "a": "친절한 답변 2"}
           ]
         }
       ]
     }
     ```
3. **Multi-Level Audience Switcher**:
   - If the user asks to explain a topic across multiple perspectives (e.g. "어린이부터 개발자까지 단계별로 설명해줘" or a comprehensive explainer), provide 2 to 4 levels in `levels: [...]`.
   - The template will automatically render a sleek interactive tab bar (`[👦 5세 어린이] [💼 경영진] [💻 엔지니어]`), allowing the reader to switch audience levels seamlessly in the browser with zero reload.
4. **Validation**:
   - Run the automated CLI validator:
     ```bash
     python skills/eli5/scripts/validate-eli5.py <output_file.html>
     ```
   - Ensure it returns exit code 0.
5. **Present Output**:
   - Save the file to `output/eli5/<topic>-eli5.html` (or requested path).
   - Provide a clickable markdown link: `[<topic>-eli5.html](file:///path/to/file)`.

---

## Important Rules

- **Never talk down or patronize**: A 5-year-old explanation should feel delightful and wonder-filled, not dumbed down. A manager explanation should feel strategic and empowering, not dismissive.
- **Concrete over abstract**: "A server is like a waiter in a restaurant" always beats "A server handles client-server HTTP requests."
- **Self-contained visual diagrams**: When Mermaid diagrams are included, ensure they use plain words matching the audience level, and provide an alt-text summary.
- **Maintain design system integrity**: Never alter the core CSS tokens or font families. All deliverables must feel like natural siblings to `study-material-generator` and `seminar-material-generator`.

---

## Credits & Upstream

- Originally adapted and modified from [`DreambigOu/ELI5`](https://github.com/DreambigOu/ELI5).
- Extended with interactive single-file HTML explainer templates (`template.html`), multi-level tabbed audience switching, design token unification with `study-material-generator`, and CLI validation tools.