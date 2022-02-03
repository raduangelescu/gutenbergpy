GutenbergPy
========

![image](https://github.com/raduangelescu/gutenbergpy/blob/master/dblogos.png?raw=true)

This package makes filtering and getting information from [Project Gutenberg](http://www.gutenberg.org) easier from python.

It's target audience is machine learning guys that need data for their project, but may be freely used by anybody.

The package:

-   Generates a local cache (of all gutenberg informations) that you can interogate to get book ids. The Local cache may be sqlite (default) or mongodb (for wich you need to have installed the pymongodb packet)
-   Downloads and cleans raw text from gutenberg books

The package has been tested with Python 3.6 on both Windows and Linux It is faster, smaller and less third-party intensive alternative to <https://github.com/c-w/Gutenberg>

About development: <http://www.raduangelescu.com/gutenbergpy.html>

Installation
============

```
pip install gutenbergpy
```

or just install it from source (it's all just python code):

```
git clone https://github.com/raduangelescu/gutenbergpy
python setup.py install
```

Usage
=====

Downloading a text
------------------
```
import gutenbergpy.textget
#this gets a book by its gutenberg id
raw_book    = gutenbergpy.textget.get_text_by_id(1000)
print raw_book
#this strips the headers from the book
clean_book  = gutenbergpy.textget.strip_headers(raw_book)
print clean_book
```
Query the cache
---------------

To do this you first need to create the cache (this is a one time thing per os, until you decide to redo it)

```
from gutenbergpy.gutenbergcache import GutenbergCache
#for sqlite
GutenbergCache.create()
#for mongodb
GutenbergCache.create(type=GutenbergCacheTypes.CACHE_TYPE_MONGODB)
```

for debugging/better control you have these boolean options on create

> -   *refresh* deletes the old cache
> -   *download* property downloads the rdf file from the gutenberg project
> -   *unpack* unpacks it
> -   *parse* parses it in memory
> -   *cache* writes the cache

```
GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=True)
```

for even better control you may set the GutenbergCacheSettings  
-   *CacheFilename*
-   *CacheUnpackDir*
-   *CacheArchiveName*
-   *ProgressBarMaxLength*
-   *CacheRDFDownloadLink*
-   *TextFilesCacheFolder*
-   *MongoDBCacheServer*

```
GutenbergCacheSettings.set( CacheFilename="", CacheUnpackDir="", 
    CacheArchiveName="", ProgressBarMaxLength="", CacheRDFDownloadLink="", TextFilesCacheFolder="", MongoDBCacheServer="")
```

After doing a create you need to wait, it will be over in about 5 minutes depending on your internet speed and computer power (On a i7 with gigabit connection and ssd it finishes in about 1 minute)

Get the cache
```
#for mongodb
cache = GutenbergCache.get_cache(GutenbergCacheTypes.CACHE_TYPE_MONGODB)
#for sqlite
cache  = GutenbergCache.get_cache()
```
Now you can do queries

Get the book Gutenberg unique indices by using this query function

Standard query fields:  
-   languages
-   authors
-   types
-   titles
-   subjects
-   publishers
-   bookshelves
-   downloadtype
```
print cache.query(downloadtype=['application/plain','text/plain','text/html; charset=utf-8'])
```
Or do a native query on the sqlite database
```
#python
cache.native_query("SELECT * FROM books")
#mongodb
cache.native_query({type:'Text'}}
```  
For SQLITE custom queries take a look at the SQLITE database scheme:

![image](https://github.com/raduangelescu/gutenbergpy/blob/master/sqlitecheme.png?raw=true)

For MongoDB queries you have all the books collection. Each book with the following fields:

> -   book(publisher, rights, language, book\_shelf, gutenberg\_book\_id, date\_issued, num\_downloads, titles, subjects, authors, files ,type)

