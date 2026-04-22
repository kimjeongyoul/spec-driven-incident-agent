# Blueprint: Experience-Based Source Standard (EBSS)

## 1. Description
개인의 기술적 경험(Experience)을 실제 활용 가능한 소스(Source)와 문서(Spec)로 변환하는 표준 구조를 정의합니다.

## 2. Structure of an 'Experience Piece'
각 공유 단위는 다음을 포함해야 합니다:
- **`specs/blueprints/[piece-name].md`**: 
  - `Context`: 어떤 상황(Context)에서 이 경험이 발생했는가?
  - `Problem`: 구체적으로 어떤 기술적 문제(Problem)였는가?
  - `Insight`: AI 시대에 이 문제를 해결하며 얻은 핵심 통찰(Insight).
  - `Implementation Spec`: 해결책을 코드로 구현하기 위한 설계 요건.
- **`src/[piece-name]/`**: 명세에 기반한 실제 소스 코드.
- **`README.md` (root)**: 전체 공유 허브의 목차와 각 경험 요약.

## 3. Sharing Guidelines
- 모든 코드는 **'가독성'**과 **'재사용성'**을 최우선으로 작성합니다.
- AI가 소스 코드를 쉽게 이해하고 수정할 수 있도록 `ai-spec` 형식을 엄격히 따릅니다.
- 실제 발생했던 에러 로그나 시행착오의 흔적을 주석(History)으로 남기는 것을 권장합니다.
