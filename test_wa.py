import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

opts = Options()
opts.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=opts)
driver.get("https://web.whatsapp.com")
print("WhatsApp Web aberto. Aguardando 60s...")
time.sleep(60)

# Tenta encontrar chats na lista principal
print("[*] Tentando encontrar chats...")
for sel in [
    '//div[@role="button"][@data-testid="chat-list-item"]',
    '//div[@data-testid="pinned-chat-list-item"]',
    '//div[contains(@class, "pinned-chat")]',
    '//div[contains(@class, "chat-list-item")]',
]:
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, sel)))
        chats = driver.find_elements(By.XPATH, sel)
        print(f"[*] {len(chats)} elementos no selector '{sel[:50]}...'")
        if chats:
            text = chats[0].text.strip()
            print(f"    Primeiro chat: '{text[:80]}'")
            break
    except Exception as e:
        print(f"[!] Erro com {sel[:40]}: {e}")

# Tenta encontrar todos os chats
print("[*] Listando todos os chats do WhatsApp...")
all_chats = []
for sel in [
    '//div[@role="button"]',
    '//div[@role="button"][@data-testid]',
]:
    try:
        all_chats.extend(driver.find_elements(By.XPATH, sel))
    except Exception:
        continue

for i, chat in enumerate(all_chats[:10]):
    txt = chat.text.strip()
    title = chat.get_attribute("title") or ""
    print(f"    {i+1}: [{chat.get_attribute('data-testid') or 'no data-testid'}] text='{txt[:60]}' title='{title[:40]}'")

driver.quit()
print("Teste concluído!")