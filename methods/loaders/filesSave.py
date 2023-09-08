import io
import os
import time
import pandas as pd
import utils.logger_config as logger_config
from utils.tools import GeneralTools
import logging
generalTools = GeneralTools()
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class FileSavers:
    def __init__(self):
        pass

    #def saveHTML(self, content, file_name: str, file_directory: str):
    #    generalTools.makeDirectory(file_directory)
    #    with io.open(os.path.join(file_directory, file_name), "w", encoding="utf-8") as fp:
    #        fp.write(content.text)

    def saveDataFrame(self, content, file_name, sep, nameDirectory):
        try:
            if not file_name.endswith(".csv"):
                file_name += ".csv"

            df = pd.DataFrame(content)
            df.reset_index(inplace=True)
            df.drop('index', axis=1, inplace=True)
            df.to_csv(os.path.join(nameDirectory, file_name), sep=f'{sep}', encoding='ISO-8859-1', index=False)
        except FileNotFoundError as e:
            logging.error(f"ERRO: {e}, O ARQUIVO {file_name} NÃO EXISTE.")
        except Exception as e:
            logging.error(f"ERRO: {e}, NÃO FOI POSSÍVEL SALVAR O DATAFRAME.")
        
    def concatDataFrame(self, df: pd.DataFrame, dictionary: dict, index: int):
        try:
            return pd.concat([df, pd.DataFrame(dictionary, index=[index])])
        except KeyError as e:
            logging.error(f"ERRO: {e}, A CHAVE {e} NÃO FOI ENCONTRADA NO DICIONÁRIO.")
        except Exception as e:
            logging.error(f"ERRO: {e}, NÃO FOI POSSÍVEL CONCATENAR OS DATAFRAMES.")
            
    def saveDictionary(self, coin: str, aboutCoin: [list, dict], data):
        try:
            dictionary = {
                    'Moeda': generalTools.hyphenToEmptySpace(coin).title() if coin != 'GERAL' else aboutCoin['name'],
                    'Sigla_Moeda': aboutCoin[3].split("preço")[1] if coin != 'GERAL' else aboutCoin['symbol'],
                    'Preco': float(generalTools.commaToEmpty(generalTools.brlToEmpty(aboutCoin[0]))) if coin != 'GERAL' else round(aboutCoin['quote']['BRL']['price'], 2),
                    'Und_Monetaria': aboutCoin[0][:2] if coin != 'GERAL' else 'BRL',
                    'Var': float(generalTools.percentageToEmpty(aboutCoin[1])) if coin != 'GERAL' else round(aboutCoin['quote']['BRL']['percent_change_24h'], 2),
                    'Periodo_Var': generalTools.removeParentheses(aboutCoin[2]) if coin != 'GERAL' else '1d',
                    'Data_Captura': generalTools.splitByEmptySpace(data)[0],
                    'Hora_Captura': generalTools.splitByEmptySpace(data)[1],
                    'Fornecimento_Total': float(generalTools.commaToEmpty(generalTools.splitByEmptySpace(aboutCoin[11])[0])) if coin != 'GERAL' else round(aboutCoin['total_supply'], 2),
                    #'Fornecimento_Max': float(generalTools.commaToEmpty(generalTools.splitByEmptySpace(aboutCoin[12])[0]))
                }
            logging.info(f"INFORMAÇÕES REFERENTE A MOEDA {generalTools.upperCase(coin)} SALVA COM SUCESSO.")
            return dictionary
        except:
            logging.error(f"INFORMAÇÕES REFERENTE A MOEDA {generalTools.upperCase(coin)} NÃO FORAM SALVAS.")