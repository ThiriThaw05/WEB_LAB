import ZODB, ZODB.FileStorage
import persistent
import transaction 
from typing import Optional, List

class Course (persistent.Persistent):
    def __init__(self, id, name = "", credit = 0):
        self.id = id
        self.name = name
        self.credit = credit

    def __str__ (self):
        return f"ID: {self.id} Course Name: {self.name}, Credit: {self.credit}" 
    
    def setName(self,name):
        self.name = name

    def getCredit(self):
        return self.credit
    
    def printDetail(self):
        print(self.__str__())

class Enrollment (persistent.Persistent):
    def __init__(self, course , student, grade = None):
        self.course = course
        self.grade = grade
        self.student = student

    def __str__ (self):
        g = self.grade if self.grade else "N/A"
        return f"Enrollment: Student {self.student.name} | Course {self.course.name} | Grade: {g}" 
    
    def getCourse(self):
        return self.course
    
    def getGrade(self):
        return self.grade
    
    def setGrade(self,grade):
        self.grade = grade
    
    def printDetail(self):
        print(self.__str__())

class Student (persistent.Persistent):
    def __init__(self, id, name = ""):
        self.id = id
        self.name = name
        self.enrolls = []

    def __str__(self):
        return "Student ID: %8s Name: %s, Enrollments: %d" (str(self.id), self.name, len(self.enrolls))
    
    def setName(self,name):
        self.name = name

    def enrollCourse(self,course):
        for e in self.enrolls:
            if e.course.id == course.id:
                return e
        enrollment = Enrollment(course,self)
        self.enrolls.append(enrollment)
        return enrollment
    
    def getEnrollment(self,course):
        for e in self.enrolls:
            if e.course.id == course.id:
                return e
        return None
    
    def printTranscript(self):
        print("Transcript for %s (ID: %s)" % (self.name,self.id))
        print("-"*50)
        if not self.enrolls:
            print("No course enrolled yet")
            return 
        gradePoints = {
            "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3 ,"C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "D-": 0.7,
            "F": 0.0
        }

        totalCredits = 0
        totalPoints = 0.0

        for e in self.enrolls:
            grade = e.grade if e.grade else "N/A"
            print("ID: %s | Course: %-20s | Credit: %d | Grade: %s" % (e.course.id, e.course.name, e.course.credit, grade))
            if e.grade in gradePoints:
                totalCredits += e.course.credit
                totalPoints += gradePoints[e.grade] * e.course.credit
            if totalCredits > 0:
                gpa = totalPoints / totalCredits
                print("-"*50)
                print("Total GPA: %.2f" % (gpa))
            else:
                print("GPA not available (no graded course).")


