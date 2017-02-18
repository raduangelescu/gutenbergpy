BEGIN TRANSACTION;

CREATE INDEX `books_dateissued_idx` ON `books` (`dateissued` ASC);
CREATE INDEX `books_numdownloads_idx` ON `books` (`numdownloads` ASC);
CREATE INDEX `gutenbergbookid_idx` ON `books` (`gutenbergbookid` ASC);

CREATE INDEX `authors_name_idx` ON `authors` (`name` ASC);

CREATE INDEX `types_name_idx` ON `types` (`name` ASC);

CREATE INDEX `titles_name_idx` ON `titles` (`name` ASC);

CREATE INDEX `subjects_name_idx` ON `subjects` (`name` ASC);

CREATE INDEX `rights_name_idx` ON `rights` (`name` ASC);

CREATE INDEX `publishers_name_idx` ON `publishers` (`name` ASC);

CREATE INDEX `languages_name_idx` ON `languages` (`name` ASC);

CREATE INDEX `bookshelves_name_idx` ON `bookshelves` (`name` ASC);

CREATE INDEX `downloadlinks_name_idx` ON `downloadlinks` (`name` ASC);


COMMIT;
