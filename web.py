from bot import app
from threading import Thread
from flask import Flask

# 🔁 Bot em paralelo
def iniciar_bot():
    print("🚀 DRI rodando via Web Service no Render!")
    app.run()

# 🌐 Flask para simular servidor web
web_app = Flask("DRI-Flask")

@web_app.route("/")
def home():
    return "DRI Bot está online! 🤖"

if __name__ == "__main__":
    Thread(target=iniciar_bot).start()
import os
port = int(os.environ.get("PORT", 5000))
web_app.run(host="0.0.0.0", port=port)
