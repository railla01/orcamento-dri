from bot import app
from threading import Thread
from flask import Flask
import os

# Inicializa o bot em paralelo
def iniciar_bot():
    print("🤖 DRI rodando via Web Service no Render!")
    app.run()

# Web app do Flask
web_app = Flask("DRI-Flask")

@web_app.route("/")
def home():
    return "✅ DRI Bot está online!"

# Start apenas do bot (Flask é gerenciado pelo Gunicorn)
if __name__ == "__main__":
    Thread(target=iniciar_bot, daemon=True).start()
