from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.caches.cache import Cache
from gutenbergpy.utils import Utils

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings

import sqlite3

class SQLiteCache(Cache):
    #name of the sql commands batch file, used to create the db (should not change)
    DB_CREATE_CACHE_FILENAME    = 'gutenbergindex.db.sql'

    def __insertManyField(self,table,field,theSet):
        if len(theSet):
            query = 'INSERT OR IGNORE INTO %s(%s) VALUES (?)' % (table,field)
            self.cursor.executemany(query,map(lambda x: (x,) , theSet))

#TODO FINISH THIS
    def __insertManyFiled(self,table,theSet,**kwargs):
        fields = ''
        for key, value in kwargs.iteritems():
            fields =  fields +str(key)+','
        query = 'INSERT OR IGNORE INTO %s(%s) VALUES (?'+',?'*len(kwargs) + ')'
        insert_tuple = ( None,) * len(kwargs)
        idx = 0
        fields = ''
        for key,value in kwargs.iteritems():
            insert_tuple[idx] = value

    def __insertManyFieldId(self,table,field1,field2,theSet):
        if len(theSet):
            query = 'INSERT OR IGNORE INTO %s(%s, %s) VALUES (?,?)' % (table,field1,field2)
            insert_array = map(lambda x: (x[0],x[1]) , theSet)
            self.cursor.executemany(query,insert_array)

    def __insertLinks(self,ids,tablename,link1name,link2name,c):
        if len(ids):
            query = "INSERT INTO %s(%s,%s) VALUES (?,?)" % (tablename,link1name,link2name)
            self.cursor.executemany(query, ids)

    def create_cache(self, parse_results):
        self.connection = sqlite3.connect(GutenbergCacheSettings.CACHE_FILENAME)
        self.cursor     = self.connection.cursor()

        create_query = open(SQLiteCache.DB_CREATE_CACHE_FILENAME, 'r').read()
        self.cursor.executescript(create_query)
        self.connection.commit()

        for pt in parse_results.field_sets:
            if pt.needs_book_id():
                self.__insertManyFieldId(pt.tableName, 'name','bookid', pt.set)
            else:
                self.__insertManyField(pt.tableName, 'name', pt.set)

        self.__insertManyField('books','description',parse_results.books)

        total = len(parse_results.books)

        for idx, book in enumerate(parse_results.books):
            Utils.update_progress_bar("SQLite progress" ,idx,total)
            book_id = idx +1

            self.__insertLinks(map(lambda x: (x,book_id) , book.creator_name),'book_authors','authorid','bookid')
            self.__insertLinks(map(lambda x: (x,book_id) , book.subject),'book_subjects','subjectid','bookid')

            if len(book.language) > 0:
                self.cursor.execute("INSERT INTO book_languages(bookid,languageid) VALUES (?,?) ", (idx, book.language[0]))
            if len(book.book_shelf) > 0:
                self.cursor.execute("INSERT INTO bookshelve_book(bookid,bookshelveid) VALUES (?,?) ", (idx, book.book_shelf[0]))

        self.connection.commit()
        self.connection.close()

    def query(self,**kwargs):
        title =[]
        type  =[]
        language =[]
        author = []
        bookshelf = []
        files = []
        if kwargs.has_key('title'):
            title = kwargs['title']
        if kwargs.has_key('type'):
            type = kwargs['type']
        if kwargs.has_key('language'):
            language = kwargs['language']
        if kwargs.has_key('author'):
            author = kwargs['author']
        if kwargs.has_key('bookshelf'):
            bookshelf = kwargs['bookshelf']
        if kwargs.has_key('files'):
            files = kwargs['files']

        query = "select titles.name as booktitle, languages.name as language from titles, books,book_titles,book_languages, languages where " \
                "titles.id = book_titles.title_id and"\
                "books.id = book_titles.book_id and"\
                "book_languages.bookid = books.id and"\
                "book_languages.languageid = languages.id and"\
                "languages.name = language"