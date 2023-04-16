from Settings import Settings
from Ldap import PyAD
from Csv import Csv
from User import Student

class School:                           
    def __init__(self,schoolClasses):
        self.__schoolClasses = schoolClasses
        
    def getSchoolClasses(self):
        return self.__schoolClasses

    def addSchoolClass(self, schoolClass):        
        self.__schoolClasses.append(schoolClass)

    def importStudentsFromCSV(self, filename):    # import students of a certain csv file 
        csv = Csv(filename)
        classNames = csv.importClassNames()       # import names of school classes

        for className in classNames:
            schoolClass = SchoolClass(className,[])
            listStudents = csv.importStudentsOfClass(className) # import student data of a certain name of school class 
            for listStudent in listStudents:
                student = Student(listStudent[0],listStudent[1],listStudent[2],schoolClass)
            self.addSchoolClass(schoolClass)

    def addToLDAP(self):        # export whole school to Active Directory
        for schoolClass in self.__schoolClasses:
            schoolClass.addToLDAP()
    
class SchoolClass:
    def __init__(self,name, students):
        self.__name = name
        self.__students = students                
        
    def getName(self):
        return self.__name

    def getStudents(self):
       return self.__students

    def addStudent(self, student):                
        self.__students.append(student)

    def addToLDAP(self):        # export school class with students to Active Directory
        ldap = PyAD(Settings.dnStudents)
        ldap.createSchoolClass(self.__name)
        for student in self.__students:
            student.addToLDAP()

    def deleteFromLDAP(self):   # delete school class with students from Active Directory
        ldap = PyAD(Settings.dnStudents)
        for student in self.__students:
            student.deleteFromLDAP()
        ldap.deleteSchoolClass(self.__name)
  

