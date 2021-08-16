import re
import time
import pandas as pd
import os
import os.path


class extractData:

    

    def __init__(self):
        pass
    #load data
    def load_data(self,location,read_type="r"):
        data=open(location,read_type)
        all_lines_data=data.readlines()
        data.close()
        return all_lines_data
    #remove space from required line
    def remove_spaces(self,line):
        return re.sub(r"\s+", "", line)


    #extract required data
    def extract_data(self,file_read):
        self.data=[]
        for line in file_read:
        
            
            
            if re.search("TRANSACTION REQUEST",line):
                
                self.trans_req=line[-9:]
                
            
            elif re.search("TVR", line):
                lines=self.remove_spaces(line)
                splitted_line=lines.split(",")
                self.tvr=splitted_line[0][12:]
                self.tsi=splitted_line[1][4:]
                
                
            elif re.search("CASH REQUEST",line):
                lines=self.remove_spaces(line)
                self.cash_req=lines[-8:]
               
                
            
            

            elif re.search("RESP CODE",line):
                lines=self.remove_spaces(line)
                self.respcode=lines[9:]
                
                
                
            elif re.search("ATM ID", line):
                lines=self.remove_spaces(line)
                self.atm_id=lines[6:]
                
                
            elif re.search("RRN",line):
                lines=self.remove_spaces(line)
                self.rrn=lines[5:-1]
                
            
            elif re.match("TXN NO",line):
                lines=self.remove_spaces(line)
                self.txn_no=lines[-3:]
                
                
            elif re.match("DATE & TIME",line):
                lines=self.remove_spaces(line)
                self.date=lines[10:-8]
                self.time=lines[-8:]
                
               
            
            elif re.match("CARD NO",line):
                lines=self.remove_spaces(line)
                self.card_num=lines[7:]
                
            
            elif re.match("TRANS AMOUNT",line):
                lines=self.remove_spaces(line)
                self.trans_amt=lines[12:]
                
            
            elif re.match("AUTH CODE",line):
                lines=self.remove_spaces(line)
                
                self.auth_code=lines[9:]
                
                
            
            elif re.match("TRACE NO/ID",line):
                lines=self.remove_spaces(line)
                self.trace_no=lines[-6:]
            
            elif re.match("TXN TYPE",line):
                lines=self.remove_spaces(line)
                
                self.txn_type=lines[8:]
                
                
            #store the data in list as key value pair after getting Transaction end in the line
            elif re.search("TRANSACTION END",line):
                self.data.append({'Transaction Request':self.trans_req,
                    'TVR':self.tvr,
                    'TSI':self.tsi,
                    'Cash Request':self.cash_req,
                    'Resp Code':self.respcode,
                    'ATM ID':self.atm_id,
                    'RRN':self.rrn,
                    'TXN':self.txn_no,
                    'TXN Type':self.txn_type,
                    'Date':self.date,
                    'Time':self.time,
                    'Card Number':self.card_num,
                    'Transaction Amount':self.trans_amt,
                    'Authentication Code':self.auth_code,
                    'Trace No':self.trace_no})
        
        return self.data
    
    #create table using pandas
    def create_table(self,table_data):
        self.dataframe=pd.DataFrame(table_data)
        return self.dataframe
    

    #check the transaction status, transaction type and authentication code according to the response code
    def add_transactionstatus(self,dataframe):
        self.dataframe['Resp Code']=self.dataframe['Resp Code'].astype(str)
        self.Trans_type=[]
        self.authcode_list=[]
        self.txn=[]

                
        for j,k in enumerate(self.dataframe['Resp Code']):
            if str(k) == str('00'):
                self.authcode_list.append(self.dataframe['Authentication Code'][j])
                self.txn.append(self.dataframe['TXN Type'][j])
                self.Trans_type.append('Successful')
            else:
                self.authcode_list.append("------")
                self.txn.append("------")
                self.Trans_type.append('Error')
            
            
            
            
        self.dataframe['Transaction Status']=self.Trans_type
        self.dataframe['Authentication Code']=self.authcode_list
        self.dataframe['TXN Type']=self.txn
        self.dataframe = self.dataframe.replace('\n',' ', regex=True)
        return self.dataframe

    #run all the functions 
    def run_functions(self,location_file):
        
        self.location_path=os.path.join("Source/",location_file)
        self.data_load=self.load_data(self.location_path)
        self.filtering_data=self.extract_data(self.data_load)
        self.creating_table=self.create_table(self.filtering_data)
        return self.add_transactionstatus(self.creating_table)




    



