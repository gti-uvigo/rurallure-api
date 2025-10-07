from db.dao import get_method, post_method, get_image_gridfs, update_method


def get_text_by_lang(text_list, lang_id):
    """Busca en una lista de diccionarios el que coincide con el lang_id y devuelve su texto."""
    for item in text_list:
        if item.get("language_id") == lang_id:
            return item.get("text")
    return None


def get_routes_descriptions_by_type(route_type: str, type: str = "featured", language_id: str = "6d68e409-c46e-4d4a-8560-f15256e9cbb3"):
    """
    Obtiene las rutas filtradas por tipo de ruta y, opcionalmente, por idioma.
    :param route_type: Tipo de ruta a filtrar.
    :param language_id: ID del idioma para filtrar las rutas (por defecto es un ID específico).
    :return: Lista de rutas que coinciden con el tipo y el idioma especificados.
    """
    if not route_type:
        raise ValueError("El tipo de ruta no puede ser vacío.")
    routes = get_method("routes", {"route_type": route_type, "type": type, "visibility": "public"}, many=True)
    for route in routes:
        route["title"] = get_text_by_lang(route.get("titles", []), language_id)
        route["short_description"] = get_text_by_lang(route.get("short_descriptions", []), language_id)
        route["long_description"] = get_text_by_lang(route.get("long_descriptions", []), language_id)
        for key in ["titles", "short_descriptions", "long_descriptions", "_id", "stages", "locations"]:
            if key in route:
                del route[key]
    return routes


def get_route_stages(route_id: str):
    """
    Obtiene todas las etapas de las rutas disponibles.
    
    :return: Lista de etapas de rutas.
    """
    route_stages = get_method("routes", {"route_id": route_id}, many=False)
    
    if "stages" not in route_stages:
        return {"stages": []}
    return route_stages["stages"]


def get_route_locations(route_id: str):
    """
    Obtiene todas las ubicaciones de las rutas disponibles.
    
    :return: Lista de ubicaciones de rutas.
    """
    route_locations = get_method("routes", {"route_id": route_id}, many=True)
    for location in route_locations:
        keys_to_delete = [key for key in location if key != "locations"]
        for key in keys_to_delete:
            del location[key]
    return route_locations



def get_poi_by_id(poi_id: str, language_id: str = "6d68e409-c46e-4d4a-8560-f15256e9cbb3"):
    """
    Obtiene un punto de interés (POI) por su ID.
    
    :param poi_id: ID del punto de interés a buscar.
    :return: Punto de interés encontrado o None si no se encuentra.
    """
    print("getting POI ID:", poi_id)
    poi = get_method("pois", {"id": poi_id})
    poi["title"] = get_text_by_lang(poi.get("titles", []), language_id)
    poi["description"] = get_text_by_lang(poi.get("descriptions", []), language_id)
    if poi:
        for key in ["_id", "titles", "descriptions"]:
            if key in poi:
                del poi[key]
    return poi



def get_languages():
    """
    Obtiene todos los idiomas disponibles.
    
    :return: Lista de idiomas.
    """
    languages = get_method("languages", {}, many=True)
    for language in languages:
        for key in ["_id"]:
            if key in language:
                del language[key]
    return languages



def get_route_types():
    """
    Obtiene todos los tipos de rutas disponibles.
    
    :return: Lista de tipos de rutas.
    """
    route_types =  get_method("route_types", {}, many=True)
    for route_type in route_types:
        for key in ["_id"]:
            if key in route_type:
                del route_type[key]
    return route_types

def get_pois_types(language_id: str = "6d68e409-c46e-4d4a-8560-f15256e9cbb3"):
    """
    Obtiene todos los tipos de puntos de interés (POIs) disponibles.
    
    :return: Lista de tipos de POIs.
    """
    types = []
    pois_types = get_method("pois_categories", {}, many=True)
    for pois_type in pois_types:
        for language in pois_type["languages"]:
            if language["language_id"] == language_id:
                text = language["name"]
                types.append({"id": pois_type["id"], "text": text})
    return types

def get_image_by_id(image_id: str):
    """
    Obtiene una imagen por su ID.
    
    :param image_id: ID de la imagen a buscar.
    :return: Imagen encontrada o None si no se encuentra.
    """
    image = get_image_gridfs(image_id)
    return image



