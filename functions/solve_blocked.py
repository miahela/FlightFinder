from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

import os
import cv2
# from openCv import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def solve_blocked(self, retry=3):
    '''
    Solve blocked
    (Cross-domain iframe cannot get elements temporarily)
    Simulate the mouse press and hold to complete the verification
    '''
    if not retry:
        return False
    element = None
    try:
        element = WebDriverWait(self.browser,15).until(EC.presence_of_element_located((By.ID,'px-captcha')))
        # Wait for the px-captcha element styles to fully load
        time.sleep(0.5)
    except BaseException as e:
        self.logger.info(f'px-captcha element not found')
        return
    self.logger.info(f'solve blocked:{self.browser.current_url}, Retry {retry} remaining times')
    template = cv2.imread(os.path.join(settings.TPL_DIR, 'captcha.png'), 0)
    # Set the minimum number of feature points to match value 10
    MIN_MATCH_COUNT = 8 
    if  element:
        self.logger.info(f'start press and hold')
        ActionChains(self.browser).click_and_hold(element).perform()
        start_time = time.time()
        while 1:
            # timeout
            if time.time() - start_time > 20:
                break
            x, y = element.location['x'], element.location['y']
            width, height = element.size.get('width'), element.size.get('height')                
            left = x*self.pixelRatio
            top = y*self.pixelRatio
            right = (x+width)*self.pixelRatio
            bottom = (y+height)*self.pixelRatio
            # full screenshot
            png = self.browser.get_screenshot_as_png() 
            im = Image.open(BytesIO(png))
            # px-captcha screenshot
            im = im.crop((left, top, right, bottom)) 
            target = cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)  
            # Initiate SIFT detector
            sift = cv2.SIFT_create()
            # find the keypoints and descriptors with SIFT
            kp1, des1 = sift.detectAndCompute(template,None)
            kp2, des2 = sift.detectAndCompute(target,None)
            # create set FLANN match
            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks = 50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(des1,des2,k=2)
            # store all the good matches as per Lowe's ratio test.
            good = []
            # Discard matches greater than 0.7
            for m,n in matches:
                if m.distance < 0.7*n.distance:
                    good.append(m)
            self.logger.info( "matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            if len(good)>=MIN_MATCH_COUNT:
                self.logger.info(f'release button')
                ActionChains(self.browser).release(element).perform()
                return
            time.sleep(0.5)
    time.sleep(1)
    retry -= 1
    self.solve_blocked(retry)