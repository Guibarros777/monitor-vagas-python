# Monitor de Vagas com Python

Automação em Python para coleta de vagas, filtragem por palavras-chave, controle de duplicidade, exportação de dados e envio de alertas automáticos via Telegram Bot API.

## Funcionalidades
- Coleta de vagas com `requests` e `BeautifulSoup`
- Filtragem por palavras-chave configuráveis (`python`, `developer`, etc.)
- Controle de histórico (`vagas_vistas.csv`) para evitar notificações repetidas
- Exportação dos resultados para `.csv` e `.xlsx` com `pandas` e `openpyxl`
- Notificação automática no Telegram usando variáveis de ambiente (`.env`)

## Tecnologias utilizadas
- Python
- Requests & BeautifulSoup4
- Pandas & OpenPyXL
- Python-dotenv
- Telegram Bot API

## Como executar localmente
1. Clone o repositório e entre na pasta do projeto:
   ```bash
   git clone [https://github.com/Guibarros777/monitor-vagas-python.git](https://github.com/Guibarros777/monitor-vagas-python.git)
   cd monitor-vagas-python