from bot import app
from threading import Thread
from flask import Flask
import os

def iniciar_bot():
    print("🚀 DRI rodando via Web Service no Render!")
    app.run()

web_app = Flask("DRI-FakeServer")

@web_app.route("/")
def home():
    return "✅ DRI Bot está online!"

if __name__ == "__main__":
    Thread(target=iniciar_bot).start()
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Servidor Flask ouvindo na porta {port}")
    web_app.run(host="0.0.0.0", port=port)
