import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

def run_login_tests():
    driver = webdriver.Chrome(options=options)
    app_url = os.getenv('APP_URL', 'http://172.17.0.1:60010')
    
    try:
        print(f"--- Iniciando pruebas de Login en {app_url} ---")
        driver.get(app_url)
        time.sleep(2) # Esperar a que cargue el DOM

        # PRUEBA 1: Login Fallido
        print("Test 1: Verificando mensaje de error en login fallido...")
        driver.find_element(By.ID, "username").send_keys("usuario_falso")
        driver.find_element(By.ID, "password").send_keys("clave_falsa")
        driver.find_element(By.XPATH, "//button[contains(text(),'ENVIAR')]").click()
        time.sleep(5)
        
        
        error_msg = driver.find_element(By.CLASS_NAME, "error")
        if error_msg.is_displayed():
            print("Resultado: ÉXITO (El mensaje de error apareció correctamente)")
        else:
            print("Resultado: FALLO (El mensaje de error no es visible)")
            driver.save_screenshot('error.png')

        # PRUEBA 2: Intento de SQL Injection (Seguridad)
        print("\nTest 2: Probando bypass de login con SQL Injection...")
        driver.refresh()
        # Intentamos entrar como 'admin' sin saber la clave usando ' OR '1'='1
        driver.find_element(By.ID, "username").send_keys("' OR '1'='1")
        driver.find_element(By.ID, "password").send_keys("' OR '1'='1")
        driver.find_element(By.XPATH, "//button[contains(text(),'ENVIAR')]").click()
        time.sleep(2)

        if "perfumes.html" in driver.current_url:
            print("ALERTA CRÍTICA: Bypass de login exitoso. La aplicación es vulnerable a SQL Injection.")
        else:
            print("Resultado: ÉXITO (La aplicación resistió el bypass simple)")

    except Exception as e:
        print(f"Error durante las pruebas: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_login_tests()