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

    def search(self, food):
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
                return response.text
        except Exception as e:
            raise e
        return "error"

if __name__ == "__main__":
    nxapi= api()
    r = nxapi.search("pepperoni pizza")
    print(r)
    print(json.dumps(r))


