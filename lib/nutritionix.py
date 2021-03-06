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

    def common_food_nutrition(self, food):
        """
        Get nutrition values for natural foods
        using Nutritionx API
        """
        headers = {
                   "x-app-id":self.x_app_id,
                   "x-app-key":self.x_app_key,
                   }
        common_query = "/natural/nutrients?query={food}".format(food=food)
        request_url = self.end_point+common_query
        try:
            b = {"query":food}
            response = requests.post(request_url,headers=headers,data=b)
            if response.status_code == 200:
                food_list = json.loads(response.text)
                return food_list["foods"][0]
            else:
                if "We couldn't match any of your foods" in response.text:
                    return ""
                elif response.status_code == 401 or response.text["message"] == "usage limits exceeded":
                    raise Exception("api usage limits exceeded")
                print(response.status_code,response.text)
        except Exception as e:
            raise e
        return ""

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
                food_list = json.loads(response.text)
                if mode == "first branded":
                    return food_list["branded"][0]
                else:
                    # maybe insert better logic to 
                    # return more accurate search result
                    raise Exception("Invalid mode.")
        except Exception as e:
            raise e
        return "error"

if __name__ == "__main__":
    nxapi= api()
