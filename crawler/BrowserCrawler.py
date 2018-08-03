# This is crawler example using selenium
# If use it, you need to download 'chromedriver' in project folder

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

# need to install module(pillow or image) for save image
import urllib.request


class BrowserCrawler:
    def __init__(self):
        self.wait_time = 1

    def __enter__(self):
        # open browser
        self.browser = webdriver.Chrome(executable_path='chromedriver')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def open(self, url):
        self.browser.get(url)

    def set_wait_time(self, sec):
        self.wait_time = sec

    def execute_script(self, func):
        self.browser.execute_script(func)
        sleep(self.wait_time)

    def click_button(self, button_id):
        try:
            self.browser.find_element_by_id(button_id).click()
        except NoSuchElementException as e:
            print(e.msg)

    def input_text(self, input_id, text):
        try:
            self.browser.find_element_by_id(input_id).clear()
            self.browser.find_element_by_id(input_id).send_keys(text)
        except NoSuchElementException as e:
            print(e.msg)

    def save_image(self, css_selector, img_name):
        img_elem = self.browser.find_element_by_css_selector(css_selector)
        urllib.request.urlretrieve(img_elem.get_property('src'), img_name)

    def get_class_tag_text(self, class_name):
        try:
            return self.browser.find_element_by_class_name(class_name).text
        except NoSuchElementException as e:
            print(e.msg)

        return ''

    def get_css_tag_text(self, css_selector):
        try:
            return self.browser.find_element_by_css_selector(css_selector).text
        except NoSuchElementException as e:
            print(e.msg)

        return ''

    def get_id_tag_text(self, id_name):
        try:
            return self.browser.find_element_by_id(id_name).text
        except NoSuchElementException as e:
            print(e.msg)

        return ''

