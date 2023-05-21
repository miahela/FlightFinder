from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def solveCaptcha(driver, element):
    print("Solving captcha...")
    actions = ActionChains(driver)
    actions.click_and_hold(element)
    actions.perform()

    # Get the current URL
    current_url = driver.current_url

    # Wait until the URL changes
    WebDriverWait(driver, timeout=60).until(EC.url_changes(current_url))

    # Release the click and hold action
    actions.release(element)
    actions.perform()
