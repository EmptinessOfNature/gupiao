import random
import time
from ib_client_fufei import SimpleClient
from ib_client_fufei import Contract
import datetime
import pandas as pd
import os

def ib_2_csv(hist_data):
    lines=[['dt','open','close','high','low','vol']]
    for i in range(hist_data.__len__()):
        lines.append([hist_data[i].date[0:17],client.hist_data[i].open,client.hist_data[i].close,client.hist_data[i].high,client.hist_data[i].low,str(client.hist_data[i].volume)])
    ret = pd.DataFrame(lines)
    return ret


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
    file_2_write = './data_server/'+now.replace(' ','').replace(':','')[0:8]+'_'+now.replace(' ','').replace(':','')[8:12]+'.csv'
    if not os.path.exists(file_2_write):
        client.reqHistoricalData(
            req_id, contract, now, "1 w", "1 min", "TRADES", False, 1, False, []
        )
        time.sleep(3)
        ret = ib_2_csv(client.hist_data)
        ret.to_csv(file_2_write)
        print(file_2_write,'保存完成！')


