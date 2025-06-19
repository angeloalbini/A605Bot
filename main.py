import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === ENVIRONMENT ===
TOKEN = os.getenv("TOKEN")

# === FLASK APP ===
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"🔔 /start dari {update.effective_user.username}")
    await update.message.reply_text(
        f"Halo {update.effective_user.first_name}, bot siap patrol 24/7! 📋"
    )

bot_app.add_handler(CommandHandler("start", start))

# === WEBHOOK ROUTE ===
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.create_task(bot_app.update_queue.put(update))
    return "OK", 200

@app.route("/")
def index():
    return "Bot is up ✅", 200

# === RUN ===
if __name__ == "__main__":
    bot_app.initialize()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
