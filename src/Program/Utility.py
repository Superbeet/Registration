'''
Created on Mar 10, 2015

@author: 507061
'''

import sys
import os
import urllib2
import subprocess
import xml.etree.ElementTree as ET
import base64
import time


# Global Variables -------------------------------------------------------------------
EventLevel = {'INFOR':0 ,'DEBUG': 1, 'ERROR': 3, 'FATAL': 4}

MinLevel = 'INFOR'

# Four levels for log recording
# Level-1:NORMAL
# Level-2:DEBUG
# Level-4:ERROR
# Level-5:FATAL

def check_connectivity(reference):
    try:
        urllib2.urlopen(reference, timeout=3)
        return True
    except urllib2.URLError:
        return False
    
def pathProgram():
    """
    Return the working path of the program in string.
    """
    FILEPATH=os.path.abspath(sys.argv[0])
    DIRPATH=os.path.dirname(FILEPATH)
    return str(DIRPATH)

def listDrives():
    #on windows
    #Get the fixed drives
    #wmic logicaldisk get name,description
    if 'win' in sys.platform:
        import win32api
        
        drives = win32api.GetLogicalDriveStrings()
        driveList = drives.split('\000')[:-1]
      
        return driveList
#         log = open(logfile, 'a')
#         log.flush()  # <-- here's something not to forget!
#         log.write('Log File\r\n-------------\r\n')
#         
#         drivelist = subprocess.Popen('wmic logicaldisk get name,description', stdout=log, stderr=log, shell=True)
#         MyPrint('-->drivelist%s' %(drivelist), level='DEBUG')
# #         drivelist = subprocess.Popen('wmic logicaldisk get name,description', shell=True, stdout=subprocess.PIPE)
#         drivelisto, err = drivelist.communicate()
#         
#         driveLines = drivelisto.split('\r\r\n')
#         for line in driveLines:
#             if len(line) == '':
#                 driveLines.remove('')
               

    elif 'linux' in sys.platform:
        listdrives=subprocess.Popen('mount', shell=True, stdout=subprocess.PIPE)
        listdrivesout, err=listdrives.communicate()
        for idx,drive in enumerate(filter(None,listdrivesout)):
            listdrivesout[idx]=drive.split()[2]
            
    # guess how it should be on mac os, similar to linux , the mount command should 
    # work, but I can't verify it...
    elif 'darwin' in sys.platform or 'macosx' in sys.platform:
        driveList = os.listdir('/Volumes')
        
        driveFullList = []
        
        for driveName in driveList:
            driveFullList.append(os.path.join('/Volumes',driveName))

        return driveFullList

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
            return False
    
def findFolder(drive_id, target_folder):
    drive_id = drive_id
    full_directory = os.path.join(drive_id, target_folder)
    
    directory_found = os.path.isdir(full_directory)
    
    MyPrint('--> Look up %s (%s)' %(full_directory,directory_found))
    
    if directory_found:
        return True
    else:
        return False

def parseXML(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    drive_info_dict = {}
    
    for drive_info_block in root.iter('DRIVEINFO'):     
        for block in drive_info_block:
            drive_info_dict.update({block.tag:block.text})
            
    return drive_info_dict

def MyPrint(msg, Verbose=(0,0), level = 'INFOR'):
    if  EventLevel[level] >= EventLevel[MinLevel]:
        MyPrintf(msg, Verbose, level)

def MyPrintf(msg, Verbose, level):
    """
    Verbose[0] is the level of verbocity requested (e.g., Verbose[0]=None means print nothing, =2 means print messages with <= 2 tabs.
    Verbose[1] is the number of tabs in the prefix: the deeper into function calls you are the more tabs there are.
    """
    curTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    prefix= ''
    line_prefix = ''
    msg = str(msg)
    if msg[0] == '\n':
        msg = msg[1:]
        line_prefix = '\n'
    for i_cnt in range(Verbose[1]):
        prefix += '\x20'*8 #Jeff Mod: Change 1 "tab" to 8 "spaces"
    if Verbose[0] != None and Verbose[0] >= Verbose[1]:
        if level == 'NORMAL':
            prefix_msg =  line_prefix + '[%s][%s] '%(curTime,level) + prefix + msg
        elif level == 'DEBUG':
            prefix_msg =  line_prefix + '[%s][%s] '%(curTime,level) + prefix + msg
        elif level == 'ERROR':
            prefix_msg =  line_prefix + '[%s][%s] '%(curTime,level) + prefix + msg
        elif level == 'FATAL':
            prefix_msg =  line_prefix + '[%s][%s] '%(curTime,level) + prefix + msg                      
        else:
            prefix_msg =  line_prefix + '[%s][%s] '%(curTime,level) + prefix + msg
            
        print prefix_msg    