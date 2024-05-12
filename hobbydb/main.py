""" Script to scrap data from hobbydb.com """

import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.append("..")


from Utils import Utils

from hobbydb.Popscrapper import Popscrapper

if __name__ == "__main__":
    with Popscrapper() as scrapper:
        WEBSITE = (
            "https://www.hobbydb.com/marketplaces/hobbydb/subjects/pop-vinyl-series"
        )
        all_links = scrapper.get_all_links(WEBSITE)
        content_url = list(map(scrapper.get_content_from_url, all_links))
        Utils.save_as_json(content_url)

    with Popscrapper() as scraper:
        links = scraper.get_all_links(URL["host"])
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(scraper.get_content_from_url, links))
        print(results)
