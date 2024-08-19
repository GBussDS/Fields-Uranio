import requests
import pandas as pd
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from bs4 import BeautifulSoup

url = "https://pris.iaea.org/PRIS/CountryStatistics/ReactorDetails.aspx?current=3"

payload = {}
headers = {
  'Cookie': 'SMIDENTITY=+b6RsRjVdySWIWGxVPQC8f3a97Pnrd/MXyb3TOsX4zC8FSMZ/11LAtf7pK62vYEkqf3bmXTi0XIRnmovs2/fCUF1prA3fK7W23qhxg0y2K5Bnpj0mYMFcufSnLk3D3NVD1DukxlWK4Fnn31NydML1dmB4QM+02nG50D9eh4A/5FrqYad25TsKNmFYEPl+YA6z0Vc4hjI4Vj5v4rZfDpCcmWX6mu4FJZdBa/gsFhi395tglQsuO6MOzXa1dEVqZKrLOHBXS5GtgYS8fdJhqAJx06k2JpK+05NfAtLuc8xsHFlkBqh9YrWNvqaP6y2m9BqUtqq1lFTks3Lj9+Sehgk/643ktk6bX9k/+yGduXbgOvwvDahWzk3u8p8W8wNp4THaLhYndvdJgtY1Q6aS/1Scp2RKsU3TU2wlU9YOfO2vsGYwQ4fcf7HTu6fKL+OpHxhxWE/4NsMjEtylXpJZcP+DRMIRiHgxIyo0z0JDDHuuAnhuTdxOG9P7fFdi0lmRwnU8o2v6vugWHhRZUKFAdZCEMOoYsD8cHdq5Mm1PnWA6GD2Zevko8WgtmFukX/ytrBM; ASP.NET_SessionId=oqzw5ap5qy2liba2awlusivj'
}

class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().proxy_manager_for(*args, **kwargs)

try:
    #Cria um contexto SSL para evitar erros
    context = ssl.create_default_context()
    context.set_ciphers('DEFAULT@SECLEVEL=1')

    session = requests.Session()
    session.mount('https://', SSLAdapter(ssl_context=context))

    response = session.get(url, headers=headers)
    response.raise_for_status()

    return_html = BeautifulSoup(response.text, 'html.parser')

    #Os dados do site sempre ficam na div de classe tablesorter ou active
    table = return_html.find('table', {'class': 'active'})

    name = []
    year = []
    elet_sup = []
    ref_unit_pow = []
    annual_time_on = []
    oper_fac = []
    ener_avail_annual = []
    ener_avail_cumul = []
    load_fac_annual = []
    load_fac_cumul = []

    #Itera sobre a tabela, os dados ficam armazenados em linha por <tr></tr>
    for row in table.find('tbody').find_all('tr'):
        # e por coluna em <td></td>
        cols = row.find_all('td')
        name.append("nome da usina")
        year.append(cols[0].text.strip())
        elet_sup.append(cols[1].text.strip().replace(',', ''))
        ref_unit_pow.append(int(cols[2].text.strip()))
        annual_time_on.append(int(cols[3].text.strip()))
        oper_fac.append(float(cols[4].text.strip()))
        ener_avail_annual.append(float(cols[5].text.strip()))
        ener_avail_cumul.append(float(cols[6].text.strip()))
        load_fac_annual.append(float(cols[7].text.strip()))
        load_fac_cumul.append(float(cols[8].text.strip()))

    #Cria o df pandas
    df = pd.DataFrame({
        'Nome': name,
        'Year': year,
        'Electricity Supplied [GW.h]': elet_sup,
        'Reference Unit Power [MW]': ref_unit_pow,
        'Annual Time On Line [h]': annual_time_on,
        'Operation Factor [%]': oper_fac,
        'Energy Availability Factor - Annual [%]': ener_avail_annual,
        'Energy Availability Factor - Cumulative [%]': ener_avail_cumul,
        'Load Factor - Annual [%]': load_fac_annual,
        'Load Factor - Cumulative [%]': load_fac_cumul
    })

    print(df)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    print(f"Exception type: {type(e).__name__}")
    print(f"Request headers: {headers}")

