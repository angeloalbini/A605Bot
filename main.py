import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# === Konfigurasi Token dan Port ===
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 5000))

# === Flask App dan Telegram Bot ===
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# === Handler untuk /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"✅ /start dari @{update.effective_user.username}")
    await update.message.reply_text(f"Halo {update.effective_user.first_name}, bot siap patrol 24/7! 🛡️")

bot_app.add_handler(CommandHandler("start", start))

# === Route webhook, pakai ASYNC ===
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        # Jalankan process_update dalam event loop
        asyncio.get_event_loop().create_task(bot_app.process_update(update))
        return "OK", 200
    except Exception as e:
        print(f"❌ ERROR WEBHOOK: {e}")
        return "Webhook error", 500

@app.route("/")
def home():
    return "Bot is live ✅", 200

# === Jalankan ===
if __name__ == "__main__":
    asyncio.run(bot_app.initialize())  # WAJIB!
    app.run(host="0.0.0
