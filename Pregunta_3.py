# Entregar el máximo y minímo peso de los pokémon de tipo fighting de primera generación
# (cuyo id sea menor o igual a 151). Tu respuesta debe ser una lista con el siguiente
# formato: [1234, 12], en donde 1234 corresponde al máximo peso y 12 al mínimo.

import requests, multiprocessing

def divide_items_in_slices(items, cantidad_de_items_por_slice):
    items_length = len(items)
    pivot_index = items_length//cantidad_de_items_por_slice
    slices = list()
    for i in range(pivot_index+1):
        slices.append(items[i*cantidad_de_items_por_slice:(i+1)*cantidad_de_items_por_slice])
    if (items_length % cantidad_de_items_por_slice) == 0:
        slices.pop()
    return slices

def consultar_pokemones(pokemon_urls, queue_, headers):
    datos_salvados = list()
    for pokemon_url in pokemon_urls:
        # print('~'*80)
        response = requests.get(url=pokemon_url, headers=headers)
        json_response = response.json()
        # print(json_response["id"])
        # print(json_response["weight"])
        if json_response["id"] <= 151:
            datos_salvados.append(json_response["weight"])
    queue_.put(datos_salvados)

def pokemon_pregunta_tres(pokemon_type_api_url, headers):
    """
    Está función nos permite obtener una lista con dos valores, los cuales corresponden al
    peso máximo y mínimo de los pokémon de tipo fighting de primera generación, cuyo id es
    menor o igual a 151.
    """
    print("Obteniendo resultado...")
    response = requests.get(url=pokemon_type_api_url, headers=headers)
    json_dct = response.json()
    for result in json_dct["results"]:
        if result["name"] == "fighting":
            type_name, type_url = result["name"], result["url"]
            # print("Type : ", type_name)
            # print("URL : ", type_url)
            break
    # ---
    response = requests.get(url=type_url, headers=headers)
    pokemon_urls = list()
    for item in response.json()["pokemon"]:
        pokemon_url = item["pokemon"]["url"]
        pokemon_urls.append(pokemon_url)
    # ---
    urls_recuperadas = len(pokemon_urls)
    urls_fraccionadas = divide_items_in_slices(
                                                items=pokemon_urls, 
                                                cantidad_de_items_por_slice=int(urls_recuperadas*0.15),
                                                )
    # ---
    queue_ = multiprocessing.Queue()
    instancias_multiprocesamiento = list()
    datos_recuperados = list()
    for fraccion_pokemon_urls in urls_fraccionadas:
        args = (fraccion_pokemon_urls, queue_, headers)
        p = multiprocessing.Process(target=consultar_pokemones, args=args)
        instancias_multiprocesamiento.append(p)
        p.start()
    for instancia_multiprocesamiento in instancias_multiprocesamiento:
        resultado = queue_.get()
        datos_recuperados.extend(resultado)
    for instancia_multiprocesamiento in instancias_multiprocesamiento:
        instancia_multiprocesamiento.join()
    del queue_
    # ---
    max_weight = max(datos_recuperados)
    min_weight = min(datos_recuperados)
    return [max_weight, min_weight]

if __name__ == "__main__":

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "host": "pokeapi.co",
    }
    api_url = "https://pokeapi.co/api/v2"
    pokemon_type_api_url = f"{api_url}/type"

    resultado = pokemon_pregunta_tres(pokemon_type_api_url, headers)
    print(resultado)

"""
JUSTIFICACIÓN DEL LAS LIBRERÍAS:

requests (versión 2.24.0):
    Con esta librería realizo la solicitud GET al API, y obtengo los datos requeridos en formato JSON.

multiprocessing (es un módulo incorporado en python, la versión de python con la que cuento es la 3.8.5):
    Dado que las URLs totales correspondientes a los pokemones que cumplían con los requisitos establecidos
    en la pregunta eran considerables, el tiempo para obtener la solución era algo considerable, por lo que
    decidí paralelizar el proceso de consultar cada URL para obtener los datos requeridos, reduciendo 
    considerablemente el tiempo de resolución del ejerecicio.

NOTA : La paralelización es muy buena idea. Sin embargo, dado que estamos realizando múltiples solicitudes
       sería mejor hacer uso de proxies residenciales rotativas. Estás últimas son de paga, por lo que no
       las incluí.

       Hacer uso de este tipo de proxies reduce en gran medida el riesgo de ser baneados debido a la cantidad
       de solicitudes que se están realizando de manera paralela. Otro detalle a tomar en cuenta, es que sería
       buena agregar un delay de tiempo random (mayor a 0 y menor a 1 segundo), para reducir a un más esta
       posibilidad y no forzar tanto el servidor donde se encuentra alojado el sitio.

"""