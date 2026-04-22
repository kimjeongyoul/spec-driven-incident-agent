import sys
import os
import asyncio
from dotenv import load_dotenv

# 상위 디렉토리 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.git_helper import GitHubHelper
from tools.messenger_helper import TelegramListener
from tools.spec_tool import spec_search, code_read
from tools.tester import SelfTester
from tools.logger import agent_logger

load_dotenv()

import google.generativeai as genai

class IncidentResponseAgent:
    def __init__(self):
        self.git = GitHubHelper()
        self.tester = SelfTester()
        self.logger = agent_logger
        
        # Gemini 설정
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
            self.logger.warning("GOOGLE_API_KEY가 없어 시뮬레이션 모드로 동작합니다.")

    async def analyze_with_llm(self, error_log: str):
        """
        Gemini 1.5 Pro를 사용하여 명세와 코드를 분석하고 핫픽스를 생성합니다.
        """
        if not self.model:
            return "def main():\n    print('Simulation mode: Timeout added')\n"

        self.logger.info("[LLM Analysis] Gemini 1.5 Pro 분석 시작...")
        
        # 1. 컨텍스트 수집
        specs = spec_search("Incident Response Protocol")
        current_code = code_read("src/app.py")
        
        # 2. 프롬프트 구성
        prompt = f"""
        당신은 실력 있는 SRE(Site Reliability Engineer)입니다.
        아래의 장애 대응 명세와 현재 소스 코드를 분석하여, 발생한 에러를 해결하는 '수정된 전체 코드'만 출력하세요.

        [장애 대응 명세]
        {specs}

        [현재 소스 코드]
        {current_code}

        [발생한 에러 로그]
        {error_log}

        규칙:
        1. 반드시 파이썬 코드만 출력하세요. 설명은 필요 없습니다.
        2. 명세에 정의된 대응 레벨을 준수하세요.
        """
        
        # 3. LLM 호출
        response = self.model.generate_content(prompt)
        suggested_code = response.text.replace("```python", "").replace("```", "").strip()
        
        self.logger.info("[LLM Analysis] Gemini가 수정 코드를 생성했습니다.")
        return suggested_code

    async def run(self, incident_message: str):
        """
        장애 대응 전체 프로세스
        """
        self.logger.info(f"🚨 [NEW INCIDENT] {incident_message}")

        # 1. 분석 (LLM 연동 단계)
        suggested_code = await self.analyze_with_llm(incident_message)

        # 2. 브랜치 생성 및 수정
        branch_name = self.git.create_hotfix_branch()
        if not branch_name: return

        # 3. 자가 교정 및 검증 루프
        # (이전 루프 로직 사용...)
        with open("src/app.py", "w", encoding="utf-8") as f:
            f.write(suggested_code)

        success, msg = self.tester.run_unit_tests()
        
        if success:
            self.git.update_file_and_commit(branch_name, "src/app.py", suggested_code, "fix: auto-correct via LLM analysis")
            pr_url = self.git.create_pull_request(branch_name, f"🚨 Hotfix: {incident_message}", "LLM 분석에 기반한 자동 수정 PR입니다.")
            self.logger.info(f"✅ PR 생성 완료: {pr_url}")
        else:
            self.logger.error("❌ 자가 검증 실패")

if __name__ == "__main__":
    agent = IncidentResponseAgent()
    
    # 텔레그램 리스너(귀) 가동
    # 리스너는 사용자의 알람을 받으면 agent.run을 호출합니다.
    listener = TelegramListener(agent_callback=agent.run)
    listener.run()
