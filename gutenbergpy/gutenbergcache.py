from __future__ import print_function
from os import path
import time
from utils import Utils

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.parse.rdfparser import RdfParser
from gutenbergpy.caches.sqlitecache import SQLiteCache


##
# Cache types
# noinspection PyClassHasNoInit
class GutenbergCacheTypes:
    CACHE_TYPE_SQLITE = 0


##
# The main class (only this should be used to interface the cache)
class GutenbergCache:
    ##
    # Get the cache by type
    @staticmethod
    def get_cache(type=GutenbergCacheTypes.CACHE_TYPE_SQLITE):
        if path.isfile(GutenbergCacheSettings.CACHE_FILENAME):
            if type == GutenbergCacheTypes.CACHE_TYPE_SQLITE:
                return SQLiteCache()
        else:
            print("NO CACHE FOUND, PLEASE CALL create() FUNCTION TO POPULATE CACHE")

    ##
    # Create the cache
    @staticmethod
    def create(**kwargs):

        if path.isfile(GutenbergCacheSettings.CACHE_FILENAME) and kwargs['refresh'] == True:
            print('Cache already exists')
            return

        if kwargs['refresh']:
            print('Deleting old files')
            Utils.delete_tmp_files(True)

        if kwargs['download']:
            Utils.download_file()

        if kwargs['unpack']:
            Utils.unpack_tarbz2()

        if kwargs['parse']:
            t0 = time.time()
            parser = RdfParser()
            result = parser.do()
            print('RDF PARSING took ' + str(time.time() - t0))

            if kwargs['cache']:
                t0 = time.time()
                cache = SQLiteCache()
                cache.create_cache(result)
                print('sql took %f' % (time.time() - t0))

        if kwargs['deleteTemp']:
            print('Deleting temporary files')
            Utils.delete_tmp_files()
        print('Done')
