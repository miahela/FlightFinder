from classes.SaveFlightToExcel import SaveFlightToExcel
from classes.CompletedLines import CompletedLines
from classes.CaptchaSolver import CaptchaSolver
from classes.URLMonitor import URLMonitor
from classes.AllLines import AllLines
from classes.Flight import Flight
from functions.checkCookiesButton import checkCookiesButton
from functions.get_random_number import get_random_number
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta
import undetected_chromedriver as uc
import logging
import time

logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d in %(funcName)s",
)


destination_codes = [
    "LCG",
    "MAD",
    "VLC",
    "REU",
    "ZAZ",
    "LEN",
    "BCN",
    "LEU",
    "VIT",
    "BIO",
    "RJL",
    "PNA",
    "EAS",
    "BIQ",
    "BOD",
]
origin_codes = ["SKP", "SOF", "SKG", "ATH", "BEG"]

allLinesObj = AllLines(destination_codes, origin_codes, "2023-06-29", "2023-07-02")

completedLinesObj = CompletedLines()
driver = uc.Chrome()
captchaSolver = CaptchaSolver(driver)
saveFlightToExcelObj = SaveFlightToExcel("return.xlsx")

url_monitor = URLMonitor(driver, captchaSolver.solve_blocked)
url_monitor.set_target_url("https://www.skyscanner.com/sttc/px/captcha-v2")
url_monitor.start()


for line in allLinesObj.get_all_lines():
    if completedLinesObj.check_if_duplicate_line(line):
        continue

    try:
        driver.get(line.link)
        print(
            "Started line "
            + line.departure
            + " - "
            + line.arrival
            + " on date "
            + line.departure_date,
            end=" ",
        )

        time.sleep(get_random_number(1, 3))

        result_elem = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/span',
                )
            )
        )
        result = result_elem.text
        if result != None and result[0] == "0":
            print("- No flights found")
            completedLinesObj.add_completed_line(line)
            continue

        cheapestBtn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button',
                )
            )
        )
        checkCookiesButton(driver)
        cheapestBtn.click()

        departure_time_elem = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/div/a/div/div[1]/div/div[1]/div[3]/div/div[2]/div[1]/span[1]/div/span',
                )
            )
        )
        departure_time = datetime.strptime(departure_time_elem.text, "%H:%M").time()

        price = driver.find_element(
            By.XPATH,
            '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button/div/div/div/span',
        )

        duration = driver.find_element(
            By.XPATH,
            '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button/p[2]',
        )

        arrival_time_elem = driver.find_element(
            By.XPATH,
            '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/div/a/div/div[1]/div/div[1]/div[3]/div/div[2]/div[3]/span[1]/div/span',
        )
        arrival_time = datetime.strptime(arrival_time_elem.text, "%H:%M").time()

        isArrivalNextDayElements = driver.find_elements(
            By.XPATH,
            '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/div/a/div/div[1]/div/div[1]/div[3]/div/div[2]/div[3]/span[1]/div/div/span',
        )

        isArrivalNextDay = False

        if len(isArrivalNextDayElements) > 0:
            isArrivalNextDay = True

        linkToFlight = driver.find_element(
            By.XPATH,
            '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/div/a',
        ).get_attribute("href")

        if isArrivalNextDay:
            arrival_date = datetime.combine(
                datetime.strptime(line.departure_date, "%y%m%d"), arrival_time
            ) + timedelta(days=1)
        else:
            arrival_date = datetime.combine(
                datetime.strptime(line.departure_date, "%y%m%d"), arrival_time
            )

        flight = Flight(
            departure=line.departure,
            arrival=line.arrival,
            departure_date=datetime.combine(
                datetime.strptime(line.departure_date, "%y%m%d"), departure_time
            ),
            arrival_date=datetime.combine(arrival_date, arrival_time),
            travel_time=duration.text,
            price=price.text,
            link=linkToFlight,
        )

        completedLinesObj.add_completed_line(line)
        saveFlightToExcelObj.save(flight)

        print("- Saved data to excel file")
    except Exception as e:
        logging.error(e)

    finally:
        url_monitor.stop()
        url_monitor.join()


time.sleep(10)
driver.quit()
