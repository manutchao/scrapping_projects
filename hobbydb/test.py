import pytest
from Popscrapper import Popscrapper

pop = Popscrapper()


usecase_param = [
    ({"foo": "test", "bar": "test2"}, "foo", "test3", {"foo": "test3", "bar": "test2"}),
    ({"foo": "test", "bar": "test2"}, "bar", "test7", {"foo": "test", "bar": "test7"}),
    ({"foo": "test"}, "foo", "test", {"foo": "test"}),
]

usecase_url_build = [
    ("http://google.fr", {"meteo": "paris"}, "http://google.fr?meteo=paris"),
    (
        "https://www.hobbydb.com/marketplaces/hobbydb/subjects/pop-vinyl-series",
        {"filters[related_to]": "49962", "filters[in_collection]": "all"},
        "https://www.hobbydb.com/marketplaces/hobbydb/subjects/pop-vinyl-series?filters%5Brelated_to%5D=49962&filters%5Bin_collection%5D=all",
    ),
]


@pytest.mark.parametrize("url, param, expected", usecase_url_build)
def test_build_url(url, param, expected):
    assert Popscrapper.build_url(url, param) == expected


@pytest.mark.parametrize("param,key, value, expected", usecase_param)
def test_update_param_url(param, key, value, expected):
    assert Popscrapper.update_param_url(param, key, value) == expected
