from gutenbergpy.gutenbergcache import GutenbergCache
from gutenbergpy.caches.sqlitecache import SQLiteCache
import cProfile
#do everything
#GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=False)

#just do parsing and cache without deleting the cache

def test_func():
    GutenbergCache.create(refresh=False, download=False, unpack=False, parse=True, cache=True, deleteTemp=False)

#GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=False)
#GutenbergCache.create(refresh=False, download=False, unpack=False, parse=True, cache=True, deleteTemp=False)
cache  = GutenbergCache.get_cache()
#languages authors types titles subjects publishers bookshelves
print cache.query(downloadtype=['application/plain','text/plain','text/html; charset=utf-8'])
#cProfile.run('test_func()')
