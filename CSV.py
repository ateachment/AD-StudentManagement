import os
from csv import reader

class Csv:
    def __init__(self, rel_path):       # constructor 
        script_dir = os.path.dirname(__file__)      # 'os' for compatibility reason 
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, newline='') as csvFile:
            self.__listStudents = list(reader(csvFile, delimiter=';'))[1:]  # omit 1st line

    def importClassNames(self):
        classNames = []                 # empty list with names of school classes
        for listStudent in self.__listStudents:
            if listStudent[3] not in classNames:    # if not already added to list
                classNames.append(listStudent[3])
        return classNames

    def importStudentsOfClass(self, className):
        studentsOfClass = []
        for listStudent in self.__listStudents:
            if listStudent[3] == className:         # if sudent is in school class
                studentsOfClass.append(listStudent)
        return studentsOfClass
    