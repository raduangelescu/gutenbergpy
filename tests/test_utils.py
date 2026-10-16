import io
import os
import tarfile

import pytest

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.utils import Utils


def write_archive(members):
    with tarfile.open(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME, 'w:bz2') as tar:
        for name, data in members:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))


def test_unpack(tmp_path):
    write_archive([('cache/epub/1/pg1.rdf', b'<rdf/>')])
    Utils.unpack_tarbz2()
    assert (tmp_path / 'cache' / 'epub' / '1' / 'pg1.rdf').read_bytes() == b'<rdf/>'


@pytest.mark.skipif(not hasattr(tarfile, 'data_filter'), reason='tarfile extraction filters need Python 3.8.17+')
def test_unpack_refuses_paths_outside_the_working_directory(tmp_path):
    write_archive([('../evil.txt', b'x')])
    with pytest.raises(tarfile.FilterError):
        Utils.unpack_tarbz2()
    assert not (tmp_path.parent / 'evil.txt').exists()


def test_delete_tmp_files(tmp_path):
    for name in (GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME, GutenbergCacheSettings.CACHE_CSV_ARCHIVE_NAME,
                 GutenbergCacheSettings.CACHE_FILENAME):
        (tmp_path / name).write_bytes(b'x')
    os.makedirs(os.path.join('cache', 'epub', '1'))
    Utils.delete_tmp_files()
    assert not (tmp_path / GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME).exists()
    assert not (tmp_path / GutenbergCacheSettings.CACHE_CSV_ARCHIVE_NAME).exists()
    assert not (tmp_path / 'cache' / 'epub' / '1').exists()
    assert (tmp_path / GutenbergCacheSettings.CACHE_FILENAME).exists()  # the cache itself is kept
    Utils.delete_tmp_files(delete_sqlite=True)
    assert not (tmp_path / GutenbergCacheSettings.CACHE_FILENAME).exists()
