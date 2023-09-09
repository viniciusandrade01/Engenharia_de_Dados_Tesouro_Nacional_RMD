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
            
            html, soup, dataref, nome_zip, link_zip = webPageDataScrapers.requestGetDefault(jsonData['source'], nameDirectory)
            logging.info(f"SALVANDO ARQUIVO XLSX, DO ZIP, REFERENTE AOS RELATÓRIOS MENSAIS DE DÍVIDA.")

            #dataref, nome_zip, link_zip = webPageDataScrapers.extractInfoUrl(soup)
            #logging.info(f"EXTRAINDO CONTEÚDO DESEJADO REFERENTE AO RELATÓRIO.")

            #webPageDataScrapers.extractZip(html, nome_zip)
            #df = transformData.extractContent(soup, jsonData['source']['generalLink'], "GERAL")
            #logging.info(f"DADOS DAS MOEDAS, COM BOM RANKING, COLETADOS COM SUCESSO.")
        else:
            nameDirectory = f"Moedas_Selecionadas_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}"
            for index, coin in enumerate(jsonData['coins']):
                logging.info(f"ACESSANDO LINK REFERENTE A MOEDA {generalTools.upperCase(coin)}.")
                
                html, soup = webPageDataScrapers.specificGetRequest(f"{jsonData['source']['specificLink']['fonte']}{coin}")
                logging.info(f"SALVANDO PÁGINA HTML REFERENTE A MOEDA {generalTools.upperCase(coin)}.")
            
                #fileSavers.saveHTML(html, f"html_{generalTools.hyphenToNull(coin)}_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}.txt", nameDirectory)
            
                logging.info(f"EXTRAINDO CONTEÚDO DESEJADO REFERENTE A MOEDA {generalTools.upperCase(coin)}.")
                
                aboutCoin = transformData.extractContent(soup, jsonData['source']['specificLink']['atributos'], coin)
            
                logging.info(f"DADOS DA MOEDA: {generalTools.upperCase(coin)} COLETADOS COM SUCESSO.")

                logging.info(f"SALVANDO INFORMAÇÕES REFERENTE A MOEDA {generalTools.upperCase(coin)}.")
                dictionary = fileSavers.saveDictionary(coin, aboutCoin, data)
                df = fileSavers.concatDataFrame(df, dictionary, index)

        file_name = f"Cotação_Moedas_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}" if len(jsonData['coins']) == 0 else f"Cotação_Moedas_Selecionadas_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(data)[0])}"
        fileSavers.saveDataFrame(df, file_name, '\t', nameDirectory)
    except FileNotFoundError as err:
        logging.error(f"ERRO: {generalTools.upperCase(err)}, O ARQUIVO JSON (data.json) NÃO FOI ENCONTRADO.")
    except (rq.exceptions.HTTPError, rq.exceptions.RequestException) as err:
        logging.error(f"ERRO DURANTE A REQUISIÇÃO: {generalTools.upperCase(err)}")
    except Exception as err:
        logging.error(f"ERRO DESCONHECIDO: {generalTools.upperCase(err)}")

if __name__ == '__main__':
    main()