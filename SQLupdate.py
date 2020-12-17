import SQLmain

import SQLmain

# UPDATE
#
# addSubject(name: str) -> void
#
# setSubjectUrls(subjectID: int, *argv) -> void 
# setSubjectZoomInfo(subjectID: int, zoomURL: str, zoomPasscode: str) -> void 


# def subjectExists(subjectID: int):

# need to make sure no collisions between aliases and names
# WHERE NOT EXISTS (SELECT * FROM aliases WHERE alias = ?);
def addSubject(name: str): # -> void
	try:
		# idea: try adding alias, if succeeds, add subject...
		SQLmain.cur.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
		SQLmain.conn.commit()
	except SQLmain.sqlite3.IntegrityError:
		pass

def addAlias(subjectID: int, alias: str): # -> void
	try:
		SQLmain.cur.execute("INSERT INTO aliases (subject_id, alias) VALUES (?, ?);", (subjectID, alias))
		SQLmain.conn.commit()
	except SQLmain.sqlite3.IntegrityError:
		pass


def addSubjectUrl(subjectID: int, URL: str): # -> void 
	try:
		SQLmain.cur.execute("INSERT INTO urls (subject_id, url) VALUES (?, ?);", (subjectID, URL))
		SQLmain.conn.commit()
	except SQLmain.sqlite3.IntegrityError:
		pass

def setSubjectZoomInfo(subjectID: int, zoomURL: str, zoomPasscode: str): # -> void 
	SQLmain.cur.execute("""
		UPDATE subjects SET
		zoomUrl = ?,
		zoomPasscode = ?
		WHERE
		id = ?;	""", (zoomURL, zoomPasscode, subjectID))
	SQLmain.conn.commit()
