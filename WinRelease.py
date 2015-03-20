import shutil, errno
import os
import sys
import time

__version__ = "0.5.1"

def packageProgram(entry_path,icon_path):
    print "[Package Program]%s"%(entry_path)
    cmd = "pyinstaller --noconsole --onefile --icon=%s %s" %(icon_path, entry_path)
#     cmd = "pyinstaller --onefile --noconsole --debug --icon=%s %s" %(icon_path, entry_path)
    print "[Package CMD]%s"%(cmd)
    os.system(cmd)

def getCodeData(path):
    print "[Code Analysis]%s" %(path)
    
    files = os.listdir(path)
    total_line_num = 0
    total_function_num = 0

    for file in files:
        #print(file)
        newpath = path+"\\"+file
        # print(newpath)
        if os.path.isdir(newpath):
            int_line_num,int_function_num = getCodeData(newpath)
            total_line_num += int_line_num
            total_function_num += int_function_num
        
        if os.path.isfile(newpath):
            if os.path.splitext(newpath)[1] == '.py':
                fileHandle = open(newpath)
                # print data.readlines()
                all_lines = fileHandle.readlines()
                line_num = len(all_lines)
                total_line_num += line_num
                # print all_lines[:10]
                function_num = 0
                for line in all_lines:
                    line = line.strip()

                    if "def" in line: 
                        function_num = function_num + 1

                # print "[line_num]",line_num
                # print "[function_num]",function_num

                total_function_num += function_num

    return (total_line_num,total_function_num)

def copyAnything(src, dst):
    try:
        print "[Copy Content]%s->%s" %(src, dst)
        shutil.copytree(src, dst)

    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def pathProgram():
    FILEPATH=os.path.abspath(sys.argv[0])
    DIRPATH=os.path.dirname(FILEPATH)
    return str(DIRPATH)

def cleanFolder(folder_dir):
    if os.path.isdir(folder_dir):
        print "[Clean Folder]%s"%(folder_dir)
        shutil.rmtree(folder_dir, ignore_errors=False)
        time.sleep(0.2)
        os.makedirs(folder_dir)
    else:
        print "[No found]%s"%(folder_dir)

def removeFolder(folder_dir):
    if os.path.isdir(folder_dir):
        time.sleep(0.2)
        print "[Remove Folder]%s"%(folder_dir)
        # shutil.rmtree(folder_dir, ignore_errors=False)
        # time.sleep(0.5)
        cmd = "@RD /S /Q %s"%(folder_dir)
        # print "cmd:%s"%(cmd)
        os.system(cmd)
    else:
        print "[No found]%s"%(folder_dir)


def changeExtension(entry_path,extension):
    print "[Modify Extension]%s"%(entry_path)
    base = os.path.splitext(entry_path)[0]
    os.rename(entry_path, base + extension)

def renameFolder(res_dir, dst_dir):
    print "[Rename Folder]'%s'->'%s'"%(res_dir,dst_dir)
    os.renames(res_dir, dst_dir)

if __name__ == "__main__":

    working_dir = os.path.join(pathProgram(),'src')
    
    release_dir = os.path.join(pathProgram(),'release')
    
    dist_dir = os.path.join(pathProgram(),'dist_win')

    build_dir = os.path.join(pathProgram(),'build')

    removeFolder(build_dir)
    removeFolder(release_dir)
    removeFolder(dist_dir)
#     cleanFolder(release_dir)

    copyAnything(working_dir, release_dir)
    
    lineNum,functionNum = getCodeData(release_dir)
    
    report_path = os.path.join(pathProgram(),'report.txt')
    
    fileHandle = open ( report_path, 'w' )
    fileHandle.write ( 'Total Line Number: %s\nTotal Method Number: %s' %(lineNum, functionNum))
    fileHandle.close()

    icon_path = os.path.join(pathProgram(),"release\\Program\\seagate_logo.ico") 
    entry_path = os.path.join(pathProgram(),"release\\Program_Start.py")

    packageProgram(entry_path, icon_path)

    version_path = os.path.join(pathProgram(), "release", "Version.py")
    version_str = "version = '%s'" %(__version__)
    
    fileHandle = open ( version_path, 'w' )
    fileHandle.write ( version_str )
    fileHandle.close()
    
    win_dist_dir = os.path.join(pathProgram(),'dist_win')
    
    renameFolder(dist_dir, win_dist_dir)
    
    removeFolder(build_dir)