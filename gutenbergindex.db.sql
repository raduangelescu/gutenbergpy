BEGIN TRANSACTION;
CREATE TABLE `types` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `titles` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `subjects` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `languages` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE "downloadlinks" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT,
	`type`	INTEGER
);
CREATE TABLE `bookshelves` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `bookshelve_book` (
	`bookid`	INTEGER,
	`bookshelveid`	INTEGER
);
CREATE TABLE "books" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`description`	TEXT
);
CREATE TABLE `book_titles` (
	`book_id`	INTEGER,
	`title_id`	INTEGER
);
CREATE TABLE `book_subjects` (
	`bookid`	INTEGER,
	`subjectid`	INTEGER
);
CREATE TABLE `book_languages` (
	`bookid`	INTEGER,
	`languageid`	INTEGER
);
CREATE TABLE `book_downloads` (
	`bookid`	INTEGER,
	`downloadsid`	INTEGER
);
CREATE TABLE `book_authors` (
	`authorid`	INTEGER,
	`bookid`	INTEGER
);
CREATE TABLE `authors` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE INDEX `typesname_idx` ON `types` (`name` );
CREATE INDEX `titles_nameidx` ON `titles` (`name` );
CREATE INDEX `languagesname_idx` ON `languages` (`name` );
CREATE INDEX `bookshelves_nameidx` ON `bookshelves` (`name` );
CREATE INDEX `authors_names` ON `authors` (`name` );
CREATE INDEX `authors_nameidx` ON `authors` (`name` );
COMMIT;
