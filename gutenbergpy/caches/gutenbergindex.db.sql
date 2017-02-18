BEGIN TRANSACTION;
CREATE TABLE `types` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `titles` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT,
	`bookid` INTEGER
);
CREATE TABLE `subjects` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `rights` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `publishers` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE `languages` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);

CREATE TABLE `downloadlinkstype` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);

CREATE TABLE `downloadlinks` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT,
	`downloadtypeid`	INTEGER,
	`bookid` INTEGER
);
CREATE TABLE `bookshelves` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);
CREATE TABLE "books" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`publisherid` INTEGER,
	`dateissued` DATE,
	`rightsid` INTEGER,
	`numdownloads` INTEGER,
	`languageid` INTEGER,
	`bookshelveid` INTEGER,
	`gutenbergbookid` INTEGER,
	`typeid` INTEGER
);
CREATE TABLE `book_subjects` (
	`bookid`	INTEGER,
	`subjectid`	INTEGER
);
CREATE TABLE `book_authors` (
	`bookid`	INTEGER,
	`authorid`	INTEGER
);
CREATE TABLE `authors` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT
);



COMMIT;
