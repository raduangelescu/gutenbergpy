from os   import path
from time import time
from utils import Utils

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.parse.rdfparser        import RdfParser
from gutenbergpy.caches.sqlitecache      import SQLiteCache

'''  'publisher':ParseTemp(tablename='publishers',xpath='//dcterms:publisher/text()'),
    'description':ParseTemp(tablename='description',xpath='//dcterms:description/text()'),'''


class GutenbergCache:

    @staticmethod
    def create(refresh = False):

        if path.isfile(GutenbergCacheSettings.CACHE_FILENAME) and refresh is False:
            print 'Cache already exists'
            return

        if refresh is True:
            Utils.delete_tmp_files(True)

        Utils.download_file()
        Utils.unpack_tarbz2()

        t0 = time.time()
        parser = RdfParser()
        result = parser.do()
        print 'RDF PARSING took ' + str(time.time() - t0)

        t0 = time.time()
        cache = SQLiteCache()
        cache.create_cache(result)
        print 'sql took %f' % (time.time() - t0)


        print 'Deleting temporary files'
        GutenbergCache.delete_tmp_files(True)
        print 'Done'



''' query english books
select titles.name as booktitle, languages.name as language from titles, books,book_titles,book_languages, languages where
titles.id = book_titles.title_id and
books.id = book_titles.book_id and
book_languages.bookid = books.id and
book_languages.languageid = languages.id and
languages.name = "en"
'''
