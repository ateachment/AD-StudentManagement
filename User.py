from Settings import Settings
from Ldap import PyAD
from Fileserver import *

class User:                                                 # superclass "User"
    def __init__(self, surname, firstname, dateOfBirth):    # constructor 
        self._surname = surname                             # protected properties/attributes => only one "_"
        self._firstname = firstname
        self._password = firstname[0] + surname[0] + dateOfBirth  
        self._dateOfBirth = dateOfBirth
        self._username = surname 
        
    def getSurname(self):                                  
        return self._surname
    
    def getFirstname(self):
        return self._firstname

    def getPassword(self):
        return self._password

    def getDateOfBirth(self):
        return self._dateOfBirth

    def getUsername(self):
        return self._username


class Student(User):    # subclass "Student" inherits every property and method from superclass "User"
    def __init__(self, surname, firstname, dateOfBirth, schoolClass):
        User.__init__(self, surname, firstname, dateOfBirth)  # constructor of superclass is invoked
        schoolClass.addStudent(self);   # adds himself to school class
        self.__schoolClass = schoolClass

    def getSchoolClass(self):              
        return self.__schoolClass

    def addToLDAP(self):
        ldap = PyAD(Settings.dnStudents)
        # add to ldap if not already in school class
        foundStudentSchoolClass = ldap.findStudent(self._surname , self._firstname, self._dateOfBirth)
        if foundStudentSchoolClass == self.__schoolClass.getName():
            pass # do nothing
        elif foundStudentSchoolClass == "": # not already in another school class -> create student
            # ldap.createStudent() returns the possibly modified username for updating
            self._username = ldap.createStudent(self._username
                               , self._surname
                               , self._firstname
                               , self._password
                               , self._dateOfBirth
                               , self.__schoolClass.getName())

            fs = Fileserver()
            fs.createHomeDirStudent(self._username)   
        else:   # already in another school class 
                # -> delete and recreate student for simplicity reason
            ldap = PyAD(Settings.dnStudents)
            ldap.deleteStudent(self._surname, self._firstname, self._dateOfBirth, foundStudentSchoolClass)
            fs = Fileserver()
            fs.deleteHomeDirStudent(self._username)
            self._username = ldap.createStudent(self._username
                               , self._surname
                               , self._firstname
                               , self._password
                               , self._dateOfBirth
                               , self.__schoolClass.getName())
    
    def deleteFromLDAP(self):
        ldap = PyAD(Settings.dnStudents)
        ldap.deleteStudent(self._surname, self._firstname, self._dateOfBirth, self.__schoolClass.getName())

        fs = Fileserver()
        fs.deleteHomeDirStudent(self._username)

        
