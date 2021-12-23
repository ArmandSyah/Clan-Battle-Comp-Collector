import sqlite3
import pandas as pd
import os

class MasterDBReader:
    def __init__(self, master_db_path) -> None:
        if not os.path.exists(master_db_path):
            raise FileNotFoundError('Master database cannot be found at current location, please double check again')
        
        self.master_db_path = master_db_path
        self.master_db_connection = None
        self.start_connection()
    
    def start_connection(self):
        self.master_db_connection = sqlite3.connect(self.master_db_path)
        print("Connection to master db has begun")
        
    def close_connection(self):
        if self.is_connected():
            self.master_db_connection.close()
            print("Connection to master db has closed")
        else:
            print("DB error occured while trying to close, it might not even be turned on")
            
    def query_master_db(self, sql_query) -> pd.DataFrame:
        return pd.read_sql_query(sql_query, self.master_db_connection)
        
    def is_connected(self):
        try:
            self.master_db_connection.cursor()
            print("Currently connected to master db")
            return True
        except sqlite3.Error:
            print("Currently not connected to master db")
            return False