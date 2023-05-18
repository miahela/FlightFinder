import time
from selenium.webdriver.common.by import By


def changeLanguage(driver):
    driver.find_element(By.XPATH, '//*[@id="culture-info"]/button').click()
    time.sleep(1)
    driver.find_element(By.ID, "culture-selector-switch-to-english").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button[title='Close']").click()
