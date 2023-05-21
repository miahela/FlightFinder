from selenium.webdriver.common.by import By
import time


def selectStartAndDestinationCountry(driver, startCountry, destinationCountry):
    driver.find_element(By.ID, "oc-ui-wrapper-flights-search-summary").click()
    time.sleep(0.2)
    driver.find_element(By.ID, "fsc-origin-search").send_keys(startCountry)
    time.sleep(0.2)
    driver.find_element(By.ID, "fsc-destination-search").send_keys(destinationCountry)
    time.sleep(0.2)
    driver.find_element(By.CSS_SELECTOR, "button[aria-label='Search flights']").click()
    time.sleep(0.2)