def get_all_pois():
    """
    Obtiene todos los puntos de interés (POIs) disponibles.
    
    :return: Lista de POIs.
    """
    pois = get_method("pois", {}, many=True)
    for poi in pois:
        for key in ["_id", "titles", "descriptions", "address", "website", "booking", "minutes_duration", "rating", "planner_priority", "image_id"]:
            if key in poi:
                del poi[key]
    return pois


def get_all_routes_by_route_type(route_type: str, language_id: str = "6d68e409-c46e-4d4a-8560-f15256e9cbb3"):
    """
    Obtiene todas las rutas filtradas por tipo de ruta.
    
    :param route_type: Tipo de ruta a filtrar.
    :return: Lista de rutas que coinciden con el tipo especificado.
    """
    if not route_type:
        raise ValueError("El tipo de ruta no puede ser vacío.")
    routes = get_method("routes", {"route_type": route_type, "type": { "$nin": ["deactivated", "pilgrim"] }}, many=True)
    for route in routes:
        route["title"] = get_text_by_lang(route.get("titles", []), language_id)
        route["route"] = route['locations']['all_points']
        for key in ["_id", "titles", "short_descriptions", "long_descriptions", "stages", "locations", "updated_at", "owner_id", "image_id", "visibility", "distance", "type", "ratings"]:
            if key in route:
                del route[key]
    return routes


def register_user(fcm_token: str, id_token: str, latitude: float, longitude: float, email: str, timestamp: str):
    """
    Registra un nuevo usuario en la base de datos.
    
    :param fcm_token: Token de Firebase Cloud Messaging del usuario.
    :param id_token: Token de identificación del usuario.
    :param latitude: Latitud de la ubicación del usuario.
    :param longitude: Longitud de la ubicación del usuario.
    :param email: Correo electrónico del usuario.
    :param last_updated: Fecha y hora de la última actualización del usuario.
    :return: Datos del usuario registrado.
    """
    user_data = {
        "fcm_token": fcm_token,
        "id_token": id_token,
        "latitude": latitude,
        "longitude": longitude,
        "email": email,
        "last_updated": timestamp
    }
    user = post_method("users", user_data)
    if "_id" in user:
        del user["_id"]
    return user


def get_user_by_id(id_token: str):
    """
    Obtiene un usuario por su ID de token.
    
    :param id_token: Token de identificación del usuario.
    :return: Datos del usuario encontrado o None si no se encuentra.
    """
    filter = {"id_token": id_token}
    user = get_method("users", filter)
    if user and "_id" in user:
        del user["_id"]
    return user

def get_all_users():
    """
    Obtiene todos los usuarios registrados en la base de datos.
    
    :return: Lista de usuarios.
    """
    users = get_method("users", {}, many=True)
    for user in users:
        if "_id" in user:
            del user["_id"]
    return users

def update_user(fcm_token: str, id_token: str, latitude: float, longitude: float, email: str, timestamp: str):
    """
    Actualiza los datos de un usuario en la base de datos.
    
    :param fcm_token: Nuevo token de Firebase Cloud Messaging del usuario (opcional).
    :param id_token: Token de identificación del usuario (obligatorio).
    :param latitude: Nueva latitud de la ubicación del usuario (opcional).
    :param longitude: Nueva longitud de la ubicación del usuario (opcional).
    :param email: Nuevo correo electrónico del usuario (opcional).
    :param last_updated: Nueva fecha y hora de la última actualización del usuario (obligatorio).
    :return: Datos del usuario actualizado.
    """
    if not id_token:
        raise ValueError("El id_token es obligatorio para actualizar un usuario.")
    
    update_data = {
        "$set": {
            "last_updated": timestamp
        }
    }
    
    if fcm_token is not None:
        update_data["$set"]["fcm_token"] = fcm_token
    if latitude is not None:
        update_data["$set"]["latitude"] = latitude
    if longitude is not None:
        update_data["$set"]["longitude"] = longitude
    if email is not None:
        update_data["$set"]["email"] = email
    
    filter = {"id_token": id_token}
    update_method("users", filter, update_data)
    
    user = get_method("users", filter)
    if user and "_id" in user:
        del user["_id"]
    return user