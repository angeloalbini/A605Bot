import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")  # dari environment variable
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 5000))

# Inisialisasi Flask dan Bot
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# Handler perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"Halo {user}, bot ini aktif 24/7 di Render! 🚀")

# Pasang handler ke bot
bot_app.add_handler(CommandHandler("start", start))

# Endpoint webhook dari Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return "OK", 200

# Menjalankan webhook saat file ini dijalankan
if __name__ == "__main__":
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_URL')}{WEBHOOK_PATH}"
    )