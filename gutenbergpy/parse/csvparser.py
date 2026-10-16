import csv
import gzip
import re

from gutenbergpy.parse.cachefields      import Fields
from gutenbergpy.parse.book             import Book
from gutenbergpy.parse.parseitem        import ParseItem
from gutenbergpy.parse.parseitemfile    import ParseItemFiles
from gutenbergpy.parse.parseitemtitles  import ParseItemTitles
from gutenbergpy.parse.rdfparseresults  import RDFParseResults
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.utils                  import Utils

ROLE_RE = re.compile(r'\s*\[([^\]]*)\]\s*$')
# brackets that are part of the name, not a contributor role
NAME_BRACKETS = ('pseud.', 'pseudonym')
# life dates the csv appends to the rdf name: "1819-1891", "1835-", "-1900", "1868?-1951", "621? BCE-565? BCE".
# "active 4th century" or "jin shi 1053" are part of the rdf name and are kept.
_YEAR = r'(approximately )?\d+\??( BCE)?'
LIFE_DATES_RE = re.compile(r'^(%s-(%s)?|-%s)$' % (_YEAR, _YEAR, _YEAR))


##
# Splits a "; " separated csv cell into its values
def split_values(cell):
    return [v.strip() for v in cell.split('; ') if v.strip()]


##
# Turns a csv author entry ("Melville, Herman, 1819-1891") into the rdf name ("Melville, Herman").
# Returns None for contributors ("Giles, Lionel, 1875-1958 [Translator]"), the rdf cache only keeps creators.
def author_name(entry):
    role = ROLE_RE.search(entry)
    if role and role.group(1) not in NAME_BRACKETS:
        return None
    parts = entry.split(', ')
    if len(parts) > 1 and LIFE_DATES_RE.match(parts[-1]):
        parts = parts[:-1]
    return ', '.join(parts)


##
# The csv parser, a fast alternative to the rdf parser.
# It reads the pg_catalog.csv.gz feed (a few MB instead of the 100+MB rdf archive) and produces the same
# parse results, but the csv has no download links, download counts, author aliases, publisher or rights.
# noinspection PyClassHasNoInit
class CsvParser:
    @staticmethod
    def do():
        result = RDFParseResults()

        result.field_sets = Fields.FIELD_COUNT * [None]
        result.field_sets[Fields.TITLE]     = ParseItemTitles(xpath=[])
        result.field_sets[Fields.SUBJECT]   = ParseItem(xpath=[])
        result.field_sets[Fields.TYPE]      = ParseItem(xpath=[])
        result.field_sets[Fields.LANGUAGE]  = ParseItem(xpath=[])
        result.field_sets[Fields.AUTHOR]    = ParseItem(xpath=[])
        result.field_sets[Fields.ALIASES]   = ParseItem(xpath=[])
        result.field_sets[Fields.BOOKSHELF] = ParseItem(xpath=[])
        result.field_sets[Fields.FILES]     = ParseItemFiles(xpath=[])
        result.field_sets[Fields.PUBLISHER] = ParseItem(xpath=[])
        result.field_sets[Fields.RIGHTS]    = ParseItem(xpath=[])

        with gzip.open(GutenbergCacheSettings.CACHE_CSV_ARCHIVE_NAME, 'rt', encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))

        total = len(rows)
        fs = result.field_sets
        for idx, row in enumerate(rows):
            if not row['Text#'].isdigit():
                continue
            if idx % 1000 == 0:
                Utils.update_progress_bar("Processing progress: %d / %d" % (idx, total), idx, total)

            book_id = len(result.books) + 1
            authors = [a for a in (author_name(e) for e in split_values(row['Authors'])) if a]

            titles_id   = fs[Fields.TITLE].do_values([row['Title']] if row['Title'] else [], book_id)
            # the rdf lists the library of congress classes (e.g. "PS") as subjects too
            subjects_id = fs[Fields.SUBJECT].do_values(split_values(row['Subjects']) + split_values(row.get('LoCC', '')))
            type_ids    = fs[Fields.TYPE].do_values([row['Type']] if row['Type'] else [])
            language_ids = fs[Fields.LANGUAGE].do_values(split_values(row['Language']))
            authors_id  = fs[Fields.AUTHOR].do_values(authors)
            shelf_ids   = fs[Fields.BOOKSHELF].do_values(split_values(row['Bookshelves']))

            date_issued   = row['Issued'] or '1000-10-10'
            language_id   = -1 if not language_ids else language_ids[0]
            bookshelf_id  = -1 if not shelf_ids    else shelf_ids[0]
            type_id       = -1 if not type_ids     else type_ids[0]

            result.books.append(Book(-1, -1, language_id, bookshelf_id,
                                     int(row['Text#']), date_issued, -1, titles_id,
                                     subjects_id, type_id, authors_id, [], []))

        return result
