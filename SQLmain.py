import sqlite3

# LIST OF FUNCS:
# createConnection(dbFile) -> connection
# setupDB() -> void
#
# addSubject(name: str) -> void
#
# setSubjectUrls(subjectID: int, *argv) -> void 
# setSubjectZoomInfo(subjectID: int, zoomURL: str, zoomPasscode: str) -> void 

# REFERENCE query, update, delete

# beware the ;'s 
# sql.cur needs tuples (value, value) https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
# (don't ask smh)


def createConnection(dbFile) -> sqlite3.Connection:
	conn = None
	try: 
		conn = sqlite3.connect(dbFile)
	except sqlite3.Error as e:
		print(e)
		exit(1)
	return conn
	

dbFile = "subjects.db"
conn = createConnection(dbFile)

cur = conn.cursor()

# enable foreign key functions (no duplicate ids, 
# # or records with missing primary IDs)
# (see dbSetup.sql)



# cur.execute("SELECT * FROM aliases INNER JOIN subjects ON subjects.id = aliases.subject_id;")
# print(cur.fetchall())

# run at the beginning - in case tables have not been created
def setupDB() -> None:
	# Open and read the file as a single buffer
	file = open('dbSetup.sql', 'r')
	sqlFile = file.read()
	file.close()

	# all SQL commands (split on ';')
	sqlCommands = sqlFile.split(';')

	# execute every command from the input file
	for command in sqlCommands:
		# skip && report sql errors
		try:
			# add stripped ;'s
			cur.execute(command + ';')
		except sqlite3.OperationalError as e:
			print("Command skipped: " + e)






setupDB()
print('DB status: ready')
	
# NOTES
# Larger example that inserts many records at a time
# purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
# 	('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
# 	('2006-04-06', 'SELL', 'IBM', 500, 53.00),
# ]
# c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
