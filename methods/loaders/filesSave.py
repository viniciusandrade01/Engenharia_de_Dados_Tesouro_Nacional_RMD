import fastavro
import datetime
import os
import time
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

    def openingSheets(self, directory: str, sheet: str, rows: int, footer: int):
        return pd.read_excel(f"{directory}", sheet_name=f"{sheet}", skiprows=rows, skipfooter=footer)

    def creatingFinalDataFrame(self, df: pd.DataFrame, data: str, fileName, sep, nameDirectory, data_cap: str, file_type: str):
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

        diretorio = os.path.join(nameDirectory, fileName)
    
        if file_type == 'csv':
            novo_df.to_csv(f"{diretorio}.csv", sep=f"{sep}", 
                           columns=['SERIE', 'TITULO', 'DATA_VENCIMENTO', 'DATA_REF', 'DATA_CAPTURA', 'FINANCEIRO (R$ BI)', 'QUANTIDADE (MIL)', 'COD_REF'], index=False)
            logging.info(f"DataFrame salvo como {fileName} em formato CSV.") 
            return fileName, file_type
        
        elif file_type == 'excel':
            novo_df.to_excel(f"{diretorio}.xlsx", index=False)
            logging.info(f"DataFrame salvo como {fileName} em formato Excel.")
            return fileName, file_type 
        
        elif file_type == 'json':
            novo_df.to_json(f"{diretorio}.json", orient='records')
            logging.info(f"DataFrame salvo como {fileName} em formato JSON.")
            return fileName, file_type
        
        elif file_type == 'parquet':
            novo_df.to_parquet(f"{diretorio}.parquet", index=False)
            logging.info(f"DataFrame salvo como {fileName} em formato Parquet.")
            return fileName, file_type
        
        elif file_type == 'hdf':
            novo_df.to_hdf(f"{diretorio}.h5", key='data')
            logging.info(f"DataFrame salvo como {fileName} em formato HDF5/H5.")
            return fileName, file_type
        
        elif file_type == 'pickle':
            novo_df.to_pickle(f"{diretorio}.pkl")
            logging.info(f"DataFrame salvo como {fileName} em formato Pickle.")
            return fileName, file_type
        
        elif file_type == 'feather':
            novo_df.to_feather(f"{diretorio}.feather")
            logging.info(f"DataFrame salvo como {fileName} em formato Feather.")
            return fileName, file_type
        
        elif file_type == 'avro':
            with open(f"{diretorio}.avro", 'wb') as out_avro:
                fastavro.writer(out_avro, novo_df.to_dict(orient='records'))
            logging.info(f"DataFrame salvo como {fileName} em formato Avro.")
            return fileName, file_type
        
        elif file_type == 'html':
            novo_df.to_html(f"{diretorio}.html", index=False)
            logging.info(f"DataFrame salvo como {fileName} em formato HTML.")
            return fileName, file_type

        else:
            logging.info("Tipo de arquivo não suportado. Por favor, escolha um formato válido.")

    def concatDataFrame(self, df: pd.DataFrame, dictionary: dict, index: int):
        try:
            return pd.concat([df, pd.DataFrame(dictionary, index=[index])])
        except KeyError as e:
            logging.error(f"ERRO: {e}, A CHAVE {e} NÃO FOI ENCONTRADA NO DICIONÁRIO.")
        except Exception as e:
            logging.error(f"ERRO: {e}, NÃO FOI POSSÍVEL CONCATENAR OS DATAFRAMES.")