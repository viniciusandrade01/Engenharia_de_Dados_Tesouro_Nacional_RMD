import json
import os
import time
import utils.logger_config as logger_config

logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class GeneralTools:
    def __init__(self):
        pass

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
    
    def removeParentheses(self, dado: str):
        return dado.replace("(","").replace(")","")
    
    def upperCase(self, dado: str):
        return dado.upper()