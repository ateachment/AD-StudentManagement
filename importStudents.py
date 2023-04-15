from School import *                        # import classes
from User import *
from Csv import Csv 
from Ldap import PyAD
import sys


def deleteObsoleteSchoolClassesFromAD(school):
    ldap = PyAD(Settings.dnStudents)
    ldapClassNames = ldap.getSchoolClasses()
    classNames = []
    for schoolClass in school.getSchoolClasses():
        classNames.append(schoolClass.getName())
    for ldapClassName in ldapClassNames:
        if ldapClassName not in classNames:     # school class in ldap is obsolete
            ldap.deleteSchoolClass(ldapClassName)
        else:
            deleteObsoleteStudentsFromAD(school, ldapClassName)

def deleteObsoleteStudentsFromAD(school, className):
    ldap = PyAD(Settings.dnStudents)
    ldapStudents = ldap.getStudents(className)
    studentsNames = []
    for schoolClass in school.getSchoolClasses():
        if schoolClass.getName() == className:
            students = schoolClass.getStudents()
            for student in students:
                studentsNames.append([student.getSurname(), student.getFirstname(), student.getDateOfBirth()])
    for ldapStudent in ldapStudents:
        if ldapStudent not in studentsNames:
            ldap.deleteStudent(ldapStudent[0], ldapStudent[1], ldapStudent[2], className)



if __name__ == "__main__":
    if(len(sys.argv)) == 1:                 # no command line argument
        filename = input("CSV import file with students: ")
    else:                                   # filename as argument
        filename = sys.argv[1]
        
    school = School([])
    print(filename + " is being imported ...")
    importStudents = school.importStudentsFromCSV(filename)      # import students
    print("Delete obsolete school classes ...")
    deleteObsoleteSchoolClassesFromAD(school)
    school.addToLDAP()


