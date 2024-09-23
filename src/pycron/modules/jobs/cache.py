import json
import os

class Cache:
    def __init__(self, id: str, **kwargs):
        self.id = id
        self.cache = {}
        path_prefix = kwargs.get("prefix", os.path.dirname(__file__))
        self.path = f"{path_prefix}/.cache"

    def load(self):
        with open(self.path, "r") as file:
            self.cache = json.load(file)

    def dump(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(self.path + f"/{self.id}.json", "x") as file:
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
