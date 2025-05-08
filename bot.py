from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from acesso import usuario_autorizado, id_autorizado
import requests
import os

# 🔐 Variáveis de ambiente obrigatórias
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# 🚨 Validação básica para evitar erro silencioso
if not all([API_ID, API_HASH, BOT_TOKEN, OPENAI_API_KEY]):
    raise EnvironmentError("⚠️ Variáveis de ambiente ausentes! Verifique API_ID, API_HASH, BOT_TOKEN e OPENAI_API_KEY.")

# 🤖 Inicializa o bot
app = Client("dri_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 📋 Prompt base da DRI
Dri_prompt = """
[Coloque aqui o prompt completo e formatado da DRI, com instruções, contexto, tom de voz etc.]
"""

# 🔐 /start → Solicita e-mail de cadastro
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("🔐 Olá! Envie o e-mail usado na compra para validar seu acesso:")

# 🤖 Validação e resposta do bot
@app.on_message(filters.private & ~filters.command(["start"]))
async def valida_email_ou_responde(client, message):
    user_id = message.from_user.id
    texto = message.text.strip()
    print(f"[Recebido] Texto: {texto} | ID: {user_id}")

    if id_autorizado(user_id):
        await message.reply_chat_action(ChatAction.TYPING)
        resposta = enviar_pro_gpt(texto)
        await message.reply_text(resposta)
    else:
        if usuario_autorizado(texto, user_id):
            await message.reply_text("✅ Acesso autorizado! Seja bem-vindo ao bot da DRI. 🤖")
        else:
            await message.reply_text(
                "🚫 Acesso negado.\nSeu e-mail está inativo, não está na lista ou já foi vinculado a outro Telegram.\nSe isso for um engano, entre em contato com o suporte."
            )

# 💬 Integração com OpenAI GPT
def enviar_pro_gpt(mensagem_usuario):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": Dri_prompt},
                {"role": "user", "content": mensagem_usuario}
            ]
        }

        resposta = requests.post(url, headers=headers, json=data)
        resposta.raise_for_status()
        retorno = resposta.json()
        return retorno['choices'][0]['message']['content']

    except Exception as e:
        print("❌ Erro ao chamar OpenAI:", e)
        return "⚠️ Tive um probleminha pra responder agora. Tente novamente em alguns segundos! 🤖"

# ▶️ Executa o bot
print("🤖 Bot DRI rodando e ouvindo os usuários...")
app.run()
