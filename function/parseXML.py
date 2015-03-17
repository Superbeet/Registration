import sys
import os
import xml.etree.ElementTree as ET


def parseXML(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    drive_info_dict = {}
    
    for drive_info_block in root.iter('DRIVEINFO'):
#         print drive_info_block.find('SERIAL_NUM').text
        
        for block in drive_info_block:
            drive_info_dict.update({block.tag:block.text})
            
    return drive_info_dict

if __name__ == '__main__':
    drive_info_dict = parseXML('SerialNumber.xml')
    print drive_info_dict
    print drive_info_dict['SERIAL_NUM']