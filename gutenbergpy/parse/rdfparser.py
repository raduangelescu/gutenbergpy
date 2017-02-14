from os   import listdir
from lxml import etree

from gutenbergpy.parse.cachefields      import Fields
from gutenbergpy.parse.book             import Book
from gutenbergpy.parse.parseitem        import ParseItem
from gutenbergpy.parse.parseitemfile    import ParseItemFiles
from gutenbergpy.parse.rdfparseresults  import RDFParseResults
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.utils                  import Utils


class RdfParser:

    def do(self):
        result = RDFParseResults()

        result.field_sets = Fields.FIELD_COUNT * [None]
        result.field_sets[Fields.TITLE]     = ParseItem(tablename='titles',xpath=['//dcterms:title/text()'])
        result.field_sets[Fields.SUBJECT]   = ParseItem(tablename='subjects', xpath =['//dcterms:subject/rdf:Description/rdf:value/text()'])
        result.field_sets[Fields.TYPE]      = ParseItem(tablename='types', xpath =['//dcterms:type/rdf:Description/rdf:value/text()'])
        result.field_sets[Fields.LANGUAGE]  = ParseItem(tablename='languages', xpath =['//dcterms:language/rdf:Description/rdf:value/text()','//dcterms:alternative/text()'])
        result.field_sets[Fields.AUTHOR]    = ParseItem(tablename='authors', xpath =['//dcterms:creator/pgterms:agent/pgterms:alias/text()','//dcterms:creator/pgterms:agent/pgterms:name/text()'])
        result.field_sets[Fields.BOOKSHELF] = ParseItem(tablename='bookshelves', xpath =['//pgterms:bookshelf/rdf:Description/rdf:value/text()'])
        result.field_sets[Fields.FILES]     = ParseItemFiles(tablename='downloadlinks', xpath =['//pgterms:file'])
        result.field_sets[Fields.PUBLISHER] = ParseItemFiles(tablename='publishers', xpath =['//dcterms:publisher/text()'])
        result.field_sets[Fields.RIGHTS]    = ParseItemFiles(tablename='rights', xpath =['//dctterms:rights/text()'])


        dirs  =  listdir(GutenbergCacheSettings.CACHE_RDF_UNPACK_DIRECTORY)
        total = len(dirs)

        for idx, dir in enumerate(dirs):

            processing_str = "Processing progress: %d / %d" % (idx,total)
            Utils.update_progress_bar(processing_str,idx,total)
            file_path = "%s%s\pg%s.rdf".(GutenbergCacheSettings.CACHE_RDF_UNPACK_DIRECTORY,dir,dir   )
            doc = etree.parse(file_path,etree.ETCompatXMLParser())

            res = Fields.FIELD_COUNT * [None]
            for idx, pt in enumerate(result.field_sets):
                res[idx] = pt.do(doc)

            gutenberg_book_id = int(dir);
            description_text  = doc.xpath('//dcterms:description/text()', namespaces=GutenbergCacheSettings.NS)[0]
            #TODO FORMAT DATA
            date_issued       = doc.xpath('//dcterms:issued/text()', namespaces=GutenbergCacheSettings.NS)[0]
            rights_text       = doc.xpath('//dcterms:rights/text()',namespaces=GutenbergCacheSettings.NS)[0]
            num_downloads     = doc.xpath('//pgterms:downloads/text()',namespaces=GutenbergCacheSettings.NS)[0]

            newbook = Book(description_text,res[Fields.PUBLISHER],rights_text,res[Fields.LANGUAGE],
                           res[Fields.BOOKSHELF],gutenberg_book_id,date_issued,num_downloads,
                           res[Fields.TITLE],res[Fields.SUBJECT],res[Fields.TYPE],res[Fields.AUTHOR],res[Fields.FILES])

            result.books.append(newbook)

        return result