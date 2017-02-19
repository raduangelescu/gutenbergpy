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

    def create_or_dict(self,name,newname, dt,out):
        if dt.has_key(name):
            dict = {}
            lst = []
            for e in dt[name]:
                lst.append ({name:e})
            out.extend(lst)

    def query(self,**kwargs):
        query = {}
        lst = []
        self.create_or_dict('languages','languages',kwargs,lst)
        self.create_or_dict('authors','authors', kwargs, lst)
        self.create_or_dict('types','type', kwargs, lst)
        self.create_or_dict('titles', 'titles', kwargs, lst)
        self.create_or_dict('subjects', 'subjects', kwargs, lst)
        self.create_or_dict('publishers', 'publisher', kwargs, lst)
        self.create_or_dict('bookshelves', 'bookshelves', kwargs, lst)
        self.create_or_dict('gutenberg_book_id', 'gutenberg_book_id', kwargs, lst)
        query['$or'] = lst
        lst =[]
        for res in  self.native_query(query):
            lst.append(res["gutenberg_book_id"])
        return lst
    ##
    # Native query function implementation
    def native_query(self,mongodb_query):
        return self.db.books.find(mongodb_query)