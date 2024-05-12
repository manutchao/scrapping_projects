""" Scrapping class for hobbydb"""

import logging
import sys
import time
import urllib.parse as urlparse
from concurrent.futures import ThreadPoolExecutor
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append("..")

from Utils import Utils
from ClientSelenium import ClientSelenium


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Popscrapper(ClientSelenium):
    """
    Class with all necessary tools to scrap data from a website

    ...

    Attributes
    ----------


    Methods
    -------

    """

    NB_PAGE = 4
    NB_RESULT_BY_PAGE = 6
    URL = {
        "host": "https://www.hobbydb.com/marketplaces/hobbydb/subjects/pop-vinyl-series",
        "filter": {
            "filters[related_to]": "49962",
            "filters[in_collection]": "all",
            "filters[in_wishlist]": "all",
            "filters[on_sale]": "all",
            "id=49962&order[name]": "name",
            "order[sort]": "asc",
            "page": "1",
            "subject_id": "49962",
            "subvariants": "true",
        },
    }

    XPATH_COOKIE = "/html/body/div[1]/div/div/div/div[2]/div/button[2]"

    def __enter__(self):
        """ """
        return self

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.reference_numbers = {}
        self.dimensions = {}
        self.production_details = {}
        self.characteristics = {}

    @staticmethod
    def build_url(host: str, param: dict) -> str:
        """_summary_

        Args:
            host (str): _description_
            param (dict): _description_

        Returns:
            str: _description_
        """
        url_parse = urlparse.urlparse(host)
        query = url_parse.query
        url_dict = dict(urlparse.parse_qsl(query))
        url_dict.update(param)
        url_new_query = urlparse.urlencode(url_dict)
        url_parse = url_parse._replace(query=url_new_query)
        return urlparse.urlunparse(url_parse)

    @staticmethod
    def update_param_url(param: dict, key: str, value: str) -> dict:
        """Update param url

        Args:
            param (dict): dictonnary of url param
            key (str): key of the param you want to update
            value (str): new value

        Returns:

            dict: dictonnary of url param updated
        """
        if key in param.keys():
            param.update({key: value})
        return param

    def get_all_links(self) -> list:
        """
        Get list of all url of a page.

            Returns:
                list_items (list): List of url string
        """
        self.driver.get(self.URL["host"])
        list_items = []
        root_xpath = "//*[@id='related-items']/catalog-item-search-results/div[1]/div[2]/div[3]/catalog-items-list"

        # Accept cookies
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.XPATH_COOKIE))
        ).click()

        for num_page in range(1, self.NB_PAGE):
            print(f"page {num_page}")
            url_updated = Popscrapper.build_url(
                str(self.URL["host"]),
                Popscrapper.update_param_url(self.URL["filter"], "page", str(num_page)),
            )
            self.driver.get(url_updated)

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div[3]/div[2]/catalog-item-search-results/div/div[2]/div[3]/catalog-items-list/div[1]/div/div[3]/div/div/a/img",
                        )
                    )
                )
                print("La page a fini de charger en JavaScript.")
                for i in range(1, self.NB_RESULT_BY_PAGE):
                    link = self.driver.find_element(
                        by=By.XPATH,
                        value=f"{root_xpath}/div[{str(i)}]/div/div[5]/div[2]/div/div[1]/a",
                    ).get_attribute("href")

                    list_items.append(link.replace("subvariants", ""))
            except:
                print("La page n'a pas pu charger en JavaScript dans le délai imparti.")

        print(list_items)
        return list_items

    def get_value_from_xpath(self, selector: str, dict_to_save: dict, node_dict: str):
        """Get value from a xpath selector

        Args:
            selector (str): _description_
            dict_to_save (dict): _description_
            node_dict (str): _description_
        """
        try:
            elem = self.driver.find_element(by=By.XPATH, value=selector)
            dict_to_save[node_dict] = elem.text
        except NoSuchElementException:
            log.info("%s not found", node_dict)

    def process_xpath_values(self, xpath_root: str):
        """_summary_

        Args:
            xpath_root (str): _description_
        """
        xpath_list = [
            f"{xpath_root}[2]/catalog-item-field-definitions/div/div[1]/div[2]/div[3]/div[2]/span/span[2]",
            f"{xpath_root}[2]/catalog-item-field-definitions/div/div[1]/div[2]/div[1]/div[2]/span[1]",
            f"{xpath_root}[2]/catalog-item-field-definitions/div/div[2]/div/div/div/div[2]/div[1]/div[2]/span/span[2]",
            f"{xpath_root}[2]/catalog-item-field-definitions/div/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/span/span[2]",
            f"{xpath_root}[2]/catalog-item-field-definitions/div/div[2]/div/div[1]/div/div[2]/div[5]/div[2]/span/span[2]",
            f"{xpath_root}[2]/catalog-item-metadata/div/div/div[1]/div[2]/div[3]/editable/div/div[2]/div[1]",
            f"{xpath_root}[2]/catalog-item-metadata/div/div/div[1]/div[2]/div[2]/editable/div/div[2]/div[1]",
            f"{xpath_root}[2]/catalog-item-metadata/div/div/div[1]/div[2]/div[5]/editable/div/div[2]/div[1]",
            f"{xpath_root}[2]/catalog-item-metadata/div/div/div[1]/div[2]/div[3]/editable/div/div[2]/div[1]",
            f"{xpath_root}[2]/catalog-item-metadata/div/div/div[1]/div[2]/div[1]",
            f"{xpath_root}[2]/catalog-item-field-definitions/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/span/span[2]",
            f"{xpath_root}[2]/catalog-item-field-definitions/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/span/span[2]",
            f"{xpath_root}[2]/catalog-item-field-definitions/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/span/span[2]",
        ]

        dict_list = [
            self.production_details,
            self.production_details,
            self.characteristics,
            self.characteristics,
            self.characteristics,
            self.reference_numbers,
            self.reference_numbers,
            self.reference_numbers,
            self.reference_numbers,
            self.reference_numbers,
            self.dimensions,
            self.dimensions,
            self.dimensions,
        ]

        node_names = [
            "materials",
            "released",
            "scale",
            "gender",
            "languages",
            "reference",
            "upc",
            "alternate_upc",
            "manufacturer_id",
            "hbid",
            "height",
            "width",
            "depth",
        ]

        for xpath, dictionary, node_name in zip(xpath_list, dict_list, node_names):
            self.get_value_from_xpath(xpath, dictionary, node_name)

    def get_content_from_url(self, url: str) -> dict:
        """
        Get content from url.

            Parameters:
                url (str): url of the page
            Returns:
                atom (list): Content
        """
        log.info(url)
        list_items = []
        self.driver.get(url)

        time.sleep(5)

        atom = {
            "name": self.driver.find_element(
                by=By.XPATH,
                value="/html/body/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[2]/h1",
            ).text,
            "img": self.driver.find_element(
                by=By.XPATH, value="//a[@ng-click='showPhotos()']//img"
            ).get_attribute("src"),
            "link": url,
        }

        self.process_xpath_values("/html/body/div[2]/div[3]/div")

        atom["production_details"] = self.production_details
        atom["characteristics"] = self.characteristics
        atom["reference_numbers"] = self.reference_numbers
        atom["reference_numbers"] = self.reference_numbers
        atom["dimensions"] = self.dimensions
        list_items.append(atom)

        return atom


if __name__ == "__main__":
    with Popscrapper() as scraper:

        links = scraper.get_all_links()
        if links:
            with ThreadPoolExecutor(max_workers=2) as executor:
                results = list(executor.map(scraper.get_content_from_url, links))
            Utils.save_as_json(results)
        else:
            log.info("No links found")
        log.info("MAPPING DONE")
