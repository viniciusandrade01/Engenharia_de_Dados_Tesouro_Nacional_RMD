import datetime
import time
import pandas as pd
import utils.logger_config as logger_config
import logging
from utils.tools import GeneralTools
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
#from methods.loaders.filesSave import FileSavers
generalTools = GeneralTools()
#fileSavers = FileSavers()
webPageDataScrapers = WebPageDataScrapers()
data = time.strftime("%Y-%m-%d %H:%M:%S")
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class TransformData:
    def __init__(self):
        pass

    def selectingData(self, df: pd.DataFrame, title: str, data: list):
        return df[df[title].isin(data)]
    
    def format_Date(self, date: str):
        try:
            return datetime.datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except:
            return ""

    def deletingColumns(self, df: pd.DataFrame, diames: str):
        arg = str(datetime.datetime.strptime(diames, "%B de %Y").strftime("%b/%y")).title()
        count = 2
        for f in range(0, len(df.columns)):
            if arg != df.iloc[0][-2]:
                df = df.drop(columns=df.columns[len(df.columns)-count:])
            elif arg == df.iloc[0][-2]:
                return df
