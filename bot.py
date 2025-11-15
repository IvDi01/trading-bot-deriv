from flask import Flask
from threading import Thread
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

# ---------------------------- BOT HANDLERS ----------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! El bot está funcionando correctamente desde Render 🚀")

# ---------------------------- FLASK KEEPALIVE ----------------------------

app = Flask(__name__)

@app.route("/")
def home():
    return "Trading Bot Deriv está corriendo OK en Render - " + datetime.utcnow().isoformat()

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def start_flask():
    thread = Thread(target=run_flask)
    thread.daemon = True
    thread.start()

# ---------------------------- START BOT ----------------------------

async def start_bot():
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))

    print(">>> BOT INICIADO EN RENDER 🚀")
    await application.run_polling()

def main():
    start_flask()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())

# ---------------------------- RUN ----------------------------

if __name__ == "__main__":
    main()
