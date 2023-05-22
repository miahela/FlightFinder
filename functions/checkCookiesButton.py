from selenium.webdriver.common.by import By

def checkCookiesButton(driver):
    cookiesBtn = driver.find_elements(By.XPATH, '//*[@id="cookieBannerContent"]/div/div[2]/button')
    otherPopup = driver.find_elements(By.XPATH, '//*[@id="price-alerts-modal"]/header/nav/button')
    if(len(cookiesBtn) > 0):
        cookiesBtn[0].click()

    if(len(otherPopup) > 0):
        otherPopup[0].click()