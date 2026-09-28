# Design Tokens (ELI5 Explainer)

> **마스터 소스 참조**: 이 파일은 `study-material-generator/references/design-tokens.md`를 **100% 따릅니다**.  
> 색상·타이포그래피·여백 토큰 변경 시 반드시 마스터 소스를 먼저 갱신하고 이 파일을 동기화하십시오.

`eli5`의 웹 산출물은 `study-material-generator`와 동일한 디자인 토큰과 타이포그래피를 준수하여 통일된 브랜드 일관성을 제공합니다.

---

## Color Tokens (마스터 동기화 — v2)

```css
/* ── 라이트 테마 (수정: canvas-soft, hairline 계열, muted 값 동기화) ── */
:root {
  --primary: #141414; --accent: #0066ff;
  --canvas: #ffffff; --canvas-soft: #f3f3f3; --field: #f0f0f0;  /* #f8f9fa → #f3f3f3 */
  --hairline-soft: #e4e4e4; --hairline: #d0d0d0;                 /* 대비 강화 */
  --ink: #141414; --ink-soft: #262626; --muted: #5a5a5a; --faint: #adadad;  /* #707070 → #5a5a5a */
  --on-primary: #ffffff;
  --code-bg: #f0f0f0;
}

/* ── 다크 테마 (수정: canvas-soft, raised, hairline-soft, muted 값 동기화) ── */
:root[data-theme="dark"] {
  --primary: #ffffff; --accent: #0066ff;
  --canvas: #0a0a0a; --canvas-soft: #1a1a1a; --field: #1e1e1e; --raised: #2e2e2e;  /* #161616→#1a1a1a, #2a2a2a→#2e2e2e */
  --hairline-soft: #303030; --hairline: #404040;                  /* #222222→#303030, #333→#404040 */
  --ink: #ffffff; --ink-soft: #e2e2e2; --muted: #9a9a9a; --faint: #707070;  /* #adadad→#9a9a9a */
  --on-primary: #141414;
  --code-bg: #1e1e1e;
}
```

### Contrast notes
- `--muted` (#5a5a5a / #9a9a9a): 보조 텍스트(캡션, 메타)에 사용. 라이트 4.95:1, 다크 모드 WCAG AA 확보.
- `--faint` (#adadad / #707070): sub-AA by design (placeholders/fine print only). 주요 읽기 텍스트에 사용 금지.
- `--hairline` (#d0d0d0 / #404040): 테이블·섹션 구분선. 이전 값 대비 가시성 향상.

---

## Typography (마스터 동기화 — v2)

- **한글/영문 기본 본문**: `Pretendard Variable` (OFL, 400~700 Variable)
- **코드 및 기술 용어 표기**: `JetBrains Mono`
- **소수점 폰트 사이즈 금지**: `15.5px` 등은 서브픽셀 렌더링 아티팩트 유발. 정수 또는 `.5px` 단위만 허용.

| 용도 | 폰트 크기 | 굵기(Weight) | Line Height | Letter-spacing | 비고 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **문서 타이틀** | 36px | 700 | 1.2 | -0.02em | Explainer 메인 제목 |
| **청중 배지 (label)** | 11.5px | 650 | 1.3 | 0.03em | 청중 유형 식별 뱃지 (**12→11.5**) |
| **섹션 제목 (H2)** | 25px | 650 | 1.25 | -0.01em | 비유, 원리, 질의응답 (**22→25**, 마스터 기준) |
| **카드 제목 (H3)** | 20px | 600 | 1.3 | 0 | 스텝 및 세부 카드 제목 (**17→20**, 마스터 기준) |
| **본질 요약 리드문 (body-lg)** | 18px | 450 | 1.65 | 0 | The Essence 한 줄 정의 (**wt 500→450**) |
| **본문 설명 (body)** | 16.5px | 420 | 1.75 | -0.01em | 쉬운 비유 및 풀이 텍스트 (**15.5→16.5**, lh 1.65→1.75) |
| **캡션 / 부가 설명 (body-sm)** | 13.5px | 450 | 1.55 | 0 | 다이어그램 설명 및 팁 (**13→13.5**) |
| **코드 (mono)** | 14px | 450 | 1.75 | 0 | 코드 블록 (**lh 1.6→1.75**) |

### eli5 전용 컴포넌트 크기

| 컴포넌트 | font-size | line-height | 비고 |
|---|---|---|---|
| `.essence-text` | 20px | 1.55 | 핵심 본질 한 줄 (**19→20**) |
| `#analogy-text` | 16.5px | 1.75 | 비유 본문 (body와 동일, **15.5→16.5** 정수화) |
| `.step-desc` | 14.5px | 1.65 | 단계 설명 (**14→14.5**) |
| `.qa-question` | 15px | 1.5 | 질문 텍스트 (**14.5→15**) |
| `.qa-answer` | 14.5px | 1.65 | 답변 텍스트 (**14→14.5**) |

---

## Spacing (마스터 동기화)

| 컴포넌트 | padding | margin |
|---|---|---|
| `main` | `28px 52px 56px` | (layout) |
| `.canvas-card-body` | `24px` | — |
| `.canvas-card-header`, `.canvas-card-footer` | `12px 18px` | — |
| `.motivation`, `.summary-box` | `22px 28px` | `0 0 24px` |
| `.callout` | `16px 20px` | `20px 0` |
| `.canvas-card` | — | `28px 0` |
| `p` | — | `0 0 18px` |

---

## Semantic Palette (Okabe-Ito 색각 이상 대응)

- **긍정 / 쉬운 비유 / 정답**: `#009E73` (Dark: `#3DDC97`)
- **주의 / 오해 방지 / 팁**: `#E69F00` (Dark: `#F5B942`)
- **흔한 착각 / 위험 / 주의사항**: `#D55E00` (Dark: `#E8734A`)
