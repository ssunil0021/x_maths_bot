import os
import datetime
import pytz
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from database import init_db

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

init_db()

application = ApplicationBuilder().token(BOT_TOKEN).build()

IST = pytz.timezone("Asia/Kolkata")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📘 Today’s Question", callback_data="today")],
        [InlineKeyboardButton("📚 Past Questions", callback_data="past")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to Higher Mathematics Daily Practice\n\nChoose an option:",
        reply_markup=reply_markup,
    )


async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "today":
        await query.message.reply_text("Today’s question will appear here.")
    elif query.data == "past":
        await query.message.reply_text("Past questions feature coming soon.")


application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_router))


@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"


@app.route("/")
def home():
    return "Bot is running!"


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    application.initialize()
    application.start()
    app.run(host="0.0.0.0", port=PORT)
