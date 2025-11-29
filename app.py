import os
import logging
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# TOKEN
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN environment variable not set!")

# Create application (sync mode)
application = Application.builder().token(TOKEN).build()

# Start command handler
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("🎮 Chơi Tiến Lên", web_app={"url": "https://tienlen-miniapp.netlify.app"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 **CHÀO BẠN ĐẾN VỚI TIẾN LÊN BOT!**\n\n"
        "👆 Bấm nút bên dưới để **chơi Tiến Lên Miền Nam** ngay!\n\n"
        "✨ Game mượt, giao diện đẹp, chơi với bạn bè!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Message handler
async def handle_message(update: Update, context):
    await update.message.reply_text("🎮 Gõ `/start` để bắt đầu chơi Tiến Lên Miền Nam!")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route('/')
def index():
    return '''
    <h1>🚀 Tiến Lên Bot v20 Live!</h1>
    <p><a href="/health">Health Check</a> | <a href="/setwebhook">Set Webhook</a></p>
    '''

@app.route('/health')
def health():
    return {'status': 'OK', 'version': 'v20-sync', 'service': 'tienlen-bot'}

@app.route('/setwebhook')
def set_webhook():
    webhook_url = f"https://{request.host}/webhook"
    try:
        # Set webhook using sync method
        application.bot.set_webhook(url=webhook_url)
        return f'<h1>✅ WEBHOOK SET SUCCESS!</h1><p>URL: {webhook_url}</p>'
    except Exception as e:
        return f'<h1>❌ WEBHOOK ERROR: {str(e)}</h1>'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        if update:
            # Process update using async_to_sync pattern
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(application.process_update(update))
            loop.close()
        return 'OK'
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'ERROR', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
