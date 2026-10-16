import gzip
import os

import pytest

import gutenbergpy.textget as textget


class FakeResponse:
    def __init__(self, status):
        self.status = status


def fake_server(monkeypatch, existing_paths):
    """Replaces the HEAD requests with a fake server that only has existing_paths."""
    requested = []

    class FakeConnection:
        def __init__(self, host):
            self.host = host

        def request(self, method, path):
            requested.append(path)
            self.path = path

        def getresponse(self):
            return FakeResponse(200 if self.path in existing_paths else 404)

    monkeypatch.setattr(textget.http.client, 'HTTPSConnection', FakeConnection)
    return requested


def test_prefers_clean_utf8_url(monkeypatch):
    fake_server(monkeypatch, {'/cache/epub/2701/pg2701.txt', '/files/2701/2701-0.txt'})
    assert textget._format_download_uri(2701) == 'https://www.gutenberg.org/cache/epub/2701/pg2701.txt'


def test_falls_back_to_legacy_urls(monkeypatch):
    requested = fake_server(monkeypatch, {'/files/123/123-0.txt'})
    assert textget._format_download_uri(123) == 'https://www.gutenberg.org/files/123/123-0.txt'
    assert requested[0] == '/cache/epub/123/pg123.txt'


def test_unknown_download_uri(monkeypatch):
    fake_server(monkeypatch, set())
    with pytest.raises(textget.UnknownDownloadUri):
        textget._format_download_uri(5)


class FakeDownload:
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data


def test_get_text_by_id_downloads_once_and_caches(monkeypatch):
    fake_server(monkeypatch, {'/cache/epub/7/pg7.txt'})
    downloads = []

    def fake_urlopen(uri):
        downloads.append(uri)
        return FakeDownload('Très bien, déjà vu à côté.\n'.encode('utf-8') * 50)

    monkeypatch.setattr(textget, 'urlopen', fake_urlopen)
    first = textget.get_text_by_id(7)
    second = textget.get_text_by_id(7)
    assert first == second
    assert len(downloads) == 1
    assert os.path.exists(os.path.join('texts', '7.txt.gz'))
    assert 'déjà vu à côté' in first.decode('utf-8')


def test_get_text_by_id_when_encoding_is_not_detected(monkeypatch):
    fake_server(monkeypatch, {'/cache/epub/8/pg8.txt'})
    monkeypatch.setattr(textget, 'urlopen', lambda uri: FakeDownload(b'\xff\xfe\x00'))
    monkeypatch.setattr(textget.chardet, 'detect', lambda data: {'encoding': None})
    assert isinstance(textget.get_text_by_id(8), bytes)


def make_book(body_lines=200):
    header = ['The Project Gutenberg eBook of Test', 'Title: Test', '',
              '*** START OF THE PROJECT GUTENBERG EBOOK TEST ***']
    body = ['body line %d' % i for i in range(body_lines)]
    footer = ['*** END OF THE PROJECT GUTENBERG EBOOK TEST ***', 'license text']
    return '\n'.join(header + body + footer).encode('utf-8')


def test_strip_headers_removes_header_and_footer():
    clean = textget.strip_headers(make_book()).decode('utf-8')
    assert 'body line 0' in clean
    assert 'body line 199' in clean
    assert 'START OF THE PROJECT GUTENBERG' not in clean
    assert 'END OF THE PROJECT GUTENBERG' not in clean
    assert 'license text' not in clean


def test_strip_headers_removes_legalese_section():
    text = make_book().replace(b'body line 5\n', b'<<THIS ELECTRONIC VERSION OF\nsecret\nSERVICE THAT CHARGES FOR DOWNLOAD\n')
    clean = textget.strip_headers(text).decode('utf-8')
    assert 'secret' not in clean
    assert 'body line 6' in clean


@pytest.mark.network
def test_real_download():
    text = textget.strip_headers(textget.get_text_by_id(2701)).decode('utf-8')
    assert 'MOBY-DICK' in text[:1000].upper()
