import logging
import sqlite3
import pandas as pd
import os
import unicodedata

class MasterDBReader:
    def __init__(self, master_db_directory, master_db) -> None:
        self.logger = logging.getLogger('dataExtractorLogger')

        self.master_db_path = os.path.join(os.getcwd(), master_db_directory, master_db)
        self.master_db_connection = None

        if not os.path.exists(self.master_db_path):
            raise FileNotFoundError('Master database cannot be found at current location, please double check again')
        
        self.start_connection()
    
    def start_connection(self):        
        self.master_db_connection = sqlite3.connect(self.master_db_path)
        self.logger.info("Connection to master db has begun")
        
    def close_connection(self):
        if self.is_connected():
            self.master_db_connection.close()
            self.logger.info("Connection to master db has closed")
        else:
            self.logger.warn("DB error occured while trying to close, it might not even be turned on")
            
        
    def is_connected(self):
        try:
            self.master_db_connection.cursor()
            self.logger.info("Currently connected to master db")
            return True
        except sqlite3.Error:
            self.logger.info("Currently not connected to master db")
            return False
        
    def query_master_db(self, sql_query) -> pd.DataFrame:
        df = pd.read_sql_query(sql_query, self.master_db_connection)
        for column in df.columns:
            df[column] = df[column].map(self.normalize_query_results)
        
        return df
    
    def normalize_query_results(self, s) -> str:
        return unicodedata.normalize('NFKC', str(s))