from gutenbergpy.gutenbergcache import GutenbergCache
import gutenbergpy.textget
import cProfile

def test_func():
    GutenbergCache.create(refresh=False, download=False, unpack=False, parse=True, cache=True, deleteTemp=False)

#GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=False)
GutenbergCache.create(refresh=False, download=False, unpack=False, parse=True, cache=True, deleteTemp=False)
cache  = GutenbergCache.get_cache()
#languages authors types titles subjects publishers bookshelves
print cache.query(downloadtype=['application/plain','text/plain','text/html; charset=utf-8'])
print gutenbergpy.textget.strip_headers(gutenbergpy.textget.get_text_by_id(1000))
#cProfile.run('test_func()')
