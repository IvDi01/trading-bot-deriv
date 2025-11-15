import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")  # Render env variable


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, ¡el bot ya está funcionando en Render! 🚀")


async def main():
    if TOKEN is None:
        raise ValueError("❌ ERROR: La variable de entorno BOT_TOKEN no está configurada.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot iniciado en Render... 🚀")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
