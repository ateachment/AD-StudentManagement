'********************************************************************
'Login script for students	1.0		
'Wolfhard Eick	10/2019


'--------------------------------------------------------------------
'Settings
'
fileserverStudents = "FSX1"						'File server of students
domain = "trainingX.net"


'--------------------------------------------------------------------
'get school class of student
'
Set WshNetwork = WScript.CreateObject("WScript.Network")

Do While wshNetwork.username = "" 					'wait until username of student
   WScript.Sleep 250 								'is available 
Loop 

username =  WshNetwork.UserName						'get actual username 
Set groups = GetObject("WinNT://" & domain & "/" & username)  		'get group memberships of student

For Each group In groups.Groups						'iterate over groups
	If left(group.Name,3) = "GL_" Then				'get gl-group of school class
		strLength = len(group.Name)
		schoolclass = mid(group.Name,4,strLength)	'extract name of school class
	end if
Next

'MsgBox username & " is a member of school class " & schoolclass, vbOkOnly, "Membership of school class"



'--------------------------------------------------------------------
'map drive
'
On Error Resume Next 
wshNetwork.RemoveNetworkDrive "P:", True, True 				'delete an eventually existing mapping

wshNetwork.MapNetworkDrive "P:", "\\" & fileserverStudents & "\" & schoolclass & "$"	'map drive

