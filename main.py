import requests
from binance.spot import Spot
from datetime import datetime, timedelta 
import pandas as pd
from tqdm import tqdm

pairs_info = requests.get('https://api.binance.com/api/v3/exchangeInfo').json()

symbols = set()

for i in range(len(pairs_info['symbols'])):
    symbols.add(pairs_info['symbols'][i]['symbol'])

start_time_poins = [1612126800000] # 1612126800000 is 2021-02-01 00:00:00 in Date from milliseconds (ms) since timestamp or unix epoch format
for i in range(1, 18):
    start_time_poins.append(int((datetime.strptime('2021-02-01 00:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(hours=i*1001)).timestamp() * 1000))

client = Spot()

data_frame_columns=['Open time', 'Open', 'High', 'Low', 
                    'Close', 'Volume', 'Close time',
                    'Quote asset volume', 'Number of trades', 
                    'Taker buy base asset volume', 
                    'Taker buy quote asset volume', 'Ignore']

for symbol in tqdm(symbols):
    result = []
    for start_time_point in start_time_poins:
        result.extend(client.klines(symbol, "1h", limit=1000, startTime = start_time_point))
    df = pd.DataFrame(result, columns=data_frame_columns)
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    df.to_csv(f'data/{symbol}.csv')
