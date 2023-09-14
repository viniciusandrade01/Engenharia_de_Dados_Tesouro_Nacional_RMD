import pandas as pd
import requests as rq
import time
from methods.loaders.filesSave import FileSavers
from methods.transformers.transformData import TransformData
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from utils.tools import GeneralTools
import utils.logger_config as logger_config
from utils.aws import AboutAWS
import logging

def main():
    try:
        fileSavers = FileSavers()
        transformData = TransformData()
        webPageDataScrapers = WebPageDataScrapers()
        generalTools = GeneralTools()
        df = pd.DataFrame()
        client = AboutAWS()
        # Variável contendo informações das moedas a serem coletadas, aws e banco de dados
        jsonData = generalTools.openJson()
        data = time.strftime("%Y-%m-%d %H:%M:%S")
        logger_config.setup_logger(data)

        nameDirectory = f"RMD_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}"
            
        html, soup, dataref, nome_zip, link_zip, xlsx = webPageDataScrapers.requestGetDefault(jsonData['source'], nameDirectory, jsonData['source']['generalLink']['params'])
        logging.info(f"SALVANDO ARQUIVO XLSX, DO ZIP, REFERENTE AOS RELATÓRIOS MENSAIS DEDÍVIDA.")

        df = fileSavers.openingSheets(f"{nameDirectory}/{xlsx}", '2.2', 6, 6)

        df = transformData.deletingColumns(df, dataref)

        df = transformData.selectingData(df, 'Título', jsonData['source']['generalLink']['rmd22'])
            
        fileName, file_type = fileSavers.creatingFinalDataFrame(df, dataref, f'R_Mensal_Divida_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}', '\t', nameDirectory, generalTools.splitByEmptySpace(data)[0], generalTools.lowerCase(jsonData['source']['generalLink']['filetype']))
        logging.info(f"DOCUMENTO CRIADO COM SUCESSO!")
        s3 = client.createClient('s3')
        localfile = f"{nameDirectory}/{fileName}.{file_type}"
        client.uploadFile(s3, localfile, 'engdadostest', localfile)
        
    except FileNotFoundError as err:
        logging.error(f"ERRO: {generalTools.upperCase(err)}, O ARQUIVO JSON (data.json) NÃO FOI ENCONTRADO.")
    except (rq.exceptions.HTTPError, rq.exceptions.RequestException) as err:
        logging.error(f"ERRO DURANTE A REQUISIÇÃO: {generalTools.upperCase(err)}")
    except Exception as err:
        logging.error(f"ERRO DESCONHECIDO: {generalTools.upperCase(err)}")

if __name__ == '__main__':
    main()