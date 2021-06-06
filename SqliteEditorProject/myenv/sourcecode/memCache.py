from pymemcache.client import base
import json

client = base.Client(('localhost', 11211))

class memCache:
    def __init__(self):
        self.client = base.Client(('localhost', 11211))

    def setCache(self, key, value):
        self.client.set(key, str(value), expire=3*24*60*60)
    
    def getCache(self, key):
        return self.client.get(key).decode("utf-8").replace("'", '"')
    
    def delete_key(self, key):
        return self.client.delete(key)