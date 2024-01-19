import requests
import pandas as pd

symbol = 'GSPC.INDX'
page_size = 1000

# Read the API key from the file
with open('tools/marketstack_api_key.txt', 'r') as file:
    api_key = file.read().strip()

offset = 0
index_data = []
while True:
    print(f'Downloading data from {offset} to {offset + page_size}')
    url = f'https://api.marketstack.com/v1/eod?access_key={api_key}&symbols={symbol}&sort=ASC&offset={offset}&limit={page_size}'
    response = requests.get(url).json()
    pagination = response['pagination']
    total = int(pagination['total'])
    data = response['data']
    index_data.extend(data)

    if offset + page_size > total:
        break

    offset += page_size

# Create a DataFrame from the list of dictionary objects
df = pd.DataFrame(index_data)
df.drop(columns=['adj_high', 'adj_low', 'adj_open', 'adj_volume', 'adj_close'], inplace=True)

# Write the DataFrame to a CSV file
df.to_csv(f'data/{symbol}.csv', index=False)
