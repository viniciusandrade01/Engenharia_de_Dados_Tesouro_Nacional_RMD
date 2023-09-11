import datetime
import json
import os
import time
import utils.logger_config as logger_config
import logging
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class GeneralTools:
    def __init__(self):
        pass

    def validateDate(self, data: str, data_param: dict):
        try:
            data_param = f"{data_param['year']}-{data_param['month']}"
            return data if data_param > data[:-3] else f"{data_param}-01"
        except ValueError:
            logging.info ("A estrutura da data_param não é válida. Deve estar no formato '%Y-%m'.")

    
    def makeDirectory(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    def openJson(self):
        with open('utils\data.json') as json_file:
            return json.load(json_file)
    
    def hyphenToNull(self, dado: str):
        return dado.replace("-","")
    
    def hyphenToEmptySpace(self, dado: str):
        return dado.replace("-"," ")
    
    def splitByEmptySpace(self, dado: str):
        return dado.split(" ")
    
    def brlToEmpty(self, dado: str):
        return dado.replace("R$","")
    
    def commaToEmpty(self, dado: str):
        return dado.replace(",","")
    
    def dotToEmpty(self, dado: str):
        return dado.replace(".","")
    
    def emptyValueToEmpty(self, dado: str):
        return dado.replace (" ","")
    
    def percentageToEmpty(self, dado: str):
        return dado.replace("%","")

    def zeroToEmpty(self, dado: str):
        return dado.replace("0","")
    
    def nanToEmpty(self, dado: str):
        return dado.replace("nan", "")
    
    def removeParentheses(self, dado: str):
        return dado.replace("(","").replace(")","")
    
    def upperCase(self, dado: str):
        return dado.upper()
    
    def lowerCase(self, dado: str):
        return dado.lower()