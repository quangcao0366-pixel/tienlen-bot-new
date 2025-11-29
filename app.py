import os
import logging
from flask import Flask, request, render_template_string
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN not set!")

bot = Bot(token=TOKEN)

@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head><title>Tiến Lên Bot</title></head>
<body>
<h1>🎮 Tiến Lên Bot Live!</h1>
<a href="/setwebhook">Set Webhook</a>
</body>
</html>
    """)

@app.route("/setwebhook")
def set_webhook():
    url = f"https://{request.host}/webhook"
    try:
        ok = bot.set_webhook(url=url)
        if ok:
            return f"<h1>✅ WEBHOOK OK: {url}</h1><a href='/'>Home</a>"
        else:
            return "<h1>❌ Webhook False</h1>"
    except Exception as e:
        return f"<h1>❌ Error: {e}</h1>"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        
        if update and update.message:
            chat_id = update.message.chat.id
            text = update.message.text or ""
            
            if text == "/start":
                keyboard = [[InlineKeyboardButton("🎮 Chơi Tiến Lên", web_app={"url": "https://tienlen-miniapp.netlify.app"})]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(
                    chat_id=chat_id,
                    text="🎉 CHÀO BẠN! Bấm nút để chơi Tiến Lên Miền Nam!",
                    reply_markup=reply_markup
                )
            else:
                bot.send_message(chat_id=chat_id, text="Gõ /start để chơi!")
        
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "ERROR", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
