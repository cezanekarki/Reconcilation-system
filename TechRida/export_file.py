import os
import pandas as pd
import time
import os.path



class export_file:
    def __init__(self):
        pass


    def export(self,dataframe,filename):
        timestr = time.strftime("%Y%m%d%H%M%S")
        self.folder='csv_files'
        self.folder2='zippedfiles'
        
        if os.path.isdir(self.folder):
            pass
        else:
            os.mkdir(self.folder)
        
        if os.path.isdir(self.folder2):
            pass
        else:
            os.mkdir(self.folder2)

        dataframe.to_csv(os.path.join(self.folder+'/',filename+timestr+".csv")) #save file atm_log_date:time


