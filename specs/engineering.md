# Engineering Standard Specification

## 🛠 Commit Convention (Spec-Driven)
모든 커밋은 작업의 성격과 대상 명세를 명확히 식별할 수 있어야 합니다.

### Format
`<type>(<scope>): <spec-id> - <description>`

### Types
- **feat**: 새로운 기능 명세 구현
- **spec**: 명세서(Blueprints/Architecture) 작성 및 수정
- **refactor**: 명세 변경 없이 코드 구조 개선
- **fix**: 명세와 불일치하는 버그 수정
- **docs**: 문서 수정

### Example
- `feat(auth): login-spec - implement JWT validation logic`
- `spec(api): payment-blueprint - define refund interface`
- `fix(core): architecture-spec - resolve context freezing logic error`

## 📐 Implementation Rule
- 모든 커밋은 하나의 명세 단위(Blueprint)를 넘지 않는 원자적(Atomic) 단위를 유지한다.
- 커밋 메시지만 보고도 어떤 명세 문서가 업데이트되었는지 추적 가능해야 한다.