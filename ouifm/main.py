""" Script to export data from the website ouifm.fr """
import argparse
from datetime import datetime
import sys

sys.path.append("..")


from Utils import Utils

from RadioScrapper import RadioScrapper


parser = argparse.ArgumentParser()
parser.add_argument("--radio", default="OUI FM")
parser.add_argument(
    "--horodatage", default=str(datetime.now().strftime("%Y-%m-%d %H:%M"))
)
args = parser.parse_args()
parameters = vars(args)


if __name__ == "__main__":
    with RadioScrapper() as scrapper:
        list_of_songs = scrapper.scrap_songs(
            parameters.get("horodatage", None), parameters.get("radio", None)
        )
        Utils.save_as_csv(list_of_songs, name_file="playlist.csv")
