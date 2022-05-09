# Obtén cuantos pokemones poseen en sus nombres "at" y tienen 2 'a' en sus nombres, incluyendo la primera del "at".
# Tu respuesta debe ser un número.

import requests

def pokemon_pregunta_uno(pokemon_api_url):
    """
    Está función nos permite obtener la cantidad de pokemones cuyos nombres contengan "at"
    y 2 'a' en sus nombres. Regresa un número como resultado.
    """
    response = requests.get(url=pokemon_api_url, headers=headers)
    json_dct = response.json()
    number_of_available_pokemons = json_dct["count"]
    # ---
    response = requests.get(url=f"{pokemon_api_url}/?limit={number_of_available_pokemons}")
    results = response.json()["results"]
    # ---
    respuesta = [result["name"] for result in results 
                    if result["name"].find("at") != -1 and result["name"].count('a') == 2]
    cantidad_pokemones_resultantes = len(respuesta)
    return cantidad_pokemones_resultantes

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "host": "pokeapi.co",
}
api_url = "https://pokeapi.co/api/v2"
pokemon_api_url = f"{api_url}/pokemon"

cantidad_pokemones_resultantes = pokemon_pregunta_uno(pokemon_api_url)
print("Cantidad total de Pokémones resultantes : ", cantidad_pokemones_resultantes)

"""
JUSTIFICACIÓN DEL LAS LIBRERÍAS:

requests (versión 2.24.0):
    Con esta librería realizo la solicitud GET al API, y obtengo los datos requeridos en formato JSON.

"""