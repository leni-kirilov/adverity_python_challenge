import requests


# TODO REQ1 - to make it more reusable for the other requirements
def get_all_characters():
    print("Getting all characters")
    url = "https://swapi.dev/api/people/"
    people = []

    while url:
        response = requests.get(url)
        data = response.json()

        people.extend(data["results"])
        url = data.get("next")
    return people


fetched_planets_cache = {}


# TODO REQ2 - maybe prefetch all planets. only 60
def get_planet_name(planet_url):
    cached_planet_name = fetched_planets_cache.get(planet_url)

    if cached_planet_name is not None:
        return cached_planet_name

    new_planet_name = requests.get(planet_url).json()['name']
    fetched_planets_cache[planet_url] = new_planet_name
    return new_planet_name