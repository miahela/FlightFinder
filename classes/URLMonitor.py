import threading
import time

class URLMonitor(threading.Thread):
    def __init__(self, driver, another_function):
        threading.Thread.__init__(self)
        self.driver = driver
        self.another_function = another_function
        self.running = True
        self.target_url = None

    def set_target_url(self, url):
        self.target_url = url

    def run(self):
        while self.running:
            if self.target_url and self.driver.current_url.startswith(self.target_url):
                self.another_function()
                time.sleep(3)

    def stop(self):
        self.running = False