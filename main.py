import sys
import pandas as pd
import datetime
import Levenshtein
import logging
import os

from ApiSheets import Sheets
from Scrapping import Scrapper

#Sistema de logs para acompanhar a execução do arquivo
pd.options.display.float_format = '{:,.2f}'.format
today = datetime.date.today().strftime("%Y-%m-%d")
logging.basicConfig(
    filename = os.path.join(os.path.dirname(__file__), "log",f"{today}.log"),
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

class ScrapperToSheets:

    def __init__(self):
        logger.info("Starting ApiManager")
        self.sheets = Sheets()
        self.scrapper = Scrapper()

    def __set_reatores_ano(self):
        logger.info("Starting reatores_ano")
        df = self.scrapper.reactors_ano()
        df = df.sort_values(by="Name")
        self.sheets.reatores_ano = df
    
    def start(self):
        logger.info("Starting start")

        self.__set_reatores_ano()

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        logger.error("MissingCommand")
        raise Exception("MissingCommand")
    # if sys.argv[1] == "update":
    #     logger.info(" main.py update")
    #     api_manager = ScrapperToSheets()
    #     api_manager.update()
    #     logger.info("Finished update")
    elif sys.argv[1] == "start":
        logger.info(" main.py start")
        api_manager = ScrapperToSheets()
        api_manager.start()
        logger.info("Finished start")
    else:
        raise Exception("CommandNotFound")
        