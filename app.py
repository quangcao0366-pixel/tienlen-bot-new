from flask import Flask, request
import os
import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Disable telegram logging
logging.getLogger("telegram").setLevel(logging.WARNING)

app = Flask(__name__)

# Get token from environment
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)

# Simple webhook handler
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return 'ok'

# Start command
def start(update, context):
    keyboard = [[InlineKeyboardButton("🎮 Chơi Tiến Lên", web_app={"url": "https://tienlen-miniapp.netlify.app"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🎉 **CHÀO BẠN ĐẾN VỚI TIẾN LÊN BOT!**\n\n"
        "👆 Bấm nút bên dưới để **chơi Tiến Lên Miền Nam** ngay!\n\n"
        "✨ Game mượt, giao diện đẹp, chơi với bạn bè!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Unknown command
def unknown(update, context):
    update.message.reply_text("🎮 Gõ `/start` để bắt đầu chơi Tiến Lên Miền Nam!")

# Initialize dispatcher
dp = Dispatcher(bot, None, workers=0)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.command, unknown))

@app.route('/')
def index():
    return "🚀 Tiến Lên Bot is running!"

@app.route('/setwebhook')
def set_webhook():
    url = request.url_root + 'webhook'
    try:
        bot.set_webhook(url=url)
        return f"✅ WEBHOOK SET: {url}"
    except Exception as e:
        return f"❌ WEBHOOK ERROR: {e}"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
