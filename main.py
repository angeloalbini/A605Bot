import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIG
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 5000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === FLASK & BOT
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# === HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 /start dari @{update.effective_user.username}")
    await update.message.reply_text(
        f"Halo {update.effective_user.first_name}, bot siap patrol 24/7!"
    )

bot_app.add_handler(CommandHandler("start", start))

# === WEBHOOK ROUTE (SYNC)
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.create_task(bot_app.process_update(update))
        return "OK", 200

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return "Error", 500

@app.route("/")
def index():
    return "Bot is running ✅", 200

# === RUN APP
if __name__ == "__main__":
    asyncio.run(bot_app.initialize())
    app.run(host="0.0.0.0", port=PORT)
