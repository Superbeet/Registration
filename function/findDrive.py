import subprocess
import sys
import os

def listDrives():
    #on windows
    #Get the fixed drives
    #wmic logicaldisk get name,description
    if 'win' in sys.platform:
        drivelist = subprocess.Popen('wmic logicaldisk get name,description', shell=True, stdout=subprocess.PIPE)
        drivelisto, err = drivelist.communicate()
        driveLines = drivelisto.split('\r\r\n')
        for line in driveLines:
            if len(line) == '':
                driveLines.remove('')
                
        return driveLines
#         print "driveLines->", driveLines     
#         for line in driveLines:
#             if len(line):   # Avoid search for empty strings
#                 print searchDriveLetter(line)
            
    elif 'linux' in sys.platform:
         listdrives=subprocess.Popen('mount', shell=True, stdout=subprocess.PIPE)
         listdrivesout, err=listdrives.communicate()
         for idx,drive in enumerate(filter(None,listdrivesout)):
             listdrivesout[idx]=drive.split()[2]
            
         print "listdrivesout->", listdrivesout
             
    # guess how it should be on mac os, similar to linux , the mount command should 
    # work, but I can't verify it...
    elif 'macosx' in sys.platform:
         print "FIXME: Let's write some code."

def searchDriveLetter(target_str):
    '''
    Search for drive letter inside a string
    
    '''
    if ':' not in target_str:
        return False
    else:
        drive_letter = target_str.split(':')[0][-1]
        
        if drive_letter.isalpha():
            return drive_letter.upper()
        else:
            raise Exception("drive_letter is invalid")
    
def findFolder(drive_letter, target_folder):
    drive_id = drive_letter+':\\'
    full_directory = os.path.join(drive_id, target_folder)
    print '--> Look up for', full_directory
    
    if os.path.isdir(full_directory):
        return full_directory
    else:
        return False

if __name__ == '__main__':
    driveLines =  listDrives()
    for line in driveLines:
        if len(line):   # Avoid search for empty strings
            drive_letter = searchDriveLetter(line)
            if drive_letter: 
                is_folder_found = findFolder(drive_letter, 'Seagate\\SerialNum')
                print 'drive_letter %s Folder found %s'%(drive_letter, is_folder_found)
