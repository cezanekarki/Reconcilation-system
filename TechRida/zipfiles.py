import os
import os.path
from zipfile import ZipFile
import zipfile
import time
import shutil

def file_zipper(file_path):
    timestr = time.strftime("%Y%m%d%H%M%S")
    new_file=timestr+'.zip'
    zip=ZipFile(new_file,'w',zipfile.ZIP_DEFLATED)
    for file_path,dir_names,files in os.walk(file_path):
        f_path= file_path.replace(file_path, '')
        f_path = f_path and f_path + os.sep
        for file in files:
                zip.write(os.path.join(file_path, file), f_path + file)
        zip.close()
        
        print("File Created successfully..")
    shutil.move(new_file,'zippedfiles')
    return new_file


