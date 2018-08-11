from .nutritionix import api
from .cache_data import nutrition_cache

nxapi = api()
cache_client = nutrition_cache()

def get_cached_info(food_name):
    """
    Get food info from cache
    """
    cached = cache_client.select(food_name)
    if cached:
        return cached[0]
    return None

def update_cached_info(food_info):
    """
    Inset food info to cache
    """
    return cache_client.insert(food_info)

def get_foodinfo(food_name):
    """
    get food info from cache or
    make an api call
    """
    cached = get_cached_info(food_name)
    #print("cached: ", cached)
    if not cached:
        print("making api call",food_name)
        response = nxapi.common_food_nutrition(food_name)
        if not response:
            response = {"food_name":food_name}
        print(response)
        saved = update_cached_info(response)
        print("saved: ", saved)
        return get_cached_info(food_name)
    return cached

def get_calories(food_name):
    """
    Return food name and its calories per serving
    """
    query_result = get_foodinfo(food_name)
    if not query_result or "nf_calories" not in query_result.keys():
        return ""
    return "{0}: {1} Cal per {2}".format(query_result["food_name"],
            query_result["nf_calories"]/query_result["serving_qty"],
            query_result["serving_unit"])
