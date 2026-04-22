# Decision: Incident Response Protocol (IRP)

## 1. Context
서비스 운영 중 발생하는 장애에 대해 AI 에이전트가 자율적으로 대응할 수 있는 가이드라인을 정의합니다.

## 2. Decision: Response Levels
- **Level 1 (Warning)**: 에러율 1~5% 발생 시. 
  - Action: 담당자에게 Slack 알림만 전송.
- **Level 2 (Critical)**: 에러율 5~15% 발생 시.
  - Action: 원인 분석 후 **Hotfix 브랜치 생성 및 수정 PR 작성**. 담당자에게 승인 요청 알림.
- **Level 3 (Fatal)**: 에러율 15% 초과 시.
  - Action: 즉시 이전 안정 버전으로 롤백 실행 및 전사 공지.

## 3. Hotfix PR Standard
- Branch Name: `hotfix/incident-[timestamp]`
- Base Branch: `main`
- Description: 장애 원인, 수정 내용, 관련 명세 ID 포함.
