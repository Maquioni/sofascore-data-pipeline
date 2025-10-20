from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import time
from datetime import datetime
import pandas as pd
import os
from webdriver_manager.chrome import ChromeDriverManager
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

# Lista de times
teams = ["arsenal", "barcelona", "psg", "inter"]

# Configuração do ChromeDriver com webdriver-manager
options = Options()
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Diretório base para os arquivos CSV
base_dir = "C:\\Users\\makki\\Desktop\\Sofascore_project\\table_space"

# Função para limpar cabeçalhos duplicados em um arquivo CSV existente
def clean_duplicate_headers(filename):
    if not os.path.exists(filename):
        return False
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        if not lines:
            return False
        header = lines[0].strip()
        cleaned_lines = [lines[0]]
        header_count = 0
        for line in lines:
            if line.strip() == header:
                header_count += 1
                if header_count > 1:
                    continue
            cleaned_lines.append(line)
        if header_count > 1:
            with open(filename, 'w', encoding='utf-8-sig') as f:
                f.writelines(cleaned_lines)
            print(f"Cabeçalhos duplicados removidos de {filename}")
            return True
        return False
    except Exception as e:
        print(f"Erro ao limpar cabeçalhos duplicados em {filename}: {e}")
        return False

# Função para criar ou atualizar arquivo CSV para um time
def create_new_team_csv(team, team_df, base_dir):
    filename = os.path.join(base_dir, f"raw_sofascore_{team}.csv")
    current_date = datetime.now().strftime("%Y%m%d")

    file_exists = os.path.exists(filename)
    if file_exists:
        clean_duplicate_headers(filename)

    if file_exists:
        try:
            existing_df = pd.read_csv(filename, encoding='utf-8-sig')
            if not existing_df[existing_df["production_date"] == current_date].empty:
                print(f"Dados para {team} na data {current_date} já existem. Pulando salvamento.")
                return False
        except Exception as e:
            print(f"Erro ao verificar duplicatas em {filename}: {e}")

    try:
        team_df.to_csv(
            filename,
            mode='a',
            header=not file_exists,
            index=False,
            encoding='utf-8-sig'
        )
        print(f"Dados salvos para {team} em {filename}")
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo {filename}: {e}")
        return False

# Função para sincronizar com o GitHub
def sync_with_github(base_dir):
    try:
        repo = Repo(base_dir)
        print("Repositório Git carregado.")

        expected_url = "https://github.com/makioni/Sofascore-data.git"
        remote_url = repo.remotes.origin.url
        if remote_url != expected_url and not remote_url.endswith("makioni/Sofascore-data.git"):
            print(f"Erro: URL do remoto 'origin' ({remote_url}) não corresponde ao esperado ({expected_url}).")
            print("Corrija com: git remote set-url origin https://github.com/makioni/Sofascore-data.git")
            return

        repo.git.add("*.csv")
        print("Arquivos CSV adicionados ao controle de versão.")

        if repo.is_dirty(untracked_files=True):
            commit_message = f"Atualização dos dados SofaScore - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            repo.git.commit(m=commit_message)
            print(f"Commit realizado: {commit_message}")

            try:
                repo.git.pull('--rebase', 'origin', 'main')
                print("Git pull --rebase executado com sucesso.")
            except GitCommandError as e:
                print(f"Erro ao executar git pull --rebase: {e}")
                print("Possível conflito. Tente resolver manualmente no PowerShell:")
                print(f"  cd {base_dir}")
                print("  git pull --rebase origin main")
                print("Resolva conflitos, adicione arquivos com 'git add', e continue com 'git rebase --continue'.")

            try:
                repo.git.push("origin", "main")
                print("Arquivos sincronizados com o GitHub.")
            except GitCommandError as e:
                print(f"Erro ao executar git push: {e}")
                print("Possíveis causas: conflitos, autenticação inválida, ou proteção de branch.")
                print("Tente manualmente no PowerShell:")
                print(f"  cd {base_dir}")
                print("  git pull --rebase origin main")
                print("  git push origin main")
                print("Se o erro for de autenticação, use um PAT (token de acesso pessoal) do GitHub.")
        else:
            print("Nenhuma alteração detectada para commitar.")
    except InvalidGitRepositoryError:
        print(f"Erro: O diretório {base_dir} não é um repositório Git válido.")
        print("Inicialize-o no PowerShell:")
        print(f"  cd {base_dir}")
        print("  git init")
        print("  git remote add origin https://github.com/makioni/Sofascore-data.git")
        print("  git add .")
        print("  git commit -m 'Initial commit'")
        print("  git push -u origin main")
    except Exception as e:
        print(f"Erro ao sincronizar com o GitHub: {e}")

# Loop time
for team in teams:
    print(f"Coletando dados para o time: {team}")
    
    driver.get("https://www.sofascore.com/pt/")
    time.sleep(3)

    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".Button.pBEmc"))
        )
        close_button.click()
        print(f"Pop-up fechado para o time: {team}")
        time.sleep(1)
    except:
        print(f"Nenhum pop-up detectado para o time: {team}")

    try:
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-input"))
        )
        search_input.clear()
        search_input.send_keys(team)
        time.sleep(3)

        elementos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Box.Flex.eUsdna.jLRkRA"))
        )
        if elementos:
            elementos[0].click()
            time.sleep(5)
        else:
            print(f"Time {team} não encontrado.")
            continue
    except Exception as e:
        print(f"Erro ao pesquisar o time {team}: {e}")
        continue

    html_da_pagina = driver.page_source
    valor = html.fromstring(html_da_pagina)

    data = {
        "production_date": datetime.now().strftime("%Y%m%d"),
        "Time": team
    }

    span_fj = valor.xpath('//span[text()="Total de finalizações por jogo"]')
    data["Finalizações por jogo"] = (
        span_fj[0].getnext().text if span_fj and span_fj[0].getnext() is not None else "N/A"
    )

    span_escanteio = valor.xpath('//span[text()="Escanteios por partida"]')
    data["Escanteios por partida"] = (
        span_escanteio[0].getnext().text if span_escanteio and span_escanteio[0].getnext() is not None else "N/A"
    )

    span_amarelo = valor.xpath('//span[text()="Cartões amarelos por partida"]')
    data["Cartões amarelos por partida"] = (
        span_amarelo[0].getnext().text if span_amarelo and span_amarelo[0].getnext() is not None else "N/A"
    )

    team_df = pd.DataFrame([data])
    create_new_team_csv(team, team_df, base_dir)

sync_with_github(base_dir)
driver.quit()