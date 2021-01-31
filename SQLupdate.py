from SQLmain import cur, conn

# addSubject(name: str) -> rowID of inserted subject: int
# addAlias(subjectID: int, alias: str): # -> void
# setSubjectUrl(subjectID: int, URL: str) -> void 
# setSubjectName(subjectID: int, newName: str) -> void
# setSubjectZoomInfo(subjectID: int, zoomURL: str, zoomPasscode: str) -> void 


# NOTES
# def subjectExists(subjectID: int)?

# shell version: need to make sure no collisions between aliases and names
# WHERE NOT EXISTS (SELECT * FROM aliases WHERE alias = ?);
# idea: try adding alias, if succeeds, add subject...

def addSubject(name: str) -> int:
	cur.execute("""INSERT OR IGNORE INTO subjects (name)
	-- OUTPUT Inserted.id
	VALUES (?);""", (name,))
	conn.commit()
	return cur.lastrowid

def addAlias(subjectID: int, alias: str) -> None:
	cur.execute("INSERT OR IGNORE INTO aliases (subject_id, alias) VALUES (?, ?);", (subjectID, alias))
	conn.commit()


def addSubjectUrl(subjectID: int, URL: str) -> None:
	cur.execute("INSERT OR IGNORE INTO urls (subject_id, url) VALUES (?, ?);", (subjectID, URL))
	conn.commit()
	

# TODO: handle name not unique/null error
def setSubjectName(subjectID: int, newName: str) -> None:
	cur.execute("UPDATE subjects SET name = ? WHERE id = ?;", (newName, subjectID))
	conn.commit()	

def setSubjectZoomInfo(subjectID: int, zoomURL: str, zoomPasscode: str) -> None: 
	cur.execute("""
		UPDATE subjects SET
		zoomUrl = ?,
		zoomPasscode = ?
		WHERE
		id = ?;	""", (zoomURL, zoomPasscode, subjectID))
	conn.commit()
