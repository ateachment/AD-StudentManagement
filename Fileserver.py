from Settings import Settings
import os
import shutil
import win32security, win32netcon, win32net, ntsecuritycon, win32file

class Fileserver():
    def createHomeDirStudent(self, username):
        homeDir = Settings.shareHomeStudents + "\\" + username
        if os.path.exists(homeDir) == False:    # if home dir does not exist
            os.mkdir(homeDir)                   # make dir

            # How to set DACLs:
            # https://stackoverflow.com/questions/26465546/how-to-authorize-deny-write-access-to-a-directory-on-windows-using-python
            
            user, domain, type = win32security.LookupAccountName("", Settings.domainName + "\\" + username) # Find the SIDs for user of home dir
            sd = win32security.GetFileSecurity(homeDir, win32security.DACL_SECURITY_INFORMATION) # Find the DACL part of the Security Descriptor for the folder
            
            dacl = sd.GetSecurityDescriptorDacl()                                                # get security descriptor DACL 
            dacl.AddAccessAllowedAceEx(win32security.ACL_REVISION, 3, 2032127, user)             # add full control to folder, subfolder and files ACE to DACL

            sd.SetSecurityDescriptorDacl(1, dacl, 0)                                             # Put new (extended) DACL into the Security Descriptor,
            win32security.SetFileSecurity(homeDir, win32security.DACL_SECURITY_INFORMATION, sd)  # update the folder with the updated Security Descriptor
            

    def deleteHomeDirStudent(self, username):
        homeDir = Settings.shareHomeStudents + "\\" + username
        if os.path.exists(homeDir) == True:             # if home dir exists
            #os.system('rmdir /S /Q "{}"'.format(homeDir))
            shutil.rmtree(homeDir, ignore_errors=True)  # remove dir with content recursively            

    def createProjectDirStudent(self, nameSchoolClass):
        projectDir = Settings.dirProjectsStudents + "\\" + nameSchoolClass
        if os.path.exists(projectDir) == False:    # if project dir does not exist
            os.mkdir(projectDir)                   # make dir

            # Find the SID of group which uses project dir
            group, domain, type = win32security.LookupAccountName("", Settings.domainName + "\\DL_" + nameSchoolClass + "_F")
            # Find the DACL part of the Security Descriptor for the folder
            sd = win32security.GetFileSecurity(projectDir, win32security.DACL_SECURITY_INFORMATION) 
            # get security descriptor DACL 
            dacl = sd.GetSecurityDescriptorDacl()
            # add full access of group to folder, subfolder and files ACE to DACL
            dacl.AddAccessAllowedAceEx(win32security.ACL_REVISION, 3, 2032127, group)   
            # put new (extended) DACL into the Security Descriptor
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            # update the folder with the updated Security Descriptor
            win32security.SetFileSecurity(projectDir, win32security.DACL_SECURITY_INFORMATION, sd)  

    def deleteProjectDirStudent(self, nameSchoolClass):
        projectDir = Settings.dirProjectsStudents + "\\" + nameSchoolClass
        if os.path.exists(projectDir) == True:             # if project dir exists
            shutil.rmtree(projectDir, ignore_errors=True)  # remove dir with content recursively         

    def addShareProjectDirStudent(self, nameSchoolClass):
        sd = win32security.SECURITY_DESCRIPTOR()
        # get the "well known" SID for the administrators group
        subAuths = ntsecuritycon.SECURITY_BUILTIN_DOMAIN_RID, ntsecuritycon.DOMAIN_ALIAS_RID_ADMINS
        sidAdmins = win32security.SID(ntsecuritycon.SECURITY_NT_AUTHORITY, subAuths)
        # Find the SID of dl group which uses share to project dir
        group, domain, type = win32security.LookupAccountName("", Settings.domainName + "\\DL_" + nameSchoolClass + "_F")
        # Set ACL, giving DL group of school class and admin full access
        dacl = win32security.ACL(128)
        dacl.AddAccessAllowedAce(win32file.FILE_ALL_ACCESS, sidAdmins)
        dacl.AddAccessAllowedAce(win32file.FILE_ALL_ACCESS, group)
        sd.SetSecurityDescriptorDacl(1, dacl, 0)
        
        sharename = nameSchoolClass + "$"   # hide share
        shinfo={}                           # shinfo struct
        shinfo['netname'] = sharename
        shinfo['type'] = win32netcon.STYPE_DISKTREE
        shinfo['remark'] = 'Project share for schoolclass %s' % (sharename,)
        shinfo['permissions'] = 0
        shinfo['max_uses'] = -1             # unlimited users
        shinfo['security_descriptor'] = sd
        shinfo['current_uses'] = 0
        shinfo['path'] = Settings.pathProjectsStudents + "\\" + nameSchoolClass
        shinfo['passwd'] = ''
        win32net.NetShareAdd("\\\\" + Settings.nameFileserver,502,shinfo) # add share
        
    def deleteShareProjectDirStudent(self, nameSchoolClass):
        win32net.NetShareDel("\\\\" + Settings.nameFileserver, nameSchoolClass + "$")
        

