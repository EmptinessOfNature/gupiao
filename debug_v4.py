import numpy as np
from MyTT import *
import akshare as ak
import glob, os
import json
import pandas as pd
#支撑
class ZhiCheng():

    def const_1(self,X_in,Y,Z):
        if X_in == 0:
            X = CONST(SUM(IF(Y, REF(Z, 1), 0), 0));  # DRAWNULL=0
            if X[-1] != 0:
                X_in = X[-1]
        else:
            X = np.array([X_in] * len(Y))
        return X,X_in

    def xinhao(self, C, L, H, V,CONST_dict):
        CLOSE = np.array(C)
        VOL = np.array(V)
        H=np.array(H)
        L=np.array(L)
        N=5
        M=15
        X_1=CLOSE;
        X_2=SUM(CLOSE*VOL,0)/SUM(VOL,0);
        X_3=SUM(CLOSE*VOL,0)/SUM(VOL,0);
        X_14=REF(CLOSE,1);
        X_15=SMA(MAX(CLOSE-X_14,0),14,1)/SMA(ABS(CLOSE-X_14),14,1)*100;
        X_16=CROSS(80,X_15);
        X_17=np.logical_and(FILTER(X_16,60), CLOSE/X_3>1.005);

        X_18=CROSS(X_15,20);
        X_19=np.logical_and(FILTER(X_18,60), CLOSE/X_3<0.995);

        X_20=np.logical_and(CLOSE>REF(CLOSE,1), CLOSE/X_2>1+N/1000);
        X_21=np.logical_and(CLOSE<REF(CLOSE,1), CLOSE/X_2<1-N/1000);
        X_22=CROSS(SUM(X_20,0),0.5);
        X_23=CROSS(SUM(X_21,0),0.5);
        X_24=np.array(SUM(X_22,0)) * np.array(CROSS(COUNT(CLOSE<REF(CLOSE,1),BARSLAST(X_22)[-1]),0.5));

        X_25=SUM(X_23,0)*CROSS(COUNT(CLOSE>REF(CLOSE,1),BARSLAST(X_23)[-1]),0.5);

        # X1=CONST(SUM(IF(X_24,REF(CLOSE,1),0),0)); #DRAWNULL=0
        X1,X1_in = self.const_1(CONST_dict['X1'],X_24,CLOSE)
        # Z1=CONST(SUM(IF(X_25,REF(CLOSE,1),0),0));
        Z1,Z1_in = self.const_1(CONST_dict['Z1'],X_25,CLOSE)
        X_26=CROSS(SUM(np.logical_and(X_20, CLOSE>X1*(1+1/100)),0),0.5);
        X_27=CROSS(SUM(np.logical_and(X_21, CLOSE<Z1*(1-1/100)),0),0.5);
        X_28=SUM(X_26,0)*CROSS(COUNT(CLOSE<REF(CLOSE,1),BARSLAST(X_26)[-1]),0.5);

        X_29=SUM(X_27,0)*CROSS(COUNT(CLOSE>REF(CLOSE,1),BARSLAST(X_27)[-1]),0.5);

        X2=CONST(SUM(IF(X_28,REF(CLOSE,1),0),0)); #DRAWNULL=0
        Z2=CONST(SUM(IF(X_29,REF(CLOSE,1),0),0)); #DRAWNULL=0
        X_30=np.logical_and(CLOSE>REF(CLOSE,1), CLOSE/X_2>1+M/1000);
        X_31=np.logical_and(CLOSE<REF(CLOSE,1), CLOSE/X_2<1-M/1000);
        X_32=CROSS(SUM(X_30,0),0.5);
        X_33=CROSS(SUM(X_31,0),0.5);
        X_34=SUM(X_32,0)*CROSS(COUNT(CLOSE<REF(CLOSE,1),BARSLAST(X_32)[-1]),0.5);
        X_35=SUM(X_33,0)*CROSS(COUNT(CLOSE>REF(CLOSE,1),BARSLAST(X_33)[-1]),0.5);
        # X_36=CONST(SUM(IF(X_34,REF(CLOSE,1),0),0)); #DRAWNULL=0
        X_36, X_36_in = self.const_1(CONST_dict['X_36'], X_34, CLOSE)
        # X_37=CONST(SUM(IF(X_35,REF(CLOSE,1),0),0));#DRAWNULL=0
        X_37, X_37_in = self.const_1(CONST_dict['X_37'], X_35, CLOSE)
        X_38=CROSS(SUM(np.logical_and(X_30, CLOSE>X_36*1.02),0),0.5);
        X_39=CROSS(SUM(np.logical_and(X_31, CLOSE<X_37*0.98),0),0.5);
        X_40=SUM(X_38,0)*CROSS(COUNT(CLOSE<REF(CLOSE,1),BARSLAST(X_38)[-1]),0.5);

        X_41=SUM(X_39,0)*CROSS(COUNT(CLOSE>REF(CLOSE,1),BARSLAST(X_39)[-1]),0.5);

        X_42=CONST(SUM(IF(X_40,REF(CLOSE,1),0),0)); #DRAWNULL=0
        X_43=CONST(SUM(IF(X_41,REF(CLOSE,1),0),0)); #DRAWNULL=0
        X_44=np.logical_and(CLOSE>REF(CLOSE,1), CLOSE/X_2>1+1/100);
        X_45=np.logical_and(CLOSE<REF(CLOSE,1), CLOSE/X_2<1-1/100);
        X_46=CROSS(SUM(X_44,0),0.5);
        X_47=CROSS(SUM(X_45,0),0.5);
        X_48=SUM(X_46,0)*CROSS(COUNT(CLOSE<REF(CLOSE,1),BARSLAST(X_46)[-1]),0.5);

        X_49=SUM(X_47,0)*CROSS(COUNT(CLOSE>REF(CLOSE,1),BARSLAST(X_47)[-1]),0.5);

        X_50=CONST(SUM(IF(X_48,REF(CLOSE,1),0),0));#DRAWNULL=0
        X_51=CONST(SUM(IF(X_49,REF(CLOSE,1),0),0));#DRAWNULL=0

        C=CLOSE

        V1=(C*2+H+L)/4*10;
        V2=EMA(V1,13)-EMA(V1,34);
        V3=EMA(V2,5);
        V4=2*(V2-V3)*5.5;

        dict = {
            "icon_1": int(X_25[-1]),
            'icon_2': int(X_24[-1]),
            'icon_11': int(X_41[-1]),
            'icon_12': int(X_40[-1]),
            'icon_13': int(X_19[-1]),
            'icon_41': int(X_17[-1]),
            'icon_34': int(X_29[-1]),
            'icon_35': int(X_28[-1]),
            'icon_38': int(X_49[-1]),
            'icon_39': int(X_48[-1])
        }
        #主力进WW=IF(V4>=0,V4,0);
        #V11=3*SMA((C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100,5,1)-2*SMA(SMA((C-LLV(L,55))/(HHV(H,55)-LLV(L,55))*100,5,1),3,1);
        #趋势线=EMA(V11,3);
        #见顶清仓=FILTER(np.logical_and(np.logical_and(趋势线>90, 趋势线<REF(趋势线,1)), 主力进WW<REF(主力进WW,1)),8);

        CONST_dict = {'X1':X1_in,'Z1':Z1_in,'X_36':X_36_in,'X_37':X_37_in}
        return dict,CONST_dict
