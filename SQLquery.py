import SQLmain

# SELECT
# getAllSubjectIDs() -> subject.id[]
# getSubjectID(name: str) -> subject.id
# getSubjectUrls(subjectID: int) -> urls.url[]
# getSubjectZoomInfo(subjectID: int) -> [subjects.zoomURL, subjects.zoomPasscode][]

def getAllSubjectInfo(): # -> [(subject.id: int, name: str, zoomUrl, zoomPasscode)] (array of tuples)
	SQLmain.cur.execute("SELECT * FROM subjects;")
	return SQLmain.cur.fetchall()

def getAllSubjectIDs(): # -> subject.id[]
	SQLmain.cur.execute("SELECT id FROM subjects;")
	# convert array of tuples to array
	return [item for t in SQLmain.cur.fetchall() for item in t]

def getSubjectID(name: str): # -> subject.id: int?
	SQLmain.cur.execute(
		"""SELECT id FROM subjects
		WHERE ? = name
		OR
		id IN 
		(SELECT subject_id from aliases WHERE ? = alias 
		LIMIT 1);""", (name, name)
	)
	id = SQLmain.cur.fetchall() # [(int,)]
	if id != None and len(id) > 0:
		return id[0][0]

def getSubjectName(subjectID: int): # -> "name"
	SQLmain.cur.execute("SELECT name FROM subjects WHERE id = ?;", (subjectID,))
	name = SQLmain.cur.fetchall()
	if name != None and len(name) > 0:
		return name[0][0]
	return ""

def getSubjectURLs(subjectID: int): # -> [(urls.url,), (urls.url2,)]?
	SQLmain.cur.execute("SELECT url FROM urls WHERE subject_id = ?;", (subjectID,))
	return [item for t in SQLmain.cur.fetchall() for item in t]

def getSubjectZoomURL(subjectID: int): # -> str
	SQLmain.cur.execute("SELECT zoomUrl FROM subjects WHERE id = ?;", (subjectID,))
	url = SQLmain.cur.fetchall()
	if url != None and len(url) > 0:
		return url[0][0]
	return ""

def getSubjectZoomPasscode(subjectID: int): # -> str
	SQLmain.cur.execute("SELECT zoomPasscode FROM subjects WHERE id = ?;", (subjectID,))
	passcode = SQLmain.cur.fetchall()
	if passcode != None and len(passcode) > 0:
		return passcode[0][0]
	return ""
	
def getSubjectAliases(subjectID: int): # -> urls.url[]
	SQLmain.cur.execute("SELECT alias FROM aliases WHERE subject_id = ?;", (subjectID,))
	return SQLmain.cur.fetchall()
