import pandas as pd
from mt940 import MT940
import os 
import os.path

class extractData:

    def __init__(self):
        pass

    def load_data(self,location):
        self.mt940=MT940(location)
        return self.mt940
    
    def extract_data(self,file_read):
        self.datatop=[]

        self.statement=file_read.statements
        for i in range(len(self.statement)):

            self.start_balance=self.statement[i].start_balance
            self.end_balance=self.statement[i].end_balance
            
            
            self.state=self.statement[i].statement
                
            self.state_acc=self.statement[i].account
            
            self.state_info=self.statement[i].information
                
            if self.start_balance!=None:
                
                self.s_date=self.start_balance.date
                self.s_amt=self.start_balance.amount  
                self.s_cur=self.start_balance.currency

            
            
            
            if str(self.end_balance)!=None:
                self.e_amt=str(self.end_balance.amount)
                self.e_cur=self.end_balance.currency
                
                self.e_date=self.end_balance.date
               

            self.state_desc=self.statement[i].description
           
                
            self.transactions=self.statement[i].transactions
            for j in range(len(self.transactions)):
                self.t_date=self.transactions[j].date
                
                self.t_amt=self.transactions[j].amount
                
                self.t_id=self.transactions[j].id
                
                self.t_ref=self.transactions[j].reference
                
                self.t_ir=self.transactions[j].institution_reference
                
                self.t_ad=self.transactions[j].additional_data
                
                self.t_desc=self.transactions[j].description
                

                self.datatop.append({
                    "Statement":self.state,
                    "Account":self.state_acc,
                    "Information":self.state_info,
                    "Start Balance Date":self.s_date,
                    "Start Balance":self.s_amt,
                    "Start Balance Currency":self.s_cur,
                    "End Balance Date":self.e_date,
                    "End Balance":self.e_amt,
                    "End Balance Currency":self.e_cur,
                    "Transactions Date":self.t_date,
                    "Transactions Amount":self.t_amt,
                    "Transactions ID":self.t_id,
                    "Transactions Reference":self.t_ref,
                    "Transactions institute reference":self.t_ir,
                    "Transactions Additional Data":self.t_ad,
                    "Transactions Description":self.t_desc,
                    "Statement Description":self.state_desc,
                })
        return self.datatop

    def create_table(self,table_data):
        self.dataframe=pd.DataFrame(table_data)
        return self.dataframe
    
    def run_functions(self,location_file):
        self.location_path=os.path.join("Source/",location_file)
        self.data_load=self.load_data(self.location_path)
        self.filtering_data=self.extract_data(self.data_load)
        return self.create_table(self.filtering_data)
        