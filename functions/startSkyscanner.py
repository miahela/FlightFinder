import time


def startSkyscanner(driver, cookies, origin, destination, date):
    base_url = "https://www.skyscanner.com/"
    driver.get(base_url)
    time.sleep(5)
    for cookie in cookies:
        driver.add_cookie(cookie)

    # driver.execute_script(
    #     'window.localStorage.setItem(\'hom.searchcontrols\', \'{"en-US":{"originId":"SKP","originName":"Skopje","originGeneralSearchGeoId":null,"destinationId":"LEN","destinationName":"Leon","destinationGeneralSearchGeoId":null,"outboundDate":"2023-06-21","outboundAlts":{"expiryStamp":null,"value":false},"inboundDate":"2023-06-27","inboundAlts":{"expiryStamp":null,"value":false},"cabinclass":"Economy","adultsV2":1,"adults":1,"children":0,"childrenV2":[],"infants":0,"locale":"en-US","tripType":"one-way","preferDirects":false,"seoAirlineCode":null,"sponsoredAgent":null,"legs":[{"date":"2023-06-21","originId":"SKP","originName":"Skopje","originCityId":"SKOP","originCountryName":null,"originRegionId":null,"originGeneralSearchGeoId":null,"originGeoContainerId":null,"originGeoId":null,"destinationId":"LEN","destinationName":"Leon","destinationCityId":"LEON","destinationCountryName":null,"destinationRegionId":null,"destinationGeneralSearchGeoId":null,"destinationGeoContainerId":null},{"date":null,"originId":null,"originName":null,"originCityId":null,"or…\');'
    # )
    # driver.execute_script(
    #     "window.localStorage.setItem('__initTest__', '__initValue__');"
    # )

    # url = (
    #     base_url + "transport/flights/" + origin + "/" + destination + "/" + date + "/"
    # )

    # driver.get(url)
