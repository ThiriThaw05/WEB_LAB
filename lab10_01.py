import ZODB, ZODB.FileStorage
import persistent
import transaction
from z_enrollment import *
import BTrees._OOBTree

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

if 'courses' not in root:
    root.courses = BTrees.OOBTree.BTree()
if 'students' not in root:
    root.students = BTrees.OOBTree.BTree()

    c1 = Course(101, "Computer Programming",4 )
    c2 = Course(201, "Web Programming",4 )
    c3 = Course(202, "Software Engineering Principle",5 )
    c4 = Course(301, "Artificial Intelligent Programming",3)
    
    root.courses[101] = c1
    root.courses[201] = c2
    root.courses[202] = c3
    root.courses[301] = c4

    s1 = Student(1101, "Mr. Christian de Neuvillette")
    s2 = Student(1102, "Mr. Zhong Li")
    s3 = Student(1103, "Mr. Dvalinn Durinson")

    e1 = s1.enrollCourse(c1)
    e2 = s1.enrollCourse(c2)
    e3 = s1.enrollCourse(c4)

    e4 = s2.enrollCourse(c1)
    e5 = s2.enrollCourse(c2)
    e6 = s2.enrollCourse(c3)

    e7 = s3.enrollCourse(c1)
    e8 = s3.enrollCourse(c2)
    e9 = s3.enrollCourse(c3)
    e10 = s3.enrollCourse(c4)

    e1.setGrade("B")
    e2.setGrade("B")
    e3.setGrade("C")

    e4.setGrade("A")
    e5.setGrade("B")
    e6.setGrade("D")

    e7.setGrade("C")
    e8.setGrade("A")
    e9.setGrade("B")
    e10.setGrade("C")

    root.students[1101] = s1
    root.students[1102] = s2
    root.students[1103] = s3

    transaction.commit()
    print("created and saved to mydata.fs")

connection.close()
db.close()