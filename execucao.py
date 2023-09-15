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
        logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))
            
        html, soup, dataref, nome_zip, link_zip, xlsx, data_capt, name_directory = webPageDataScrapers.requestGetDefault(jsonData['source'], jsonData['source']['generalLink']['params'])
        logging.info(f"SALVANDO ARQUIVO XLSX, DO ZIP, REFERENTE AOS RELATÓRIOS MENSAIS DEDÍVIDA.")

        df = fileSavers.openingSheets(f"{name_directory}/{xlsx}", '2.2', 6, 6)

        df = transformData.deletingColumns(df, data_capt)

        df = transformData.selectingData(df, 'Título', jsonData['source']['generalLink']['rmd22'])
            
        fileName, file_type = fileSavers.creatingFinalDataFrame(df, dataref, f'R_Mensal_Divida_{generalTools.hyphenToNull(data_capt)}', '\t', name_directory, data_capt, generalTools.lowerCase(jsonData['source']['generalLink']['filetype']))
        logging.info(f"DOCUMENTO CRIADO COM SUCESSO!")
        s3 = client.createClient('s3')
        localfile = f"{name_directory}/{fileName}.{file_type}"
        client.uploadFile(s3, localfile, 'engdadostest', localfile)
        
    except FileNotFoundError as err:
        logging.error(f"ERRO: {generalTools.upperCase(err)}, O ARQUIVO JSON (data.json) NÃO FOI ENCONTRADO.")
    except (rq.exceptions.HTTPError, rq.exceptions.RequestException) as err:
        logging.error(f"ERRO DURANTE A REQUISIÇÃO: {generalTools.upperCase(err)}")
    except Exception as err:
        logging.error(f"ERRO DESCONHECIDO: {generalTools.upperCase(err)}")

if __name__ == '__main__':
    main()