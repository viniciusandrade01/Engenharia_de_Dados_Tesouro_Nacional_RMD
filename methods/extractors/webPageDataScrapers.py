import datetime
from io import BytesIO
import zipfile
import os
from zipfile import ZipFile
import requests as rq
from bs4 import BeautifulSoup as bs4
import time
import utils.logger_config as logger_config
import logging
import locale
import io
from utils.tools import GeneralTools

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))
generalTools = GeneralTools()

class WebPageDataScrapers:
    def __init__(self):
        self.xlsx = []
        self.zip = []

    #def requestGetApi(self, link: str, endpoint: str, params: dict, headers: dict):
    #    try:
    #        response = rq.get(f'{link}{endpoint}', params=params, headers=headers)
    #        data = response.json()
    #    except rq.exceptions.HTTPError as http_err:
    #        logging.error(f"Erro HTTP: {http_err}")
    #    except rq.exceptions.RequestException as req_err:
    #        logging.error(f"Erro de Requisição: {req_err}")
    #    except Exception as err:
    #        logging.error(f"Erro Desconhecido: {err}")
    #        
    #    return response, data

    def extractInfoUrl(self, html):
        dataref = str(html.find_all('div', class_='descricao')).split("<p>")[-1].split("</p>")[0].replace(" – "," - ").split(" - ")[-1]
        nome_zip = 'Anexo_RMD_' + datetime.datetime.strptime(dataref, "%B de %Y").strftime("%B_%y").capitalize() +'.zip'
        #link_zip = html.find_all('a', class_='tooltip-toggle')[0].attrs['href']
        link_zip = html.find_all("a", {"title": f"{nome_zip}"})[0].get('href')
        return dataref, nome_zip, link_zip

    def extractZip(self, response, nome_zip: str, namedirectory: str):
        generalTools.makeDirectory(namedirectory)
        z = ZipFile(nome_zip, 'r')
        z.extractall(namedirectory)
        z.close()
        os.remove(nome_zip)

    def downloadUrl(self, link_zip, nome_zip, namedirectory: str):
        response = rq.get(link_zip)
        nome_arquivo_zip = os.path.join(namedirectory, nome_zip)
        with open(nome_arquivo_zip, 'wb') as arquivo_zip:
            arquivo_zip.write(response.content)

        # Extraia o conteúdo do arquivo ZIP para o diretório de destino
        with zipfile.ZipFile(nome_arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall(namedirectory)

        # Remova o arquivo ZIP depois de extraído (opcional)
        os.remove(nome_arquivo_zip)
        #with open(nome_zip, 'wb') as file:
        #    file.write(response.content)
        #    
        #    if len(str(response.content).split('"')) > 2:
        #        #os.remove(nome_zip)
        #        response = rq.get(str(response.content).split('"')[-2])
        #    with open(nome_zip, 'wb') as file:
        #        file.write(response.content)
        #
        #with zipfile.ZipFile(nome_zip, 'r') as zip_ref:
        #    zip_ref.extractall(namedirectory)

    def requestGetDefault(self, link: dict, namedirectory: str):
        try:
            html = rq.get(link['generalLink']['url'])
            html.raise_for_status()
            soup = bs4(html.text, 'html.parser')
            dataref, nome_zip, link_zip = self.extractInfoUrl(soup)
            self.downloadUrl(link_zip, nome_zip, namedirectory)
            self.xlsx.append(nome_zip.split(".")[0] + '.xlsx')
            self.extractZip(link_zip, nome_zip, namedirectory)

        except rq.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP: {http_err}")
        except rq.exceptions.RequestException as req_err:
            logging.error(f"Erro de Requisição: {req_err}")
        except Exception as err:
            logging.error(f"Erro Desconhecido: {err}")
        
        return html, soup, dataref, nome_zip, link_zip
    
    #def specificGetRequest(self, link: str):
    #    try:
    #        html = rq.get(link)
    #        html.raise_for_status()
    #        soup = bs4(html.text, 'html.parser')
#
    #    except rq.exceptions.HTTPError as http_err:
    #        logging.error(f"ERRO HTTP: {http_err} PARA MOEDA {link.split('/')[-1].title()}")
    #    except rq.exceptions.RequestException as req_err:
    #        logging.error(f"ERRO DE REQUISIÇÃO: {req_err} PARA MOEDA {link.split('/')[-1].title#()}")
    #    except Exception as err:
    #        logging.error(f"ERRO DESCONHECIDO: {err} PARA MOEDA {link.split('/')[-1].title()}")
    #    
    #    return html, soup