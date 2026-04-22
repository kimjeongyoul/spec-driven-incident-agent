# 🚨 Spec-Driven Incident Response Agent (IRA)

> **"명세(Spec)가 에이전트를 리드하고, AI가 스스로 코드를 검증한다."**

AI 시대의 장애 대응 표준을 제시하는 **`spec-driven-incident-agent`**입니다. 이 프로젝트는 단순한 자동화를 넘어, 프로젝트의 명세(`specs/`)를 직접 읽고 스스로 판단하여 핫픽스 PR을 생성하는 **지능형 에이전트 프레임워크**를 구현합니다.

---

## 🌟 Key Features

- **Spec-Driven Thinking**: `ai-spec-kit` 표준을 따라 `specs/`의 장애 대응 프로토콜을 실시간으로 분석하여 대응합니다.
- **Autonomous Self-Correction**: AI가 수정한 코드를 맹신하지 않습니다. 내장된 `SelfTester`를 통해 문법과 로직을 검증하며, 실패 시 최대 3회까지 스스로 코드를 재수정합니다.
- **Full-Cycle Automation**: 브랜치 생성 -> 코드 수정 -> 커밋 -> PR 생성 -> 텔레그램 승인 요청까지의 전 과정을 자동화합니다.
- **Production-Ready Logging**: 에이전트의 사고(Thought)와 행동(Action)을 상세히 기록하여 사후 분석(Post-mortem)이 용이합니다.
- **Configurable Architecture**: 환경 변수(`.env`) 하나로 대상 브랜치, 임계치, API 연동 설정을 자유롭게 조절할 수 있습니다.

---

## 🏗 System Architecture

```text
Experience Layer (Alerts)  -->  Thinking Layer (ReAct Loop)  -->  Action Layer (Tools)
       [Telegram Bot]           [Spec-Driven Analysis]          [GitHub / Git / Test]
```

- **Thinking Layer**: `Incident Response Protocol` 명세를 바탕으로 장애 등급(Level)을 스스로 판별.
- **Action Layer**: `PyGithub`를 통한 자동 PR 생성 및 `python-telegram-bot`을 활용한 승인 인터페이스.

---

## 📂 Project Structure

```text
.
├── .ai/                    # AI 협업 규칙
├── specs/                  # [SSOT] 프로젝트 명세 및 의사결정 문서
│   ├── blueprints/         # 에이전트 설계도
│   └── decisions/          # 장애 대응 프로토콜 (Incident Protocol)
├── src/
│   ├── support-agent/      # 에이전트 코어 로직
│   │   ├── agent/          # 메인 에이전트 (Incident Core)
│   │   ├── tools/          # Git, Messenger, Tester, Logger 도구함
│   │   └── prompts/        # 에이전트 페르소나 및 사고 유도 프롬프트
│   └── app.py              # 에이전트의 수정 대상 (Target Source)
└── .env.template           # 환경 변수 가이드
```

---

## 🚀 Quick Start

### 1. Prerequisite
- Python 3.9+
- GitHub Personal Access Token (with repo scope)
- Telegram Bot Token & Chat ID

### 2. Setup
```bash
git clone https://github.com/kimjeongyoul/spec-driven-incident-agent.git
cd spec-driven-incident-agent
pip install -r requirements.txt
```

### 3. Environment Config
`.env.template` 파일을 `.env`로 복사하고 실제 값을 입력하세요.
```bash
cp .env.template .env
```

### 4. Run (Simulation)
```bash
python src/support-agent/agent/incident_core.py
```

---

## 💡 Why This Project?

이 소스는 **"AI 에이전트가 어떻게 실무 운영(Ops)에 개입하여 신뢰를 얻을 수 있는가"**에 대한 해답입니다. 단순히 코드를 짜는 AI가 아니라, **규칙(Spec)을 지키고 결과(Test)를 책임지는** 에이전트 아키텍처를 경험해 보세요.

---

## 📜 License
MIT License

## 🤝 Contribution
개인의 기술적 경험을 자산화하여 AI 시대의 표준 소스로 공유하려는 모든 시도를 환영합니다.
