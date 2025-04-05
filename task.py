from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

driver = webdriver.Chrome()
driver.maximize_window()

# Авторизация
driver.get('https://e.mail.ru/login')
wait = WebDriverWait(driver, 20)

# Ввод логина
email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]')))
email_input.send_keys('ваш_логин@mail.ru')
driver.find_element(By.XPATH, '//button[contains(text(), "Ввести пароль")]').click()

# Переключение на iframe с паролем
wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe.ag-popup__frame__layout__iframe')))

# Ввод пароля
password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
password_input.send_keys('ваш_пароль')
driver.find_element(By.XPATH, '//button[contains(text(), "Войти")]').click()
driver.switch_to.default_content()

# Поиск письма
wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@title, "тест-отправитель")]')))
driver.find_element(By.XPATH, '//a[contains(@title, "тест-отправитель")]').click()

# Извлечение ссылки
mail_body = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-body'))).text
url_match = re.search(r'(https?://\S+)', mail_body)
if url_match:
    found_url = url_match.group(1)

    # Открытие новой вкладки
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(found_url)

    # Создание скриншота
    time.sleep(3)
    driver.save_screenshot('screenshot.png')

    # Возврат на mail.ru
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Выход
menu_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ph-avatar-img')))
menu_button.click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Выйти"]'))).click()

driver.quit()

