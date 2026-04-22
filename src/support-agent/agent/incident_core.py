import sys
import os
import asyncio
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.spec_tool import spec_search, code_read
from tools.tester import SelfTester
from tools.logger import agent_logger
from tools.llm_provider import llm
from tools.messenger_provider import MessengerProvider
from tools.git_provider import GitProvider # 새 Git 프로바이더

load_dotenv()

class IncidentResponseAgent:
    def __init__(self):
        self.git = GitProvider() # 추상화된 Git 사용
        self.tester = SelfTester()
        self.logger = agent_logger
        self.llm = llm
        self.messenger = None 

    async def analyze_with_llm(self, error_log: str):
        self.logger.info(f"[LLM Analysis] {self.llm.provider_type} 엔진 분석 시작")
        specs = spec_search("Incident Response Protocol")
        current_code = code_read("src/app.py")
        
        prompt = f"Specs: {specs}\nCode: {current_code}\nError: {error_log}\n해결 코드를 파이썬으로만 출력해."
        suggested_code = await self.llm.ask(prompt)
        return suggested_code

    async def run(self, incident_message: str):
        self.logger.info(f"🚨 [INCIDENT] {incident_message}")
        await self.messenger.send_alert(f"장애 분석 시작: {incident_message}")

        # 분석
        suggested_code = await self.analyze_with_llm(incident_message)
        
        # Git 액션 (추상화된 인터페이스)
        branch_name = self.git.create_hotfix_branch()
        if not branch_name: return

        with open("src/app.py", "w", encoding="utf-8") as f:
            f.write(suggested_code)

        # 검증 및 PR (추상화된 인터페이스)
        success, msg = self.tester.run_unit_tests()
        if success:
            self.git.update_file_and_commit(branch_name, "src/app.py", suggested_code, "fix: auto-hotfix")
            pr_url = self.git.create_pull_request(branch_name, f"Hotfix: {incident_message}", "Autonomous fix verified.")
            await self.messenger.request_approval(pr_url, f"장애 대응 PR 생성 완료.")
            self.logger.info(f"✅ 작업 완료. PR: {pr_url}")
        else:
            self.logger.error("❌ 자가 검증 실패")

if __name__ == "__main__":
    agent = IncidentResponseAgent()
    messenger = MessengerProvider(agent_callback=agent.run)
    agent.messenger = messenger
    messenger.listen()
