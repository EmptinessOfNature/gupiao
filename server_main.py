import random
import time
from ib_client_fufei import SimpleClient
from ib_client_fufei import Contract
import datetime
import pandas as pd

client = SimpleClient("127.0.0.1", 7497, 5)
time.sleep(3)

while True:
    time.sleep(3)
    contract = Contract()
    contract.symbol = "TSLA"
    contract.secType = "STK"
    contract.currency = "USD"
    # In the API side, NASDAQ is always defined as ISLAND in the exchange field
    # contract.exchange = "ISLAND"
    contract.exchange = "SMART"
    now = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
    req_id = 100
    client.reqHistoricalData(
        req_id, contract, now, "1 w", "1 min", "TRADES", False, 1, False, []
    )

    file_2_write = './data_server/'+now.replace(' ','').replace(':','')+'txt'
    with open(file_2_write,'w') as f:
        f.write(str(client.hist_data))

