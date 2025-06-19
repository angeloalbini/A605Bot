import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

@app.route("/")
def index():
    return "Bot is running", 200

# Endpoint webhook dari Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return "OK", 200

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Halo {update.effective_user.first_name}, bot aktif 24/7 🚀")

bot_app.add_handler(CommandHandler("start", start))

# Jangan pakai run_webhook() — Render akan jalankan Flask
if __name__ == "__main__":
    bot_app.initialize()  # penting!
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
