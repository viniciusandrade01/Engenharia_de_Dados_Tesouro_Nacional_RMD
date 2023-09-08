import logging

def setup_logger(data: str):
    logging.basicConfig(filename=f"Log_{data.split(' ')[0].replace('-','')}.log",
                        level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')