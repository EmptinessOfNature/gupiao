from MyTT import *
import akshare as ak
import math

class KDJ():
    def kdj(self, CLOSE, LOW, HIGH):
        NA=80;
        M1A=19;
        M2A=3;
        RSV=(CLOSE-LLV(LOW,NA))/(HHV(HIGH,NA)-LLV(LOW,NA))*100;
        K=SMA(RSV,M1A,1);
        D=SMA(K,M2A,1);
        NOTEXTDX=SMA(K,M2A,1);
        白角=math.atan((SMA(K,M2A,1)/REF(SMA(K,M2A,1),1)-1)[-1]*100)*180/3.1416;
        return 白角

if __name__ == '__main__':
    result = ak.stock_us_hist_min_em(symbol="105.TSLA")
    open = result['开盘']
    close = result['收盘']
    high = result['最高']
    low = result['最低']

    result = KDJ().kdj(close, low, high)
    print(result)
