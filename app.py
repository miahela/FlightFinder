from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import openpyxl

spain_airports_codes = [
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
balkan_airports_codes = ["SKP", "SOF", "SKG", "ATH", "BEG"]
going_dates = ["230619", "230620", "230621", "230622", "230623"]
return_dates = ["29", "30", "1"]


urls = []
base_url = "https://www.skyscanner.com/"

for origin in balkan_airports_codes:
    for destination in spain_airports_codes:
        for date in going_dates:
            url = (
                base_url
                + "transport/flights/"
                + origin
                + "/"
                + destination
                + "/"
                + date
                + "/"
            )

            urls.append([url, origin, destination, date])

df = pd.DataFrame(urls, columns=["url", "origin", "destination", "date"])
df.to_excel("urls.xlsx", index=False)