def json_2_ready_json(filtered_name):
    # 现在，filtered_names 列表包含了满足条件的文件名
    data_path_in = '../data/'
    data_path_out='../data_ready/'
    with open(data_path_in+filtered_name, "r") as ff:
        ret = (
                '[["dt", "open", "close", "high", "low", "vol", "cje", "zxj", "Code"],'
                + ff.readline()[:-1]
                + "]"
        )
    with open(data_path_out+filtered_name, "w") as f:
        f.write(ret)
    print(filtered_name,'完成')
def read_ak_and_calc():
    result = ak.stock_us_hist_min_em(symbol="105.TSLA")
    print(result)
    result = result[(result['时间'].str.contains("2024-04-19") & (result['时间'].str[11:13].astype(int) >= 21)) | (
        result['时间'].str.contains("2024-04-20"))]
    print(result)
    open = result['开盘']
    close = result['收盘']
    high = result['最高']
    low = result['最低']
    volme = result['成交量']
    time = result['时间']

    zhicheng = ZhiCheng()
    for i in range(len(open)):
        if i == 0:
            continue
        res = zhicheng.xinhao(close[0:i], low[0:i], high[0:i], volme[0:i])
        if res['b_1'] + res['b_2'] + res['b_3'] + res['b_4'] + res['b_5'] + res['s_1'] + res['s_2'] + res['s_3'] + res[
            's_4'] + res['s_5'] > 0:
            print('time:', np.array(time)[i], res)

