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
    ret = pd.DataFrame(lines[1:],columns=lines[0])
    return ret


client = SimpleClient("127.0.0.1", 7497, 5)
time.sleep(3)
last_now = ''

while True:
    time.sleep(1)
    contract = Contract()
    contract.symbol = "TSLA"
    contract.secType = "STK"
    contract.currency = "USD"
    # In the API side, NASDAQ is always defined as ISLAND in the exchange field
    # contract.exchange = "ISLAND"
    contract.exchange = "SMART"
    now = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
    now_minute = datetime.datetime.now().strftime("%Y%m%d %H:%M")
    if now_minute==last_now:
        print('该分钟已拉取过，跳过',now_minute)
        continue
    last_now = now_minute
    # 如果是下午，那么就是当天的数据，如果是上午，那么就应该算是昨天的数据
    # '2024-05-14.csv'中存的应该是0514 21:30到0515 03:00之间的数据
    today = datetime.datetime.now().date().strftime("%Y-%m-%d") if datetime.datetime.now().hour>13 else (datetime.datetime.now() - datetime.timedelta(days=1)).date().strftime("%Y-%m-%d")
    req_id = 100
    # file_2_write = './data_server/'+now.replace(' ','').replace(':','')[0:8]+'_'+now.replace(' ','').replace(':','')[8:12]+'.csv'
    file_2_write = './data_server/' + today.replace('-','')+'.csv'
    # if not os.path.exists(file_2_write):
    client.clear_hist_data()
    client.reqHistoricalData(
        req_id, contract, now, "1 w", "1 min", "TRADES", False, 1, False, []
    )
    time.sleep(2)
    ret = ib_2_csv(client.hist_data)
    ret.dt = pd.to_datetime(ret.dt)
    threshold_date = pd.Timestamp(today) + datetime.timedelta(hours=13)
    ret = ret[ret.dt >= threshold_date]
    ret.to_csv(file_2_write)
    print(file_2_write,'保存完成！')


