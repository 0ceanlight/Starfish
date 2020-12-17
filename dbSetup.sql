-- .read dbSetup.sql

-- .open subjects.db
PRAGMA foreign_keys = ON;
-- subject
CREATE TABLE IF NOT EXISTS subjects (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL UNIQUE,
	zoomUrl TEXT,
	zoomPasscode TEXT
);

-- alternate names for a subject
CREATE TABLE IF NOT EXISTS aliases (
	subject_id INTEGER NOT NULL,
	alias TEXT NOT NULL UNIQUE,
	FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

-- urls to be opened when a subject is selected
CREATE TABLE IF NOT EXISTS urls (
	subject_id INTEGER NOT NULL,
	url TEXT NOT NULL UNIQUE,
	FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

-- -- information on zoom meetings
-- CREATE TABLE IF NOT EXISTS zoom (
-- 	id INTEGER PRIMARY KEY AUTOINCREMENT,
-- 	subject_id INTEGER NOT NULL,
-- 	-- precedence INTEGER NOT NULL, -- autoincrement? uncomment unless only supporting 1 zoom/subject
-- 	url TEXT NOT NULL,
-- 	passcode TEXT NOT NULL,
-- 	FOREIGN KEY (subject_id) REFERENCES subjects(id)
-- );

-- .quit
