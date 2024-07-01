import pandas as pd
import os

f_path = './data_ready/'
code = 'NVDA'
csvs = sorted(os.listdir(f_path+code))
csvs = [f_path+code+'/'+p for p in csvs]
for csv in csvs:
    data = pd.read_csv(csv)

    icon_buy = (
            (
                    data["icon_1"].fillna(0)
                    + data["icon_38"].fillna(0)
                    + data["icon_34"].fillna(0)
                    + data["icon_13"].fillna(0)
                    + data["icon_11"].fillna(0)
            )
            >= 1
    ).astype(int)
    icon_jw_bottom = (
            ((data["jw5"] < 20).astype(int) + (data["jw30"] < 20).astype(int)) >= 2
    ).astype(int)
    icon_sell = (
            (
                    data["icon_2"].fillna(0)
                    + data["icon_39"].fillna(0)
                    + data["icon_35"].fillna(0)
                    + data["icon_12"].fillna(0)
                    + data["icon_41"].fillna(0)
            )
            >= 1
    ).astype(int)
    icon_jw_top = (
            ((data["jw5"] > 80).astype(int) + (data["jw30"] > 80).astype(int)) >= 2
    ).astype(int)

    data['buy_signal'] = icon_jw_bottom*icon_buy
    data['sell_signal'] = icon_sell

    # if(icon_jw_bottom*icon_buy).sum()>0:
    #     print(csv,'出现jw底部且买点')
        # print(data[data['buy_signal']>0])
    data['chicang']=0
    meiri_cash = 100000
    for i in range(len(data)):
        if i==0:
            data.loc[i,'cash']=meiri_cash
        elif i==390-3:
            data.loc[i,'cash']=data.loc[i-1,'cash']+data.loc[i-1,'chicang']*data.loc[i,'open']
            data.loc[i,'chicang']=0
        elif data.loc[i,'buy_signal']==1:
            if data.loc[i,'cash']>=data.loc[i,'open']*3:
                data.loc[i,'chicang']=meiri_cash//3//data.loc[i,'open']
                data.loc[i,'cash'] = data.loc[i-1,'cash']-(meiri_cash//3//data.loc[i,'open'])*data.loc[i,'open']

print(1)
