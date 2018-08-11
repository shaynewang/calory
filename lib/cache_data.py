import random
from datetime import datetime
from google.cloud import datastore

"""
Cache nutrition data when a query is made
"""

class nutrition_cache():
    kind = 'Nutrition'
    store = None
    seed = None
    sample = "sample.json"
    
    def __init__(self):
        self.store = datastore.Client()
        self.seed = random.seed()
    
    def _get_random_id(self):
        return int(random.uniform(0,1) * 100000000)

    def _get_schema(self):
        with open(self.sample,'r') as f:
            sample = json.loads(f.read())
        return sample
    
    def insert(self, food_info):
        """
        insert nutrition information to cache database
        """
        try:
            rid = self._get_random_id()
            random_key = self.store.key(self.kind,rid)
            food_entry = datastore.Entity(key=random_key)
            food_entry.update(food_info)
            self.store.put(food_entry)
        except Exception as e:
            raise e
            return False
        return True
    
    def get_available_food(self):
        """
        get all available food names 
        """
        query = self.store.query(kind=self.kind)
        response = query.fetch()
        return set([entity["food_name"] for entity in response])
    
    
    def select(self, food_name):
        """
            Select nutrition info for food
        """
        query = self.store.query(kind=self.kind)
        query.add_filter("food_name","=",food_name)
        response = query.fetch()
        return [entity for entity in response]
