import os
from dotenv import load_dotenv

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
    from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
    from telegram.constants import ParseMode
except ImportError:
    Update = InlineKeyboardButton = InlineKeyboardMarkup = Bot = None
    ApplicationBuilder = CommandHandler = ContextTypes = ParseMode = None

load_dotenv()

class TelegramProvider:
    def __init__(self, agent_callback=None):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.agent_callback = agent_callback
        self.bot = Bot(token=self.token) if (Bot and self.token) else None

    async def send_alert(self, message: str):
        if self.bot and self.chat_id:
            await self.bot.send_message(chat_id=self.chat_id, text=f"🚨 {message}")
        else:
            print(f"[Mock Alert] {message}")

    async def request_approval(self, pr_url: str, description: str):
        print(f"[Mock Approval] {description} -> {pr_url}")

    def listen(self):
        if not (ApplicationBuilder and self.token):
            print("[Mock Listener] 라이브러리 부재로 시뮬레이션 모드에서 대기합니다.")
            return
        # ... (생략)

class MessengerProvider:
    def __init__(self, agent_callback=None):
        self.provider_type = os.getenv("MESSENGER_PROVIDER", "telegram")
        self.instance = TelegramProvider(agent_callback)

    async def send_alert(self, message: str):
        await self.instance.send_alert(message)

    async def request_approval(self, pr_url: str, description: str):
        await self.instance.request_approval(pr_url, description)

    def listen(self):
        self.instance.listen()
