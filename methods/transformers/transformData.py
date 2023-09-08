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

    def extractContent(self, html, tags: dict, coin: str):
        return 'oi'