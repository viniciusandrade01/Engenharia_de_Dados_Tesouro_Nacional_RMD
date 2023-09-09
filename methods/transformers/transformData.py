import datetime
import time
import pandas as pd
import utils.logger_config as logger_config
import logging
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))
from utils.tools import GeneralTools
from methods.loaders.filesSave import FileSavers
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
generalTools = GeneralTools()
fileSavers = FileSavers()
webPageDataScrapers = WebPageDataScrapers()
data = time.strftime("%Y-%m-%d %H:%M:%S")

class TransformData:
    def __init__(self):
        self.aboutCoin = []
        self.padrao = []

    def selectingData(self, df: pd.DataFrame, title: str, data: list):
        return df[df[title].isin(data)]

    def deletingColumns(self, df: pd.DataFrame, diames: str):
        arg = str(datetime.datetime.strptime(diames, "%B de %Y").strftime("%b/%y")).title()
        count = 2
        for f in range(0, len(df.columns)):
            if arg != df.iloc[0][-2]:
                df = df.drop(columns=df.columns[len(df.columns)-count:])
            elif arg == df.iloc[0][-2]:
                return df
