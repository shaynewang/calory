from .nutritionix import api
from .cache_data import nutrition_cache

DEBUG = False

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
    if DEBUG: print("Getting nutrition info for {0} from cache".format(food_name))
    if not cached:
        if DEBUG: print("making api call",food_name)
        response = nxapi.common_food_nutrition(food_name)
        if not response:
            response = {"food_name":food_name}
        # cache result for both foodname in the query and response
        saved = update_cached_info(response)
        response.update({"food_name":food_name})
        saved = update_cached_info(response)
        if DEBUG: print("saved result to cache: ", saved)
        return get_cached_info(food_name)
    return cached

def get_calories(food_name):
    """
    Return food name and its calories per serving
    """
    try:
        query_result = get_foodinfo(food_name)
    except Exception as e:
        if "limits exceeded" in str(e):
            return str(e) + ", only displaying cached calories information."
    # return empty string if no calories information available
    if not query_result or "nf_calories" not in query_result.keys():
        return ""
    return "{0}: {1} calories per {2}".format(query_result["food_name"],
            int(query_result["nf_calories"]/query_result["serving_qty"]),
            query_result["serving_unit"])
