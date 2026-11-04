import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--disable-dev-shm-usage")
print("Criando driver Chrome...")
driver = webdriver.Chrome(options=opts)
print("Driver criado.")
driver.get("https://web.whatsapp.com")
print("Página aberta.")
time.sleep(5)
print("Verificando elementos...")
try:
    btn = driver.find_element("tag name", "button")
    print(f"Botão encontrado: {btn.is_displayed()}")
except Exception as e:
    print(f"Erro ao encontrar botão: {e}")
print("Tudo OK!")
driver.quit()