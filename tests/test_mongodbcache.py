"""MongoDB cache tests that don't need a MongoDB server."""
import bson

from gutenbergpy.caches.mongodbcache import MongodbCache
from gutenbergpy.parse.rdfparser import RdfParser
from gutenbergpy.utils import Utils


def offline_cache():
    return MongodbCache.__new__(MongodbCache)  # skips connecting to a server


def test_book_documents_can_be_stored(rdf_archive):
    # issue #15: "cannot encode object: <map object>"
    Utils.unpack_tarbz2()
    result = RdfParser.do()
    cache = offline_cache()
    docs = [cache._MongodbCache__get_book_json(book, result.field_sets) for book in result.books]
    for doc in docs:
        bson.encode(doc)
    alice = next(d for d in docs if d['gutenberg_book_id'] == 11)
    assert alice['titles'] == ["Alice's Adventures in Wonderland"]
    assert alice['authors'] == ['Carroll, Lewis']
    assert alice['language'] == 'en'
    assert alice['files'] == ['https://www.gutenberg.org/ebooks/11.txt.utf-8']


def test_query_uses_the_document_field_names(monkeypatch):
    cache = offline_cache()
    seen = []
    monkeypatch.setattr(cache, 'native_query', lambda q: seen.append(q) or [{'gutenberg_book_id': 1}])
    assert cache.query(languages=['en'], types=['Text'], publishers=['P'], bookshelves=['B']) == [1]
    assert seen[0] == {'$or': [{'language': 'en'}, {'type': 'Text'}, {'publisher': 'P'}, {'book_shelf': 'B'}]}


def test_query_without_filters(monkeypatch):
    cache = offline_cache()
    seen = []
    monkeypatch.setattr(cache, 'native_query', lambda q: seen.append(q) or [])
    cache.query()
    assert seen[0] == {}  # an empty $or is rejected by MongoDB
