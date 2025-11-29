import os
from flask import Flask, request, jsonify
import logging
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# TOKEN
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN not set!")

# Bot
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("🎮 Chơi Tiến Lên", web_app={"url": "https://tienlen-miniapp.netlify.app"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 CHÀO BẠN! Bấm nút để chơi Tiến Lên Miền Nam!",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context):
    await update.message.reply_text("Gõ /start để chơi!")

# Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/")
def index():
    return "<h1>🚀 Tiến Lên Bot Live! v20</h1><a href='/health'>Health</a>"

@app.route("/health")
def health():
    return jsonify({"status": "OK", "version": "v20"})

@app.route("/setwebhook")
async def set_webhook():
    webhook_url = f"https://{request.host}/webhook"
    await application.bot.set_webhook(url=webhook_url)
    return f"<h1>✅ WEBHOOK SET v20: {webhook_url}</h1>"

@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        if update:
            await application.process_update(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "ERROR", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # Render requires explicit port binding
    app.run(host="0.0.0.0", port=port)
