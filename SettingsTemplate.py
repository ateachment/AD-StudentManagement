class Settings:
    domainName = "trainingX.net"
    dnSchool = "dc=trainingX, dc=net"                       # Distinguished of domaine
    dnStudents = "ou=Students, ou=SchoolUsers, " + dnSchool # Distinguished Name of OU Students

    dnGLGroups = "ou=GL-Groups, " + dnSchool                # Distinguished Name of OU GL- and DL-Groups
    dnDLGroups = "ou=DL-Groups, " + dnSchool
    
    nameFileserver = "FSX1"
    shareHomeStudents = "\\\\"+nameFileserver+"\\HomeStudents$"         # "\" must be escaped by another "\"
    homeDrive = "H:"
    dirProjectsStudents = "\\\\"+nameFileserver+"\\Projects$"           # student's projects base dir
    pathProjectsStudents = "D:\\Projects"
    projectDrive = "P:"
