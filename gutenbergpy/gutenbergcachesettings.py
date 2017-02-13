class GutenbergCacheSettings():
    #name of the gutenberg link for the rdf arhive (should not change)
    CACHE_RDF_DOWNLOAD_LINK     = 'https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2'
    #name of the caches file name (sqlite db)
    CACHE_FILENAME              = 'gutenbergindex.db'
    #name of the rdf unpack directory (this will be used when unpacking the rdf tar)
    CACHE_RDF_UNPACK_DIRECTORY  = 'cache\\epub\\'
    #name of the downloaded rdf arhive
    CACHE_RDF_ARCHIVE_NAME      = 'rdf-files.tar.bz2'
    #number of #'s shown in loading bar (common to all loading bars)
    DOWNLOAD_NUM_DIVS = 20
    #used to hold download progress for rdf tar downloading

    ##########READONLY VARIABLES (please put readonly variables here)
    #namespace used for the rds parsing (should not change)
    NS ={
        'cc':"http://web.resource.org/cc/",
        'dcam':"http://purl.org/dc/dcam/",
        'dcterms':"http://purl.org/dc/terms/",
        'rdfs':"http://www.w3.org/2000/01/rdf-schema#",
        'rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'pgterms':"http://www.gutenberg.org/2009/pgterms/"}
    ##########END OF READONLY VARIABLES


    def __init__(**kwargs):
        if kwargs.has_key('CacheFilename'):
            GutenbergCacheSettings.CACHE_FILENAME = kwargs['CacheFilename']
        if kwargs.has_key('CacheUnpackDir'):
            GutenbergCacheSettings.CACHE_RDF_UNPACK_DIRECTORY = kwargs['CacheUnpackDir']
        if kwargs.has_key('CacheArchiveName'):
            GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME = kwargs['CacheArchiveName']
        if kwargs.has_key('ProgressBarMaxLength'):
            GutenbergCacheSettings.DOWNLOAD_NUM_DIVS = kwargs['ProgressBarMaxLength']
        if kwargs.has_key('CacheRDFDownloadLink'):
            GutenbergCacheSettings.CACHE_RDF_DOWNLOAD_LINK = kwargs['CacheRDFDownloadLink']
