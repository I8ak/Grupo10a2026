import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    print("Iniciando DAST con Selenium...")
    driver = webdriver.Chrome(options=options)
    
    # IMPORTANTE: 
    # 1. Usamos la IP que Jenkins nos pasa (el Gateway)
    # 2. Usamos el puerto 60010 porque el Gateway redirige al host
    app_url = os.getenv('APP_URL', 'http://172.17.0.1:60010')
    
    # REINTENTOS: Por si el contenedor 'pythona10' está reiniciando
    for i in range(10):
        try:
            print(f"Intento {i+1}: Conectando a {app_url}...")
            driver.get(app_url)
            if "Iniciado" in driver.title or driver.title != "": # Verifica que cargó algo
                break
        except Exception as e:
            print(f"Esperando a la aplicación... {e}")
            time.sleep(5)
    
    print(f"Título de la página: {driver.title}")
    
    # Tu lógica de cookies...
    cookies = driver.get_cookies()
    for cookie in cookies:
        if not cookie.get('httpOnly'):
            print(f"ADVERTENCIA DE SEGURIDAD: Cookie {cookie['name']} sin HttpOnly")

finally:
    if 'driver' in locals():
        driver.quit()