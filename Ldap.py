from abc import ABC, abstractmethod     # import Abstract Base Classes (ABCs)

class AbstractLDAP(ABC):
 
    def __init__(self, dnStudents):
        self._dnStudents = dnStudents
        super().__init__()
    
    @abstractmethod
    def createStudent(self, username, nameSchoolClass):
        pass
    @abstractmethod
    def deleteStudent(self, username, nameSchoolClass):
        pass
    @abstractmethod
    def createSchoolClass(self, nameSchoolClass):
        pass
    @abstractmethod
    def deleteSchoolClass(self, nameSchoolClass):
        pass

from pyad import *
from Settings import Settings
from Fileserver import *

class PyAD(AbstractLDAP):
    def createStudent(self, username, surname, firstname, password, dateOfBirth, nameSchoolClass):
        query = adquery.ADQuery()
        cnUnique = False
        numChar = 0
        while(cnUnique == False):
            query.execute_query(attributes = ["cn"],            # query: does cn already exist
                where_clause=("cn = '" + username + "'"),
                base_dn = Settings.dnSchool)
            if query.get_row_count() > 0:                       # yes: add character
                numChar = numChar + 1
                if(numChar <= len(firstname)):                  # if the character set of the first name is large enough
                    username = surname + firstname[:numChar]    # add number of characters from beginning of first ame
                else:                                           # if the character set of the first name is used up
                    username = surname + firstname + (numChar - len(firstname))  * 'x'  # added number of 'x'
            else:                                               # cn is unique => create user
                cnUnique = True
                ouSchoolClass = pyad.adcontainer.ADContainer("ou="+nameSchoolClass+", "+self._dnStudents, adsi_ldap_com_object=None, options={})
                student = aduser.ADUser.create(username
                                     , ouSchoolClass
                                     , password=password
                                     , upn_suffix=None
                                     , enable=True
                                     , optional_attributes={"sn":surname
                                                            , "givenName":firstname
                                                            , "employeeID":dateOfBirth  # using existing employeeId attribute is easier than extending AD scheme
                                                            , "description":"Student"
                                                            , "pwdLastSet":0            # password must be changed on first login
                                                            , "homeDrive":Settings.homeDrive                                   # set home drive
                                                            , "homeDirectory":Settings.shareHomeStudents + "\\" + username})   # set home directory
                # put new student in global group of its school class
                gl_groupSchoolClass = pyad.from_dn("cn=GL_" + nameSchoolClass + ", " + Settings.dnGLGroups)   
                gl_groupSchoolClass.add_members([student])           
        return username    # return possibly modified username     

    def deleteStudent(self, surname, firstname, dateOfBirth, nameSchoolClass):
        # print("delete ", surname, firstname, dateOfBirth, nameSchoolClass)
        dnSchoolClass = "ou="+nameSchoolClass + ", " + self._dnStudents
        query = adquery.ADQuery()
        query.execute_query(attributes = ["cn"],
                where_clause=("sn = '" + surname + "' and givenName = '" + firstname + "' and employeeID = '" + dateOfBirth + "'"),
                base_dn = dnSchoolClass)
        if query.get_row_count() >= 1:                              # if student exists => delete it
            ouSchoolClass = pyad.adcontainer.ADContainer(dnSchoolClass, adsi_ldap_com_object=None, options={})
            fs = Fileserver()
            for row in query.get_results():
                ouSchoolClass.from_cn(row["cn"]).delete()
                fs.deleteHomeDirStudent(row["cn"])
   
    def createSchoolClass(self, nameSchoolClass):
        query = adquery.ADQuery()
        query.execute_query(attributes = ["distinguishedName"],
                where_clause=("ou = '" +nameSchoolClass + "'"),
                base_dn = self._dnStudents)
        if query.get_row_count() == 0:                              # if school class not yet exists => create
            ouStudents = pyad.adcontainer.ADContainer(self._dnStudents, adsi_ldap_com_object=None, options={})
            ouStudents.create_container(nameSchoolClass)
            # create a new global group for students of school class
            ouGLgroups = pyad.adcontainer.ADContainer.from_dn(Settings.dnGLGroups)
            gl_groupSchoolClass = ouGLgroups.create_group("GL_" + nameSchoolClass
                                                 , security_enabled=True
                                                 , scope='GLOBAL'
                                                 , optional_attributes = {"description":"Students of school class " + nameSchoolClass})
            # create a new domaine local for project dir of students
            ouDLgroups = pyad.adcontainer.ADContainer.from_dn(Settings.dnDLGroups)
            dl_groupSchoolClass = ouDLgroups.create_group("DL_" + nameSchoolClass + "_F" 
                                            , security_enabled=True
                                            , scope='LOCAL'
                                            , optional_attributes = {"description":"Full access for project dir of students of school class " + nameSchoolClass})
            
            gl_groupStudents = pyad.from_dn("cn=GL_Students, " + Settings.dnGLGroups) # put global group of school class
            gl_groupStudents.add_members([gl_groupSchoolClass])             # into global group of all students "GL_Students" and
            dl_groupSchoolClass.add_members([gl_groupSchoolClass])          # into domaine local group of students of a school class
            # create folder and share
            fs = Fileserver()
            fs.createProjectDirStudent(nameSchoolClass)
            fs.addShareProjectDirStudent(nameSchoolClass)
 
    def deleteSchoolClass(self, nameSchoolClass):
        dnSchoolClass = "ou="+nameSchoolClass+", "+ self._dnStudents
        query = adquery.ADQuery()
        query.execute_query(attributes = ["distinguishedName"],
                where_clause=("ou = '" +nameSchoolClass + "'"),
                base_dn = self._dnStudents)
        if query.get_row_count() == 1:                          # if school class exists
            query = adquery.ADQuery()
            query.execute_query(attributes = ["sn", "givenName", "employeeID"],  # employeeID holds date of birth
                where_clause=("cn = '*'"),
                base_dn = dnSchoolClass)
            if query.get_row_count() > 0:                       # if school class not empty 
                for row in query.get_results():                 # delete students
                    self.deleteStudent(row["sn"], row["givenName"], row["employeeID"],  nameSchoolClass)
            ouSchoolClass = pyad.adcontainer.ADContainer(dnSchoolClass, adsi_ldap_com_object=None, options={})
            ouSchoolClass.delete()                              # delete school class ou
            # delete global and domaine local groups of school class
            gl_groupSchoolClass = pyad.from_dn("cn=GL_" + nameSchoolClass + ", " + Settings.dnGLGroups) 
            gl_groupSchoolClass.delete()
            dl_groupSchoolClass = pyad.from_dn("cn=DL_" + nameSchoolClass + "_F" + ", " + Settings.dnDLGroups) 
            dl_groupSchoolClass.delete()
            # delete folder and share
            fs = Fileserver()
            fs.deleteProjectDirStudent(nameSchoolClass)
            fs.deleteShareProjectDirStudent(nameSchoolClass)
            
    def getSchoolClasses(self):
        query = adquery.ADQuery()
        query.execute_query(attributes = ["ou"],
            where_clause=("ou = '*' and ou <> 'Students'"),     # exclude users and base dn
            base_dn = self._dnStudents)
        schoolClasses = []
        result = query.get_results()        
        for schoolClass in result:
            schoolClasses.append(schoolClass['ou'][0])
        return schoolClasses
    
    def getStudents(self, nameSchoolClass):
        dnSchoolClass = "ou="+nameSchoolClass + ", " + self._dnStudents
        query = adquery.ADQuery()
        query.execute_query(attributes = ['sn', 'givenName', 'employeeID'],
                    # surname, firstname, employeeID holds date of birth       
        # query.execute_query(attributes = ['cn', 'sn', 'givenName', 'employeeID'],  
                    # username, surname, firstname, employeeID holds date of birth       
            where_clause=("ou <> '" + nameSchoolClass + "'"),     # exclude base dn   
            base_dn = dnSchoolClass)
        students = []
        result = query.get_results()       
        for student in result:
            # students.append(student['cn'], [student['sn'], student['givenName'], student['employeeID']])
            students.append([student['sn'], student['givenName'], student['employeeID']])
        return students
    
    def findStudent(self, surname, firstname, dateOfBirth):
        # print("find ", surname, firstname, dateOfBirth)
        query = adquery.ADQuery()
        query.execute_query(attributes = ["distinguishedName"],
                where_clause=("sn = '" + surname + "' and givenName = '" + firstname + "' and employeeID = '" + dateOfBirth + "'"),
                base_dn = Settings.dnStudents)
        if query.get_row_count() >= 1:                              
            for row in query.get_results():
                # i.e. row["distinguishedName"] = CN=Colligan,OU=c1,OU=Students,OU=SchoolUsers,DC=trainingX,DC=net
                className = row["distinguishedName"].split(",")[1].split("=")[1]
                return className
        return ""   # not found -> not already in other school class