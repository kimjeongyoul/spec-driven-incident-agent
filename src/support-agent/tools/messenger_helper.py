import os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from dotenv import load_dotenv
import asyncio

load_dotenv()

class TelegramHelper:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not self.token or not self.chat_id:
            # 실습 시에는 에러 대신 안내 메시지 출력
            print("[Warning] .env 파일에 TELEGRAM_BOT_TOKEN과 TELEGRAM_CHAT_ID가 필요합니다.")
        
        self.bot = Bot(token=self.token) if self.token else None

    async def send_alert(self, message: str):
        """
        장애 발생 알람을 전송합니다.
        """
        if not self.bot:
            print(f"[Mock Telegram Alert]: {message}")
            return

        full_message = f"🚨 *[Incident Alert]*\n\n{message}"
        await self.bot.send_message(
            chat_id=self.chat_id, 
            text=full_message, 
            parse_mode=ParseMode.MARKDOWN
        )

    async def request_approval(self, pr_url: str, description: str):
        """
        PR 승인 요청을 전송합니다. (인라인 버튼 포함)
        """
        if not self.bot:
            print(f"[Mock Telegram Approval Request]:\n- Description: {description}\n- PR URL: {pr_url}")
            return

        keyboard = [
            [
                InlineKeyboardButton("✅ 승인 (Merge)", callback_data='approve'),
                InlineKeyboardButton("❌ 거절 (Close)", callback_data='reject')
            ],
            [InlineKeyboardButton("🔗 PR 확인하기", url=pr_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            f"🛠 *[Hotfix PR Created]*\n\n"
            f"*Description*: {description}\n"
            f"*PR URL*: {pr_url}\n\n"
            f"위 수정을 승인하시겠습니까?"
        )
        
        await self.bot.send_message(
            chat_id=self.chat_id, 
            text=message, 
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

if __name__ == "__main__":
    # 비동기 실행 테스트
    async def test():
        helper = TelegramHelper()
        await helper.send_alert("에러율 12% 감지! 장애 대응을 시작합니다.")
    
    # asyncio.run(test()) # 실제 토큰 설정 후 주석 해제하여 실행
    print("TelegramHelper 준비 완료.")
