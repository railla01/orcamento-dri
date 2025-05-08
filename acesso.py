import os
import json
import gspread

def normalizar(valor):
    return str(valor).strip().lower()

def conectar_planilha():
    """Conecta à planilha do Google Sheets usando variável de ambiente com a credencial JSON."""
    try:
        google_creds = os.environ.get('GOOGLE_CREDS')
        if not google_creds:
            raise ValueError("Variável de ambiente 'GOOGLE_CREDS' não encontrada.")
        
        info = json.loads(google_creds)
        cliente = gspread.service_account_from_dict(info)
        planilha = cliente.open("Controle DRI")
        aba = planilha.worksheet("usuarios")
        return aba

    except Exception as e:
        print(f"[ERRO] Falha ao conectar com a planilha: {e}")
        raise

def usuario_autorizado(email, telegram_id):
    aba = conectar_planilha()
    dados = aba.get_all_records()

    for i, linha in enumerate(dados, start=2):
        email_planilha = normalizar(linha.get('email', ''))
        status = normalizar(linha.get('status', ''))
        id_salvo = str(linha.get('id_telegram', '')).strip()

        if email_planilha == normalizar(email):
            if status != "ativo":
                return False

            if not id_salvo:
                aba.update_cell(i, 2, str(telegram_id))
                return True
            elif id_salvo == str(telegram_id):
                return True
            else:
                return False

    return False

def id_autorizado(telegram_id):
    aba = conectar_planilha()
    dados = aba.get_all_records()

    for linha in dados:
        id_salvo = str(linha.get('id_telegram', '')).strip()
        status = normalizar(linha.get('status', ''))

        if id_salvo == str(telegram_id).strip():
            return status == "ativo"

    return False
