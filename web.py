from bot import app
from threading import Thread
from flask import Flask
import os

# Web app do Flask
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "✅ DRI Bot está online!"

# Inicializa o bot em paralelo
def iniciar_bot():
    print("🤖 DRI rodando via Web Service no Render!", flush=True)
    app.run()

# Start apenas do bot (Flask é gerenciado pelo Gunicorn)
if __name__ == "__main__":
    Thread(target=iniciar_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    web_app.run(host="0.0.0.0", port=port)
