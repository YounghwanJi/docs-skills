# Design Tokens (ELI5 Explainer)

`eli5`의 웹 산출물은 `study-material-generator` 및 `seminar-material-generator`와 100% 동일한 디자인 토큰과 타이포그래피를 준수하여 통일된 브랜드 일관성을 제공합니다.

## Color Tokens

```css
:root {
  --primary: #141414; --accent: #0066ff;
  --canvas: #ffffff; --canvas-soft: #f8f9fa; --field: #f0f0f0;
  --hairline-soft: #f0f0f0; --hairline: #e0e0e0;
  --ink: #141414; --ink-soft: #262626; --muted: #707070; --faint: #adadad;
  --on-primary: #ffffff;
  --code-bg: #f0f0f0;
}
:root[data-theme="dark"] {
  --primary: #ffffff; --accent: #0066ff;
  --canvas: #0a0a0a; --canvas-soft: #161616; --field: #1e1e1e; --raised: #2a2a2a;
  --hairline-soft: #222222; --hairline: #333333;
  --ink: #ffffff; --ink-soft: #e2e2e2; --muted: #adadad; --faint: #707070;
  --on-primary: #141414;
  --code-bg: #1e1e1e;
}
```

## Typography

- **한글/영문 기본 본문**: `Pretendard Variable` (OFL, 400~700 Variable)
- **코드 및 기술 용어 표기**: `JetBrains Mono`

| 용도 | 폰트 크기 | 굵기(Weight) | Line Height | 비고 |
| :--- | :--- | :--- | :--- | :--- |
| **문서 타이틀** | 36px | 700 | 1.2 | Explainer 메인 제목 |
| **청중 배지** | 12px | 650 | 1.0 | 청중 유형 식별 뱃지 |
| **섹션 제목 (H2)** | 22px | 650 | 1.3 | 비유, 원리, 질의응답 |
| **카드 제목 (H3)** | 17px | 600 | 1.35 | 스텝 및 세부 카드 제목 |
| **본질 요약 리드문** | 18px | 500 | 1.6 | The Essence 한 줄 정의 |
| **본문 설명** | 15.5px | 450 | 1.65 | 쉬운 비유 및 풀이 텍스트 |
| **캡션 / 부가 설명** | 13px | 450 | 1.5 | 다이어그램 설명 및 팁 |

## Semantic Palette (Okabe-Ito 색각 이상 대응)

- **긍정 / 쉬운 비유 / 정답**: `#009E73` (Dark: `#3DDC97`)
- **주의 / 오해 방지 / 팁**: `#E69F00` (Dark: `#F5B942`)
- **흔한 착각 / 위험 / 주의사항**: `#D55E00` (Dark: `#E8734A`)
