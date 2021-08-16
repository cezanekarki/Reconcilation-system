import re
import time
import pandas as pd
import os
import os.path


class extractData:

    def __init__(self):
        pass
    #load the data
    def load_data(self,location,read_type="r"):
        data=open(location,read_type)
        all_lines_data=data.readlines()
        data.close()
        return all_lines_data
    #remove spaces from the lines
    def remove_spaces(self,line):
        return re.sub(r"\s+", "", line)
    
    #extracts data from the file
    def extract_data(self,file_read):
        self.data=[]

        
        for read_line in file_read:
            self.organised=re.sub("a", " ",read_line)
            self.line=self.remove_spaces(self.organised)
            if re.search("CASH WITHDRAWAL",self.organised) or re.search("BALANCE INQUIRY",self.organised):  #check according to regex for getting the specific line
                self.respcode=re.search("RESP CODE",self.organised) #extract response code
                start=self.respcode.start()+16  #start() for getting the starting index of the searched data
                end=self.respcode.start()+19
                self.resp=self.organised[start:end]

                if int(self.resp) == int('00'):
                    if re.search("ATM ID",self.organised):
                        self.match=re.search("ATMID",self.line)
                        self.start=self.match.start()+6
                        self.end=self.start+8

                        self.lin=self.line[self.start:self.end]
                        
                    if re.search("DATE & TIME",self.organised):
                        self.match=re.search("DATE&TIME",self.line)
                        self.start=self.match.start()+10
                        self.end=self.start+8
                        self.date=self.line[self.start:self.end]
                        self.time=self.line[self.start+8:self.end+8]

                        
                    if re.search("RRN",self.organised):
                        self.rrn_match=re.search("RRN",self.line)
                        self.rrn_start=self.rrn_match.start()+5
                        self.rrn_end=self.rrn_start+18
                        self.rrn_number=self.line[self.rrn_start:self.rrn_end]
                        self.finalrrn_number=re.sub("[^0-9.,]","",self.rrn_number)
                    
                else:
                    if re.search("ATM_ID",self.organised):
                        self.match=re.search("ATM_ID",self.line)
                        self.start=self.match.start()+7
                        self.end=self.start+8

                        self.lin=self.line[self.start:self.end]
       
                        
                    if re.search("DATE",self.organised):
                        self.match=re.search("DATE",self.line)
                        self.start=self.match.start()+5
                        self.end=self.start+8
                        self.date=self.line[self.start:self.end]
                        self.time=self.line[self.start+8:self.end+8]
                      
                        
                    if re.search("RRN",self.organised):
                        self.rrn_match=re.search("RRN",self.line)
                        self.rrn_start=self.rrn_match.start()+5
                        self.rrn_end=self.rrn_start+12
                        self.rrn_number=self.line[self.rrn_start:self.rrn_end]
                        self.finalrrn_number=re.sub("[^0-9.,]","",self.rrn_number)

                    

                self.card_match=re.search("CARDNO",self.line)
                self.card_start=self.card_match.start()+7
                self.card_end=self.card_start+16
                self.cardno=self.line[self.card_start:self.card_end]
         
                
                self.auth_match=re.search("AUTHCODE",self.line)
                if int(self.resp) == int('00'):
                    self.auth_start=self.auth_match.start()+9
                    self.auth_end=self.auth_start+8
                    self.auth_code=self.line[self.auth_start:self.auth_end]
                    if str(self.auth_code)==str("TRACENO/"):
                        self.auth_code="------"
                else:
                    self.auth_code="------"
                
                
                self.txn_match=re.search("TXN TYPE",self.organised)
                if int(self.resp) == int('00'):
                    self.txn_start=self.txn_match.start()
                    self.txn_end=self.txn_start+32
                    self.txn=self.organised[self.txn_start:self.txn_end].split(':')
                    self.txn_type=self.txn[1][0:16]
                else:
                    self.txn_type="------"
       
                
                self.trace_no=re.search("TRACENO/ID",self.line)
                self.trace_start=self.trace_no.start()+11
                self.trace_end=self.trace_start+15
                self.trace_id=self.line[self.trace_start:self.trace_end]
                self.trace_id=re.sub("[^0-9.,]","",self.trace_id)
     
                
                self.trans=re.search("TRANS AMOUNT",self.organised)
                if re.search("CASH WITHDRAWAL",self.organised):
                    self.trans_start=self.trans.start()
                    self.trans_end=self.trans_start+36
                    self.t_amt=self.organised[self.trans_start:self.trans_end].split(":")
                    self.t=self.t_amt[-1]
                    self.trans_amt=self.t.split('NPR',1)[0]
                    
                else:
                    self.trans_amt="------"
                
                
                self.inq=re.search("BALANCE:",self.line)
                if re.search("BALANCE INQUIRY",self.organised):
                    self.inq_start=self.inq.start()+8
                    self.inq_end=self.inq_start+15
                    self.inq_bal=self.line[self.inq_start:self.inq_end]
                    self.inq_bal=re.sub("[^0-9.,]","",self.inq_bal)
                    
                else:
                    self.inq_bal="------"

                #append the data to the list with key value format
                self.data.append({'ATM ID':self.lin,
                    'Date':self.date,
                    'Time':self.time,
                    'Card Number':self.cardno,
                    'Resp Code':self.resp,
                    'Balance Enquiry':self.inq_bal,
                    'Transaction Amount':self.trans_amt,
                    'TXN Type':self.txn_type,
                    'RRN':self.finalrrn_number,
                    'Authentication Code':self.auth_code,
                    'Trace No':self.trace_id})
                
        return self.data
        
    #create table using pandas
    def create_table(self,table_data):
        self.dataframe=pd.DataFrame(table_data)
        return self.dataframe

    #check the transaction status according to the response code
    def add_transactionstatus(self,dataframe):
        self.dataframe['Resp Code']=self.dataframe['Resp Code'].astype(str)
        self.Trans_type=[]
        for i in self.dataframe['Resp Code']:
            if int(i) == int('00'):
                self.Trans_type.append('Successful')
            else:
                self.Trans_type.append('TRANSACTION HAVE A PROBLEM!')
                
        self.dataframe['Transaction Status']=self.Trans_type
        self.dataframe = self.dataframe.replace('\n',' ', regex=True)
        return self.dataframe


    #run all the functions 
    def run_functions(self,location_file):
        self.location_path=os.path.join("Source/",location_file)
        self.data_load=self.load_data(self.location_path)
        self.filtering_data=self.extract_data(self.data_load)
        self.creating_table=self.create_table(self.filtering_data)
        return self.add_transactionstatus(self.creating_table)





    


                



        
