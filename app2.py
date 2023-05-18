from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from functions.changeLanguage import changeLanguage

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(
    options=options,
    executable_path=r"C:\\Users\\DIPRAJ\\Programming\\adclick_bot\\chromedriver.exe",
)

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

url = "https://www.skyscanner.com/transport/flights/SKP/BCN/230619/"

driver.get(url)
time.sleep(5)
element = driver.find_element(By.ID, "acceptCookieButton")
element.click()
time.sleep(5)

changeLanguage(driver)

driver.quit()
