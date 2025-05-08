import gspread
from oauth2client.service_account import ServiceAccountCredentials

def conectar_planilha():
    """Conecta à planilha do Google Sheets e retorna a aba 'usuarios'."""
    escopos = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credenciais = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', escopos)
    cliente = gspread.authorize(credenciais)
    planilha = cliente.open("Controle DRI")  # Nome exato da planilha
    aba = planilha.worksheet("usuarios")     # Nome exato da aba
    return aba

def usuario_autorizado(email, telegram_id):
    """
    Verifica se o e-mail está autorizado e, se o ID for novo, registra.
    """
    aba = conectar_planilha()
    dados = aba.get_all_records()

    for i, linha in enumerate(dados, start=2):  # Linha 2 = primeira linha de dados (após cabeçalho)
        email_planilha = linha.get('email', '').strip().lower()
        status = linha.get('status', '').strip().lower()
        id_salvo = str(linha.get('id_telegram', '')).strip()

        if email_planilha == email.strip().lower():
            if status != "ativo":
                return False  # E-mail está inativo

            if id_salvo == "":
                # Primeiro acesso: registra o ID
                aba.update_cell(i, 2, str(telegram_id))  # Coluna B = id_telegram
                return True
            elif id_salvo == str(telegram_id):
                return True  # ID já está registrado corretamente
            else:
                return False  # E-mail já vinculado a outro Telegram

    return False  # E-mail não encontrado

def id_autorizado(telegram_id):
    """
    Verifica se o ID do Telegram já está na planilha e está com status 'ativo'.
    """
    aba = conectar_planilha()
    dados = aba.get_all_records()

    for linha in dados:
        id_salvo = str(linha.get('id_telegram', '')).strip()
        status = linha.get('status', '').strip().lower()

        if id_salvo == str(telegram_id).strip():
            return status == "ativo"

    return False
