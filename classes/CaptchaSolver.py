import os
import time
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class CaptchaSolver:
    def __init__(self, webdriver):
        # printgging.getLogger(__name__)
        self.browser = webdriver  # Replace with your preferred browser
        self.pixelRatio = webdriver.execute_script("return window.devicePixelRatio")
        print(self.pixelRatio)
  # Replace with your actual pixel ratio
        self.TPL_DIR = "images"  # Replace with your actual template directory path

    def solve_blocked(self, retry=3):
        print("Start solving click and hold...")
        if not retry:
            return False
        element = None
        try:
            element = WebDriverWait(self.browser,15).until(EC.presence_of_element_located((By.ID,'px-captcha')))
            time.sleep(0.5)
        except BaseException as e:
            print(f'px-captcha element not found')
            return
        print(f'solve blocked:{self.browser.current_url}, Retry {retry} remaining times')
        template = cv2.imread(os.path.join(self.TPL_DIR, 'captcha.png'), 0)
        MIN_MATCH_COUNT = 6
        if element:
            print(f'start press and hold')
            ActionChains(self.browser).click_and_hold(element).perform()
            start_time = time.time()
            while 1:
                if time.time() - start_time > 20:
                    break
                x, y = element.location['x'], element.location['y']
                width, height = element.size.get('width'), element.size.get('height')                
                left = x*self.pixelRatio
                top = y*self.pixelRatio
                right = (x+width)*self.pixelRatio
                bottom = (y+height)*self.pixelRatio
                png = self.browser.get_screenshot_as_png()
                # save the screenshot 
                im = Image.open(BytesIO(png))
                im = im.crop((left, top, right, bottom))
                if im is None:
                    print("Failed to crop the image!")
                    return
                # im.save('screenshots/cropped_screenshot' + str(time.time()) + '.png')
                target = cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)  
                sift = cv2.SIFT_create()
                kp1, des1 = sift.detectAndCompute(template,None)
                kp2, des2 = sift.detectAndCompute(target,None)
                FLANN_INDEX_KDTREE = 0
                index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
                search_params = dict(checks = 50)
                flann = cv2.FlannBasedMatcher(index_params, search_params)
                matches = flann.knnMatch(des1,des2,k=2)
                good = []
                for m,n in matches:
                    if m.distance < 0.7*n.distance:
                        good.append(m)
                print( "matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
                if len(good)>=MIN_MATCH_COUNT:
                    print(f'release button')
                    ActionChains(self.browser).release(element).perform()
                    return
                time.sleep(0.1)
        time.sleep(1)
        retry -= 1
        self.solve_blocked(retry)