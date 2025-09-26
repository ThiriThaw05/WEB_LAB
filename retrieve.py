import ZODB, ZODB.FileStorage
import persistent
import transaction
from z_enrollment import *
import BTrees._OOBTree

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

if __name__ == "__main__":
    print("Courses: ")
    courses = root.courses
    for c in courses:
        course = courses[c]
        course.printDetail()
        print()

    print("Students and Transcripts: ")
    students = root.students
    for s in students:
        student = students[s]
        student.printTranscript()
        print()
