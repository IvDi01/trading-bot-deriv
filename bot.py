from flask import Flask
from threading import Thread
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

# ---------------------------- BOT HANDLERS ----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bot de Deriv funcionando correctamente en Render! 🚀")

# ---------------------------- FLASK KEEPALIVE ----------------------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Trading Bot Deriv está corriendo OK en Render - " + datetime.utcnow().isoformat()

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    server = Thread(target=run_flask)
    server.daemon = True
    server.start()

# ---------------------------- START BOT ----------------------------

async def start_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))

    await app_bot.run_polling()

if __name__ == "__main__":
    keep_alive()
    asyncio.run(start_bot())
