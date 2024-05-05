import random
import time
from ib_client_fufei import SimpleClient
from ib_client_fufei import Contract
import datetime
import pandas as pd

class Ib_client:
    def __init__(self):
        self.client = SimpleClient("127.0.0.1", 7497, 5)
        self.client.reqCurrentTime()
    def get_data_ib(self):
        contract = Contract()
        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.currency = "USD"
        # In the API side, NASDAQ is always defined as ISLAND in the exchange field
        # contract.exchange = "ISLAND"
        contract.exchange = "SMART"
        now = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
        req_id = random.randint(1,10000)
        self.client.reqHistoricalData(
            req_id, contract, now, "1 w", "1 min", "TRADES", False, 1, False, []
        )
        time.sleep(1)
        lines = []
        for i in range(4800):
            ori_data = self.client.hist_data[i]
            line = [
                ori_data.date[0:4]
                + "-"
                + ori_data.date[4:6]
                + "-"
                + ori_data.date[6:8]
                + " "
                + ori_data.date[9:17],
                ori_data.open,
                ori_data.close,
                ori_data.high,
                ori_data.low,
                int(ori_data.volume),
                float(ori_data.volume),
            ]
            lines.append(line)
            hist = pd.DataFrame(lines,columns=["dt", "open", "close", "high", "low", "vol", "cje"])
        return hist

if __name__ == "__main__":
    ib = Ib_client()
    ib.get_data_ib()
    ib.client.disconnect()