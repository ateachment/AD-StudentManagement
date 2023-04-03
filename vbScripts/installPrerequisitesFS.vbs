' VBScript for installing prerequisites on fileserver
' Run as domain administrator on file server
' Filename:  installPrerequisitesFS.vbs		
' Wolfhard Eick	03/2023

Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")

' Create folders if not exist
If Not fso.FolderExists("D:\Home") then
    fso.CreateFolder "D:\Home"
End If
If Not fso.FolderExists("D:\Home\SchoolUsers") then
    fso.CreateFolder "D:\Home\SchoolUsers"
End If
If Not fso.FolderExists("D:\Home\SchoolUsers\Students") then
    fso.CreateFolder "D:\Home\SchoolUsers\Students"
End If
If Not fso.FolderExists("D:\Projects") then
    fso.CreateFolder "D:\Projects"
End If

' Create shares
Const FILE_SHARE = 0
Const MAXIMUM_CONNECTIONS = 10000
strComputer = "."

Set objWMIService = GetObject("WINMGMTS:{impersonationLevel=impersonate,(Security)}!\\" & strComputer & "\ROOT\CIMV2")
Set SecDescClass = objWMIService.Get("Win32_SecurityDescriptor")
Set SecDesc = SecDescClass.SpawnInstance_()
Set Trustee =  objWMIService.Get("Win32_Trustee").SpawnInstance_ 
Trustee.Name = "EVERYONE"
Set ACE = objWMIService.Get("Win32_Ace").SpawnInstance_
ACE.Properties_.Item("AccessMask") = 2032127 '2032127 = "Full"; 1245631 = "Change"; 1179817 = "Read"
ACE.Properties_.Item("AceFlags") = 3
ACE.Properties_.Item("AceType") = 0
ACE.Properties_.Item("Trustee") = Trustee
SecDesc.Properties_.Item("DACL") = Array(ACE)
Set Share = objWMIService.Get("Win32_Share")

Set InParam = Share.Methods_("Create").InParameters.SpawnInstance_()
InParam.Properties_.Item("Access") = SecDesc
InParam.Properties_.Item("Description") = "Share for students homefolder"
InParam.Properties_.Item("Name") = "HomeStudents$"
InParam.Properties_.Item("Path") = "D:\Home\SchoolUsers\Students"
InParam.Properties_.Item("Type") = 0
Share.ExecMethod_ "Create", InParam

Set InParam = Share.Methods_("Create").InParameters.SpawnInstance_()
InParam.Properties_.Item("Access") = SecDesc
InParam.Properties_.Item("Description") = "Share for students project"
InParam.Properties_.Item("Name") = "Projects$"
InParam.Properties_.Item("Path") = "D:\Projects"
InParam.Properties_.Item("Type") = 0
Share.ExecMethod_ "Create", InParam

WScript.Echo " Created folders:",vbCr,"D:\Home\SchoolUsers\Students",vbCr,"D:\Projects",vbCr,"Created shares:",vbCr,"HomeStudents$",vbCr,"Projects$"

