from gutenbergpy.gutenbergcache import GutenbergCache
import gutenbergpy.textget

#create from scratch
GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=False)
#get cache
cache  = GutenbergCache.get_cache()
#languages authors types titles subjects publishers bookshelves
#query ids
print cache.query(downloadtype=['application/plain','text/plain','text/html; charset=utf-8'])
#print stripped text
print gutenbergpy.textget.strip_headers(gutenbergpy.textget.get_text_by_id(1000))
