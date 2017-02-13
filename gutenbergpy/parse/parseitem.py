from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.orderedset import OrderedSet

class ParseItem:
    def __init__(self,tablename,xpath):
        self.tableName = tablename
        self.xPath     = xpath
        self.set       = OrderedSet()

        def att_to_set(self,xpathResults,ret):
            if len(xpathResults) > 0:
                for el in xpathResults:
                    ret.append(self.set.add(el.replace("\"","'")))

        def do(self,doc):
            tmp = []
            for xpth in self.xPath:
                xpathResults = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
                self.att_to_set(xpathResults,tmp)
                xpathResults = None
            return tmp
