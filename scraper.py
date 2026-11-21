import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from notifier import enviar_alerta_telegram

url = "https://realpython.github.io/fake-jobs/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

palavras_chave = ["python", "developer"]
arquivo_vistos = "vagas_vistas.csv"

resposta = requests.get(url, headers=headers)
soup = BeautifulSoup(resposta.text, "html.parser")

cards = soup.find_all("div", class_="card-content")
vagas_encontradas = []

for card in cards:
    titulo = card.find("h2", class_="title").get_text(strip=True)
    empresa = card.find("h3", class_="company").get_text(strip=True)
    local = card.find("p", class_="location").get_text(strip=True)

    links = card.find_all("a")
    link_vaga = links[1]["href"] if len(links) > 1 else ""

    texto_busca = f"{titulo} {empresa} {local}".lower()

    if any(palavra in texto_busca for palavra in palavras_chave):
        vagas_encontradas.append({
            "titulo": titulo,
            "empresa": empresa,
            "local": local,
            "link": link_vaga
        })

links_vistos = set()
if os.path.exists(arquivo_vistos):
    df_vistos = pd.read_csv(arquivo_vistos)
    if "link" in df_vistos.columns:
        links_vistos = set(df_vistos["link"].dropna().tolist())

novas_vagas = [vaga for vaga in vagas_encontradas if vaga["link"] not in links_vistos]

print(f"Total encontradas no filtro: {len(vagas_encontradas)}")
print(f"Novas vagas (ainda não vistas): {len(novas_vagas)}")

for vaga in novas_vagas[:5]:
    print(f"- [NOVA] {vaga['titulo']} | {vaga['empresa']} | {vaga['link']}")

if vagas_encontradas:
    df_todas = pd.DataFrame(vagas_encontradas).drop_duplicates(subset=["link"])
    if os.path.exists(arquivo_vistos):
        df_antigo = pd.read_csv(arquivo_vistos)
        df_atualizado = pd.concat([df_antigo, df_todas], ignore_index=True).drop_duplicates(subset=["link"])
    else:
        df_atualizado = df_todas

    df_atualizado.to_csv(arquivo_vistos, index=False, encoding="utf-8-sig")
    df_atualizado.to_csv("vagas_filtradas.csv", index=False, encoding="utf-8-sig")
    df_atualizado.to_excel("vagas_filtradas.xlsx", index=False)
    print("Planilhas e histórico de vagas atualizados com sucesso!")
else:
    print("Nenhuma vaga encontrada com essas palavras-chave.")

enviar_alerta_telegram(novas_vagas)