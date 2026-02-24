from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configuración para que funcione en Docker/Jenkins
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# En Linux/Docker usamos el binario de chromium
service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Iniciando DAST con Selenium...")
    driver.get("http://10.227.89.30:60010") # La URL de tu app en Docker Compose
    print(f"Título de la página: {driver.title}")
    
    # Aquí puedes añadir lógica para buscar 'vulnerabilidades'
    # Ejemplo: verificar si las cookies tienen el flag 'HttpOnly'
    cookies = driver.get_cookies()
    for cookie in cookies:
        if not cookie.get('httpOnly'):
            print(f"ADVERTENCIA DE SEGURIDAD: Cookie {cookie['name']} sin HttpOnly")

finally:
    driver.quit()