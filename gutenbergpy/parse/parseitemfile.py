from gutenbergpy.parse.parseitem import ParseItem
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.orderedset import OrderedSet


##
# Parser helper for download links
# noinspection PyMethodOverriding
class ParseItemFiles(ParseItem):

    def __init__(self, xpath):
        ParseItem.__init__(self, xpath)
        self.xPath = xpath
        self.setTypes = OrderedSet()
        self.setLinks = OrderedSet()

    def needs_book_id(self):
        return True

    @staticmethod
    def add(theset, xpath_result, book_id, type_id):
        text = xpath_result.replace("\"", "'")
        index = theset.index(text)
        if index is not -1:
            theset[text][1] = book_id
        else:
            index = theset.add((text, book_id,type_id))
        return index

    @staticmethod
    def add_simple(the_set, xpath_result):
        text = xpath_result.replace("\"", "'")
        return the_set.add(text)

    def do(self,doc,book_id):
        arr =[]
        for xpth in self.xPath:
            book_files = doc.xpath(xpth, namespaces=GutenbergCacheSettings.NS)
            for bk in book_files:

                xpath_results_type = bk.xpath('.//dcterms:format/rdf:Description/rdf:value/text()', namespaces=GutenbergCacheSettings.NS)
                xpath_results_link = bk.xpath('.//pgterms:file/@rdf:about', namespaces=GutenbergCacheSettings.NS)

                if xpath_results_link and xpath_results_type:
                    type_id = self.add_simple( self.setTypes, xpath_results_type[0])
                    link_id = self.add(self.setLinks, xpath_results_link[0], book_id, type_id)

                    arr.append(link_id)
        return arr
