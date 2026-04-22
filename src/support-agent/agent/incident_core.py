import sys
import os
import asyncio
from dotenv import load_dotenv

# 상위 디렉토리 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.git_helper import GitHubHelper
from tools.messenger_helper import TelegramHelper
from tools.spec_tool import spec_search
from tools.tester import SelfTester
from tools.logger import agent_logger # 실무형 로그 시스템 도입

load_dotenv()

class IncidentResponseAgent:
    def __init__(self):
        self.git = GitHubHelper()
        self.telegram = TelegramHelper()
        self.tester = SelfTester()
        self.logger = agent_logger # 에이전트 로거 초기화

    async def run(self, incident_message: str):
        self.logger.info(f"🚨 [NEW INCIDENT] {incident_message} 감지")
        
        # 1. Thought & Spec Check
        self.logger.info("[Thought] 1. 장애 등급 파악을 위해 대응 명세(IRP)를 조회합니다.")
        protocol = spec_search("Incident Response Protocol")
        self.logger.info("[Observation] 장애 대응 지침(Level 2) 확인 완료")

        await self.telegram.send_alert(f"장애 발생: {incident_message}\n자가 교정 루프를 시작합니다.")

        # 2. Action: 브랜치 생성
        self.logger.info("[Action] Git Hotfix 브랜치 생성을 시작합니다.")
        branch_name = self.git.create_hotfix_branch()
        if not branch_name:
            self.logger.error("❌ 브랜치 생성 실패로 작업을 중단합니다.")
            return

        # 3. Self-Correction Loop
        self.logger.info("🛠 자가 교정(Self-Correction) 루프 진입")
        
        attempts = 0
        max_attempts = 3
        current_code = "def main():\n    print('Running without timeout...') # Error simulation"
        
        while attempts < max_attempts:
            attempts += 1
            self.logger.info(f"--- 시도 {attempts}/{max_attempts} ---")
            
            with open("src/app.py", "w", encoding="utf-8") as f:
                f.write(current_code)

            # 테스트 실행
            self.logger.info(f"[Action] 수정된 코드({attempts}회차)에 대해 자가 테스트를 실행합니다.")
            success, msg = self.tester.run_unit_tests()
            
            if success:
                self.logger.info(f"✅ [Success] {attempts}회차 만에 테스트 통과!")
                break
            else:
                self.logger.warning(f"⚠️ [Test Fail] {attempts}회차 테스트 실패: {msg}")
                self.logger.info("[Thought] 에러 원인을 분석하여 핫픽스 코드를 보완합니다.")
                # 재수정 로직 (Timeout 추가)
                current_code = "def main():\n    # FIXED: Timeout logic added by Self-Correction\n    print('Running with 5s Timeout...')\n"
        
        if success:
            # 4. Action: 최종 검증된 코드 커밋 및 PR 생성
            self.logger.info("[Action] 최종 검증된 코드를 GitHub에 푸시합니다.")
            self.git.update_file_and_commit(
                branch_name=branch_name,
                file_path="src/app.py",
                new_content=current_code,
                commit_message=f"fix(core): incident-{incident_message} (Self-Corrected)"
            )

            pr_url = self.git.create_pull_request(
                branch_name=branch_name,
                title=f"🚨 [Hotfix/Self-Corrected] {incident_message}",
                body=f"자가 교정 루프를 거쳐 {attempts}번의 시도 끝에 검증된 PR입니다.\n- 결과: {msg}"
            )

            if pr_url:
                self.logger.info(f"🚀 [PR Created] URL: {pr_url}")
                await self.telegram.request_approval(
                    pr_url=pr_url,
                    description=f"장애({incident_message})에 대해 {attempts}번의 자가 교정 및 검증을 완료한 PR입니다."
                )
        else:
            self.logger.error("🚫 [Fatal] 모든 자가 교정 시도가 실패했습니다. 즉시 수동 대응이 필요합니다.")
            await self.telegram.send_alert("⚠️ 자가 교정 모든 시도 실패! 즉시 확인 바랍니다.")

if __name__ == "__main__":
    agent = IncidentResponseAgent()
    
    # 디렉토리 확인
    if not os.path.exists("src"): os.makedirs("src")
    
    asyncio.run(agent.run("Error rate 12% in Production"))
