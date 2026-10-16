"""Builds real SQLite caches from both sources and checks the queries users run on them."""
import pytest

import os

from gutenbergpy.gutenbergcache import GutenbergCache, GutenbergCacheSources
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.utils import Utils
from tests.conftest import BOOKS

ALL_IDS = sorted(b['id'] for b in BOOKS)


def build(source):
    GutenbergCache.create(source=source, refresh=False, download=False, deleteTemp=False)
    assert GutenbergCache.exists()
    return GutenbergCache.get_cache()


@pytest.fixture(params=[GutenbergCacheSources.RDF, GutenbergCacheSources.CSV])
def cache(request, rdf_archive, csv_catalog):
    c = build(request.param)
    yield c
    c.connection.close()


def test_query_without_filters_returns_all_books(cache):
    assert sorted(cache.query()) == ALL_IDS


def test_query_by_author(cache):
    # the csv has "Shelley, Mary Wollstonecraft, 1797-1851", the dates must be stripped like in the rdf
    assert cache.query(authors=['Shelley, Mary Wollstonecraft']) == [84]


def test_query_title_with_apostrophe(cache):
    assert cache.query(titles=["Alice's Adventures in Wonderland"]) == [11]


def test_query_non_ascii_title(cache):
    assert cache.query(titles=['Les Misérables']) == [135]


def test_query_by_subject(cache):
    assert sorted(cache.query(subjects=['Fantasy fiction'])) == [11, 135]


def test_filters_are_combined_with_and(cache):
    assert cache.query(subjects=['Fantasy fiction'], languages=['en']) == [11]


def test_values_of_one_filter_are_combined_with_or(cache):
    assert sorted(cache.query(languages=['en', 'fr'])) == ALL_IDS


def test_query_by_bookshelf_and_type(cache):
    assert sorted(cache.query(bookshelves=['Category: Novels'], types=['Text'])) == [11, 84]


def test_query_values_are_not_interpreted_as_sql(cache):
    assert cache.query(titles=["x') OR 1=1 --"]) == []


def test_native_query_with_parameters(cache):
    rows = cache.native_query(
        "SELECT books.gutenbergbookid FROM books, titles WHERE titles.bookid = books.id AND titles.name LIKE ?",
        ('%Frankenstein%',)).fetchall()
    assert rows == [(84,)]


def test_odd_archive_folders_are_skipped(rdf_archive):
    # issue #19: 'test/' and a numbered folder without its pgN.rdf file must not break parsing
    cache = build(GutenbergCacheSources.RDF)
    count = cache.native_query('SELECT COUNT(*) FROM books').fetchone()[0]
    cache.connection.close()
    assert count == len(BOOKS)


def test_rdf_only_fields(rdf_archive):
    cache = build(GutenbergCacheSources.RDF)
    assert sorted(cache.query(downloadtype=['text/plain; charset=utf-8'])) == ALL_IDS
    aliases = sorted(r[0] for r in cache.native_query('SELECT name FROM aliases'))
    assert aliases == sorted(b['alias'] for b in BOOKS)
    top = cache.native_query('SELECT gutenbergbookid FROM books ORDER BY numdownloads DESC LIMIT 1').fetchone()
    cache.connection.close()
    assert top == (11,)


def test_csv_source_has_no_download_data(csv_catalog):
    cache = build(GutenbergCacheSources.CSV)
    assert cache.query(downloadtype=['text/plain; charset=utf-8']) == []
    downloads = {r[0] for r in cache.native_query('SELECT numdownloads FROM books')}
    cache.connection.close()
    assert downloads == {-1}


def test_both_sources_give_the_same_metadata(rdf_archive, csv_catalog, tmp_path, monkeypatch):
    def snapshot(source):
        monkeypatch.setattr(GutenbergCacheSettings, 'CACHE_FILENAME', str(tmp_path / ('%s.db' % source)))
        cache = build(source)
        rows = cache.native_query(
            "SELECT books.gutenbergbookid, titles.name, authors.name, languages.name, books.dateissued "
            "FROM books, titles, authors, book_authors, languages "
            "WHERE titles.bookid = books.id AND book_authors.bookid = books.id "
            "AND authors.id = book_authors.authorid AND languages.id = books.languageid "
            "ORDER BY books.gutenbergbookid").fetchall()
        cache.connection.close()
        return rows

    from_rdf = snapshot(GutenbergCacheSources.RDF)
    from_csv = snapshot(GutenbergCacheSources.CSV)
    assert len(from_rdf) == len(BOOKS)
    assert from_csv == from_rdf


def test_refresh_false_keeps_existing_cache(csv_catalog, capsys):
    build(GutenbergCacheSources.CSV)
    GutenbergCache.create(source='csv', refresh=False, download=False)
    assert 'Cache already exists' in capsys.readouterr().out


def test_refresh_true_rebuilds_existing_cache(csv_catalog, capsys, monkeypatch):
    data = open(csv_catalog, 'rb').read()
    build(GutenbergCacheSources.CSV)
    capsys.readouterr()

    downloads = []

    def fake_download(link=None, file_name=None):
        downloads.append(link)
        with open(file_name, 'wb') as f:
            f.write(data)

    monkeypatch.setattr(Utils, 'download_file', staticmethod(fake_download))
    GutenbergCache.create(source='csv', refresh=True)
    out = capsys.readouterr().out
    assert 'Cache already exists' not in out
    assert downloads == [GutenbergCacheSettings.CACHE_CSV_DOWNLOAD_LINK]
    assert GutenbergCache.exists()


def test_unknown_source_is_rejected():
    with pytest.raises(ValueError):
        GutenbergCache.create(source='xml')


def test_temp_files_are_deleted(csv_catalog):
    GutenbergCache.create(source='csv', refresh=False, download=False, deleteTemp=True)
    assert not os.path.exists(csv_catalog)
    assert GutenbergCache.exists()
