from gutenbergpy.gutenbergcache import GutenbergCache

#do everything
#GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=False)

#just do parsing and cache without deleting the cache
GutenbergCache.create(refresh=False, download=False, unpack=False, parse=True, cache=True, deleteTemp=False)
