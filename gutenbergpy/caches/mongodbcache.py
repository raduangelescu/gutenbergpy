from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.caches.cache import Cache
from gutenbergpy.utils import Utils
from gutenbergpy.parse.cachefields import Fields
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings


from pymongo import MongoClient


##
# SQLite cache implementation
class MongodbCache(Cache):

    def __init__(self):
        self.client = MongoClient(GutenbergCacheSettings.MONGO_DB_CONNECTION_SERVER)
        self.db = self.client.mongodbgutenbergcache

    def __get_book_json(self,parseItem,fields):
        book_dict ={}

        book_dict['publisher']      = fields[Fields.PUBLISHER].set[parseItem.publisher_id-1] if parseItem.publisher_id and parseItem.publisher_id != -1 else 'None'
        book_dict['rights']         = fields[Fields.RIGHTS].set[parseItem.rights_id-1] if parseItem.rights_id and parseItem.rights_id != -1 else 'None'
        book_dict['language']       = fields[Fields.LANGUAGE].set[parseItem.language_id-1] if parseItem.language_id and parseItem.language_id != -1 else 'None'
        book_dict['book_shelf']     = fields[Fields.BOOKSHELF].set[parseItem.bookshelf_id-1] if parseItem.bookshelf_id and parseItem.bookshelf_id != -1 else 'None'
        book_dict['gutenberg_book_id'] = parseItem.gutenberg_book_id
        book_dict['date_issued']    = parseItem.date_issued
        book_dict['num_downloads']  = parseItem.num_downloads

        book_dict['titles']         = map(lambda x: x[0] , fields[Fields.TITLE].set[[x - 1 for x in parseItem.titles_id]])  if parseItem.titles_id and parseItem.titles_id != -1 else ['None']
        book_dict['subjects']       = map(lambda x: x , fields[Fields.SUBJECT].set[[x - 1 for x in parseItem.subjects_id]]) if parseItem.subjects_id and parseItem.subjects_id != -1 else ['None']
        book_dict['authors']        = map(lambda x: x , fields[Fields.AUTHOR].set[[x - 1 for x in parseItem.authors_id]]) if parseItem.authors_id and parseItem.authors_id != -1 else ['None']
        book_dict['files']          = map(lambda x: x[0] , fields[Fields.FILES].setLinks[[x - 1 for x in parseItem.files_id]]) if parseItem.files_id and parseItem.files_id != -1 else ['None']
        book_dict['type']           = fields[Fields.TYPE].set[parseItem.type_id-1]  if parseItem.type_id and parseItem.type_id != -1 else 'None'
        return book_dict
    ##
    # Create the MongoDB cache
    def create_cache(self, parse_results):
        self.db.books.drop()
        book_collection = self.db.books
        total = len (parse_results.books)

        for idx,book in enumerate(parse_results.books):
            Utils.update_progress_bar("MongoDB progress", idx, total)
            json = self.__get_book_json(book,parse_results.field_sets)
            self.db.books.insert_one(json)

    def query(self,**kwargs):
        query = {}
        if kwargs.has_key('languages'):
            query['languages'] = kwargs['languages']
        if kwargs.has_key('authors'):
            query['authors'] = kwargs['authors']
        if kwargs.has_key('types'):
            query['types'] = kwargs['types']
        if kwargs.has_key('titles'):
            query['titles'] = kwargs['titles']
        if kwargs.has_key('subjects'):
            query['subjects'] = kwargs['subjects']
        if kwargs.has_key('publishers'):
            query['publishers'] = kwargs['publishers']
        if kwargs.has_key('bookshelves'):
            query['bookshelves'] = kwargs['bookshelves']

        print self.db.books.find(query)
    ##
    # Native query function implementation
    def native_query(self,sql_query):
        pass