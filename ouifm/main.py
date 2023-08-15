""" Script to export data from the website ouifm.fr """
import sys
from datetime import datetime
import click
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.firefox import GeckoDriverManager

sys.path.append("..")
from Scrapper import Scrapper

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


@click.command()
@click.option(
    "--horodatage", type=str, default=str(datetime.now().strftime("%d/%m/%Y %H:%M"))
)
@click.option("--radio", default="OUI FM", type=str)
def scrap_songs(horodatage: str, radio: str):
    """
    Export songs
    """
    str_date, str_time = horodatage.split(" ")
    url = "https://www.ouifm.fr/retrouver-un-titre"
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(
        options=options,
        service=Service(executable_path=GeckoDriverManager().install()),
    )
    driver.get(url)

    # Accept cookies
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="popin_tc_privacy_button"]'))
    ).click()

    # Fill form
    Select(driver.find_element(By.ID, "radio")).select_by_visible_text(radio)
    driver.find_element(By.ID, "date").send_keys(str_date)
    driver.find_element(By.ID, "time").send_keys(str_time)
    driver.find_element(
        "xpath",
        "//div[starts-with(@id, 'remonteeTitresMusicaux')]/form/div/div[4]/button",
    ).click()

    nb_songs = driver.find_elements(
        "xpath", "//div[starts-with(@id, 'remonteeTitresMusicaux')]/div/div"
    )

    list_songs = []
    for i in range(1, int(len(nb_songs)) + 1):
        root_path = "//*[starts-with(@id, 'remonteeTitresMusicaux')]/div/div"
        artist = driver.find_element(
            "xpath",
            f"{root_path}[{str(i)}]/div/div/p",
        ).text
        song = driver.find_element(
            "xpath",
            f"{root_path}[{str(i)}]/div/div/h3",
        ).text
        time_of_diffusion = driver.find_element(
            "xpath",
            f"{root_path}[{str(i)}]/div/figure/div/span/span",
        ).text
        print(f"{artist.title()} - {song.capitalize()} - {time_of_diffusion}")
        list_songs.append(
            [f"{str_date} {time_of_diffusion}", artist.title(), song.capitalize()]
        )
    Scrapper.save_as_csv(list_songs, name_file="playlist.csv")
    driver.quit()


if __name__ == "__main__":
    # scrap_songs("2023-08-14 18:47", "OUI FM")
    scrap_songs()
