import pandas as pd
import datetime
import requests
from json import loads
dir = "~/Documents/potc/"
def tx_in_block_to_file(dir : str):
    # Starting block number
    start_block = 0
    # Number of blocks to crawl
    num_blocks = 10  # You can change this to the desired number of blocks
    # Base URL
    base_url = 'https://paraclear-mainnet.starknet.io/feeder_gateway/get_block?blockNumber='
    json_data = requests.get(base_url+"latest").text
    # Parse the JSON data
    data = loads(json_data)
    # Extract the block_number
    num_blocks = data['block_number']
    data_dict = []
    end_block = num_blocks
    start_block = 23404
    end_block = num_blocks
    for block_number in range(start_block, end_block):
        # Construct the URL for the current block number
        url = f'{base_url}{block_number}'
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the content of the response
            content = response.text
            # Parse the JSON data
            data = loads(content)
            transactions = data['transactions']
            num_transactions = len(transactions)
            block_number = data['block_number']
            gas_price = int(data['gas_price'],16)
            time = data['timestamp']
            # Format the datetime object as a string
            dt_object = datetime.datetime.fromtimestamp(time)
            date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            #actual_fee = int(data['actual_fee'],16)
            #n_steps = data["execution_resources"]["n_steps"]
            data_dict.append({"block_number" : block_number, "time" : date_string, "num_transactions" : num_transactions, "gas_price" : gas_price})
            print(f"{data['block_number']} 'number of transaction' {len(transactions)}")
        else:
            print(f'Failed to retrieve data for block {block_number}. Status code: {response.status_code}')
    df = pd.DataFrame(data_dict)
    df.to_csv(f"{dir}blocks_{start_block}_{end_block}.csv", index=False)
    
def gas_used_per_block_to_file():
    API_KEY = 'PBEFEH51THZN9DDEXEX3UAP7WKTEJAF5VQ'
    address = '0xF338cad020D506e8e3d9B4854986E0EcE6C23640'
    start_block = 18677174
    end_block = 18677174
    URL = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start_block}&toBlock={end_block}&apikey={API_KEY}'
    response = requests.get(URL)
    result = loads(response.content)['result']
    for tx in result:
        print(f'blockNumber: {tx["blockNumber"]}, gasUsed: {tx["gasUsed"]}')