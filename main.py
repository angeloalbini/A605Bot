from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import os

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # dari Render ENV
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Halo, {update.effective_user.first_name}! Bot aktif 24/7 🚀")

bot_app.add_handler(CommandHandler("start", start))

# 📌 INI YANG WAJIB ADA: Endpoint webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return "OK", 200

# Jalankan bot
if __name__ == "__main__":
    if WEBHOOK_URL:
        print(f"✅ Webhook mode aktif: {WEBHOOK_URL}")
        bot_app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL + WEBHOOK_PATH
        )
    else:
        print("⚠️ WEBHOOK_URL tidak ditemukan. Jalan polling mode...")
        bot_app.run_polling()
