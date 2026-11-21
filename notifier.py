import os
import requests
from dotenv import load_dotenv

load_dotenv()


def enviar_alerta_telegram(novas_vagas):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Aviso: TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não configurados no .env.")
        return

    if not novas_vagas:
        print("Nenhuma vaga nova para enviar no Telegram.")
        return

    linhas = [f"*{len(novas_vagas)} nova(s) vaga(s) encontrada(s):*\n"]
    for vaga in novas_vagas[:10]:
        linhas.append(
            f"• *{vaga['titulo']}*\n"
            f"  Empresa: {vaga['empresa']} | Local: {vaga['local']}\n"
            f"  [Ver vaga]({vaga['link']})\n"
        )

    mensagem = "\n".join(linhas)
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    resposta = requests.post(url, json=payload, timeout=15)
    if resposta.status_code == 200:
        print("Alerta enviado no Telegram com sucesso!")
    else:
        print(f"Falha ao enviar no Telegram: {resposta.status_code} - {resposta.text}")