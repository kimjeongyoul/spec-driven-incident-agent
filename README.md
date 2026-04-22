# 🚨 Spec-Driven Incident Response Agent (IRA)

> **"명세(Spec)가 에이전트를 리드하고, AI가 스스로 코드를 검증한다."**

AI 시대의 장애 대응 표준을 제시하는 **`spec-driven-incident-agent`**입니다. 이 프로젝트는 단순한 자동화를 넘어, 프로젝트의 명세(`specs/`)를 직접 읽고 스스로 판단하여 핫픽스 PR을 생성하는 **지능형 에이전트 프레임워크**를 구현합니다.

---

## 🔄 How it Works (에이전트 작동 원리)

본 에이전트는 장애 발생부터 해결까지의 전 과정을 **'사고하는 AI'**의 관점에서 자동화합니다.

### 1. Listen (장애 감지)
- **The Ear**: `MessengerProvider`를 통해 텔레그램 등의 메신저로부터 실시간 알람을 수신합니다.
- **Trigger**: 사용자가 `/alert "Error rate 12%"`와 같은 메시지를 보내면 에이전트가 즉시 가동됩니다.

### 2. Analyze (지능형 분석)
- **The Brain**: Gemini 1.5 Pro(LLM)가 다음 세 가지 데이터를 교차 분석합니다.
    - **Error Log**: 발생한 문제의 본질 파악.
    - **Specs**: 프로젝트의 장애 대응 규칙(`specs/decisions/incident-protocol.md`) 확인.
    - **Source Code**: 현재 코드의 취약점 및 수정 지점 식별.
- **Result**: 명세에 정의된 대응 레벨에 맞춰 최적의 '수정 코드'를 생성합니다.

### 3. Verify (자가 검증 및 교정)
- **The Eye**: 생성된 코드가 안전한지 `SelfTester`를 통해 자가 진단을 수행합니다.
- **Self-Correction**: 문법 오류나 로직 결함 발견 시, 에러 로그를 다시 LLM에게 전달하여 최대 3회까지 스스로 코드를 재수정합니다.

### 4. Execute (자동화 수행)
- **The Hand**: `GitProvider`를 통해 실무 표준에 맞는 작업을 수행합니다.
    - 새 핫픽스 브랜치 생성 (`hotfix/incident-[timestamp]`).
    - 검증된 코드 커밋 및 푸시.
    - GitHub/GitLab에 Pull Request 생성.

### 5. Notify (최종 보고)
- **The Voice**: PR 링크와 함께 상세 분석 결과를 메신저로 보고합니다.
- **Human Approval**: 사용자는 텔레그램에서 PR을 최종 확인하고 승인 버튼을 누르는 것으로 장애 대응을 마무리합니다.

---

## 🌟 Key Features

- **Pluggable Architecture**: LLM, Messenger, Git 엔진을 `.env` 설정만으로 자유롭게 교체 가능.
- **Spec-Driven**: 모든 행동의 근거는 사람이 작성한 명세서(`specs/`)에 기반함.
- **Self-Correction**: 테스트를 통과한 '검증된 코드'만 PR로 올리는 높은 신뢰성.
- **Production-Ready Logging**: 에이전트의 모든 사고 과정을 로그 파일로 영구 보관.

---

## 📂 Project Structure
(상세 구조 생략)

---

## 🚀 Quick Start
(설치 방법 생략)

---

## 💡 Why This Project?
이 프로젝트는 **"AI에게 어떻게 실무 운영권을 안전하게 위임할 것인가?"**에 대한 실전적인 해답을 제시합니다. 명세(Spec)라는 가이드라인과 자가 검증(Test)이라는 안전장치가 결합되었을 때, AI 에이전트는 비로소 팀의 신뢰할 수 있는 동료가 됩니다.
