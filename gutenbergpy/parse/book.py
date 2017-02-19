##
# Used to hold a book in parse results after parsing
class Book:
    def __init__(self, publisher_id, rights_id, language_id,
                 bookshelf_id, gutenberg_book_id,
                 date_issued, num_downloads,
                 titles_id, subjects_id, type_id, authors_id, files_id):
        self.publisher_id = publisher_id
        self.rights_id = rights_id
        self.language_id = language_id
        self.bookshelf_id = bookshelf_id
        self.gutenberg_book_id = gutenberg_book_id
        self.date_issued = date_issued
        self.num_downloads = num_downloads
        self.titles_id = titles_id
        self.subjects_id = subjects_id
        self.authors_id = authors_id
        self.files_id = files_id
        self.type_id = type_id
