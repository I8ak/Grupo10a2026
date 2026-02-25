import os
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = os.getenv("http://10.227.87.30:60010")

def test_xss_login():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get(f"{BASE_URL}/login")

    username = driver.find_element(By.NAME, "username")
    username.send_keys("<script>alert(1)</script>")

    driver.find_element(By.NAME, "submit").click()

    assert "<script>" not in driver.page_source

    driver.quit()