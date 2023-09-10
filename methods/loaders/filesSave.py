#import io
import datetime
import os
import time
import numpy as np
import pandas as pd
import utils.logger_config as logger_config
from utils.tools import GeneralTools
from methods.transformers.transformData import TransformData
import logging
generalTools = GeneralTools()
transformData = TransformData()
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))

class FileSavers:
    def __init__(self):
        pass

    #def saveHTML(self, content, file_name: str, file_directory: str):
    #    generalTools.makeDirectory(file_directory)
    #    with io.open(os.path.join(file_directory, file_name), "w", encoding="utf-8") as fp:
    #        fp.write(content.text)

    def openingSheets(self, directory: str, sheet: str, rows: int, footer: int):
        return pd.read_excel(f"{directory}", sheet_name=f"{sheet}", skiprows=rows, skipfooter=footer)

    def saveDataFrameWithDict(self, content, file_name, sep, nameDirectory):
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

    def creatingFinalDataFrame(self, df: pd.DataFrame, data: str, fileName, sep, nameDirectory, data_cap: str):
        novo_df = pd.DataFrame()
        novo_df['SERIE'] = df['Código ISIN'].map(lambda x: str(x).replace("nan","").lstrip())
        novo_df['TITULO'] = df.iloc[:,0].map(lambda x: f"'{x}'")
        novo_df['DATA_VENCIMENTO'] = df['Data de Vencimento'][:].apply(lambda x: transformData.format_Date(x))
        novo_df['DATA_REF'] = str(datetime.datetime.strptime(data, "%B de %Y").strftime("%Y-%m-%d"))
        novo_df['DATA_CAPTURA'] = data_cap
        novo_df['FINANCEIRO (R$ BI)'] = df.iloc[:,-1].map(lambda x: generalTools.zeroToEmpty(str(x)) if len(str(x)) == 1 else generalTools.nanToEmpty(str(x)))
        novo_df['QUANTIDADE (MIL)'] = df.iloc[:,-2].map(lambda x: generalTools.zeroToEmpty(str(x)) if len(str(x)) == 1 else generalTools.nanToEmpty(str(x)))
        novo_df['COD_REF'] = novo_df['SERIE'].apply(lambda x: f"'{x}'")

        novo_df = novo_df[(novo_df['QUANTIDADE (MIL)'] != '') & (novo_df['FINANCEIRO (R$ BI)'] != '')]

        return novo_df.to_csv(os.path.join(nameDirectory, fileName), sep=f"{sep}", 
                              columns=['SERIE', 'TITULO', 'DATA_VENCIMENTO', 'DATA_REF', 'DATA_CAPTURA', 'FINANCEIRO (R$ BI)', 'QUANTIDADE (MIL)', 'COD_REF'], 
                              index=False)

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
                    #conteudo
                }
            logging.info(f"INFORMAÇÕES SALVAS COM SUCESSO.")
            return dictionary
        except:
            logging.error(f"INFORMAÇÕES NÃO FORAM SALVAS.")