import unittest
from unittest.mock import patch, MagicMock

from core.services import swapi

_ONE_PAGE_RESULT = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [
        {
            "title": "A New Hope",
            "episode_id": 4,
            "opening_crawl": "It is a period of civil war",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
            "characters": [
                "https://swapi.dev/api/people/1/",
                "https://swapi.dev/api/people/2/"
            ],
            "planets": [
                "https://swapi.dev/api/planets/1/",
                "https://swapi.dev/api/planets/3/"
            ],
            "starships": [
                "https://swapi.dev/api/starships/2/"
            ],
            "vehicles": [
                "https://swapi.dev/api/vehicles/4/"
            ],
            "species": [
                "https://swapi.dev/api/species/1/"
            ],
            "created": "2014-12-10T14:23:31.880000Z",
            "edited": "2014-12-20T19:49:45.256000Z",
            "url": "https://swapi.dev/api/films/1/"
        }
    ]
}
_FIRST_PAGE_RESULT = {
    "count": 2,
    "next": "https://swapi.dev/api/planets/?page=2",
    "previous": "null",
    "results": [
        {
            "name": "Tatooine",
            "rotation_period": "23",
            "orbital_period": "304",
            "diameter": "10465",
            "climate": "arid",
            "gravity": "1 standard",
            "terrain": "desert",
            "surface_water": "1",
            "population": "200000",
            "residents": [
                "https://swapi.dev/api/people/1/",
            ],
            "films": [
                "https://swapi.dev/api/films/1/",
            ],
            "created": "2014-12-09T13:50:49.641000Z",
            "edited": "2014-12-20T20:58:18.411000Z",
            "url": "https://swapi.dev/api/planets/1/"
        },
    ]
}
_LAST_PAGE_RESULT = {
    "count": 2,
    "next": None,
    "previous": None,
    "results": [
        {
            "name": "Naboo",
            "rotation_period": "26",
            "orbital_period": "312",
            "diameter": "12120",
            "climate": "temperate",
            "gravity": "1 standard",
            "terrain": "grassy hills, swamps, forests, mountains",
            "surface_water": "12",
            "population": "4500000000",
            "residents": [
                "https://swapi.dev/api/people/3/",
            ],
            "films": [
                "https://swapi.dev/api/films/3/",
            ],
            "created": "2014-12-10T11:52:31.066000Z",
            "edited": "2014-12-20T20:58:18.430000Z",
            "url": "https://swapi.dev/api/planets/8/"
        },
    ]
}


class SwapiTestCase(unittest.TestCase):

    def test_get_all_items_negative(self):
        self.assertRaises(ValueError, swapi.get_all_items, None)
        self.assertRaises(ValueError, swapi.get_all_items, "")

    @patch("core.services.swapi.requests")
    def test_get_all_items_single_page(self, mock_requests=None):
        # given a mocked response
        self.create_mock_response(mock_requests, _ONE_PAGE_RESULT)

        # expect 1 item
        result = swapi.get_all_items("https://swapi.dev/api/films/")
        self.assertEqual(1, len(result))

    @patch("core.services.swapi.requests")
    def test_get_all_items_many_pages(self, mock_requests):
        self.setup_mock_planets(mock_requests)

        result = swapi.get_all_items(swapi.SWAPI_PLANETS_ENDPOINT)
        self.assertEqual(2, len(result))

    def test_get_planet_name_negative(self):
        self.assertRaises(ValueError, swapi.get_planet_name, None)
        self.assertRaises(ValueError, swapi.get_planet_name, "")

    def test_get_planet_name_from_cache(self):
        swapi._planet_url_to_name_cache = {"planet-url1": "Earth"}
        self.assertEqual("Earth", swapi.get_planet_name("planet-url1"), )

    @patch("core.services.swapi.requests")
    def test_get_planet_name_fill_cache(self, mock_requests):
        # given cache is empty
        swapi._planet_url_to_name_cache = {}
        self.setup_mock_planets(mock_requests)

        # expect correct result and cache is filled
        self.assertEqual("Tatooine", swapi.get_planet_name("https://swapi.dev/api/planets/1/"), )
        self.assertEqual(2, len(swapi._planet_url_to_name_cache), )

    # Util functions
    def setup_mock_planets(self, mock_requests):
        mock_response_page_1 = self.create_mock_response(mock_requests, _FIRST_PAGE_RESULT)
        mock_response_page_2 = self.create_mock_response(mock_requests, _LAST_PAGE_RESULT)

        # Configure side_effect to return different responses based on the URL
        def mock_get(url, *args, **kwargs):
            if url == swapi.SWAPI_PLANETS_ENDPOINT:
                return mock_response_page_1
            elif url == swapi.SWAPI_PLANETS_ENDPOINT + "?page=2":
                return mock_response_page_2
            else:
                raise ValueError(f"Unexpected URL called: {url}")

        mock_requests.get.side_effect = mock_get

    def create_mock_response(self, mock_requests, return_value):
        mock_response_page1 = MagicMock()
        mock_response_page1.json.return_value = return_value
        mock_requests.get.return_value = mock_response_page1
        return mock_response_page1


if __name__ == "__main__":
    unittest.main()
