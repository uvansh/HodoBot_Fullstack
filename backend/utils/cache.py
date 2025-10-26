class QueryCache:
    def __init__(self,max_size=100):
        self.cache = {}
        self.max_size = max_size
        
    def get(self, key):
        return self.cache.get(key, None)
    
    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            self.cache.pop(next(iter(self.cache)))
            self.cache[key] = value
        else:
            self.cache[key] = value
            
    def clear(self):
        self.cache = {}
        query_cache = QueryCache(max_size=100)
        
        return query_cache