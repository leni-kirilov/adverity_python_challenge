from typing import Any

import requests

SWAPI_CHARACTERS_ENDPOINT = "https://swapi.dev/api/people/"
SWAPI_PLANETS_ENDPOINT = "https://swapi.dev/api/planets/"

planet_url_2_name_cache = {}


def get_all_characters() -> list:
    return get_all_items(SWAPI_CHARACTERS_ENDPOINT)


def get_planet_name(planet_url: str) -> str:
    if not planet_url: raise ValueError("planet_url cannot be None or empty")

    if not planet_url_2_name_cache:
        planet_url_2_name_cache.update({
            planet['url']: planet['name']
            for planet in get_all_items(SWAPI_PLANETS_ENDPOINT)
        })

    return planet_url_2_name_cache.get(planet_url)

def get_all_items(swapi_url: str) -> list[Any] | None:
    if not swapi_url: raise ValueError("swapi_url cannot be None or empty")

    items = []

    while swapi_url:
        response = requests.get(swapi_url)
        data = response.json()

        items.extend(data["results"])
        swapi_url = data.get("next")
    return items
