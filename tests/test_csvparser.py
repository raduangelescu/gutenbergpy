import pytest

from gutenbergpy.parse.cachefields import Fields
from gutenbergpy.parse.csvparser import CsvParser, author_name, split_values
from tests.conftest import write_catalog_csv


@pytest.mark.parametrize('entry, expected', [
    ('Melville, Herman, 1819-1891', 'Melville, Herman'),
    ('Aesop, 621? BCE-565? BCE', 'Aesop'),
    ('Twain, Mark, 1835-', 'Twain, Mark'),
    ('Moore, John, -1900', 'Moore, John'),
    ('Macdonald, Clare I., 1868?-1951?', 'Macdonald, Clare I.'),
    ('Pausanias, approximately 110-approximately 180', 'Pausanias'),
    # these suffixes are part of the rdf name
    ('Sunzi, active 6th century B.C.', 'Sunzi, active 6th century B.C.'),
    ('Nennius, active 796', 'Nennius, active 796'),
    ('Wu, Chuhou, jin shi 1053', 'Wu, Chuhou, jin shi 1053'),
    ('Great Britain. Army. Highland Light Infantry. Battalion, 5th', 'Great Britain. Army. Highland Light Infantry. Battalion, 5th'),
    ('Diogenes [pseudonym]', 'Diogenes [pseudonym]'),
    ('Apuleius', 'Apuleius'),
    ('Anonymous', 'Anonymous'),
    ('Way, Arthur S. (Arthur Sanders), 1847-1930', 'Way, Arthur S. (Arthur Sanders)'),
    # contributors are not authors (the rdf parser only keeps dcterms:creator)
    ('Giles, Lionel, 1875-1958 [Translator]', None),
    ('Morris, Woodrow W. [Editor]', None),
])
def test_author_name(entry, expected):
    assert author_name(entry) == expected


def test_split_values():
    assert split_values('de; en') == ['de', 'en']
    assert split_values('') == []
    assert split_values('Whaling -- Fiction; Sea stories') == ['Whaling -- Fiction', 'Sea stories']


def row(**kw):
    base = {'Text#': '1', 'Type': 'Text', 'Issued': '2000-01-01', 'Title': 'T', 'Language': 'en',
            'Authors': '', 'Subjects': '', 'LoCC': '', 'Bookshelves': ''}
    base.update(kw)
    return base


def test_multiple_authors_languages_and_contributors():
    write_catalog_csv([row(Authors='Aesop, 621? BCE-565? BCE; Townsend, George Fyler, 1814-1900 [Translator]',
                           Language='de; en', Subjects='Fables; Animals -- Fiction', LoCC='PZ')])
    result = CsvParser.do()
    book = result.books[0]
    authors = [result.field_sets[Fields.AUTHOR].set[i - 1] for i in book.authors_id]
    subjects = [result.field_sets[Fields.SUBJECT].set[i - 1] for i in book.subjects_id]
    assert authors == ['Aesop']
    assert subjects == ['Fables', 'Animals -- Fiction', 'PZ']  # LoCC classes are subjects, like in the rdf
    assert list(result.field_sets[Fields.LANGUAGE].set) == ['de', 'en']
    assert result.field_sets[Fields.LANGUAGE].set[book.language_id - 1] == 'de'


def test_missing_values_and_bad_rows():
    write_catalog_csv([row(**{'Text#': 'not-a-number'}), row(Issued='', Title='', Language='')])
    result = CsvParser.do()
    assert len(result.books) == 1
    book = result.books[0]
    assert book.date_issued == '1000-10-10'
    assert book.language_id == -1
    assert book.titles_id == []


def test_multiline_titles_are_kept():
    write_catalog_csv([row(Title='Moby Dick\nOr, The Whale')])
    result = CsvParser.do()
    assert result.field_sets[Fields.TITLE].set[0][0] == 'Moby Dick\nOr, The Whale'
