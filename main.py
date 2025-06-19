import os
from flask import Flask, request
import telegram

TOKEN = os.getenv("TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    text = update.message.text

    if text == "/start":
        bot.send_message(chat_id=chat_id, text="Halo! Bot ini aktif 24/7 🚀")

    return "OK", 200

@app.route("/")
def home():
    return "Bot is running ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
