import unittest
from core.services import swapi


# TODO check how to do parameteriszed
class SwapiTestCase(unittest.TestCase):

    def test_get_all_items_negative(self):
        self.assertRaises(ValueError, swapi.get_all_items, None)
        self.assertRaises(ValueError, swapi.get_all_items, '')

    def test_get_all_items_single_page(self):
        result = swapi.get_all_items('https://swapi.dev/api/films/')
        self.assertEqual(len(result), 6)

    def test_get_all_items_many_pages(self):
        result = swapi.get_all_items(swapi.SWAPI_CHARACTERS_ENDPOINT)
        self.assertEqual(len(result), 82)

    def test_get_planet_name_negative(self):
        self.assertRaises(ValueError, swapi.get_planet_name, None)
        self.assertRaises(ValueError, swapi.get_planet_name, '')

    def test_get_planet_name_from_cache(self):
        swapi.planet_url_2_name_cache = {'planet-url1': 'Earth'}
        self.assertEqual(swapi.get_planet_name('planet-url1'), 'Earth')

    def test_get_planet_name_fill_cache(self):
        # given cache is empty
        swapi.planet_url_2_name_cache = {}

        # expect correct result and cache is filled
        self.assertEqual(swapi.get_planet_name('https://swapi.dev/api/planets/1/'), 'Tatooine')
        self.assertEqual(len(swapi.planet_url_2_name_cache), 60)


if __name__ == '__main__':
    unittest.main()
