import pandas as pd
import numpy as np

df = pd.read_csv('./data_tdx_raw/74#TSLA.txt',sep='\t',encoding='gbk',skiprows=1)[:-1]
df.columns=['date','time','open','high','low','close','cjl','vol']

