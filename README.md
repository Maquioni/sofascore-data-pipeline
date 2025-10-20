# Sofascore Data Pipeline (Scrapy)

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Scrapy](https://img.shields.io/badge/Scrapy-2.x-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Projeto autoral para **coleta e tratamento de dados de partidas de futebol** a partir do Sofascore, focando em **estatísticas de equipes e jogadores**. Construído com **Scrapy (Python)** e preparado para armazenamento em estruturas compatíveis com **engenharia de dados** (CSV/Parquet).

> **Objetivo:** demonstrar habilidades práticas em **coleta de dados**, **limpeza/organização** e **preparo para análise** — conectando com conhecimentos de **cloud (Microsoft Azure)**.

---

## 🔧 Tecnologias
- Python, Scrapy, Pandas
- (Opcional) Armazenamento em nuvem: Azure Blob Storage / Data Lake
- (Opcional) Orquestração: cron/CI

---

## 🗂️ Estrutura do repositório
```
.
├── README.md
├── requirements.txt
├── scrapy.cfg
├── .gitignore
├── LICENSE
├── data/
│   ├── raw/        # saídas brutas do scraper
│   └── processed/  # dados tratados/limpos
├── notebooks/
│   └── exploration.ipynb  # análise e exploração de dados
└── sofascore_pipeline/
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        ├── __init__.py
        └── sofascore_spider.py
```

---

## ▶️ Como rodar localmente
```bash
# 1) Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# 2) Instale as dependências
pip install -r requirements.txt

# 3) Execute o spider (salvando CSV em data/raw/)
scrapy crawl sofascore -O data/raw/matches.csv
```

> **Dica:** para utilizar parâmetros (por ex., liga/time), use `-a`:
```bash
scrapy crawl sofascore -O data/raw/matches_SERIEA_2025.csv -a league=SERIEA -a season=2025
```

---

## 🧹 Pós-processamento (Pandas)
Após a coleta, utilize o notebook `notebooks/exploration.ipynb` para limpeza e consolidação dos dados.
Exemplo (simplificado):
```python
import pandas as pd
df = pd.read_csv("data/raw/matches.csv")
# suas transformações...
df.to_csv("data/processed/matches_clean.csv", index=False)
```

---

## 📦 Publicação (opcional)
- **Azure Blob Storage / Data Lake**: enviar `data/processed/` para um container do Azure.
- **CI/CD (GitHub Actions)**: agendar execução do spider (respeite limites/ToS do site).

---

## ⚠️ Avisos importantes
- **Respeite os Termos de Uso** do Sofascore e a legislação local.
- Scraping deve ser **ético** e **responsável** (rate limit, cache, horários).

---

## 👤 Autor
**Gustavo Maquioni Fernandes Pinto** — São José dos Campos/SP  
📧 makionipa@gmail.com  
Certificação: **Microsoft Azure Fundamentals**

---

## 📄 Licença
Este projeto é licenciado sob a **MIT License**. Veja `LICENSE`.