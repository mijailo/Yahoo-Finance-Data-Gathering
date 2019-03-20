from datetime import datetime
import numpy as np
import requests
import calendar
import csv
import re

def get(yahoo_code,inicio,fin):
    """ get financial historical data from yahoo
    """
    #######################################
    #inicio=(aaaa,mm,dd), fin=(aaaa,mm,dd)#
    #######################################
    # connection parameters
    # ----------------------------------- #

    # http timeout
    timeout_secs = 5

    # retries
    num_retries = 4

    # url encoding
    yahoo_url = r'https://finance.yahoo.com/quote/{0}/history?p={0}'.format(yahoo_code)

    # init headers
    headers = dict()
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['User-Agent'] = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"


    # manejo de conexion
    # ----------------------------------- #

    csv_data = None
    while num_retries>0:

        try:

            session = requests.Session()

            r = session.get(yahoo_url,headers=headers,timeout=timeout_secs)
            r.encoding = 'utf-8'
            html_text = r.text

            # get crumb
            pattern = r"(\"CrumbStore\":{\"crumb\":\")([^\"]+)(\"})"
            m = re.search(pattern, html_text)
            crumb = m.group(2).replace("\\u002F","/")

            # Obtener datos desde inicio=(aaaa,mm,dd) (UTC)
            start_time = calendar.timegm(datetime(inicio[0],inicio[1],inicio[2]).utctimetuple())
#           #hasta hoy: end_time = calendar.timegm(datetime.now().utctimetuple())   
            end_time = calendar.timegm(datetime(fin[0],fin[1],fin[2]).utctimetuple())

            # url para descargar datos
            data_url = r"https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}".format(yahoo_code, start_time, end_time, crumb)

            # bajar datos en formato csv
            r = session.get(data_url,headers=headers,timeout=timeout_secs)
            csv_data = csv.reader(r.content.decode().splitlines(),delimiter=',')

        except requests.exceptions.Timeout:

            wtext = 'Connection timeout, {0} reintentos restantes'.format(str(num_retries))

            # print or log
            print(wtext)

        except AttributeError:

            wtext = 'Error de migajas (crumb error), {0} reintentos restantes'.format(str(num_retries))

            # print or log
            print(wtext)

        except Exception:

            wtext = 'Error genérico, {1} intentos restantes'.format(str(num_retries))

            # print or log
            print(wtext)

        finally:

            if csv_data:
                wtext = 'Los datos para {0} se bajaron sin pedos'.format(yahoo_code)

                # print or log
                print(wtext)
                break

            else:
                num_retries -= 1

    # asset-data
    if csv_data:
        eod_data = []
        for ii,row in enumerate(csv_data):

            if ii>0 and not 'null' in row:

                eod_data.append({
                    'date': row[0],
                    'open': float(row[1]),
                    'high': float(row[2]),
                    'low': float(row[3]),
                    'close': float(row[4]),
                    'adj_close': float(row[5]),
                    'volume': int(row[6])
                    })

    else:

        wtext = 'No se pudo descargar {0} :c'.format(yahoo_code)

        # print or log
        print(wtext)

    return eod_data