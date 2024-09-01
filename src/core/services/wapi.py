import requests

SWAPI_CHARACTERS_ENDPOINT = "https://swapi.dev/api/people/"

fetched_planets_cache = {}


def get_all_characters() -> list:
    print("Getting all characters")
    url = SWAPI_CHARACTERS_ENDPOINT
    people = []

    while url:
        response = requests.get(url)
        data = response.json()

        people.extend(data["results"])
        url = data.get("next")
    return people


# TODO REQ2 - maybe prefetch all planets. only ~60
def get_planet_name(planet_url: str) -> str:
    cached_planet_name = fetched_planets_cache.get(planet_url)

    if cached_planet_name is not None:
        return cached_planet_name

    new_planet_name = requests.get(planet_url).json()['name']
    fetched_planets_cache[planet_url] = new_planet_name
    return new_planet_name
