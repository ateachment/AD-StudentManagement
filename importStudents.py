from School import *                         # import classes
from User import *
from CSV import Csv 

school = School([])

school.importStudentsFromCSV("import/students.csv") # import students
'''
school.addToLDAP()

schoolClasses = school.getSchoolClasses()    # output
for sc in schoolClasses:
    print(f"School class: {sc.getName()}") 
    Students = sc.getStudents()
    for student in Students:   
        print(f"\t{student.getSurname()}, {student.getFirstname()} in school class {student.getSchoolClass().getName()}")

'''
schoolClasses = school.getSchoolClasses()    
for sc in schoolClasses:
    sc.deleteFromLDAP()

