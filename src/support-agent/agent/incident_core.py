import sys
import os
import asyncio
from dotenv import load_dotenv

# 상위 디렉토리 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.git_helper import GitHubHelper
from tools.spec_tool import spec_search, code_read
from tools.tester import SelfTester
from tools.logger import agent_logger
from tools.llm_provider import llm
from tools.messenger_provider import MessengerProvider # 새 메신저 프로바이더

load_dotenv()

class IncidentResponseAgent:
    def __init__(self):
        self.git = GitHubHelper()
        self.tester = SelfTester()
        self.logger = agent_logger
        self.llm = llm
        # 에이전트 생성 시 메신저는 아직 리스너를 실행하지 않음
        self.messenger = None 

    async def analyze_with_llm(self, error_log: str):
        self.logger.info(f"[LLM Analysis] {self.llm.provider_type} 엔진으로 분석 시작...")
        specs = spec_search("Incident Response Protocol")
        current_code = code_read("src/app.py")
        
        prompt = f"Specs: {specs}\nCode: {current_code}\nError: {error_log}\n해결 코드를 파이썬으로만 제안해."
        suggested_code = await self.llm.ask(prompt)
        
        self.logger.info(f"[LLM Analysis] 분석 완료.")
        return suggested_code

    async def run(self, incident_message: str):
        self.logger.info(f"🚨 [INCIDENT] {incident_message}")
        
        # 메신저 알림 (추상화된 인터페이스 사용)
        await self.messenger.send_alert(f"장애 감지 및 분석 시작: {incident_message}")

        # 분석 및 수정
        suggested_code = await self.analyze_with_llm(incident_message)
        branch_name = self.git.create_hotfix_branch()
        if not branch_name: return

        with open("src/app.py", "w", encoding="utf-8") as f:
            f.write(suggested_code)

        # 검증 및 PR
        success, msg = self.tester.run_unit_tests()
        if success:
            self.git.update_file_and_commit(branch_name, "src/app.py", suggested_code, "fix: autonomous fix")
            pr_url = self.git.create_pull_request(branch_name, f"Hotfix: {incident_message}", "Verified fix.")
            
            # 메신저 승인 요청 (추상화된 인터페이스 사용)
            await self.messenger.request_approval(pr_url, f"장애 {incident_message} 해결을 위한 PR 생성 완료.")
        else:
            self.logger.error("Test failed.")

if __name__ == "__main__":
    agent = IncidentResponseAgent()
    
    # 메신저 프로바이더 초기화 (에이전트의 run 메서드를 콜백으로 연결)
    messenger = MessengerProvider(agent_callback=agent.run)
    agent.messenger = messenger # 에이전트에게 메신저 장착
    
    # 리스너 가동 (Polling)
    messenger.listen()
