from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd
import os
import pygsheets

SPREADSHEET_TITLE = "Fields"

class Sheets():

    CURRENT = os.path.dirname(__file__)
    KEYS_FOLDER = "keys"
    SERVICE_ACCOUNT_CREDENTIALS = os.path.join(CURRENT, KEYS_FOLDER, "email-credential.json")
    VALUE_RENDER = pygsheets.ValueRenderOption.UNFORMATTED_VALUE

    def __init__(self,):
        self.gc = pygsheets.authorize(
            service_file=self.SERVICE_ACCOUNT_CREDENTIALS
        )
        self.sh = self.gc.open(SPREADSHEET_TITLE)
    
    def __set_df(self, ws_name, df):
        ws = self.sh.worksheet_by_title(ws_name)
        ws.clear()
        ws.update_values("A1", [df.columns.tolist()], extend=True)
        ws.update_values("A2", df.values.tolist(), extend=True)
        ws.adjust_column_width(start=1, end=df.shape[1])

    @property
    def reatores_ano(self):
        ws = self.sh.worksheet_by_title("Reatores/Ano")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @reatores_ano.setter
    def reatores_ano(self, df):
        self.__set_df("Reatores/Ano", df)

    @property
    def reatores_info(self):
        ws = self.sh.worksheet_by_title("Reatores Info")
        return ws.get_as_df(value_render=self.VALUE_RENDER)
    
    @reatores_info.setter
    def reatores_info(self, df):
        self.__set_df("Reatores Info", df)

if __name__ == "__main__":
    sheet = Sheets()
    df = pd.read_csv('Reactors_Info.csv')
    df_novo = df.where(pd.notnull(df), '')
    sheet.reatores_ano = df_novo