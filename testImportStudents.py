# filename: testImportStudents.py 
CAUTION: Running the Unittest file will delete all school classes and students from AD. 
Do NOT run the tests in production mode.

from School import *                        
from User import *
from Fileserver import *
from Ldap import PyAD
import importStudents 

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
        students = self.schoolClass1.getStudents()
        self.assertEqual(len(students), 2, 'Number of students wrong.')
        self.assertEqual(students[0].getUsername(),'Miller', 'Students username wrong.')

    def test_AddToLDAP(self):
        # remove school classes and/or students if there are any left in AD
        ldap = PyAD(Settings.dnStudents) 
        classNames = ldap.getSchoolClasses()
        for className in classNames:
            # print("delete school class: " + className)
            ldap.deleteSchoolClass(className)
        
        self.school.addToLDAP()
        ldap = PyAD(Settings.dnStudents)
        classNames = ldap.getSchoolClasses()
        self.assertEqual(classNames, ['c1', 'c2'], 'From ldap returned school classes wrong.')
        students = ldap.getStudents('c1')
        self.assertEqual(students, [["Miller", "Sam", "22.11.2004"], ["Smith", "Jake", "13.02.2003"]], 'From ldap returned students wrong.')
        # clean up
        schoolClasses = self.school.getSchoolClasses()
        for schoolClass in schoolClasses:
            schoolClass.deleteFromLDAP()
        classNames = ldap.getSchoolClasses()
        self.assertEqual(classNames, [], 'Ldap returns still school classe(s). Still not empty.')

    def test_ImportCsvFile(self):
        # remove school classes and/or students if there are any left in AD
        ldap = PyAD(Settings.dnStudents) 
        classNames = ldap.getSchoolClasses()
        for className in classNames:
            ldap.deleteSchoolClass(className)
        
        school = School([])
        school.importStudentsFromCSV("import/students.csv")
        school.addToLDAP()

        classNames = ldap.getSchoolClasses()
        
        self.assertEqual(classNames, ['c1', 'c2'], 'From ldap returned school classes wrong.')
        students = ldap.getStudents('c1')
        self.assertEqual(students, [["Colligan", "Manda", "22.09.2004"], ["Thieme", "Madelaine", "02.12.2000"]], 'From ldap returned students wrong.')
        
        school2 = School([])
        school2.importStudentsFromCSV("import/students2.csv")
        importStudents.deleteObsoleteSchoolClassesFromAD(school2)  # 'c2' will be deleted

        classNames = ldap.getSchoolClasses()
        self.assertEqual(classNames, ['c1'], 'From ldap returned school classes wrong.')

        school2.addToLDAP()
        classNames = ldap.getSchoolClasses()
        self.assertEqual(classNames, ['c1', 'c3'], 'From ldap returned school classes wrong.')
        students = ldap.getStudents('c1')
        self.assertEqual(students, [["Colligan", "Manda", "22.09.2004"], ["Belafonte", "Harry", "01.03.1927"]], 'From ldap returned students wrong.')
        students = ldap.getStudents('c3')
        self.assertEqual(students, [["Tarleton","Vito","22.02.2004"]], 'From ldap returned students wrong.')

        # clean up
        classNames = ldap.getSchoolClasses()
        for className in classNames:
            ldap.deleteSchoolClass(className)

if __name__ == '__main__':
    unittest.main()