BEGIN TRANSACTION;
CREATE TABLE `types` (
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
CREATE TABLE `bookshelves` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `authors` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `publishers` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `rights` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);

CREATE TABLE "files" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT,
	`typeid`	INTEGER,
	`bookid` INTEGER
);
CREATE TABLE `titles` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
	`bookid` INTEGER
);

CREATE TABLE `book_subjects` (
	`bookid`	INTEGER,
	`subjectid`	INTEGER
);

CREATE TABLE `book_authors` (
	`bookid`	INTEGER,
	`authorid`	INTEGER
);

CREATE TABLE "books" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`publisher` INTEGER,
	`dateissued` DATE,
	`rights` INTEGER,
	`descriptionlink` TEXT,
	`numdownloads` INTEGER,
	`languageid` INTEGER,
	`bookshelveid` INTEGER
	`gutenbergbookid` INTEGER
);

COMMIT;
