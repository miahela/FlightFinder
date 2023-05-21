from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
import random
from functions.selectStartAndDestinationCountry import selectStartAndDestinationCountry
from functions.startSkyscanner import startSkyscanner
import threading
from functions.solveCaptcha import solveCaptcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from functions.solve_blocked import solve_blocked

import undetected_chromedriver as uc


class URLMonitor(threading.Thread):
    def __init__(self, driver):
        threading.Thread.__init__(self)
        self.driver = driver
        self.current_url = driver.current_url

    def run(self):
        while True:
            if self.current_url != self.driver.current_url:
                print("Redirected to", self.driver.current_url)
                self.current_url = self.driver.current_url
            time.sleep(1)  # Check every second


# from functions.changeLanguage import changeLanguage
from functions.data_manipulations import get_urls, save_array_to_excel


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

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

cookies = [
    # {
    #     "name": "scanner",
    #     "value": "currency:::USD&legs:::SKP|2023-06-21|LEN|||&tripType:::one-way&rtn&preferDirects:::false&outboundAlts&inboundAlts&from:::SKP&to:::LEN&adults:::1&children:::0&infants:::0&adultsV2:::1&cabinclass:::Economy&childrenV2&oym:::2306&oday:::21&wy:::0&iym:::2306&iday:::27",
    # },
    # {
    #     "name": "pxcts",
    #     "value": "cbbbbd8e-f570-11ed-a388-644b53695464",
    # },
    # {
    #     "name": "_pxvid",
    #     "value": "ca1fd86b-f570-11ed-8825-734e66714c4d",
    # },
    # {
    #     "name": "QSI_S_ZN_8fcHUNchqVNRM4S",
    #     "value": "v:0:0",
    # },
    # {
    #     "name": "_pxhd",
    #     "value": "YtQwgaNwazDOTU0QzVM2IOo2e/ogdq-0XlAn0dVHOh5SXokIeYXFelb1b6m-aML/pg2VK0MefE008yQqFtGang==:kgrK/SJtqiRgRbIVzJcikU4y4NtcqvwxIqNWlC6hjAy1HUlzboXoo9u6F7MoDPQUVnHVfdkJqTE/eXSIPwkonbNPyZwikeTs6E2TRT6mz1o=",
    # },
    # {
    #     "name": "ssab",
    #     "value": "BD_HotelDetail_RoomGrouping_standard_exploring_V1:::b&BD_map_enable_auto_refresh_default_V3:::a&Display_other_offer_if_use_discount_filter_desktop_V6:::a&Multi_city_search_Nav_Card_on_Desktop_V3:::a&WE_culture_selector_release_V4:::a&baggage_plugin_30k_splitting_V3:::a&fps_enable_agora_web_V12:::a&fps_mr_fqs_flights_ranking_haumea_v3_gpu__25i_desktop_V2:::a&fps_ttlr_early_timeout_banana_V83:::a&fps_ttlr_early_timeout_web_V21:::a&global_inline_test_v2_V3:::e&mat_hotwire_with_bumblebee_endpoint_V5:::a&rts_who_precompute_V4:::a&travel_api_ff_mirror_ap_northeast_1_V28:::a&travel_api_ff_mirror_ap_southeast_1_V27:::a&travel_api_ff_mirror_eu_central_1_V28:::a&travel_api_ff_mirror_sa_east_1_V28:::a&travel_api_ff_mirror_us_east_1_V28:::a&travel_api_ff_mirror_us_west_2_V28:::a&travel_api_ff_mirror_us_west_2_V29:::a",
    # },
    # {
    #     "name": "ssac",
    #     "value": "BD_HotelDetail_RoomGrouping_standard_exploring_V1:::b&BD_map_enable_auto_refresh_default_V3:::a&Display_other_offer_if_use_discount_filter_desktop_V6:::a&Multi_city_search_Nav_Card_on_Desktop_V3:::a&WE_culture_selector_release_V4:::a&baggage_plugin_30k_splitting_V3:::a&fps_enable_agora_web_V12:::a&fps_mr_fqs_flights_ranking_haumea_v3_gpu__25i_desktop_V2:::a&fps_ttlr_early_timeout_banana_V83:::a&fps_ttlr_early_timeout_web_V21:::a&global_inline_test_v2_V3:::e&mat_hotwire_with_bumblebee_endpoint_V5:::a&rts_who_precompute_V4:::a&travel_api_ff_mirror_ap_northeast_1_V28:::a&travel_api_ff_mirror_ap_southeast_1_V27:::a&travel_api_ff_mirror_eu_central_1_V28:::a&travel_api_ff_mirror_sa_east_1_V28:::a&travel_api_ff_mirror_us_east_1_V28:::a&travel_api_ff_mirror_us_west_2_V28:::a&travel_api_ff_mirror_us_west_2_V29:::a",
    # },
    # {
    #     "name": "ssad",
    #     "value": "BD_HotelDetail_RoomGrouping_standard_exploring_V1:::b&BD_map_enable_auto_refresh_default_V3:::a&Display_other_offer_if_use_discount_filter_desktop_V6:::a&Multi_city_search_Nav_Card_on_Desktop_V3:::a&WE_culture_selector_release_V4:::a&baggage_plugin_30k_splitting_V3:::a&fps_enable_agora_web_V12:::a&fps_mr_fqs_flights_ranking_haumea_v3_gpu__25i_desktop_V2:::a&fps_ttlr_early_timeout_banana_V83:::a&fps_ttlr_early_timeout_web_V21:::a&global_inline_test_v2_V3:::e&mat_hotwire_with_bumblebee_endpoint_V5:::a&rts_who_precompute_V4:::a&travel_api_ff_mirror_ap_northeast_1_V28:::a&travel_api_ff_mirror_ap_southeast_1_V27:::a&travel_api_ff_mirror_eu_central_1_V28:::a&travel_api_ff_mirror_sa_east_1_V28:::a&travel_api_ff_mirror_us_east_1_V28:::a&travel_api_ff_mirror_us_west_2_V28:::a&travel_api_ff_mirror_us_west_2_V29:::a",
    # },
]


