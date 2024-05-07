from MyTT import *
import akshare as ak

class KDJ():
    def kdj(self, CLOSE, LOW, HIGH):
        N1=45;
        M1=15;
        M2=15;
        RSV=(CLOSE-LLV(LOW,N1))/(HHV(HIGH,N1)-LLV(LOW,N1))*100;
        K=SMA(RSV,M1,1);
        D=SMA(K,M2,1);
        JW=3*K-2*D;
        dict={"k":K.tolist(), "d":D.tolist(), "jw":JW.tolist()}
        return dict

if __name__ == '__main__':
    result = ak.stock_us_hist_min_em(symbol="105.TSLA")
    open = result['开盘']
    close = result['收盘']
    high = result['最高']
    low = result['最低']

    result = KDJ().kdj(close, low, high)
    print(result)