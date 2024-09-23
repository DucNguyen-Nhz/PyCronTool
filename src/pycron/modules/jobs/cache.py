import json
import os
import logging

class Cache:
    def __init__(self, id: str, **kwargs):
        self._id = id
        self.cache = {}
        path_prefix = kwargs.get("prefix", os.path.dirname(__file__))
        self.path = f"{path_prefix}/.cache"

    def load(self):
        with open(self.path + f"/{self._id}.json", "r") as file:
            self.cache = json.load(file)

    def dump(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            logging.info(f"Creating cache directory {self.path}")

        logging.info(f"Dumping cache to {self.path}/{self._id}.json")

        with open(self.path + f"/{self._id}.json", "x") as file:
            json.dump(self.cache, file)

    def add(self, key, value):
        self.cache[key] = value

    def get(self, key):
        return self.cache.get(key, None)

    def remove(self, key):
        if key in self.cache:
            del self.cache[key]
        raise KeyError(f"Key {key} not found in cache")

    def clear(self):
        self.cache.clear()
