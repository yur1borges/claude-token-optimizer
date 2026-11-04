"""
WhatsApp agent that monitors GROUP called "Eu" for Instagram link/video messages,
extracts skills/plugins/mcp/modes, and installs missing ones in Claude on the local PC.
"""
import time
import json
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException, TimeoutException

WHATSAPP_GROUP_NAME = "Eu"
INSTALLED_SKILLS_DIR = Path.home() / ".claude" / "skills"
MCP_CONFIG_PATH = Path.home() / ".config" / "mcp" / "config.json"

def extract_items_from_url(url):
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            page = p.chromium.new_page()
            page.goto(url, wait_until="networkidle", timeout=15000)
            text = page.inner_text("body")
            page.close()
        items = re.findall(r'[\w-]+ (skill|plugin|mcp)', text, re.IGNORECASE)
        results = [s.strip().lower() for s in items]
        return list(dict.fromkeys(results))
    except Exception as e:
        print(f"[!] Erro ao extrair de {url}: {e}")
        return []

def check_installed():
    installed = []
    if INSTALLED_SKILLS_DIR.exists():
        for f in INSTALLED_SKILLS_DIR.iterdir():
            if f.suffix == ".md" or f.name.endswith(".skill") or f.name.endswith(".txt"):
                installed.append(f.stem.lower())
    if MCP_CONFIG_PATH.exists():
        try:
            cfg = json.loads(MCP_CONFIG_PATH.read_text())
            for server in cfg.get("servers", []):
                if isinstance(server, dict):
                    name = list(server.keys())[0] if server else None
                    if name:
                        installed.append(name.lower())
                elif isinstance(server, str):
                    installed.append(server.lower())
        except Exception:
            pass
    return installed

def install_skill(item):
    print(f"[+] Instalando skill: {item}...")
    skill_dir = INSTALLED_SKILLS_DIR / item
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(f"# {item}\n\nInstalado automaticamente.\n", encoding="utf-8")
    print(f"[OK] Skill {item} instalada em {skill_dir}")

def install_mcp(item):
    print(f"[+] Instalando MCP: {item}...")
    mcp_dir = MCP_CONFIG_PATH / "servers"
    mcp_dir.mkdir(parents=True, exist_ok=True)
    existing = json.loads(MCP_CONFIG_PATH.read_text() if MCP_CONFIG_PATH.exists() else '{}')
    existing.setdefault("servers", {})[item] = {"command": f"npx", "args": [f"-y {item}"], "env": {}}
    (MCP_CONFIG_PATH / f".{item}.json").write_text(json.dumps(existing["servers"][item], indent=2), encoding="utf-8")
    print(f"[OK] MCP {item} instalado")

def find_and_select_group(driver, group_name, max_attempts=30):
    """Busca e seleciona o grupo 'group_name', rolando se necessário. Retorna True se achado."""
    # Seletores de chats fixados primeiro, depois regulares
    sel_pinned = [
        '//div[@role="button"][@data-testid="pinned-chat-list-item"]',
        '//div[@data-testid="pinned-chat-list-item"]',
        '//div[contains(@class, "pinned-chat")]//div[@role="button"]',
        '//div[contains(@class, "pinned-chat")]',
        '//div[@aria-label="Pinned"]//div[@role="button"]',
        '//div[@id="pane-side"]//div[contains(@class, "pinned-chat")]',
    ]
    sel_normal = [
        '//div[@role="button"][@data-testid="chat-list-item"]',
        '//div[contains(@class, "chat-list-item")]',
        '//div[@id="pane-side"]//div[@role="button"]',
    ]

    for attempt in range(max_attempts):
        try:
            # Tenta chats fixados
            found = False
            for sel in sel_pinned:
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_all_elements_located((By.XPATH, sel))
                    )
                    chats = driver.find_elements(By.XPATH, sel)
                    for chat in chats:
                        txt = chat.text.strip()
                        title = chat.get_attribute("title") or ""
                        if group_name in txt or group_name in title:
                            driver.execute_script("arguments[0].scrollIntoView(true);", chat)
                            time.sleep(0.5)
                            chat.click()
                            found = True
                            break
                    if found:
                        break
                except (InvalidSessionIdException, TimeoutException):
                    continue

            if not found:
                # Tenta chats regulares
                for sel in sel_normal:
                    try:
                        chats = driver.find_elements(By.XPATH, sel)
                        for chat in chats:
                            txt = chat.text.strip()
                            title = chat.get_attribute("title") or ""
                            if group_name in txt or group_name in title:
                                driver.execute_script("arguments[0].scrollIntoView(true);", chat)
                                time.sleep(0.5)
                                chat.click()
                                found = True
                                break
                        if found:
                            break
                    except (InvalidSessionIdException, TimeoutException):
                        continue

            if found:
                print(f"[*] Grupo '{group_name}' selecionado (tentativa {attempt+1}/{max_attempts})")
                return True

            # Rola para ver mais chats
            driver.execute_script("window.scrollBy(0, 600);")
            time.sleep(1)

        except (InvalidSessionIdException, TimeoutException, Exception) as e:
            print(f"[!] Tentativa {attempt+1} falhou: {e}")
            # Recarrega a página
            try:
                driver.get("https://web.whatsapp.com")
                time.sleep(30)  # Aguarda novo QR scan
            except Exception:
                pass
            # Sessão perdeu, recomeça do zero
            print(f"[*] Reconectando driver (tentativa {attempt+1})...")
            return False

    print(f"[!] Grupo '{group_name}' não encontrado após {max_attempts} tentativas.")
    return False

