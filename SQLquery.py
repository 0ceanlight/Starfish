import SQLmain

# SELECT
# getAllSubjectIDs() -> subject.id[]
# getSubjectID(name: str) -> subject.id
# getSubjectUrls(subjectID: int) -> urls.url[]
# getSubjectZoomInfo(subjectID: int) -> [subjects.zoomURL, subjects.zoomPasscode][]
# addSubject(name: str) -> void

def allSubjectInfo(): # -> [(subject.id: int, name: str, zoomUrl, zoomPasscode)] (array of tuples)
	SQLmain.cur.execute("SELECT * FROM subjects;")
	return SQLmain.cur.fetchall()

def allSubjectIDs(): # -> subject.id[()]
	SQLmain.cur.execute("SELECT id FROM subjects;")
	return SQLmain.cur.fetchall()

def subjectID(name: str): # -> subject.id: int?
	SQLmain.cur.execute(
		"""SELECT id FROM subjects
		WHERE ? = name
		OR
		id IN 
		(SELECT subject_id from aliases WHERE ? = alias 
		LIMIT 1);""", (name, name)
	)
	id = SQLmain.cur.fetchall() # [(int,)]
	if id != []:
		return id[0][0]
	

def subjectUrls(subjectID: int): # -> [(urls.url,), (urls.url2,)]?
	SQLmain.cur.execute("SELECT url FROM urls WHERE subject_id = ?;", (subjectID,))
	return SQLmain.cur.fetchall()

def subjectZoomURL(subjectID: int): # -> str
	SQLmain.cur.execute("SELECT zoomUrl FROM subjects WHERE id = ?;", (subjectID,))
	if (url := SQLmain.cur.fetchall()) != []:
		return url[0][0]

def subjectZoomPasscode(subjectID: int): # -> str
	SQLmain.cur.execute("SELECT zoomPasscode FROM subjects WHERE id = ?;", (subjectID,))
	if (passcode := SQLmain.cur.fetchall()) != []:
		return passcode[0][0]
	
def subjectAliases(subjectID: int): # -> urls.url[]
	SQLmain.cur.execute("SELECT alias FROM aliases WHERE subject_id = ?;", (subjectID,))
	return SQLmain.cur.fetchall()

print(subjectZoomURL(1))