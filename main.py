import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # isi manual di Render ENV
WEBHOOK_PATH = "/webhook"
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(f"Halo {user}, bot ini aktif 24/7! 🚀")

bot_app.add_handler(CommandHandler("start", start))

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return "OK", 200

if __name__ == "__main__":
    if WEBHOOK_URL:
        print(f"✅ Menjalankan bot dengan Webhook di {WEBHOOK_URL}")
        bot_app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL + WEBHOOK_PATH
        )
    else:
        print("⚠️ WEBHOOK_URL tidak ditemukan. Menjalankan dengan polling...")
        bot_app.run_polling()
