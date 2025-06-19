import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# === Inisialisasi ===
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 5000))
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# === Handler /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"✅ /start dari @{update.effective_user.username}")
    await update.message.reply_text(f"Halo {update.effective_user.first_name}, bot siap patrol 24/7! 🛡️")

bot_app.add_handler(CommandHandler("start", start))

# === Route webhook: pakai ASYNC dan AWAIT ===
@app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running ✅", 200

# === Jalankan ===
if __name__ == "__main__":
    asyncio.run(bot_app.initialize())  # WAJIB
    app.run(host="0.0.0.0", port=PORT)