def send_report_to_chat(installed, new_items):
    try:
        for chat in driver.find_elements(By.XPATH, '//div[@role="button"][@data-testid="chat-list-item"]'):
            if WHATSAPP_GROUP_NAME in chat.text:
                chat.click()
                break
        time.sleep(1)
        msg_box = driver.find_element(By.XPATH, '//div[@contenteditable[@data-tab="chat"]]')
        msg = f"🤖 *Habilidades detectadas:* {', '.join(new_items)}\n📦 *Já instaladas:* {', '.join(installed)}"
        msg_box.send_keys(msg)
        msg_box.send_keys(Keys.ENTER)
        print("[*] Relatório enviado para grupo 'Eu'")
    except Exception as e:
        print(f"[!] Erro ao enviar relatório: {e}")

def monitor_messages():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=opts)
    driver.get("https://web.whatsapp.com")

    # Aguarda pelo menos 90s para QR scan e carregamento
    print("[*] Aguardando 90 segundos para scan do QR code e carregamento...")
    for i in range(18):  # 90 segundos / 5 = 18 iterações
        time.sleep(5)
        # Verifica se há algum botão/elemento na página
        try:
            btn = driver.find_element(By.TAG_NAME, "button")
            if btn.is_displayed():
                print("[*] Página carregada, voltando para a lista principal...")
                driver.back()
                time.sleep(3)
                break
        except Exception:
            pass

    # Busca e seleciona o grupo com retry
    while not find_and_select_group(driver, WHATSAPP_GROUP_NAME):
        time.sleep(5)

    print(f"[*] Monitorando grupo '{WHATSAPP_GROUP_NAME}'...")

    try:
        while True:
            # Tenta encontrar mensagens
            msgs = None
            for xpath in [
                '//div[@role="main"]//div[contains(@class, "_1pd6u")]',
                '//div[@data-testid="conversation-panel-messages"]//div[contains(@class, "message")]',
                '//div[contains(@class, "message-in")]',
                '//div[contains(@class, "message-out")]',
            ]:
                try:
                    msgs = driver.find_elements(By.XPATH, xpath)
                    if msgs:
                        break
                except Exception:
                    continue

            if msgs:
                latest = msgs[-1].text
                print(f"[*] Nova mensagem: {latest[:80]}...")
                urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', latest)
                if urls:
                    print(f"[*] URLs detectadas: {urls}")
                    for url in urls:
                        if url.startswith("www."):
                            url = "https://" + url
                        print(f"[*] Processando URL: {url}")
                        items = extract_items_from_url(url)
                        print(f"[*] Itens extraídos: {items}")
                        if items:
                            installed = check_installed()
                            to_install = [i for i in items if i not in installed]
                            for item in to_install:
                                if "skill" in item or item.replace("-", "").replace("_", "").isalnum():
                                    install_skill(item)
                                else:
                                    install_mcp(item)
                            send_report_to_chat(installed, to_install)
                        else:
                            print(f"[*] Nenhuma skill/plugin/mcp encontrada em: {url}")
                else:
                    print("[*] Sem URLs na mensagem")
            else:
                print("[*] Nenhuma mensagem encontrada")

            # Verifica se sessão foi perdida
            try:
                driver.execute_script("return document.title;")
            except (InvalidSessionIdException, Exception):
                print("[!] Sessão perdida. Reiniciando monitoramento...")
                driver.quit()
                while not find_and_select_group(driver, WHATSAPP_GROUP_NAME):
                    time.sleep(5)
                print("[*] Monitorando grupo 'Eu' novamente...")
                continue

            time.sleep(5)

    finally:
        driver.quit()

if __name__ == "__main__":
    monitor_messages()