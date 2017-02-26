from __future__ import print_function
from os import path
import time
from utils import Utils

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.parse.rdfparser import RdfParser
from gutenbergpy.caches.sqlitecache import SQLiteCache
from gutenbergpy.caches.mongodbcache import MongodbCache

##
# Cache types
# noinspection PyClassHasNoInit
class GutenbergCacheTypes:
    CACHE_TYPE_SQLITE  = 0
    CACHE_TYPE_MONGODB = 1


##
# The main class (only this should be used to interface the cache)
class GutenbergCache:
    ##
    # Get the cache by type
    @staticmethod
    def get_cache(type=GutenbergCacheTypes.CACHE_TYPE_SQLITE):
            if type == GutenbergCacheTypes.CACHE_TYPE_SQLITE:
                return SQLiteCache()
            elif type == GutenbergCacheTypes.CACHE_TYPE_MONGODB:
                return MongodbCache()
            print("CACHE TYPE UNKNOWN")
            return None

    ##
    # Create the cache
    @staticmethod
    def create(**kwargs):
        cache_type  = GutenbergCacheTypes.CACHE_TYPE_SQLITE if kwargs.has_key('type') is False else kwargs['type']
        refresh     = True  if kwargs.has_key('refresh') is False else kwargs['refresh']
        download    = True  if kwargs.has_key('download') is False else kwargs['download']
        unpack      = True  if kwargs.has_key('unpack') is False else kwargs['unpack']
        parse       = True  if kwargs.has_key('parse') is False else kwargs['parse']
        deleteTmp   = True  if kwargs.has_key('deleteTemp') is False else kwargs['deleteTemp']

        if path.isfile(GutenbergCacheSettings.CACHE_FILENAME) and refresh and cache_type == GutenbergCacheTypes.CACHE_TYPE_SQLITE:
            print('Cache already exists')
            return

        if refresh:
            print('Deleting old files')
            Utils.delete_tmp_files(True)

        if download:
            Utils.download_file()

        if unpack:
            Utils.unpack_tarbz2()

        if parse:
            t0 = time.time()
            parser = RdfParser()
            result = parser.do()
            print('RDF PARSING took ' + str(time.time() - t0))

            if kwargs['cache']:
                t0 = time.time()
                cache = GutenbergCache.get_cache(cache_type)
                cache.create_cache(result)
                print('sql took %f' % (time.time() - t0))

        if deleteTmp:
            print('Deleting temporary files')
            Utils.delete_tmp_files()

        print('Done')
