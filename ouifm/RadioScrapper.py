""" Script to export data from the website ouifm.fr """

import sys
from ClientSelenium import ClientSelenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

sys.path.append("..")


headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


class RadioScrapper(ClientSelenium):
    """
    Class with tools to scrap data from a ouifm.fr

    ...

    Attributes
    ----------


    Methods
    -------

    """

    def __init__(self):
        super().__init__()
        self.url = "https://www.ouifm.fr/retrouver-un-titre"
        self.driver.get(self.url)

    def scrap_songs(self, horodatage: str, radio: str) -> list:
        """
        Export songs
        """
        str_date, str_time = horodatage.split(" ")

        # Accept cookies
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="popin_tc_privacy_button"]'))
        ).click()

        # Fill form
        Select(self.driver.find_element(By.ID, "radio")).select_by_visible_text(radio)
        self.driver.find_element(By.ID, "date").send_keys(str_date)
        self.driver.find_element(By.ID, "time").send_keys(str_time)
        self.driver.find_element(
            "xpath",
            "//div[starts-with(@id, 'remonteeTitresMusicaux')]/form/div/div[4]/button",
        ).click()

        nb_songs = self.driver.find_elements(
            "xpath", "//div[starts-with(@id, 'remonteeTitresMusicaux')]/div/div"
        )

        list_songs = []
        for i in range(1, int(len(nb_songs)) + 1):
            root_path = "//*[starts-with(@id, 'remonteeTitresMusicaux')]/div/div"
            artist = self.driver.find_element(
                "xpath",
                f"{root_path}[{str(i)}]/div/div/p",
            ).text
            song = self.driver.find_element(
                "xpath",
                f"{root_path}[{str(i)}]/div/div/h3",
            ).text
            time_of_diffusion = self.driver.find_element(
                "xpath",
                f"{root_path}[{str(i)}]/div/figure/div/span/span",
            ).text
            list_songs.append(
                [f"{str_date} {time_of_diffusion}", artist.title(), song.capitalize()]
            )
        return list_songs
