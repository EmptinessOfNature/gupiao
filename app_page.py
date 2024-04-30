import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import akshare as ak
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_cand_volume(data, dt_breaks):
    # Create subplots and mention plot grid size
    fig = make_subplots(
        rows=1,
        cols=1,
        # row_heights=[1,0.5,0.5,0.5],
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(""),
        row_width=[1,],
    )
    # 绘制k数据
    # fig.add_trace(go.Candlestick(x=data["dt"], open=data["open"], high=data["high"],
    #                              low=data["low"], close=data["close"], name=""),
    #               row=1, col=1
    #               )

    # 走势图
    fig.add_trace(
        go.Scatter(x=data["dt"], y=data["close"], showlegend=True, name="分时图"),
        row=1,
        col=1,
    )

    # # 盆形底买入信号
    # data_new = data[data["XG_IN"] == 1]
    # fig.add_trace(go.Scatter(
    #     x=data_new["dt"],
    #     y=data_new["XG_IN"] * data_new["close"] * 1.01, mode='markers', text='👇', marker={"color": "green"},showlegend=True,name='盆型底'), row=1,
    #     col=1)  # 散点大小
    #
    # data_new2 = data[data["XG_OUT"] * -1 == 1]
    # fig.add_trace(go.Scatter(
    #     x=data_new2["dt"],
    #     y=data_new2["XG_OUT"] * data_new2["close"] * (-0.99), mode='markers', text='^', marker={"color": "red"},showlegend=True,name='盆型顶'), row=1,
    #     col=1)  # 散点大小
    # '''
    # data_nm24 = data[data["icon_2"] == 1]
    # fig.add_trace(
    #     go.Scatter(
    #         x=data_nm24["dt"],
    #         y=data_nm24["icon_2"] * data_nm24["close"] * (1.001),
    #         mode="markers",
    #         text="2",
    #         marker={"color": "red"},
    #         showlegend=True,
    #         name="icon_2",
    #     ),
    #     row=1,
    #     col=1,
    # )  # 散点大小
    #
    # data_nm25 = data[data["icon_1"] == 1]
    # fig.add_trace(
    #     go.Scatter(
    #         x=data_nm25["dt"],
    #         y=data_nm25["icon_1"] * data_nm25["close"] * (1.001),
    #         mode="markers",
    #         text="1",
    #         marker={"color": "green"},
    #         showlegend=True,
    #         name="icon_1",
    #     ),
    #     row=1,
    #     col=1,
    # )  # 散点大小
    # data_nm_dict = {}
    # for icon in (
    #     "icon_11",
    #     "icon_12",
    #     "icon_13",
    #     "icon_34",
    #     "icon_35",
    #     "icon_38",
    #     "icon_39",
    #     "icon_41",
    # ):
    #     data_nm_dict[icon] = data[data[icon] == 1]
    #     fig.add_trace(
    #         go.Scatter(
    #             x=data_nm_dict[icon]["dt"],
    #             y=data_nm_dict[icon][icon] * data_nm_dict[icon]["close"] * (1.001),
    #             mode="markers",
    #             text="2",
    #             marker={"color": "red"},
    #             showlegend=True,
    #             name=icon,
    #         ),
    #         row=1,
    #         col=1,
    #     )  # 散点大小
    #
    # # 绘制成交量数据
    # fig.add_trace(
    #     go.Bar(x=data["dt"], y=data["vol"], showlegend=True, name="成交量"), row=2, col=1
    # )
    #
    # # 绘制策略点5分钟盆型底
    # fig.add_trace(
    #     go.Scatter(x=data["dt"], y=data["JW_30"], showlegend=True, name="JW_30"),
    #     row=3,
    #     col=1,
    # )
    #
    # fig.add_trace(
    #     go.Scatter(x=data["dt"], y=data["JW_5"], showlegend=True, name="JW_5"),
    #     row=3,
    #     col=1,
    # )
    # fig.update_yaxes(range=[-10, 110], row=3, col=1)
    #
    #
    # fig.add_trace(go.Bar(x=data["dt"], y=[1]*data.shape[0],marker=dict(color=data["DING_30min"]),showlegend=False,name='5min盆型'), row=4, col=1)
    # # fig.add_trace(go.Bar(x=data["dt"], y=[data["XG_5min"],data["XG_30min"]], showlegend=False), row=3, col=1)
    #
    # # fig.add_trace(go.Bar(x=data["dt"], y=data["XG_30min"],marker=dict(color=data["XG_30min"]), showlegend=False), row=4, col=1)
    # fig.add_trace(go.Bar(x=data["dt"], y=[1]*data.shape[0], marker=dict(color=data["DI_30min"]),showlegend=False,name='30min盆型'),
    #               row=5, col=1)
    # '''
    # 绘制策略点

    # fig.add_trace(
    #     go.Scatter(x=data["dt"], y=data["JW"], showlegend=True,name='5min盆型曲线'), row=5, col=1
    # )

    fig.update_yaxes(
        showline=True,
        linecolor="black",
        linewidth=1,
        gridwidth=1,
        title={"font": {"size": 18}, "text": "", "standoff": 10},
        automargin=True,
    )

    # fig.update_xaxes(
    #     title_text='dt',
    #     rangeslider_visible=True,  # 下方滑动条缩放
    #     rangeselector=dict(
    #         # 增加固定范围选择
    #         buttons=list([
    #             dict(count=1, label='1M', step='month', stepmode='backward'),
    #             dict(count=6, label='6M', step='month', stepmode='backward'),
    #             dict(count=1, label='1Y', step='year', stepmode='backward'),
    #             dict(count=1, label='YTD', step='year', stepmode='todate'),
    #             dict(step='all')])))

    # # Do not show OHLC's rangeslider plot
    # fig.update(layout_xaxis_rangeslider_visible=False)
    # # 去除休市的日期，保持连续
    # fig.update_xaxes(tickformat = "%Y-%m-%d %H:%M:%S" ,rangebreaks=[dict(values=dt_breaks)])

    # fig.update_xaxes(tickformat = "%Y-%m-%d %H:%M:%S" ,rangebreaks=[dict(values=dt_breaks)])
    # fig.update_xaxes(tickformat = "%Y-%m-%d %H:%M:%S",rangebreaks=[dict(values=["2023-08-17 13:50:00"])])
    # A股break时间
    # fig.update_xaxes(tickformat="%Y-%m-%d %H:%M:%S", rangebreaks=[dict(bounds=[11.5, 13], pattern="hour"),dict(bounds=[15, 9.5], pattern="hour"),dict(bounds=[6,1], pattern="day of week")])

    fig.update_xaxes(
        tickformat="%Y-%m-%d %H:%M:%S",
        rangebreaks=[
            # dict(bounds=[8, 16], pattern="hour"),
            dict(bounds=[4, 21.5], pattern="hour"),
            dict(bounds=["sat", "sun"]),
        ],
    )
    hovertext = []  # 添加悬停信息

    for i in range(len(data["close"])):  # <br>表示
        hovertext.append(
            "时间: " + str(data["dt"][i]) + "<br>价格: " + str(data["close"][i])
        )

    fig.update_layout(hovermode="x unified")

    return fig
# 设置Streamlit页面标题
st.title('股票分时图展示')

# 获取用户输入的股票代码
ticker_symbol = st.text_input('请输入股票代码:', '105.TSLA')

# 使用yfinance获取股票数据
if st.button('获取数据'):
    try:
        stock = ak.stock_us_hist_min_em(symbol=ticker_symbol)
        hist = ak.stock_us_hist_min_em(symbol=ticker_symbol)
        hist.columns=['dt','open','close','high','low','vol','cje','zxj']
        hist.dt=pd.to_datetime(hist.dt)
        print(hist)
        fig = plot_cand_volume(hist,'')
        st.write(f'获取到 {ticker_symbol} 的数据')
    except Exception as e:
        st.error(f'无法获取 {ticker_symbol} 的数据: {e}')
        hist = None

    # 如果成功获取到数据，绘制并展示分时图
if fig is not None:
    st.plotly_chart(fig)




