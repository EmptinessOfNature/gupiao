import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

def parse_tdx_rawdata_1d(r_path,code,w_path='./data_server/'):
    df=pd.read_csv(r_path,sep='\t',skiprows=1,encoding='gbk')[:-1]
    df.columns=['date','time','open','high','low','close','vol','cje']
    df['time']=df['time'].astype(int).astype(str).str.zfill(4)
    df['date']=df['date'].str.replace('/','-')
    df['vol'] = df['vol'].astype(int)
    df['tdx_dt'] = df['date'].str[:] + ' ' + df['time'].str[0:2]+':'+df['time'].str[2:4]+':00'

    ret = df[['tdx_dt','open','close','high','low','vol']]
    ret['dt']=pd.to_datetime(ret['tdx_dt'])
    def add_day_if_before_11(time):
        if time.hour <= 11:
            return time + pd.Timedelta(days=1)
        return time

    ret["dt"] = ret['dt'].apply(add_day_if_before_11)
    data = ret[['dt','open','close','high','low','vol']]

    date_list = sorted(data["dt"].dt.date.unique())
    for i in range(max(len(date_list) - 1, 1)):  # 遍历所有输入data中的每个日期
        date_1d = str(date_list[i])
        date_1d_add1 = str(date_list[i + 1])
        data.dt = data.dt.astype("str")
        data_1d = data[
            (
                    data["dt"].str.contains(date_1d)
                    & (data["dt"].str[11:13].astype(int) >= 20)
            )
            | (
                    data["dt"].str.contains(date_1d_add1)
                    & (data["dt"].str[11:13].astype(int) <= 4)
            )
            ]
        data_1d = data_1d.reset_index(drop=True)
        path_to_save = w_path+code+date_1d.replace('-','')+'.csv'
        data_1d.to_csv(path_to_save)
        print(path_to_save,'保存完成')

if __name__=="__main__":
    parse_tdx_rawdata_1d(r_path='./data_tdx_raw/74#TSLA.txt',code='TSLA',w_path ='./data_server/' )