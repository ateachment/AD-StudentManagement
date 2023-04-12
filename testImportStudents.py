# filename: testImportStudents.py 
# It makes sense that the name contains 'test' in order to be recognised by the framework as a test file.

from School import *                        
from User import *
from Fileserver import *
from Ldap import PyAD

import unittest                                     # import unit tests


class TestImportStudents(unittest.TestCase):
    @classmethod
    def setUpClass(self):                           # is executed once for all tests    
        self.schoolClass1 = SchoolClass("c1",[])         
        self.schoolClass2 = SchoolClass("c2",[])

        self.student1 = Student("Miller","Sam","22.11.2004",self.schoolClass1)  
        self.student2 = Student("Smith","Jake","13.02.2003",self.schoolClass1)
        self.student3 = Student("Hampton","Oliver","11.01.2004",self.schoolClass2)

        self.school = School([self.schoolClass1, self.schoolClass2]) 

    def test_School(self):                      # test names must start with 'test_' otherwise will not executed
        schoolClasses = self.school.getSchoolClasses()
        self.assertEqual(len(schoolClasses), 2, 'Number of school classes wrong.')
        self.assertEqual(schoolClasses[0].getName(), "c1", '1st school class wrong.')
        self.assertEqual(schoolClasses[1].getName(), "c2", '2nd school class wrong.')

    def test_Schoolclass(self):
        students = self.schoolClass1.getStudents()
        self.assertEqual(len(students), 2, 'Number of students wrong.')
        self.assertEqual(students[0].getUsername(),'Miller', 'Students username wrong.')

    def test_AddToLDAP(self):
        self.school.addToLDAP()
        ldap = PyAD(Settings.dnStudents)
        schoolClasses = ldap.getSchoolClasses()
        self.assertEqual(schoolClasses, ['c1', 'c2'], 'From ldap returned school classes wrong.')

    def test_DeleteFromLDAP(self):
        self.schoolClass1.deleteFromLDAP()
        self.schoolClass2.deleteFromLDAP()
        ldap = PyAD(Settings.dnStudents)
        schoolClasses = ldap.getSchoolClasses()
        self.assertEqual(schoolClasses, [], 'Ldap returns still school class(es).')

    def test_importCsvFile(self):
        self.school.importStudentsFromCSV("import/students.csv")
        self.student3 = Student("Tarleton","Vito","22.02.2004",self.schoolClass2)





if __name__ == '__main__':
    unittest.main()