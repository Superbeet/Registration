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
        drivelist = subprocess.Popen('wmic logicaldisk get name,description', shell=True, stdout=subprocess.PIPE)
        drivelisto, err = drivelist.communicate()
        driveLines = drivelisto.split('\r\r\n')
        for line in driveLines:
            if len(line) == '':
                driveLines.remove('')
               
        return driveLines
#        print "driveLines->", driveLines     
#        for line in driveLines:
#            if len(line):   # Avoid search for empty strings
#                print searchDriveLetter(line)
           
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
            return False
    
def findFolder(drive_letter, target_folder):
    drive_id = drive_letter+':\\'
    full_directory = os.path.join(drive_id, target_folder)
    print '--> Look up for', full_directory
    
    if os.path.isdir(full_directory):
        return full_directory
    else:
        return False

def parseXML(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    drive_info_dict = {}
    
    for drive_info_block in root.iter('DRIVEINFO'):
#         print drive_info_block.find('SERIAL_NUM').text
        
        for block in drive_info_block:
            drive_info_dict.update({block.tag:block.text})
            
    return drive_info_dict

