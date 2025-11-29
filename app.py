import os
import logging
from flask import Flask, request, render_template
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder="static", template_folder="templates")

# TOKEN TELEGRAM CỦA BẠN
TOKEN = os.environ.get("TOKEN", "8324573152:AAGkfklkdCvYpjkGTYKFGzA8L2M9JFzNxug")
bot = Bot(token=TOKEN)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/setwebhook")
def set_webhook():
    url = f"https://{request.host}/webhook"
    try:
        logger.info(f"🔗 Setting webhook to: {url}")
        ok = bot.set_webhook(url=url)
        if ok:
            return f"""
            <h1>✅ WEBHOOK SET THÀNH CÔNG!</h1>
            <p><strong>URL:</strong> <code>{url}</code></p>
            <h3>📱 TEST BOT:</h3>
            <ol>
                <li>Mở Telegram</li>
                <li>Tìm bot của bạn</li>
                <li>Gửi <code>/start</code></li>
                <li>Bấm "Chơi Tiến Lên"</li>
            </ol>
            <p><em>🎉 Bot đã live 24/7!</em></p>
            """
        else:
            return "<h1>❌ Webhook failed</h1>"
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
                keyboard = [[InlineKeyboardButton("🎮 Chơi Tiến Lên", web_app=WebAppInfo(url="https://tienlen-miniapp.netlify.app"))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(
                    chat_id=chat_id,
                    text="🎉 **CHÀO BẠN ĐẾN VỚI TIẾN LÊN BOT!**\n\n"
                         "👆 Bấm nút bên dưới để **chơi Tiến Lên Miền Nam** ngay!\n\n"
                         "✨ Game mượt, giao diện đẹp, chơi với bạn bè!",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text="🎮 Gõ `/start` để bắt đầu chơi Tiến Lên Miền Nam!"
                )
                
    except Exception as e:
        logger.exception("Webhook error")
    
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