def ib_data_calc():
    stock_dict = {'TCEHY': '2006', 'TQQQ': '2001', 'SQQQ': '2002', 'YANG': '2003', 'YINN': '2004', 'QQQ': '2005',
                  'TSLA': '1001', 'MSFT': '1002', 'NVDA': '1003', 'AAPL': '1004', 'AMZN': '1005', 'TSM': '1006',
                  'NFLX': '1007', 'GOOG': '1008',
                  'META': '1009', 'ASML': '1010', 'ARKK': '1011', 'PDD': '1012'}
    # ,'COIN': '1013'}
    stock_dict_invert = {}
    for k, v in stock_dict.items():
        stock_dict_invert[v] = k
    # for code in stock_dict_invert.keys():
    #     raw_json = code + '240421.json'
    #     print('raw_json',raw_json)
    #     json_2_ready_json(raw_json)
    code = '1001'
    with open('./data_ready/' + code + '240421.json', 'r') as f:
        raw_data = json.load(f)
        data = pd.DataFrame(raw_data[1:], columns=raw_data[0])
        result_dianwei = data.iloc[:0].copy()
    for dd in (17, 18, 19):
        result = data[(data['dt'].str.contains("2024-04-" + str(dd)) & (data['dt'].str[11:13].astype(int) >= 21)) | (
                    data['dt'].str.contains("2024-04-" + str(dd + 1)) & (data['dt'].str[11:13].astype(int) <= 3))]
        result = result.reset_index(drop=True)
        open = result['open']
        close = result['close']
        high = result['high']
        low = result['low']
        volme = result['vol']
        time = result['dt']
        zhicheng = ZhiCheng()
        for i in range(len(open)):
            if i == 0:
                continue
            res = zhicheng.xinhao(close[0:i], low[0:i], high[0:i], volme[0:i])
            for k in res.keys():
                result.loc[i, k] = res[k]
            if sum(res.values()) > 0:
                print('time:', np.array(time)[i], res)
                result_dianwei = result_dianwei._append(result.loc[i], ignore_index=True)
    result_dianwei.insert(0, '股票代码', stock_dict_invert[code])
    result_dianwei.to_csv('./data_calc/' + stock_dict_invert[code] + '.csv')

if __name__ == '__main__':
    code = 'NVDA'
    file_name = './data_tdx_tmp/'+'74#'+code+'.txt'
    with open(file_name,'r') as f:
        lines=f.readlines()[2:-1]
        new_lines = []
        for line in lines:
            line = line.strip('\n').split('\t')
            new_line = [line[0].replace('/', '-') + ' ' + line[1][0:2] + ':' + line[1][2:4] + ':00'] + line[2:]
            new_lines.append(new_line)
    column_names = ['dt', 'open', 'high', 'low','close','vol','cje']
    data = pd.DataFrame(new_lines,columns=column_names)
    result_dianwei = data.iloc[:0].copy()

    for dd in [16,17,18]:
        result = data[(data['dt'].str.contains("2024-04-" + str(dd)))]
        result = result.reset_index(drop=True)
        open = result['open'].astype('float')
        close = result['close'].astype('float')
        high = result['high'].astype('float')
        low = result['low'].astype('float')
        volme = result['vol'].astype('float')
        time = result['dt']
        zhicheng = ZhiCheng()
        CONST_dict = {'X1':0,'Z1':0,'X_36':0,'X_37':0}
        for i in range(len(open)):
            if i == 0:
                continue
            res,CONST_dict = zhicheng.xinhao(close[0:i], low[0:i], high[0:i], volme[0:i],CONST_dict)
            for k in res.keys():
                result.loc[i, k] = res[k]
            if sum(res.values()) > 0:
                print('time:', np.array(time)[i], res)
                result_dianwei = result_dianwei._append(result.loc[i], ignore_index=True)
    result_dianwei.insert(0, '股票代码', code)
    result_dianwei.to_csv('./data_tdxtmp_calc/' + code + '.csv')
