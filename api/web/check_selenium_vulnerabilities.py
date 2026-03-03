from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configuración simplificada para la imagen de Selenium Standalone
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-gpu')

# NO pongas service ni binary_location. 
# La imagen ya sabe dónde están.

try:
    print("Iniciando DAST con Selenium...")
    driver = webdriver.Chrome(options=options)
    
    # IMPORTANTE: Asegúrate de usar la IP correcta que detectamos en el Jenkinsfile
    # Si usas APP_URL como variable de entorno, úsala aquí:
    import os
    app_url = os.getenv('APP_URL', 'http://172.17.0.1:5000')
    
    driver.get(app_url)
    print(f"Título de la página: {driver.title}")
    
    # Tu lógica de seguridad...
    cookies = driver.get_cookies()
    for cookie in cookies:
        if not cookie.get('httpOnly'):
            print(f"ADVERTENCIA DE SEGURIDAD: Cookie {cookie['name']} sin HttpOnly")

finally:
    if 'driver' in locals():
        driver.quit()