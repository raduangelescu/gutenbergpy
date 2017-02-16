from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.orderedset import OrderedSet

class ParseItem:
    def __init__(self,tablename,xpath):
        self.tableName      = tablename
        self.xPath          = xpath
        self.set            = OrderedSet()

    def needs_book_id(self):
        return False

    def att_to_set(self,xpathResults,ret):
        if len(xpathResults) > 0:
            for el in xpathResults:
                ret.append(self.set.add(el.replace("\"","'")))

    def att_to_set_book_id(self,xpathResults,ret,book_id):
        if len(xpathResults) > 0:
            for el in xpathResults:
                text = el.replace("\"","'")
                index = self.set.index(text)
                if index is not -1:
                    set['text'][1] = book_id
                else:
                    new_index = self.set.add((text,book_id))
                    ret.append(new_index)

    def do(self,doc):
        tmp = []
        for xpth in self.xPath:
            xpathResults = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
            self.att_to_set(xpathResults,tmp)
            xpathResults = None
        return tmp
