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

or just install it from source (it's all just python code)

Usage
=====

Downloading a text
------------------

Query the cache
---------------

To do this you first need to create the cache (this is a one time thing per os, until you decide to redo it)

for debugging/better control you have these boolean options on create

> -   *refresh* deletes the old cache
> -   *download* property downloads the rdf file from the gutenberg project
> -   *unpack* unpacks it
> -   *parse* parses it in memory
> -   *cache* writes the cache

for even better control you may set the GutenbergCacheSettings  
-   *CacheFilename*
-   *CacheUnpackDir*
-   *CacheArchiveName*
-   *ProgressBarMaxLength*
-   *CacheRDFDownloadLink*
-   *TextFilesCacheFolder*
-   *MongoDBCacheServer*

After doing a create you need to wait, it will be over in about 5 minutes depending on your internet speed and computer power (On a i7 with gigabit connection and ssd it finishes in about 1 minute)

Get the cache

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

Or do a native query on the sqlite database

For SQLITE custom queries take a look at the SQLITE database scheme:

![image](https://github.com/raduangelescu/gutenbergpy/blob/master/sqlitecheme.png%0A%20:alt:%20SQLITE%20database%20scheme%0A%20:width:%20100%%0A%20:align:%20center)

For MongoDB queries you have all the books collection. Each book with the following fields:

> -   book(publisher, rights, language, book\_shelf, gutenberg\_book\_id, date\_issued, num\_downloads, titles, subjects, authors, files ,type)

