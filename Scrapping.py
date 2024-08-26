import requests
import pandas as pd
import numpy as np
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from bs4 import BeautifulSoup

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

class Scrapper:

    HEADERS = {'Cookie': 'SMIDENTITY=+b6RsRjVdySWIWGxVPQC8f3a97Pnrd/MXyb3TOsX4zC8FSMZ/11LAtf7pK62vYEkqf3bmXTi0XIRnmovs2/fCUF1prA3fK7W23qhxg0y2K5Bnpj0mYMFcufSnLk3D3NVD1DukxlWK4Fnn31NydML1dmB4QM+02nG50D9eh4A/5FrqYad25TsKNmFYEPl+YA6z0Vc4hjI4Vj5v4rZfDpCcmWX6mu4FJZdBa/gsFhi395tglQsuO6MOzXa1dEVqZKrLOHBXS5GtgYS8fdJhqAJx06k2JpK+05NfAtLuc8xsHFlkBqh9YrWNvqaP6y2m9BqUtqq1lFTks3Lj9+Sehgk/643ktk6bX9k/+yGduXbgOvwvDahWzk3u8p8W8wNp4THaLhYndvdJgtY1Q6aS/1Scp2RKsU3TU2wlU9YOfO2vsGYwQ4fcf7HTu6fKL+OpHxhxWE/4NsMjEtylXpJZcP+DRMIRiHgxIyo0z0JDDHuuAnhuTdxOG9P7fFdi0lmRwnU8o2v6vugWHhRZUKFAdZCEMOoYsD8cHdq5Mm1PnWA6GD2Zevko8WgtmFukX/ytrBM; ASP.NET_SessionId=oqzw5ap5qy2liba2awlusivj'}

    def __init__(self):
        #Cria um contexto SSL para evitar erros
        CONTEXT = ssl.create_default_context()
        CONTEXT.set_ciphers('DEFAULT@SECLEVEL=1')

        self.SESSION = requests.Session()
        self.SESSION.mount('https://', SSLAdapter(ssl_context=CONTEXT))

    def reactors(self):
        """
        Função para obter as informações dos reatores ao longo dos anos, além das informações gerais dos reatores.

        Returns:
            pandas.DataFrame: Reatores Info,
            pandas.Dataframe: Reatores Ano.
        """

        url_reatores_ano = "https://pris.iaea.org/PRIS/CountryStatistics/ReactorDetails.aspx?current="
        existing_pages = [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 62, 63, 64, 65, 66, 67, 68, 69, 74, 75, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 96, 97, 98, 100, 101, 102, 104, 106, 107, 108, 114, 119, 121, 122, 123, 124, 125, 126, 127, 133, 134, 135, 136, 137, 138, 139, 140, 141, 146, 149, 150, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 278, 279, 280, 281, 285, 286, 287, 288, 289, 290, 291, 292, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 310, 311, 318, 325, 326, 327, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 420, 421, 422, 423, 427, 428, 429, 442, 443, 447, 448, 451, 453, 460, 467, 468, 469, 470, 474, 475, 476, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 502, 503, 505, 506, 507, 508, 513, 519, 524, 525, 526, 527, 528, 529, 530, 531, 532, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 553, 554, 555, 556, 557, 558, 559, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 581, 582, 584, 586, 589, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 683, 684, 686, 687, 689, 690, 691, 692, 693, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 710, 711, 712, 713, 714, 715, 717, 718, 719, 725, 727, 729, 730, 735, 736, 737, 738, 739, 742, 751, 752, 764, 765, 789, 790, 791, 836, 837, 838, 839, 840, 841, 842, 843, 852, 853, 856, 859, 860, 862, 864, 865, 867, 873, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 890, 891, 892, 893, 894, 895, 896, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 912, 913, 914, 915, 918, 919, 921, 922, 923, 924, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 957, 966, 973, 974, 975, 976, 986, 987, 993, 994, 995, 996, 997, 998, 999, 1000, 1008, 1042, 1043, 1044, 1045, 1050, 1051, 1052, 1053, 1055, 1056, 1059, 1060, 1061, 1067, 1068, 1072, 1073, 1074, 1075, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1090, 1091, 1094, 1101, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1120, 1121, 1123, 1124]
        df_ano = pd.DataFrame()
        df_info = pd.DataFrame()
        
        for i in existing_pages:
            url = url_reatores_ano + str(i)

            try:
                response = self.SESSION.get(url, headers=self.HEADERS)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                print(f"Exception type: {type(e).__name__}")
                print(f"Request headers: {self.HEADERS}")
                continue

            try:
                response.raise_for_status()
            except:
                continue
            
            return_html = BeautifulSoup(response.text, 'html.parser')

            if return_html.find('div', {'class':'alert-error'}) != None:
                continue
            
            df_ano = pd.concat([df_ano, self.reactors_ano(return_html)], ignore_index=True)
            df_info = pd.concat([df_info, self.reactors_info(return_html)], ignore_index=True)
            
        return df_ano, df_info
    
    def reactors_info(self, return_html):
        """
        Função para obter as informações dos reatores como localização e data de inauguração.

        Returns:
            pandas.DataFrame: Reatores Info.
        """

        # Os dados ficam em partes com id específicos
        reactor_name = return_html.find('span', {'id': 'MainContent_MainContent_lblReactorName'}).text.strip()
        reactor_country = return_html.find('a', {'id': 'MainContent_litCaption'}).text.replace('\n', '').replace('\r', '').strip()
        reactor_status = return_html.find('span', {'id': 'MainContent_MainContent_lblReactorStatus'}).text.strip()
        reactor_type = return_html.find('span', {'id': 'MainContent_MainContent_lblType'}).text.strip()
        reference_unit_power = return_html.find('span', {'id': 'MainContent_MainContent_lblNetCapacity'}).text.strip()
        cons_st_date = return_html.find('span', {'id': 'MainContent_MainContent_lblConstructionStartDate'}).text.strip().replace('N/A', '')
        fst_grid_date = return_html.find('span', {'id': 'MainContent_MainContent_lblGridConnectionDate'}).text.strip().replace('N/A', '')
        comm_oper_date = return_html.find('span', {'id': 'MainContent_MainContent_lblCommercialOperationDate'}).text.strip().replace('N/A', '')
        per_shut_date = return_html.find('span', {'id': 'MainContent_MainContent_lblPermanentShutdownDate'}).text.strip().replace('N/A', '')
        susp_date = return_html.find('span', {'id': 'MainContent_MainContent_lblLongTermShutdownDate'}).text.strip().replace('N/A', '')
        back_date = return_html.find('span', {'id': 'MainContent_MainContent_lblRestartDate'}).text.strip().replace('N/A', '')
        
        # Cria o df pandas
        df = pd.DataFrame({
            'Name': [reactor_name],
            'Country': [reactor_country],
            'Status': [reactor_status],
            'Reactor Type': [reactor_type],
            'Reference Unit Power (Net Capacity)': [reference_unit_power],
            'Construction Start Date': [cons_st_date],
            'First Grid Connection': [fst_grid_date],
            'Commercial Operation Date': [comm_oper_date],
            'Permanent Shutdown Date': [per_shut_date],
            'Suspended Operation Date': [susp_date],
            'Restart Date': [back_date]
        })

        # # Substitui os None novamente por nada para que não ocorra erro ao ir para o Sheets
        # df = df.where(pd.notnull(df), '')

        return df

    def reactors_ano(self, return_html):
        """
        Função para obter os dados dos reatores ao longo dos anos.

        Returns:
            pandas.DataFrame: Reatores Ano.
        """

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


        #Para esse tipo de página os dados ficam na div 'active'
        table = return_html.find('table', {'class': 'active'})

        #O nome do reator fica em um lugar diferente do resto dos dados
        reactor_name = return_html.find('span', {'id': 'MainContent_MainContent_lblReactorName'}).text

        #Para os reatores que não tem histórico
        try:
            rows = table.find('tbody').find_all('tr')
        except:
            return
        
        #Itera sobre a tabela, os dados ficam armazenados em linha por <tr></tr>
        for row in rows:
            # e por coluna em <td></td>
            cols = row.find_all('td')

            #Substituo por None aqui para que a lista tenha entradas vazias
            if len(cols) == 9:
                name.append(reactor_name)
                year.append(int(cols[0].text.strip()) if cols[0].text.strip() != '' else None)
                elet_sup.append(float(cols[1].text.strip()) if cols[1].text.strip() != '' else None)
                ref_unit_pow.append(int(cols[2].text.strip()) if cols[2].text.strip() != '' else None)
                annual_time_on.append(int(cols[3].text.strip()) if cols[3].text.strip() != '' else None)
                oper_fac.append(float(cols[4].text.strip()) if cols[4].text.strip() != '' else None)
                ener_avail_annual.append(float(cols[5].text.strip()) if cols[5].text.strip() != '' and cols[5].text.strip() != 'NC' else None)
                ener_avail_cumul.append(float(cols[6].text.strip()) if cols[6].text.strip() != '' and cols[6].text.strip() != 'NC' else None)
                load_fac_annual.append(float(cols[7].text.strip()) if cols[7].text.strip() != '' and cols[7].text.strip() != 'NC' else None)
                load_fac_cumul.append(float(cols[8].text.strip()) if cols[8].text.strip() != '' and cols[8].text.strip() != 'NC' else None)
            else:
                continue
        
        #Cria o df pandas
        df = pd.DataFrame({
            'Name': name,
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

        #Substituo os None novamente por nada para que não ocorra erro ao ir para o Sheets
        df = df.where(pd.notnull(df), '')

        return df
    
    def download_csv(self):
        df_ano, df_info = self.reactors()
        df_ano.to_csv('planilhas/Reactors_Ano.csv', index=False)
        df_info.to_csv('planilhas/Reactors_Info.csv', index=False)
    
if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.download_csv()