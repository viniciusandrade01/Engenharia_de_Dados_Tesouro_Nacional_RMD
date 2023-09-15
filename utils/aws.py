import os
import boto3
import time
import utils.logger_config as logger_config
import logging
from utils.tools import GeneralTools
from utils.tools import GeneralTools
generalTools = GeneralTools()
logger_config.setup_logger(time.strftime("%Y-%m-%d %H:%M:%S"))


class AboutAWS:
    def __init__(self):
        self.jsonData = generalTools.openJson()

    def createClient(self, service: str):
        try:
            # ACESSAR OS DADOS PELO DATA.JSON, aws_account
            client = boto3.client(
                service_name=service,
                aws_access_key_id=self.jsonData['aws_account']['access_key'],
                aws_secret_access_key=self.jsonData['aws_account']['secret_key'],
                region_name=self.jsonData['aws_account']['region']
                # Podendo usar qualquer região
            )
            return client
        except Exception as e:
            logging.info(f"OCORREU UM ERRO AO CRIAR O CLIENTE S3: {str(e)}")

    def createBucket(self, client, bucketname: str):
        try:
            client.create_bucket(
                ACL='private',
                Bucket=bucketname, # altere para um nome qualquer
                CreateBucketConfiguration={
                    'LocationConstraint': self.jsonData['aws_account']['region']
                },
            )
        except Exception as e:
            logging.info(f"OCORREU UM ERRO AO CRIAR BUCKET: {str(e)}")

    def uploadFile(self, client, localfile: str, bucketname: str, cloudfile: str):
        try:
            client.upload_file(localfile, bucketname, cloudfile)
            logging.info(f"OBJETOS INSERIDOS NO BUCKET {str(generalTools.upperCase(e))} COM SUCESSO!")
        except Exception as e:
            logging.info(f"OCORREU UM ERRO AO TENTAR SUBIR OBJETO AO BUCKET: {str(e)}")
