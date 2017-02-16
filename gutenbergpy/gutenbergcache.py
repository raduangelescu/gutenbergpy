from os   import path
import time
from utils import Utils

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.parse.rdfparser        import RdfParser
from gutenbergpy.caches.sqlitecache      import SQLiteCache


class GutenbergCache:

    @staticmethod
    def create(**kwargs):

        if path.isfile(GutenbergCacheSettings.CACHE_FILENAME) and kwargs['refresh'] == True :
            print 'Cache already exists'
            return

        if kwargs['refresh'] == True:
            print 'Deleting old files'
            Utils.delete_tmp_files(True)

        if kwargs['download'] == True:
            Utils.download_file()

        if kwargs['unpack'] == True:
            Utils.unpack_tarbz2()

        if kwargs['parse'] == True:
            t0 = time.time()
            parser = RdfParser()
            result = parser.do()
            print 'RDF PARSING took ' + str(time.time() - t0)

        if kwargs['cache'] == True:
            t0 = time.time()
            cache = SQLiteCache()
            cache.create_cache(result)
            print 'sql took %f' % (time.time() - t0)

        if kwargs['deleteTemp'] == True:
            print 'Deleting temporary files'
            GutenbergCache.delete_tmp_files(True)
        print 'Done'
