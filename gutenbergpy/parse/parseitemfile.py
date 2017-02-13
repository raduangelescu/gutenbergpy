from gutenbergpy.parse.parseitem import ParseItem
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings

class ParseItemFiles(ParseItem):
    def do(self,doc):
        arr =[]
        for xpth in self.xPath:
            book_files = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
            for bk in book_files:
                xpathResults = bk.xpath('.//dcterms:format/rdf:Description/rdf:value/text()', namespaces=GutenbergCacheSettings.NS)[0]
                self.att_to_set([xpathResults],arr)
                xpathResults = None
            book_files = None
        return arr
