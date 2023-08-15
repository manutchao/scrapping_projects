import logging
import json
import time
import csv
import urllib.parse as urlparse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Scrapper:
    """
    Class with all necessary tools to scrap data from a website

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
        options.headless = True
        self.driver = webdriver.Firefox(
            options=options,
            service=Service(executable_path=GeckoDriverManager().install()),
        )

    @staticmethod
    def save_as_json(
        content: list,
        name_file="export.json",
        mode="w",
        nb_indent=4,
        style_encoding="utf-8",
        ascii=False,
    ):
        if content:
            with open(name_file, mode, encoding=style_encoding) as f:
                json.dump(content, f, ensure_ascii=ascii, indent=int(nb_indent))

    @staticmethod
    def save_as_csv(
        content: list, name_file="export.csv", mode="w", delimiter_field=";"
    ):
        if content:
            with open(name_file, mode) as file:
                writer = csv.writer(file, delimiter=delimiter_field)
                writer.writerows(content)
