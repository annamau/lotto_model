import pandas as pd
import requests
import json as js
from datetime import date as dt
from tools import get_limit

def get_lotto_numbers():
    # Change user agent to match the current session
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    headers = {'Use-Agent' : user_agent}
        
    dates_combinations = {}

    today = dt.today()
    yesterday = get_limit(today)
    while yesterday > dt(1992, 1 ,1):
        url = f'https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=EMIL&celebrados=true&fechaInicioInclusiva={yesterday.strftime("%Y%m%d")}&fechaFinInclusiva={today.strftime("%Y%m%d")}'
        
        print(f'Request sent from {today.strftime("%d-%m-%Y")} to {yesterday.strftime("%d-%m-%Y")}, waiting for response...')
        json_raw = requests.get(url, headers = headers).content
        
        # Update next time interval for call 
        today = yesterday
        yesterday = get_limit(today)
        
        print("Data recieved, parsing it!")

        json = js.loads(json_raw)

        for item in json:
            try:
                date = item['fecha_sorteo'].split(" ")[0]
                dates_combinations[date] = item['combinacion'].replace(" ", "")
            except TypeError:
                print("Reached all lotto numbers in database")
                yesterday = dt(1992, 1 ,1)
                break

    print('Data parsed! Ready to use!')

    # Create CSV with data in specific format date 5 numbers 2 special numbers and the full combination
    print('Creating CSV...')
    df = pd.DataFrame(columns=["Date","1.N", "2.N", "3.N", "4.N", "5.N", "1.S", "2.S", "Full_Combination"])
    for date in dates_combinations.keys():
        combination_raw = dates_combinations[date]
        combination = combination_raw.split("-")
        row = [date, combination_raw]
        row[1:1] = combination
        df.loc[len(df.index)] = row
    df.to_csv("./data/lotto_numbers.csv", index=False)
    print("CSV created!!")

if __name__ ==  '__main__':
    get_lotto_numbers()
    