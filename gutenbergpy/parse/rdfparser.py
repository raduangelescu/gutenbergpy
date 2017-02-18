from os   import listdir
from lxml import etree

from gutenbergpy.parse.cachefields      import Fields
from gutenbergpy.parse.book             import Book
from gutenbergpy.parse.parseitem        import ParseItem
from gutenbergpy.parse.parseitemfile    import ParseItemFiles
from gutenbergpy.parse.parseitemtitles  import ParseItemTitles
from gutenbergpy.parse.rdfparseresults  import RDFParseResults
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.utils                  import Utils


class RdfParser:

    def do(self):
        result = RDFParseResults()

        result.field_sets = Fields.FIELD_COUNT * [None]
        result.field_sets[Fields.TITLE]     = ParseItemTitles(xpath=['//dcterms:title/text()','//dcterms:alternative/text()'])
        result.field_sets[Fields.SUBJECT]   = ParseItem(xpath =['//dcterms:subject/rdf:Description/rdf:value/text()'])
        result.field_sets[Fields.TYPE]      = ParseItem(xpath =['//dcterms:type/rdf:Description/rdf:value/text()'])
        result.field_sets[Fields.LANGUAGE]  = ParseItem(xpath =['//dcterms:language/rdf:Description/rdf:value/text()'])
        result.field_sets[Fields.AUTHOR]    = ParseItem(xpath =['//dcterms:creator/pgterms:agent/pgterms:alias/text()','//dcterms:creator/pgterms:agent/pgterms:name/text()'])
        result.field_sets[Fields.BOOKSHELF] = ParseItem(xpath =['//pgterms:bookshelf/rdf:Description/rdf:value/text()'])
        result.field_sets[Fields.FILES]     = ParseItemFiles(xpath =['//dcterms:hasFormat'])
        result.field_sets[Fields.PUBLISHER] = ParseItem(xpath =['//dcterms:publisher/text()'])
        result.field_sets[Fields.RIGHTS]    = ParseItem( xpath =['//dcterms:rights/text()'])


        dirs  =  listdir(GutenbergCacheSettings.CACHE_RDF_UNPACK_DIRECTORY)
        total = len(dirs)

        for idx, dir in enumerate(dirs):
            processing_str = "Processing progress: %d / %d" % (idx,total)
            Utils.update_progress_bar(processing_str,idx,total)
            file_path = "%s%s\pg%s.rdf" % (GutenbergCacheSettings.CACHE_RDF_UNPACK_DIRECTORY,dir,dir)
            doc = etree.parse(file_path,etree.ETCompatXMLParser())

            res = Fields.FIELD_COUNT * [-1]
            for idx_field, pt in enumerate(result.field_sets):
                if not pt.needs_book_id():
                    res[idx_field] = pt.do(doc)
                else:
                    res[idx_field] = pt.do(doc,idx+1)

            gutenberg_book_id = int(dir);

            date_issued_x   = doc.xpath('//dcterms:issued/text()', namespaces=GutenbergCacheSettings.NS)
            num_downloads_x = doc.xpath('//pgterms:downloads/text()',namespaces=GutenbergCacheSettings.NS)

            date_issued       = '1000-10-10' if not date_issued_x or date_issued_x[0] =='None' else date_issued_x[0]
            num_downloads     =  -1 if not num_downloads_x else int(num_downloads_x[0])
            publisher_id      =  -1 if not res[Fields.PUBLISHER] else res[Fields.PUBLISHER][0]
            rights_id         =  -1 if not res[Fields.RIGHTS]    else res[Fields.RIGHTS][0]
            language_id       =  -1 if not res[Fields.LANGUAGE] else res[Fields.LANGUAGE][0]
            bookshelf_id      =  -1 if not res[Fields.BOOKSHELF] else res[Fields.BOOKSHELF][0]
            type_id           =  -1 if not  res[Fields.TYPE]    else  res[Fields.TYPE][0]
            newbook = Book(publisher_id,
                           rights_id,
                           language_id,
                           bookshelf_id,
                           gutenberg_book_id,
                           date_issued,
                           num_downloads,
                           res[Fields.TITLE],
                           res[Fields.SUBJECT],
                           type_id,
                           res[Fields.AUTHOR],
                           res[Fields.FILES])

            result.books.append(newbook)

        return result