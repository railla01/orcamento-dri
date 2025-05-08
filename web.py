from bot import app
from threading import Thread
from flask import Flask
import os  # Importa antes, pra usar no run

# 🔁 Bot rodando em paralelo
def iniciar_bot():
    print("🚀 DRI rodando via Web Service no Render!")
    app.run()

# 🌐 Mini servidor Flask só pra "enganar" o Render
web_app = Flask("DRI-Flask")

@web_app.route("/")
def home():
    return "✅ DRI Bot está online! 🤖"

# 🎯 Aqui está o bloco principal correto
if __name__ == "__main__":
    Thread(target=iniciar_bot).start()
    port = int(os.environ.get("PORT", 5000))
    web_app.run(host="0.0.0.0", port=port)
