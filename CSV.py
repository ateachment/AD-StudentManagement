from csv import reader

class Csv:
    def __init__(self, filename):       # constructor 
        with open('students.csv', newline='') as csvFile:
            self.__listStudents = list(reader(csvFile, delimiter=';'))[1:]

    def importClassNames(self):
        classNames = []                 # empty list with names of school classes
        for listStudent in self.__listStudents:
            if listStudent[3] not in classNames: # if not already added to list
                classNames.append(listStudent[3])
        return classNames

    def importStudentsOfClass(self, className):
        studentsOfClass = []
        for listStudent in self.__listStudents:
            if listStudent[3] == className:       # if sudent is in school class
                studentsOfClass.append(listStudent)
        return studentsOfClass
'''    
csv = Csv("students.csv")
classNames = csv.importClassNames()

for className in classNames:
    print(className)
    print(csv.importStudentsOfClass(className))
'''
