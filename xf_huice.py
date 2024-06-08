import os

import pandas as pd
from xf_zhibiao import IndexCalculation
import xgboost as xgb
import numpy as np


def calc_zhibiao(data):
    # data = pd.read_csv('./data_server/DEBUG/20230627.csv',index_col=0)
    ic = IndexCalculation()
    # kdj
    kdj_dict = ic.kdj(data.close, data.low, data.high)
    k = kdj_dict["k"]
    d = kdj_dict["d"]
    j = kdj_dict["j"]

    duanxian_dict = ic.duanxian(data.close, data.low, data.high, 5)
    duanxian = duanxian_dict["duanxian"]

    ema_dict = ic.ema_qushi(data.close)
    pianliEMA = ema_dict["pianliEMA"]
    pianli = ema_dict["pianli"]

    atr_dict = ic.atr(data.close, data.low, data.high)
    atr = atr_dict["atr"]

    obv_dict = ic.obv(data.close, data.vol)
    obv = obv_dict["obv"]
    m5 = obv_dict["m5"]
    m10 = obv_dict["m10"]

    feat_list = [k, d, j, duanxian, pianliEMA, pianli, atr, obv, m5, m10]
    (
        data["k"],
        data["d"],
        data["j"],
        data["duanxian"],
        data["pianliEMA"],
        data["pianli"],
        data["atr"],
        data["obv"],
        data["m5"],
        data["m10"],
    ) = (k, d, j, duanxian, pianliEMA, pianli, atr, obv, m5, m10)
    return data


def calc_train_data(data):
    # data = pd.read_csv('./data_server/DEBUG/20230627.csv', index_col=0)
    data["close_nxt30min"] = data["close"].shift(-30)
    data["close_diff_nxt30min"] = data["close_nxt30min"] - data["close"]
    data["close_diffrate_nxt30min"] = data["close_diff_nxt30min"] / data["close"]
    data["label1"] = data["close_diffrate_nxt30min"] > 0.000
    return data


if __name__ == "__main__":
    # file_atr = './data_server/TQQQ/'
    file_atr = "./data_ready/TQQQ/"
    all_file_names = os.listdir(file_atr)
    data_tr, data_te = "", ""
    for file_name in all_file_names:
        if file_name[0:4] in ("2023"):
            data = pd.read_csv(file_atr + file_name, index_col=0)
            data = calc_zhibiao(calc_train_data(data))
            if data_tr is "":
                data_tr = data
            else:
                data_tr = pd.concat([data_tr, data], ignore_index=True)
        elif file_name[0:4] == "2024":
            data = pd.read_csv(file_atr + file_name, index_col=0)
            data = calc_zhibiao(calc_train_data(data))
            if data_te is "":
                data_te = data
            else:
                data_te = pd.concat([data_te, data], ignore_index=True)

    X_train = data_tr[
        ["close","vol"]
        + ["k", "d", "j", "duanxian", "pianliEMA", "pianli", "atr", "obv", "m5", "m10"]
        # + [
        #     "icon_1",
        #     "icon_2",
        #     "icon_11",
        #     "icon_12",
        #     "icon_13",
        #     "icon_41",
        #     "icon_34",
        #     "icon_35",
        #     "icon_38",
        #     "icon_39",
        #     "jw1",
        #     "jw5",
        #     "jw30",
        # ]
    ]
    y_train = data_tr[["label1"]]

    X_test = data_te[
        ["close","vol"]
        + ["k", "d", "j", "duanxian", "pianliEMA", "pianli", "atr", "obv", "m5", "m10"]
        # + [
        #     "icon_1",
        #     "icon_2",
        #     "icon_11",
        #     "icon_12",
        #     "icon_13",
        #     "icon_41",
        #     "icon_34",
        #     "icon_35",
        #     "icon_38",
        #     "icon_39",
        #     "jw1",
        #     "jw5",
        #     "jw30",
        # ]
    ]
    y_test = data_te[["label1"]]

    param = {
        "max_depth": 4,  # 树的最大深度
        "eta": 0.1,  # 学习率
        "objective": (
            "binary:logistic" if len(np.unique(y_train)) == 2 else "multi:softmax"
        ),  # 目标函数，根据任务调整
        "num_class": (
            len(np.unique(y_train)) if len(np.unique(y_train)) > 2 else None
        ),  # 多分类时的类别数
        "eval_metric": (
            "auc" if len(np.unique(y_train)) == 2 else "mlogloss"
        ),  # 评估指标
    }

    # 转换数据格式为DMatrix，XGBoost的内置数据结构，更高效
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    bst = xgb.train(param, dtrain, num_boost_round=20)
    data_te["predict_score"] = bst.predict(dtest)
    data_te.to_csv("./huice_TQQQ_xf.csv")
    print(1)
    huice_ret = []
    for threshold in np.arange(0, 0.7, 0.1):
        top_buy = data_te[data_te["predict_score"] > threshold].reset_index(drop=True)
        shenglv = (top_buy.close_diffrate_nxt30min > 0).sum() / len(top_buy)
        shouyilv = top_buy.close_diffrate_nxt30min.sum()
        buy_cnt = len(top_buy)
        huice_ret.append([threshold,buy_cnt,shenglv,shouyilv])
        print(
            "阈值：",
            str(threshold),
            "，买入次数：",
            str(buy_cnt),
            "，胜率：",
            str(shenglv),
            "，收益率：",
            str(shouyilv),
        )
    ret=pd.DataFrame(huice_ret,columns=['阈值','买入次数','胜率','收益率'])
    ret.to_csv('huice_param_TQQQ.csv')
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)
    top_buy = data_te[data_te["predict_score"] > 0.5].reset_index(drop=True)
    top_buy['ts_diff'] = top_buy.ts.diff()
    while (top_buy['ts_diff']<1800).any():
        first_occurrence_idx = top_buy[top_buy['ts_diff'] < 1800].index[0]
        print(first_occurrence_idx)
        print(len(top_buy))
        if len(top_buy)<=100:
            print(1)
        top_buy=top_buy.drop(index = first_occurrence_idx)
        top_buy['ts_diff'] = top_buy.ts.diff()
    top_buy.to_csv('./huice_cangwei_TQQQ.csv')
    print(1)
