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
        self._username = ldap.createStudent(self._username
                               , self._surname
                               , self._firstname
                               , self._password
                               , self._dateOfBirth
                               , self.__schoolClass.getName())

        fs = Fileserver()
        fs.createHomeDirStudent(self._username)
    
    def deleteFromLDAP(self):
        ldap = PyAD(Settings.dnStudents)
        ldap.deleteStudent(self._username, self.__schoolClass.getName())

        fs = Fileserver()
        fs.deleteHomeDirStudent(self._username)

        
