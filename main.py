
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime

TOKEN = os.getenv("TOKEN")
LOG_FILE = "smoking_log.txt"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    return update.message.reply_text(f"Привет, {user.first_name}! Я твой трекер. Пиши мне сколько выкурил — я всё запишу. 💪")

async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {user.username or user.first_name}: {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    await update.message.reply_text("Записал. 📌")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(LOG_FILE):
        await update.message.reply_text("Пока нет записей 😶")
        return
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    total_msgs = len(lines)
    last_entries = lines[-5:] if total_msgs >= 5 else lines
    reply = f"📊 Всего записей: {total_msgs}\n\n📝 Последние записи:\n" + ''.join(last_entries)
    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))
    print("Бот запущен. Ждёт сообщений... 🟢")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

