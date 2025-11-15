import os
import time
import json
import threading
import asyncio
import websockets
from flask import Flask
from datetime import datetime

# ==== TELEGRAM ====
from telegram.ext import ApplicationBuilder, CommandHandler

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# ============== CONFIG (usa env vars en Render) ============
DERIV_API_KEY = os.getenv("DERIV_API_KEY")
APP_ID = os.getenv("DERIV_APP_ID", "1089")
CHECK_INTERVAL = float(os.getenv("CHECK_INTERVAL", "1"))
# ============================================================

app = Flask(__name__)

@app.route("/")
def home():
    return "Trading Bot Deriv está corriendo OK en Render - " + datetime.utcnow().isoformat()



# ============================================================
# ================   SERVIDOR FLASK   =========================
# ============================================================

def start_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ============================================================
# ================   WEBSOCKET DERIV   ========================
# ============================================================

DERIV_WS = f"wss://ws.binaryws.com/websockets/v3?app_id={APP_ID}"

async def deriv_listen_example():
    try:
        async with websockets.connect(DERIV_WS) as ws:
            await ws.send(json.dumps({"ticks": "frxEURUSD", "subscribe": 1}))
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                print("TICK:", data)

    except Exception as e:
        print("Websocket error:", e)
        await asyncio.sleep(2)
        return await deriv_listen_example()

def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(deriv_listen_example())


# ============================================================
# ================   TELEGRAM BOT   ==========================
# ============================================================

async def cmd_start(update, context):
    await update.message.reply_text(
        "🤖 ¡Bot conectado correctamente!\n\nRecibirás señales aquí."
    )

def start_telegram_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    print("✔ Telegram bot iniciado (polling).")
    app.run_polling()


# ============================================================
# ================   PROCESO PRINCIPAL   ======================
# ============================================================

def trading_bot():
    # Iniciar Websocket Deriv
    print("Arrancando websocket Deriv...")
    ws_thread = threading.Thread(target=start_async_loop, daemon=True)
    ws_thread.start()

    # Iniciar Telegram en otro hilo
    print("Arrancando bot de Telegram...")
    tg_thread = threading.Thread(target=start_telegram_bot, daemon=True)
    tg_thread.start()

    # Loop principal continuo
    while True:
        print(f"[{datetime.utcnow().isoformat()}] Ciclo principal ejecutado.")
        time.sleep(CHECK_INTERVAL)



# ============================================================
# ================   EJECUCIÓN GLOBAL   =======================
# ============================================================

if __name__ == "__main__":
    # Flask en otro hilo
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Bot principal
    trading_bot()
