import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Habilitamos el log del navegador
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

def run_login_tests():
    driver = webdriver.Chrome(options=options)
    app_url = os.getenv('APP_URL', 'http://172.17.0.1:60010')
    
    # Creamos un archivo para guardar los logs
    with open("selenium_debug.log", "w") as log_file:
        try:
            log_file.write(f"Iniciando pruebas en {app_url}\n")
            driver.get(app_url)
            time.sleep(3)

            # TEST 1
            log_file.write("Ejecutando Test 1: Login Fallido\n")
            driver.find_element(By.ID, "username").send_keys("usuario_falso")
            driver.find_element(By.ID, "password").send_keys("clave_falsa")
            driver.find_element(By.XPATH, "//button[contains(text(),'ENVIAR')]").click()
            time.sleep(5)
            
            error_msg = driver.find_element(By.CLASS_NAME, "error")
            if error_msg.is_displayed():
                log_file.write("Resultado: ÉXITO (Mensaje visible)\n")
            else:
                log_file.write("Resultado: FALLO (Mensaje NO visible)\n")
                driver.save_screenshot('error.png') # Sacamos la foto si falla
            
            # Capturamos errores de la consola de Chrome (JavaScript)
            log_file.write("\n--- LOGS DEL NAVEGADOR (CONSOLA) ---\n")
            for entry in driver.get_log('browser'):
                log_file.write(f"{entry}\n")

        except Exception as e:
            log_file.write(f"\nERROR TÉCNICO: {str(e)}\n")
            driver.save_screenshot('error.png')
        finally:
            driver.quit()

if __name__ == "__main__":
    run_login_tests()