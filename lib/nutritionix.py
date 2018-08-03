import os
import json
import requests

"""
Nutritionix API for
making requests for food items
then return calories information
on requested food items
"""
class api:
    def __init__(self):
        self.end_point = "https://trackapi.nutritionix.com/v2"
        self.x_app_id  = os.getenv("NUTRITIONIX_APP_ID")
        self.x_app_key = os.getenv("NUTRITIONIX_KEY")

    def search(self, food, mode="first branded"):
        """
        Search for food in nutritionix database
        then return json as string
        """
        headers = {
                   "x-app-id":self.x_app_id,
                   "x-app-key":self.x_app_key,
                   }
        query = "/search/instant?query={food}".format(food=food)
        request_url = self.end_point+query
        try:
            response = requests.get(request_url,headers=headers)
            if response.status_code == 200:
                # 20 branded and 20 common foods results are
                # returned but we are only using the top result
                if mode == "first common":
                    # no calories information available
                    return json.loads(response.text)["common"][0]
                elif mode == "first branded":
                    return json.loads(response.text)["branded"][0]
                else:
                    # maybe insert better logic to 
                    # return more accurate search result
                    raise Exception("Invalid mode.")
        except Exception as e:
            raise e
        return "error"

    def get_calories(self, food, mode="first branded"):
        """
        Return food name and its calories per serving
        """
        query_result = self.search(food,mode)
        return "{0}: {1} Cal per {2}".format(query_result["food_name"],
                query_result["nf_calories"]/query_result["serving_qty"],
                query_result["serving_unit"])

if __name__ == "__main__":
    nxapi= api()
    print(nxapi.get_calories("pepperoni pizza"))
    print(nxapi.get_calories("Godiva Chocolate"))
    print(nxapi.get_calories("Granny Smith apple"))
