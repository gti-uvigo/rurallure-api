import base64
import requests


def create_poi():
    image =  None
    title = None
    description = 'Una hermosa casa en el campo.'
    latitude = 40.7128
    longitude = -74.0060
    types = []

    url = "http://193.146.210.235:5050/"

    # cargamos el modelo
    requests.get(url + "load_model")
    print("Modelo cargado")
    
    if not title and not description:
        return ({"status": "error", "message": "Title or description required"}), 400
    if latitude is None or longitude is None:
        return ({"status": "error", "message": "Latitude and longitude required"}), 400
    
    # Generar título si no existe
    if not title:
        prompt = f"Genera un título para un punto de interés con la descripción: {description}. El título debe ser breve y atractivo."
        response = requests.post(url + "generate_text", json={"prompt": prompt}, headers={"Content-Type": "application/json"})
        title = response
        print("Título generado:", title)

    # Generar descripción si no existe
    if not description:
        prompt = f"Genera una descripción para un punto de interés con el título: {title}. La descripción debe ser detallada y atractiva."
        response = requests.post(url + "generate_text", json={"prompt": prompt})
        description = response
        print("Descripción generada:", description)

    # Generar tipos si no existen
    if not types:
        prompt = f"Dime un tipo posible para un punto de interés con el título: {title} y la descripción: {description}. El tipo debe ser uno de los siguientes: restaurante, museo, parque, monumento, iglesia, playa, montaña, río, lago, bosque, ciudad, pueblo."
        response = requests.post(url + "generate_text", json={"prompt": prompt})
        type_text = response.json().get("text")
        types = [t.strip() for t in type_text.split(",")]  # convertir en lista
        print("Tipos generados:", types)

    # Traducir títulos y descripciones
    languages = [
        {"id": 1, "name": "Inglés"},
        {"id": 2, "name": "Francés"},
        {"id": 3, "name": "Alemán"},
        {"id": 4, "name": "Italiano"},
        {"id": 5, "name": "Portugués"}]
    titles = []
    descriptions_list = []

    for lang in languages:
        lang_id = lang['id']
        lang_name = lang['name']

        # Título
        prompt = f"Traduce el siguiente texto al {lang_name}: {title}"
        response = requests.post(url + "generate_text", json={"prompt": prompt})
        translated_title = response.json().get("text")
        titles.append({"language_id": lang_id, "name": translated_title})
        print(f"Título traducido al {lang_name}:", translated_title)

        # Descripción
        prompt = f"Traduce el siguiente texto al {lang_name}: {description}"
        response = requests.post(url + "generate_text", json={"prompt": prompt})
        translated_description = response.json().get("text")
        descriptions_list.append({"language_id": lang_id, "text": translated_description})
        print(f"Descripción traducida al {lang_name}:", translated_description)

    # descargamos el modelo
    requests.get(url + "unload_model")
    print("Modelo descargado")

    # Generar imagen si no existe
    if not image:
        prompt = f"Genera una imagen para un punto de interés con el título: {title} y la descripción: {description}. La imagen debe ser atractiva y relevante."
        response = requests.post(url + "generate_image", json={"prompt": prompt})
        image_base64 = response.json().get("image_base64")
        # guardo la imagen en jpeg
        with open("poi_image.jpg", "wb") as img_file:
            img_file.write(base64.b64decode(image_base64))
        print("Imagen generada")

    return ({"status": "poi created"}), 200



create_poi()