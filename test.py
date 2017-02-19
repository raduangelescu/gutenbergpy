from __future__ import print_function
import gutenbergpy.textget
from gutenbergpy.gutenbergcache import GutenbergCache

# create cache from scratchfrom scratch
GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=True)
# get the default cache (SQLite)
cache = GutenbergCache.get_cache()
# For the query function you can use the following fields: languages authors types titles subjects publishers bookshelves
print(cache.query(downloadtype=['application/plain', 'text/plain', 'text/html; charset=utf-8']))
# Print stripped text
print(gutenbergpy.textget.strip_headers(gutenbergpy.textget.get_text_by_id(1000)))
