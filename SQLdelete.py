import SQLmain

# DELETE
# deleteSubject(subjectID: int) -> void?
# deleteURLs(subjectID: int, url: str)
# deleteAllURLs(subjectID: int)
# deleteZoom(subjectID: int)

# note: you might have to conn.commit


# def deleteSubject(subjectID: int):
def deleteAllURLs(subjectID: int):
    SQLmain.cur.execute("DELETE FROM urls WHERE subject_id = ?", (subjectID,))
    SQLmain.conn.commit()

def deleteSubjectUrl(subjectID: int, url: str):
    SQLmain.cur.execute("DELETE FROM urls WHERE subject_id = ? AND url = ?", (subjectID, url))
    SQLmain.conn.commit()


# beware this one
def deleteSubject(subjectID: int):
    SQLmain.cur.execute("DELETE FROM aliases WHERE subject_id = ?", (subjectID,)) 
    SQLmain.cur.execute("DELETE FROM urls WHERE subject_id = ?", (subjectID,)) 
    SQLmain.cur.execute("DELETE FROM subjects WHERE id = ?", (subjectID,))
    SQLmain.conn.commit()