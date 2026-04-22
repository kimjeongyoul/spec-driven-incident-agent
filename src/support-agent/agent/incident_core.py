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
from tools.llm_provider import llm # 캡슐화된 LLM 제공자 임포트

load_dotenv()

class IncidentResponseAgent:
    def __init__(self):
        self.git = GitHubHelper()
        self.tester = SelfTester()
        self.logger = agent_logger
        self.llm = llm # 캡슐화된 LLM 사용

    async def analyze_with_llm(self, error_log: str):
        """
        캡슐화된 LLM 인터페이스를 사용하여 장애를 분석합니다.
        """
        self.logger.info(f"[LLM Analysis] {self.llm.provider_type} 엔진으로 분석 시작...")
        
        specs = spec_search("Incident Response Protocol")
        current_code = code_read("src/app.py")
        
        prompt = f"""
        당신은 SRE 전문가입니다. 아래 명세와 코드를 분석하여 장애 해결 코드를 제안하세요.
        [Specs] {specs}
        [Code] {current_code}
        [Error] {error_log}
        반드시 파이썬 코드만 출력하세요.
        """
        
        # 추상화된 인터페이스 호출
        suggested_code = await self.llm.ask(prompt)
        
        self.logger.info(f"[LLM Analysis] {self.llm.provider_type} 분석 완료.")
        return suggested_code

    async def run(self, incident_message: str):
        # ... (이전과 동일한 워크플로우)
        self.logger.info(f"🚨 [INCIDENT] {incident_message}")
        suggested_code = await self.analyze_with_llm(incident_message)
        
        branch_name = self.git.create_hotfix_branch()
        if not branch_name: return

        with open("src/app.py", "w", encoding="utf-8") as f:
            f.write(suggested_code)

        success, msg = self.tester.run_unit_tests()
        if success:
            self.git.update_file_and_commit(branch_name, "src/app.py", suggested_code, "fix: auto-correct")
            pr_url = self.git.create_pull_request(branch_name, f"Hotfix: {incident_message}", "Auto-fix PR")
            self.logger.info(f"PR Created: {pr_url}")
        else:
            self.logger.error("Test failed after LLM correction")

if __name__ == "__main__":
    agent = IncidentResponseAgent()
    listener = TelegramListener(agent_callback=agent.run)
    listener.run()
