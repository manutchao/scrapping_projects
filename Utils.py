""" Usefull methods """

import json
import csv


class Utils:
    """
    Class Utils

    ...

    Attributes
    ----------


    Methods
    -------

    """

    @staticmethod
    def save_as_json(
        content: list,
        name_file="export.json",
        mode="w",
        nb_indent=4,
        style_encoding="utf-8",
        ascii=False,
    ):
        """Save content list in a JSON"""
        if content:
            with open(name_file, mode, encoding=style_encoding) as export_file:
                json.dump(
                    content, export_file, ensure_ascii=ascii, indent=int(nb_indent)
                )

    @staticmethod
    def save_as_csv(
        content: list,
        name_file="export.csv",
        mode="w",
        delimiter_field=";",
        style_encoding="utf-8",
    ):
        """Save content list in a CSV"""
        if content:
            with open(name_file, mode, encoding=style_encoding) as file:
                writer = csv.writer(file, delimiter=delimiter_field)
                writer.writerows(content)
