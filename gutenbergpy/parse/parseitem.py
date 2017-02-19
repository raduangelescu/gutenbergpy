from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.orderedset import OrderedSet


##
# Helper for parsing a rdf file item
class ParseItem:
    def __init__(self, xpath):
        self.xPath = xpath
        self.set = OrderedSet()

    def needs_book_id(self):
        return False

    def add_to_set_internal(self, xpathResults, ret):
        if len(xpathResults) > 0:
            for el in xpathResults:
                ret.append(self.set.add(el.replace("\"", "'")))

    def add_to_set(self, xpathResults, ret):
        self.add_to_set_internal(xpathResults, ret)

    def do(self, doc):
        tmp = []
        for xpth in self.xPath:
            xpathResults = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
            self.add_to_set(xpathResults, tmp)
        return tmp
