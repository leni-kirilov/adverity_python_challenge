import requests

SWAPI_CHARACTERS_ENDPOINT = "https://swapi.dev/api/people/"
SWAPI_PLANETS_ENDPOINT = "https://swapi.dev/api/planets/"

_planet_url_to_name_cache = dict()


def get_all_characters() -> list:
    """Fetch all StarWars Characters using the API"""
    return get_all_items(SWAPI_CHARACTERS_ENDPOINT)


def get_planet_name(planet_url: str) -> str:
    """Get planet name

    Keyword arguments:
    planet_url -- comes from other StarWars API entities fields

    Uses a cache dict which prefetches all planets on first usage to reduce network calls.
    """
    if not planet_url:
        raise ValueError("planet_url cannot be None or empty")

    if not _planet_url_to_name_cache:
        _planet_url_to_name_cache.update({
            planet["url"]: planet["name"]
            for planet in get_all_items(SWAPI_PLANETS_ENDPOINT)
        })

    return _planet_url_to_name_cache.get(planet_url)


def get_all_items(swapi_url: str) -> list:
    """Fetch all pages for a StarWars root entity url"""
    if not swapi_url:
        raise ValueError("swapi_url cannot be None or empty")

    items = []

    while swapi_url:
        response = requests.get(swapi_url)
        data = response.json()

        items.extend(data["results"])
        swapi_url = data.get("next")
    return items
