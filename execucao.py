import pandas as pd
import requests as rq
import time
from methods.loaders.filesSave import FileSavers
from methods.transformers.transformData import TransformData
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from utils.tools import GeneralTools
import utils.logger_config as logger_config
import logging

def main():
    fileSavers = FileSavers()
    transformData = TransformData()
    webPageDataScrapers = WebPageDataScrapers()
    generalTools = GeneralTools()
    try:
        # Variável contendo informações das moedas a serem coletadas, aws e banco de dados
        jsonData = generalTools.openJson()
        data = time.strftime("%Y-%m-%d %H:%M:%S")
        logger_config.setup_logger(data)
        df = pd.DataFrame()

        if len(jsonData['source']['generalLink']['params']['year']) == 4:
            nameDirectory = f"RMD_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}"
            
            html, soup, dataref, nome_zip, link_zip, xlsx = webPageDataScrapers.requestGetDefault(jsonData['source'], nameDirectory)
            logging.info(f"SALVANDO ARQUIVO XLSX, DO ZIP, REFERENTE AOS RELATÓRIOS MENSAIS DE DÍVIDA.")

            df = fileSavers.openingSheets(f"{nameDirectory}/{xlsx}", '2.2', 6, 6)

            df = transformData.deletingColumns(df, dataref)

            df = transformData.selectingData(df, 'Título', jsonData['source']['generalLink']['rmd22'])
            
            fileSavers.creatingFinalDataFrame(df, dataref, f'R_Mensal_Divida_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}.csv', '\t', nameDirectory, generalTools.splitByEmptySpace(data)[0])
            logging.info(f"DATAFRAME CRIADO COM SUCESSO!")
        else:
            print('OK')
    except FileNotFoundError as err:
        logging.error(f"ERRO: {generalTools.upperCase(err)}, O ARQUIVO JSON (data.json) NÃO FOI ENCONTRADO.")
    except (rq.exceptions.HTTPError, rq.exceptions.RequestException) as err:
        logging.error(f"ERRO DURANTE A REQUISIÇÃO: {generalTools.upperCase(err)}")
    except Exception as err:
        logging.error(f"ERRO DESCONHECIDO: {generalTools.upperCase(err)}")

if __name__ == '__main__':
    main()