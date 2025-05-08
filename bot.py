from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from acesso import usuario_autorizado, id_autorizado
import requests
import os  # ✅ Novo: para pegar variáveis de ambiente com segurança

# 🔐 Suas credenciais seguras
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Inicializa o bot
app = Client("dri_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Prompt da DRI (mantido igual ao seu original)
Dri_prompt = """
[... 👇 aqui entra todo seu prompt completo, igual ao que você já escreveu ...]
"""

# 🔐 /start → Solicita e-mail
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text("🔐 Olá! Envie o e-mail usado na compra para validar seu acesso:")

# 📩 Valida e-mail, ID e status na planilha ou envia mensagem ao GPT
@app.on_message(filters.private & ~filters.command(["start"]))
async def valida_email_ou_responde(client, message):
    user_id = message.from_user.id
    texto = message.text.strip()
    print(f"[Recebido] E-mail: {texto} | ID: {user_id}")

    if usuario_autorizado(texto, user_id):
        await message.reply_text("✅ Acesso autorizado! Seja bem-vindo ao bot da DRI. 🤖")
        return

    if id_autorizado(user_id):
        await message.reply_chat_action(ChatAction.TYPING)
        resposta = enviar_pro_gpt(texto)
        await message.reply_text(resposta)
    else:
        await message.reply_text("🚫 Acesso negado.\nSeu e-mail está inativo, não está na lista ou já foi vinculado a outro Telegram.\nSe isso for um engano, entre em contato com o suporte.")

# 💬 Integração com ChatGPT usando o prompt completo
def enviar_pro_gpt(mensagem_usuario):
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

    if resposta.status_code == 200:
        retorno = resposta.json()
        mensagem = retorno['choices'][0]['message']['content']
        return mensagem
    else:
        print("❌ Erro na resposta do GPT:", resposta.text)
        return "⚠️ Tive um probleminha pra responder agora. Tente novamente em instantes, tá bom? 🤖"

# ▶️ Inicia o bot
print("🤖 Bot rodando e ouvindo os usuários...")
app.run()
