from gutenbergpy.parse.parseitem import ParseItem
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings


##
# Parser helper for title items
class ParseItemTitles(ParseItem):
    def needs_book_id(self):
        return True

    def att_to_set_book_id(self,xpathResults,ret,book_id):
        if len(xpathResults) > 0:
            for el in xpathResults:
                text = el.replace("\"","'")
                index = self.set.index(text)
                if index is not -1:
                    self.set[text][1] = book_id
                else:
                    new_index = self.set.add((text,book_id))
                    ret.append(new_index)

    def do(self,doc,book_id):
        tmp = []
        for xpth in self.xPath:
            xpathResults = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
            self.att_to_set_book_id(xpathResults,tmp,book_id)
            xpathResults = None
        return tmp