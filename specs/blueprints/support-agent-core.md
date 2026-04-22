# Blueprint: Support Agent Core (SAC)

## 1. Overview
사용자의 기술적 문의를 분석하고, 프로젝트의 명세(`specs/`)와 코드를 바탕으로 정확한 해결책을 제안하는 실무형 AI 에이전트입니다.

## 2. Thinking Pattern (ReAct 기반)
에이전트는 모든 요청에 대해 다음 단계를 거칩니다:
1. **Thought**: 사용자의 의도를 파악하고, 필요한 정보(`specs` 혹은 `source`)가 무엇인지 판단합니다.
2. **Action**: 필요한 도구(`spec_reader`, `file_read` 등)를 실행합니다.
3. **Observation**: 도구의 실행 결과를 분석합니다.
4. **Conclusion**: 최종 답변을 구성하거나, 추가 행동이 필요하면 1단계로 돌아갑니다.

## 3. Core Tools
- **`spec_search`**: `specs/` 디렉토리 내에서 키워드 기반으로 관련 정책을 찾습니다.
- **`code_inspector`**: 실제 소스 코드의 구조나 로직을 읽어옵니다.
- **`draft_proposer`**: 해결을 위한 코드 수정안이나 새로운 명세 초안을 작성합니다.

## 4. Implementation Plan (src/support-agent/)
- `agent.py`: ReAct 루프 및 메인 로직.
- `tools/`: 각 도구의 구현체.
- `prompts/`: 에이전트의 페르소나 및 사고 유도 프롬프트.

## 5. Success Metrics
- 사용자가 질문했을 때 관련 `spec` 문서를 참조하여 답변하는가?
- 단순 텍스트 답변을 넘어 실행 가능한 코드나 수정안을 제안하는가?
