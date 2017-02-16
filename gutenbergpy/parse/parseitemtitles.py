from gutenbergpy.parse.parseitem import ParseItem
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings


class ParseItemTitles(ParseItem):
    def needs_book_id(self):
        return True

    def do(self,doc,book_id):
        tmp = []
        for xpth in self.xPath:
            xpathResults = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
            self.att_to_set_book_id(xpathResults,tmp,book_id)
            xpathResults = None
        return tmp