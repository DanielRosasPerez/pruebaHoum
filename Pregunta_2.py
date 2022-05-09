# ¿Con cuántas especies de pokémon puede procrear raichu? (2 Pokémon pueden procrear si están dentro del mismo egg group).
# Tu respuesta debe ser un número. Recuerda eliminar los duplicados.

import requests

def pokemon_pregunta_dos(pokemon_api_url):
    """
    Está función nos permite saber con cuantás especies de pokémon puede procrear
    raichu, cumpliendo con los criterios establecidos en la pregunta.
    """
    response = requests.get(url=pokemon_api_url, headers=headers)
    json_dct = response.json()
    number_of_available_pokemons = json_dct["count"]
    # ---
    response = requests.get(url=f"{pokemon_api_url}/?limit={number_of_available_pokemons}")
    results = response.json()["results"]
    # ---
    for result in results:
        if result["name"] == "raichu":
            pokemon_name, pokemon_url = result["name"], result["url"]
            # print("Pokemon : ", pokemon_name)
            # print("URL : ", pokemon_url)
            break
    response = requests.get(url=pokemon_url, headers=headers)
    url_species = response.json()["species"]["url"]
    response = requests.get(url=url_species, headers=headers)
    egg_groups_urls = [item["url"] for item in response.json()["egg_groups"]]
    pokemon_species_urls = set([item["url"] for egg_group_url in egg_groups_urls 
                                for item in requests.get(url=egg_group_url, headers=headers).json()["pokemon_species"]])
    respuesta = len(pokemon_species_urls)
    return respuesta

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "host": "pokeapi.co",
}
api_url = "https://pokeapi.co/api/v2"
pokemon_api_url = f"{api_url}/pokemon"

respuesta = pokemon_pregunta_dos(pokemon_api_url)
print(f"Cantidad de especies de pokémon que pueden procrear con raichu  : ")
print(respuesta)

"""
JUSTIFICACIÓN DEL LAS LIBRERÍAS:

requests (versión 2.24.0):
    Con esta librería realizo la solicitud GET al API, y obtengo los datos requeridos en formato JSON.

"""
