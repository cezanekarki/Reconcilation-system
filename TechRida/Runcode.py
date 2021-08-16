import JRN_dataextraction
import ZERO_dataextraction
import MT940data_extraction
import export_file
import os
import zipfiles

def runprog(filename,folder_dir):
    check_file=filename.split(".")
    #try:
        
    if str(check_file[1])==str('0'):

        file_call=ZERO_dataextraction.extractData()
        file_print=file_call.run_functions(filename)
        
        
    elif check_file[1]=='jrn':

        file_call=JRN_dataextraction.extractData()
        file_print=file_call.run_functions(filename)
        

    file_export=export_file.export_file()
    file_export.export(file_print,filename)

    
        
    '''except:
        print("Error working with the file.")'''

folder_dir='Source'
i=0
while i<len(os.listdir(folder_dir)):
    if os.listdir(folder_dir)[i].endswith(".0"):
        runprog(os.listdir(folder_dir)[i],folder_dir)
    elif os.listdir(folder_dir)[i].endswith(".jrn"):
        runprog(os.listdir(folder_dir)[i],folder_dir)
    
    i=i+1
    print(i)

zipfiles.file_zipper(folder_dir)
   


    


