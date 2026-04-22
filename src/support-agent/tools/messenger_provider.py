import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from telegram import Bot

load_dotenv()

class TelegramProvider:
    """텔레그램 메신저 구현체"""
    def __init__(self, agent_callback=None):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.agent_callback = agent_callback
        self.bot = Bot(token=self.token) if self.token else None

    async def send_alert(self, message: str):
        if self.bot and self.chat_id:
            await self.bot.send_message(chat_id=self.chat_id, text=f"🚨 *[Alert]*\n{message}", parse_mode=ParseMode.MARKDOWN)
        else:
            print(f"[Mock Alert] {message}")

    async def request_approval(self, pr_url: str, description: str):
        if self.bot and self.chat_id:
            keyboard = [[InlineKeyboardButton("🔗 PR 확인", url=pr_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await self.bot.send_message(
                chat_id=self.chat_id, 
                text=f"🛠 *[Approval Request]*\n{description}\nURL: {pr_url}", 
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            print(f"[Mock Approval] {description} -> {pr_url}")

    def listen(self):
        """리스너 가동 (Polling)"""
        if not self.token: return
        app = ApplicationBuilder().token(self.token).build()
        
        async def alert_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            msg = " ".join(context.args)
            await update.message.reply_text(f"🔍 대응 시작: {msg}")
            if self.agent_callback: await self.agent_callback(msg)

        app.add_handler(CommandHandler("alert", alert_handler))
        print("📡 Telegram 리스너 가동 중...")
        app.run_polling()

class MessengerProvider:
    """메신저 통합 캡슐화 레이어"""
    def __init__(self, agent_callback=None):
        self.provider_type = os.getenv("MESSENGER_PROVIDER", "telegram")
        if self.provider_type == "telegram":
            self.instance = TelegramProvider(agent_callback)
        # 나중에 SlackProvider 등을 여기에 추가 가능

    async def send_alert(self, message: str):
        await self.instance.send_alert(message)

    async def request_approval(self, pr_url: str, description: str):
        await self.instance.request_approval(pr_url, description)

    def listen(self):
        self.instance.listen()
