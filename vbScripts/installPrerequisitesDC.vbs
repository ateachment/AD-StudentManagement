' VBScript for installing prerequisites on domain controller
' Run as domain administrator on domain controller
' Filename: installPrerequisitesDC.vbs		
' Wolfhard Eick	03/2023

Const dnSchool = "dc=trainingX, dc=net"                       ' Distinguished of domaine

' create OUs
Set objDomain = GetObject("LDAP://" + dnSchool)
Set objOU = objDomain.Create("organizationalUnit", "ou=DL-Groups")
objOU.SetInfo  

Set objOU = objDomain.Create("organizationalUnit", "ou=GL-Groups")
objOU.SetInfo  

Set objOU = objDomain.Create("organizationalUnit", "ou=SchoolUsers")
objOU.SetInfo  

Set objOU1 = GetObject("LDAP://ou=SchoolUsers," + dnSchool)
Set objOU = objOU1.Create("organizationalUnit", "ou=Students")
objOU.SetInfo

' create global groups
Const ADS_GROUP_TYPE_GLOBAL_GROUP = &h2
Const ADS_GROUP_TYPE_SECURITY_ENABLED = &h80000000

Set objOU = GetObject("LDAP://ou=GL-Groups," + dnSchool)
Set objGroup = objOU.Create("Group", "cn=GL_Students")
objGroup.Put "sAMAccountName", "GL-Students"
objGroup.Put "groupType", ADS_GROUP_TYPE_GLOBAL_GROUP Or _
    ADS_GROUP_TYPE_SECURITY_ENABLED
objGroup.SetInfo

Set objOU = GetObject("LDAP://ou=GL-Groups," + dnSchool)
Set objGroup = objOU.Create("Group", "cn=GL_SchoolUsers")
objGroup.Put "sAMAccountName", "GL_SchoolUsers"
objGroup.Put "groupType", ADS_GROUP_TYPE_GLOBAL_GROUP Or _
    ADS_GROUP_TYPE_SECURITY_ENABLED
objGroup.SetInfo

' add GL-Students to GL-SchoolUsers
Const ADS_PROPERTY_APPEND = 3 

Set objGroup = GetObject("LDAP://cn=GL_SchoolUsers,ou=GL-Groups," + dnSchool) 
 
objGroup.PutEx ADS_PROPERTY_APPEND, "member", Array("cn=GL_Students,ou=GL-Groups," + dnSchool)
objGroup.SetInfo

WScript.Echo " Created OUs:",vbCr,"DL-Groups",vbCr,"GL-Groups",vbCr,"SchoolUsers",vbCr, "Created global groups:",vbCr,"GL_Students",vbCr,"GL_SchoolUsers" 