from School import *                        
from User import *
from Fileserver import *

schoolClass = SchoolClass("school_class1",[])         
schoolClass2 = SchoolClass("school_class2",[])       
student = Student("Miller", "Sam", "11.11.2000", schoolClass)
student = Student("Meyer", "Sam", "11.11.2000", schoolClass2)

schoolClass.addToLDAP()
schoolClass2.addToLDAP()

#schoolClass.deleteFromLDAP()
#schoolClass2.deleteFromLDAP()


