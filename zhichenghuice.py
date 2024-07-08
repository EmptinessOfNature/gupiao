import pandas as pd
import os



def huice_1d(data,first_cash):
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
    icon_jw5_30_bottom = (
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
    icon_jw5_30_top = (
            ((data["jw5"] > 80).astype(int) + (data["jw30"] > 80).astype(int)) >= 2
    ).astype(int)

    data['buy_signal'] = icon_jw5_30_bottom * icon_buy
    data['sell_signal'] = icon_sell

    for i in range(len(data)):
        if i==0:
            act_init_1d(data,i,first_cash)
            sell_no_mod_2 = 0
        else:
            act_init_1line(data,i)
        if data.loc[i,'buy_signal']==1:
            act_buy(data,i,first_cash)
            print(1)
        if data.loc[i,'sell_signal']==1:
            if sell_no_mod_2==0:
                act_sell_1half(data,i)
                print(1)
            else:
                act_sell_2half()
            sell_no_mod_2 = 1 - sell_no_mod_2
        if i==390-3:
            act_sell_2half()

def act_sell_1half(data,i):
    all_chicang = data.loc[i,'chicang'].split(';')[0:-1]
    chicang_prices = [float(j.split(':')[0]) for j in all_chicang]
    chicang_nums = [float(j.split(':')[1]) for j in all_chicang]
    sell_nums = [(float(j)/2).__ceil__() for j in chicang_nums]
    sell_cash = 0
    profit = 0
    for j in range(len(all_chicang)):
        data.loc[i,'sell_detail'] += str(data.loc[i,'open'])+':'+str(sell_nums[j]) +';'
        sell_cash += data.loc[i,'open'] * sell_nums[j]
        data.loc[i, 'chicang'] = str(chicang_prices[j]) + ':' + str(chicang_nums[j]-sell_nums[j]) + ';'
        profit += (data.loc[i,'open'] - chicang_prices[j]) * sell_nums[j]
    data.loc[i, 'cash'] = data.loc[i, 'cash']+sell_cash
    data.loc[i, 'profit'] = profit


def act_sell_2half():
    all_chicang = data.loc[i, 'chicang'].split(';')
def act_buy(data,i,first_cash):
    buy_amt = first_cash//2//data.loc[i,'open']
    data.loc[i, 'cash'] =  data.loc[i,'cash'] - buy_amt*data.loc[i,'open']
    data.loc[i,'chicang']+= str(data.loc[i,'open'])+':'+str(buy_amt) +';'
    data.loc[i,'buy_detail']+= str(data.loc[i,'open'])+':'+str(buy_amt) +';'


def act_init_1d(data,i,first_cash):
    data.loc[i,'cash']=first_cash
    data.loc[i,'chicang']=""
    data.loc[i,'buy_detail'] = ""
    data.loc[i,'sell_detail']= ""
    data.loc[i,'profit']=0

def act_init_1line(data,i):
    data.loc[i,'cash']=data.loc[i-1,'cash']
    data.loc[i,'chicang']=data.loc[i-1,'chicang']
    data.loc[i,'buy_detail'] = ""
    data.loc[i,'sell_detail']= ""
    data.loc[i,'profit']=0

if __name__=='__main__':
    f_path = './data_ready/'
    code = 'NVDA'
    csvs = sorted(os.listdir(f_path + code))
    csvs = [f_path + code + '/' + p for p in csvs]
    data = pd.read_csv(csvs[10],index_col=0)
    huice_1d(data,100000)
#
# for csv in csvs:
#     data = pd.read_csv(csv)
#
#     icon_buy = (
#             (
#                     data["icon_1"].fillna(0)
#                     + data["icon_38"].fillna(0)
#                     + data["icon_34"].fillna(0)
#                     + data["icon_13"].fillna(0)
#                     + data["icon_11"].fillna(0)
#             )
#             >= 1
#     ).astype(int)
#     icon_jw_bottom = (
#             ((data["jw5"] < 20).astype(int) + (data["jw30"] < 20).astype(int)) >= 2
#     ).astype(int)
#     icon_sell = (
#             (
#                     data["icon_2"].fillna(0)
#                     + data["icon_39"].fillna(0)
#                     + data["icon_35"].fillna(0)
#                     + data["icon_12"].fillna(0)
#                     + data["icon_41"].fillna(0)
#             )
#             >= 1
#     ).astype(int)
#     icon_jw_top = (
#             ((data["jw5"] > 80).astype(int) + (data["jw30"] > 80).astype(int)) >= 2
#     ).astype(int)
#
#     data['buy_signal'] = icon_jw_bottom*icon_buy
#     data['sell_signal'] = icon_sell
#
#     # if(icon_jw_bottom*icon_buy).sum()>0:
#     #     print(csv,'出现jw底部且买点')
#         # print(data[data['buy_signal']>0])
#     data['chicang']=0
#     meiri_cash = 100000
#     for i in range(len(data)):
#         if i==0:
#             data.loc[i,'cash']=meiri_cash
#         elif i==390-3:
#             data.loc[i,'cash']=data.loc[i-1,'cash']+data.loc[i-1,'chicang']*data.loc[i,'open']
#             data.loc[i,'chicang']=0
#         elif data.loc[i,'buy_signal']==1:
#             if data.loc[i,'cash']>=data.loc[i,'open']*3:
#                 data.loc[i,'chicang']=meiri_cash//3//data.loc[i,'open']
#                 data.loc[i,'cash'] = data.loc[i-1,'cash']-(meiri_cash//3//data.loc[i,'open'])*data.loc[i,'open']

print(1)
