# -*- coding: utf-8 -*-

from MyTT import *
import numpy as np
# import talib as ta
class IndexCalculation():
    #短线操盘 日线
    def duanxian(self, CLOSE, LOW, HIGH, 周期):
        try:
            C=np.array(CLOSE)
            L=np.array(LOW)
            H=np.array(HIGH)
            N=周期;
            M=35;
            B1=(HHV(H,N)-C)/(HHV(H,N)-LLV(L,N))*100- M;
            B2=SMA(B1,N,1)+100;
            B3=(C-LLV(L,N))/(HHV(H,N)- LLV(L,N))*100;
            B4=SMA(B3,3,1);
            B5=SMA(B4,3,1)+100;
            R6=B5-B2;
            dict = {'duanxian':R6.tolist()}
            return dict
        except:
            print('短线操盘error')

    #ema判断趋势
    def ema_qushi(self, C):
        try :
            M5=EMA(C,5);
            M10=EMA(C,10);
            M20=EMA(C,20);
            M30=EMA(C,30);
            偏离=-((M30-M20)+(M30-M10)+(M30-M5)+(M20-M10)+(M20-M5)+(M10-M5))/M30
            偏离MA5=EMA(偏离,5)
            dict={'pianliEMA': 偏离MA5.tolist(), 'pianli': 偏离.tolist()}
            return dict
        except:
            print("ema指标计算异常")

    def kdj(self, CLOSE, LOW, HIGH):
        N1=45;
        M1=15;
        M2=15;
        RSV=(CLOSE-LLV(LOW,N1))/(HHV(HIGH,N1)-LLV(LOW,N1))*100;
        K=SMA(RSV,M1,1);
        D=SMA(K,M2,1);
        J=3*K-2*D;
        dict={"k":K.tolist(), "d":D.tolist(), "j":J.tolist()}
        return dict

    def atr(self, C, L, H):
        try :
            C=np.array(C)
            L=np.array(L)
            H=np.array(H)
            MTR=MAX(MAX((H-L),ABS(REF(C,1)-H)),ABS(REF(C,1)-L));
            ATR=MA(MTR,14);
            dict={"atr":ATR.tolist()}
            return dict
        except:
            print("atr 计算失败")

    def obv(self, C, V):
        try :

            C=np.array(C)
            V=np.array(V)
            VP=V;

            VA=IF(C>REF(C,1),VP,-VP);
            OBV=SUM(VA,0)

            M5=EMA(OBV,5)
            M10=EMA(OBV,50)
            dict={"obv":OBV.tolist(), "m5":M5.tolist(), "m10":M10.tolist()}
            return dict
        except:
            print("obv 计算失败")


