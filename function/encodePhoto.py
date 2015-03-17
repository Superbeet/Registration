import base64
import os
import sys
import StringIO

from PIL import Image
from PIL import ImageDraw
from PyQt4 import QtCore, QtGui

photo_path = 'welcome.png'

myimage = Image.open(photo_path)
myimage.load()
myimagestr = 'welcome_image_b64 = \\\n"""' + base64.encodestring(open(photo_path,"rb").read()) + '"""'

fid = open('image_string.txt', 'w')
fid.write('%s'%(myimagestr))
fid.close()

print myimagestr