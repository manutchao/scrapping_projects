""" Selenium """

import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


class ClientSelenium:
    """
    Class to use Selenium

    ...

    Attributes
    ----------


    Methods
    -------

    """

    def __enter__(self):
        """ """
        return self

    def __init__(self):
        options = Options()
        options.add_argument("-headless")
        log.info("Start Selenium")
        self.driver = webdriver.Firefox(
            options=options,
            service=Service(executable_path=GeckoDriverManager().install()),
        )

    def __exit__(self, exc_type, exc_value, traceback):
        """Close selenium driver"""
        log.info("Stop Selenium")
        self.driver.quit()
