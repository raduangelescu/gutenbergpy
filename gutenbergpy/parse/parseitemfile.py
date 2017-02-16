from gutenbergpy.parse.parseitem import ParseItem
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings

class ParseItemFiles(ParseItem):

    def needs_book_id(self):
        return True

    def do(self,doc,book_id):
        arr =[]
        for xpth in self.xPath:
            book_files = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
            for bk in book_files:
                xpathResults = bk.xpath('.//dcterms:format/rdf:Description/rdf:value/text()', namespaces=GutenbergCacheSettings.NS)[0]
                self.att_to_set_book_id([xpathResults],arr,book_id)
                xpathResults = None
            book_files = None
        return arr