options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = uc.Chrome()

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

monitor = URLMonitor(driver)
monitor.start()

data = []


def get_random_number(minimum, maximum):
    return random.randint(minimum, maximum)


counter = 0
time.sleep(5)
startSkyscanner(driver, cookies, "SKP", "MAD", "230621")
# time.sleep(10)
# for origin in origin_codes:
#     for destination in destination_codes:
#         selectStartAndDestinationCountry(driver, origin, destination)
#         time.sleep(get_random_number(5, 10))


for url in get_urls():
    try:
        driver.get(url)
        time.sleep(get_random_number(1, 5))

        price = driver.find_element(
            By.XPATH,
            '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button/div/div/div/span',
        )

        time.sleep(get_random_number(1, 5))

        duration = driver.find_element(
            By.XPATH,
            '//*[@id="app-root"]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button/p[2]',
        )

        time.sleep(get_random_number(1, 5))
    except:
        while True:
            solve_blocked(driver)
            time.sleep(0.5)
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        # )

        # text = driver.find_element(
        #     By.XPATH,
        #     "//*[starts-with(text(), 'Моля') or starts-with(text(), 'Please')]",
        # )

        # ActionChains(driver).move_to_element_with_offset(
        #     text, 15, 90
        # ).click_and_hold().perform()
        # time.sleep(6)
        # ActionChains(driver).release()
        # print("-------------------------------")
        # print(iframes)
        # print("-------------------------------")
        # # Filter iframes that have 'display: block' in their style attribute
        # for iframe in iframes:
        #     print(iframe)

        # # print(block_iframes)
        # # iframe = WebDriverWait(driver, 30).until(
        # #     EC.presence_of_element_located(
        # #         (By.XPATH, "//iframe[contains(@style, 'display: block')]")
        # #     )
        # # )

        # # Switch to iframe
        # driver.switch_to.frame(iframes[0])
        # iframeXPath = "//iframe[contains(@style, 'display: block')]"
        # elements = WebDriverWait(driver, 30).until(
        #     EC.presence_of_all_elements_located(
        #         (
        #             By.XPATH,
        #             "//*[text() = 'Click and hold' or text() = 'Щракнете тук и задръжте']",
        #         )
        #     )
        # )

        # # elements = driver.find_elements(
        # #     By.XPATH,
        # #     "//*[text() = 'Click and hold' or text() = 'Щракнете тук и задръжте']",
        # # )
        # print(elements)
        # for element, i in elements:
        #     print()
        #     print(i * 11111111111111111111111)
        #     print("-------------------------------")
        #     print(element)
        #     print("-------------------------------")
        #     print(i * 11111111111111111111111)
        #     print()
        # solveCaptcha(driver, elements)
    # data.append([url, origin, destination, date, price.text, duration.text])

    # save_array_to_excel(data, "data.xlsx")
    print("Saved data to excel file")
    time.sleep(get_random_number(1, 5))
# element = driver.find_element(By.ID, "acceptCookieButton")
# element.click()
time.sleep(10)

# changeLanguage(driver)


driver.quit()
