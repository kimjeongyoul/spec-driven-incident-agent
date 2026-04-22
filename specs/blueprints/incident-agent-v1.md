# Blueprint: Incident Response Agent (IRA)

## 1. Description
장애 감지 시, `specs/decisions/incident-protocol.md`에 정의된 정책에 따라 자동으로 핫픽스 PR을 생성하고 메신저로 승인 요청을 보냅니다.

## 2. Core Workflow (ReAct Based with Self-Correction)
1.  **Monitor(Mock)**: Telegram 봇으로부터 에러 수신 (`/alert "Error rate 10%"`)
2.  **Thought**: 에러 등급(Level 2)을 판단하고 대응 지침(`incident-protocol.md`)을 읽음.
3.  **Action (Source Analysis)**: `src/` 내의 잠재적 버그 지점 식별.
4.  **Action (Code Fix)**: 브랜치 생성 및 코드 수정.
5.  **Action (Self-Correction Loop)**:
    - **Test Action**: 수정된 코드에 대해 테스트 실행 (`tools/tester.py`).
    - **Observation**: 테스트 결과(성공/실패 및 에러 로그) 확인.
    - **Correction**: 테스트 실패 시 에러 로그를 분석하여 코드를 재수정 (최대 3회 시도).
6.  **Action (Git & PR)**: 테스트 통과 시에만 푸시 및 PR 생성 API 호출.
7.  **Action (Telegram Tool)**: PR 링크와 함께 "검증 완료된 PR" 승인 요청 발송.

## 3. Implementation Stack
- `agent/incident_core.py`: 메인 루프 (Telegram -> Spec Read -> Git Action)
- `tools/git_helper.py`: GitHub API(PyGithub 혹은 Mock) 연동.
- `tools/messenger_helper.py`: Telegram Bot API(Mock) 연동.

## 4. Expected Output
- GitHub 상의 새 PR.
- Telegram 메시지 (PR 링크 포함).
