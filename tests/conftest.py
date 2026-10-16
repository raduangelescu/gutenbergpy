import csv
import gzip
import os
import tarfile

import pytest

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings

RDF_TEMPLATE = '''<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:pgterms="http://www.gutenberg.org/2009/pgterms/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dcam="http://purl.org/dc/dcam/">
  <pgterms:ebook rdf:about="ebooks/{id}">
    <dcterms:title>{title}</dcterms:title>
    <dcterms:publisher>Project Gutenberg</dcterms:publisher>
    <dcterms:rights>Public domain in the USA.</dcterms:rights>
    <dcterms:issued rdf:datatype="http://www.w3.org/2001/XMLSchema#date">{issued}</dcterms:issued>
    <pgterms:downloads>{downloads}</pgterms:downloads>
    <dcterms:creator><pgterms:agent><pgterms:name>{author}</pgterms:name><pgterms:alias>{alias}</pgterms:alias></pgterms:agent></dcterms:creator>
    <dcterms:language><rdf:Description><rdf:value>{language}</rdf:value></rdf:Description></dcterms:language>
    <dcterms:type><rdf:Description><rdf:value>Text</rdf:value></rdf:Description></dcterms:type>
    <dcterms:subject><rdf:Description><rdf:value>{subject}</rdf:value></rdf:Description></dcterms:subject>
    <pgterms:bookshelf><rdf:Description><rdf:value>{bookshelf}</rdf:value></rdf:Description></pgterms:bookshelf>
    <dcterms:hasFormat><pgterms:file rdf:about="https://www.gutenberg.org/ebooks/{id}.txt.utf-8">
      <dcterms:format><rdf:Description><rdf:value>text/plain; charset=utf-8</rdf:value></rdf:Description></dcterms:format>
    </pgterms:file></dcterms:hasFormat>
  </pgterms:ebook>
</rdf:RDF>'''

BOOKS = [
    dict(id=11, title="Alice's Adventures in Wonderland", author="Carroll, Lewis", author_dates="1832-1898",
         alias="Dodgson, Charles Lutwidge", language="en", subject="Fantasy fiction", bookshelf="Category: Novels",
         issued="2008-06-27", downloads=100),
    dict(id=84, title="Frankenstein; Or, The Modern Prometheus", author="Shelley, Mary Wollstonecraft",
         author_dates="1797-1851", alias="Godwin, Mary", language="en", subject="Horror tales",
         bookshelf="Category: Novels", issued="1993-10-01", downloads=50),
    dict(id=135, title="Les Misérables", author="Hugo, Victor", author_dates="1802-1885", alias="Hugo, V.",
         language="fr", subject="Fantasy fiction", bookshelf="Category: Classics", issued="1994-06-01",
         downloads=10),
]


@pytest.fixture(autouse=True)
def in_tmp_dir(tmp_path, monkeypatch):
    """All cache files are relative to the working directory, so every test runs in its own empty one."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def rdf_archive(tmp_path):
    """Writes an rdf-files.tar.bz2 like the Project Gutenberg one, including the odd folders it really has."""
    src = tmp_path / 'src'
    epub = src / 'cache' / 'epub'
    for book in BOOKS:
        folder = epub / str(book['id'])
        folder.mkdir(parents=True)
        (folder / ('pg%d.rdf' % book['id'])).write_text(RDF_TEMPLATE.format(**book), encoding='utf-8')
    # issue #19: the real archive has a 'test' folder whose file name doesn't match the folder
    (epub / 'test').mkdir()
    (epub / 'test' / 'pg11.rdf').write_text(RDF_TEMPLATE.format(**BOOKS[0]), encoding='utf-8')
    # a numbered folder without its rdf file
    (epub / '99999').mkdir()
    with tarfile.open(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME, 'w:bz2') as tar:
        tar.add(str(src / 'cache'), arcname='cache')
    return os.path.abspath(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME)


def write_catalog_csv(rows):
    fields = ['Text#', 'Type', 'Issued', 'Title', 'Language', 'Authors', 'Subjects', 'LoCC', 'Bookshelves']
    with gzip.open(GutenbergCacheSettings.CACHE_CSV_ARCHIVE_NAME, 'wt', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return os.path.abspath(GutenbergCacheSettings.CACHE_CSV_ARCHIVE_NAME)


@pytest.fixture
def csv_catalog():
    """Writes a pg_catalog.csv.gz with the same books as the rdf archive, in the real csv format."""
    rows = []
    for book in BOOKS:
        rows.append({'Text#': str(book['id']), 'Type': 'Text', 'Issued': book['issued'], 'Title': book['title'],
                     'Language': book['language'],
                     'Authors': '%s, %s' % (book['author'], book['author_dates']),
                     'Subjects': book['subject'], 'LoCC': 'PR', 'Bookshelves': book['bookshelf']})
    return write_catalog_csv(rows)
