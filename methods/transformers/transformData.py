import datetime
import time
import pandas as pd
import utils.logger_config as logger_config
import logging
import fastavro
from utils.tools import GeneralTools
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from sqlalchemy import create_engine
generalTools = GeneralTools()
webPageDataScrapers = WebPageDataScrapers()
#data = time.strftime("%Y-%m-%d %H:%M:%S")
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class TransformData:
    def __init__(self):
        pass

    def dfToExcel(self, df: pd.DataFrame, file_name: str, sheet_name='Sheet1'):
        df.to_excel(file_name, sheet_name=sheet_name, index=False)
        return df.to_excel()
    
    def dfToJson(self, df: pd.DataFrame, file_name: str):
        df.to_json(file_name, orient='records')
        return df.to_json()
    
    def dfToParquet(self, df: pd.DataFrame, file_name: str):
        df.to_parquet(file_name, index=False)
        return df.to_parquet()
    
    def df_to_sql(self, df: pd.DataFrame, db_url, table_name):
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        return df.to_sql()
    
    def df_to_pickle(self, df: pd.DataFrame, file_name: str):
        df.to_pickle(file_name)
        return df.to_pickle()
    
    def df_to_avro(self, df: pd.DataFrame, file_name: str):
        with open(file_name, 'wb') as out_avro:
            fastavro.writer(out_avro, df.to_dict(orient='records'))
        return df
    
    def df_to_html(self, df: pd.DataFrame, file_name: str):
        df.to_html(file_name, index=False)
        return df.to_html()

    def selectingData(self, df: pd.DataFrame, title: str, data: list):
        return df[df[title].isin(data)]
    
    def format_Date(self, date: str):
        try:
            return datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except:
            return ""

    def deletingColumns(self, df: pd.DataFrame, diames: str):
        #arg = str(datetime.datetime.strptime(diames, "%B de %Y").strftime("%b/%y")).title()
        arg = str(datetime.datetime.strptime(diames, "%Y-%m-%d").strftime("%b/%y")).title()
        count = 2
        for f in range(0, len(df.columns)):
            if arg != df.iloc[0][-2]:
                df = df.drop(columns=df.columns[len(df.columns)-count:])
            elif arg == df.iloc[0][-2]:
                return df
