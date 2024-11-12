from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

def launch_driver():

    chrome_driver_path= "chromedriver/chromedriver-win64/chromedriver.exe"

    driver = webdriver.Chrome(service=ChromeService(chrome_driver_path))
    driver.maximize_window()

    return driver