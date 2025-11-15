import time
from flask import Flask
import threading

app = Flask(__name__)


# ----------------------------
#   SERVER PARA RENDER
# ----------------------------
@app.route("/")
def home():
    return "Trading Bot Deriv está corriendo OK en Render"


def start_flask():
    # Flask debe correr en un hilo separado
    app.run(host="0.0.0.0", port=10000)


# ----------------------------
#   BOT DE TRADING (LO QUE YA TENEMOS)
# ----------------------------
def trading_bot():
    while True:
        # Aquí va tu lógica principal del bot:
        # - obtener velas
        # - analizar tendencia
        # - detectar estrategia
        # - ejecutar operaciones
        # - manejar martingalas (si las usamos)
        # - logs
        print("Analizando mercado...")  # TEMPORAL
        time.sleep(1)  # Ajustaremos después según timeframe


# ----------------------------
#   INICIO DEL PROGRAMA
# ----------------------------
if __name__ == "__main__":
    # Iniciar el servidor Flask
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Iniciar el bot
    trading_bot()
