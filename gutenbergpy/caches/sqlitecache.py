from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.caches.cache import Cache
from gutenbergpy.utils import Utils
from gutenbergpy.parse.cachefields import Fields
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings

import sqlite3

class SQLiteCache(Cache):
    #name of the sql commands batch file, used to create the db (should not change)
    DB_CREATE_CACHE_FILENAME         = 'gutenbergindex.db.sql'
    DB_CREATE_CACHE_INDICES_FILENAME = 'gutenbergindex_indices.db.sql'

    def __init__(self):
        self.cursor     = None
        self.connection = None
        self.table_map = [None] * Fields.FIELD_COUNT

        self.table_map[Fields.TITLE]    =   'titles'
        self.table_map[Fields.SUBJECT]  =   'subjects'
        self.table_map[Fields.TYPE]     =   'types'
        self.table_map[Fields.LANGUAGE] =   'languages'
        self.table_map[Fields.AUTHOR]   =   'authors'
        self.table_map[Fields.BOOKSHELF]=   'bookshelves'
        self.table_map[Fields.FILES]    =   '/---/'
        self.table_map[Fields.PUBLISHER]=   'publishers'
        self.table_map[Fields.RIGHTS]   =   'rights'

    def __insertManyField(self,table,field,theSet):
        if len(theSet):
            query = 'INSERT OR IGNORE INTO %s(%s) VALUES (?)' % (table,field)
            self.cursor.executemany(query,map(lambda x: (x,) , theSet))


    def __insertManyFieldId(self,table,field1,field2,theSet):
        if len(theSet):
            query = 'INSERT OR IGNORE INTO %s(%s, %s) VALUES (?,?)' % (table,field1,field2)
            insert_array = map(lambda x: (x[0],x[1]) , theSet)
            self.cursor.executemany(query,insert_array)

    def __insertLinks(self,ids,tablename,link1name,link2name):
        if len(ids):
            query = "INSERT INTO %s(%s,%s) VALUES (?,?)" % (tablename,link1name,link2name)
            self.cursor.executemany(query, ids)

    def create_cache(self, parse_results):
        self.connection = sqlite3.connect(GutenbergCacheSettings.CACHE_FILENAME)
        self.cursor     = self.connection.cursor()

        create_query = open(SQLiteCache.DB_CREATE_CACHE_FILENAME, 'r').read()
        self.cursor.executescript(create_query)
        self.connection.commit()

        for idx,pt in enumerate(parse_results.field_sets):
            if idx == Fields.FILES:
                self.__insertManyField('downloadlinkstype','name', pt.setTypes )
                self.cursor.executemany(
                    'INSERT OR IGNORE INTO downloadlinks(name,bookid,downloadtypeid) VALUES (?,?,?)'
                    , map(lambda x: (x[0], x[1], x[2]), parse_results.field_sets[Fields.FILES].setLinks))

            elif pt.needs_book_id():
                self.__insertManyFieldId(self.table_map[idx], 'name','bookid', pt.set)
            else:
                self.__insertManyField(self.table_map[idx], 'name', pt.set)


        total = len(parse_results.books)



        for idx, book in enumerate(parse_results.books):
            Utils.update_progress_bar("SQLite progress" ,idx,total)
            book_id = idx +1
            self.__insertLinks(map(lambda x: (x,book_id) , book.authors_id),'book_authors','authorid','bookid')
            self.__insertLinks(map(lambda x: (x,book_id) , book.subjects_id),'book_subjects','subjectid','bookid')

            self.cursor.execute("INSERT OR IGNORE INTO books(publisherid,dateissued,rightsid,numdownloads,languageid,bookshelveid,gutenbergbookid,typeid) " \
                    "VALUES (?,?,?,?,?,?,?,?)" , (book.publisher_id, book.date_issued, book.rights_id,
                                                book.num_downloads,book.language_id,book.bookshelf_id,book.gutenberg_book_id,book.type_id))

        self.connection.commit()

        create_indices_query = open(SQLiteCache.DB_CREATE_CACHE_INDICES_FILENAME, 'r').read()
        self.cursor.executescript(create_indices_query)
        self.connection.commit()


        self.connection.close()

    def query(self,**kwargs):
        class HelperQuery:
            def __init__(self, tables, query_struct):
                self.tables         = tables
                self.query_struct   = query_struct
        helpers=[
            HelperQuery(['languages'], ('languages.id = books.languageid', 'languages.name',
                        kwargs['languages'] if kwargs.has_key('languages') else None)),
            HelperQuery(['authors', 'book_authors'],
                        ('authors.id = book_authors.authorid and books.id = book_authors.bookid', 'authors.name',
                         kwargs['authors'] if kwargs.has_key('authors') else None)),
            HelperQuery(['types'],('books.typeid = types.id', 'types.name',
                         kwargs['types'] if kwargs.has_key('types') else None)),
            HelperQuery(['titles'],('titles.bookid = books.id', 'titles.name',
                         kwargs['titles'] if kwargs.has_key('titles') else None)),
            HelperQuery(['subjects', 'book_subjects'],
                        ('subjects.id = book_subjects.bookid and books.id = book_subjects.subjectid ', 'subjects.name',
                         kwargs['subjects'] if kwargs.has_key('subjects') else None)),
            HelperQuery(['publishers'],
                        ('publishers.id = books.publisherid', 'publishers.name',
                         kwargs['publishers'] if kwargs.has_key('publishers') else None)),
            HelperQuery(['bookshelves'],
                        ('bookshelves.id = books.bookshelveid', 'bookshelves.name',
                         kwargs['bookshelves'] if kwargs.has_key('bookshelves') else None)),
            HelperQuery(['downloadlinks','downloadlinkstype'],
                        ('downloadlinks.downloadtypeid =  downloadlinkstype.id and downloadlinks.bookid = books.id', 'downloadlinkstype.name',
                         kwargs['downloadtype'] if kwargs.has_key('downloadtype') else None))
        ]
        runtime  = list(filter(lambda x: x.query_struct[2] , helpers))

        query = "SELECT DISTINCT books.gutenbergbookid FROM books";
        for q in runtime:
            query = "%s,%s"% (query ,','.join(map(str,  q.tables)))
        query = "%s WHERE "%(query)

        for idx,q in enumerate(runtime):
            query = "%s %s and %s in (%s) " % (query,q.query_struct[0],q.query_struct[1],','.join(map(lambda x: "'%s'"%(str(x)), q.query_struct[2])))
            if idx != len(runtime) -1:
                query = "%s and "%(query)

        res = []
        for row in self.native_query(query):
            res.append(int(row[0]))

        return res

    def native_query(self,sql_query):
        if self.cursor is None or self.connection is None:
            self.connection = sqlite3.connect(GutenbergCacheSettings.CACHE_FILENAME)
            self.cursor     = self.connection.cursor()

        return self.cursor.execute(sql_query)
