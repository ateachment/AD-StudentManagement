from School import *                        # import classes
from User import *
from Csv import Csv 
import sys

if __name__ == "__main__":
    if(len(sys.argv)) == 1:                 # no command line argument
        filename = input("CSV import file with students: ")
    else:                                   # filename as argument
        filename = sys.argv[1]

print(filename + " is being imported ...")

school = School([])
school.importStudentsFromCSV(filename)      # import students
school.addToLDAP()

schoolClasses = school.getSchoolClasses()   # output
for sc in schoolClasses:
    print(f"School class: {sc.getName()}") 
    Students = sc.getStudents()
    for student in Students:   
        print(f"\t{student.getSurname()}, {student.getFirstname()} in school class {student.getSchoolClass().getName()}")


schoolClasses = school.getSchoolClasses()    
for sc in schoolClasses:
    sc.deleteFromLDAP()

