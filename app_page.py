import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import akshare as ak
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from buy_sell_point import ZhiCheng
import datetime

# from ib_req import get_data_ib


def plot_cand_volume(data, dt_breaks):
    # Create subplots and mention plot grid size
    fig = make_subplots(
        rows=3,
        cols=1,
        # row_heights=[1,0.5,0.5,0.5],
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(""),
        row_width=[1, 1,2],
    )
    fig.update_layout(
        width=1000,  # 设置宽度为1000像素
        height=600  # 设置高度为600像素
    )

    # 走势图
    fig.add_trace(
        go.Scatter(
            x=data["dt"],
            y=data["close"],
            # marker=dict(
            # symbol=icons[icon]['symbol'],  # 使用自定义符号
            # size=icons[icon]['size'],  # 可调整符号大小
            # color='#0000FF',  # 设置颜色
            # ),
            showlegend=True,
            name="分时图",
        ),
        row=1,
        col=1,
    )
    # import base64
    # path = './res/xiajian1.png'
    # with open(path, "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    # b64_icon =encoded_string

    icons = {
        "icon_1": {"symbol": "triangle-up", "size": 10, "color": "#00FF00"},
        "icon_2": {"symbol": "triangle-down", "size": 10, "color": "#AA0000"},
        "icon_11": {"symbol": "triangle-up-open", "size": 10, "color": "#00FF00"},
        "icon_12": {"symbol": "triangle-down", "size": 10, "color": "red"},
        "icon_13": {"symbol": "triangle-up-dot", "size": 10, "color": "#00FF00"},
        "icon_41": {"symbol": "triangle-down", "size": 10, "color": "red"},
        "icon_34": {"symbol": "triangle-up-open-dot", "size": 10, "color": "#00FF00"},
        "icon_35": {"symbol": "triangle-down", "size": 10, "color": "#FF0000"},
        "icon_38": {"symbol": "triangle-up", "size": 10, "color": "#00AA00"},
        "icon_39": {"symbol": "triangle-down", "size": 10, "color": "red"},
    }
    for icon in icons.keys():
        fig.add_trace(
            go.Scatter(
                x=data["dt"],
                y=data[icon] * (data["close"] - 0.1),
                showlegend=True,
                mode="markers",
                marker=dict(
                    symbol=icons[icon]["symbol"],  # 使用自定义符号
                    size=icons[icon]["size"],  # 可调整符号大小
                    color=icons[icon]["color"],  # 设置颜色
                ),
                name=icon,
            ),
            row=1,
            col=1,
        )

    # # 盆形底JW5分钟信号图
    # data_new = data[data["XG_IN"] == 1]
    fig.add_trace(
        go.Scatter(
            x=data["dt"],
            y=data["jw5"],
            marker={"color": "black"},
            showlegend=True,
            name="JW5",
        ),
        row=2,
        col=1,
    )
    # 绘制阴影
    for i in range(len(data.dt)):
        if data.jw5[i] >= 100 and i % 5 == 0:
            fig.add_trace(
                go.Scatter(
                    x=[data.dt[i], data.dt[i]],
                    y=[100, data.jw5[i] - 0.01],
                    mode="lines",
                    marker={"color": "red"},
                    showlegend=False,
                    hoverinfo="skip",
                    name="JW5",
                ),
                row=2,
                col=1,
            )
        if data.jw5[i] < 0 and i % 5 == 0:
            fig.add_trace(
                go.Scatter(
                    x=[data.dt[i], data.dt[i]],
                    y=[0, data.jw5[i] - 0.01],
                    mode="lines",
                    marker={"color": "green"},
                    showlegend=False,
                    hoverinfo="skip",
                    name="JW5",
                ),
                row=2,
                col=1,
            )
    # 30分钟jw线
    fig.add_trace(
        go.Scatter(
            x=data["dt"],
            y=data["jw30"],
            marker={"color": "black"},
            showlegend=True,
            name="JW30",
        ),
        row=3,
        col=1,
    )
    # 绘制阴影
    for i in range(len(data.dt)):
        if data.jw30[i] >= 100 and i % 5 == 0:
            fig.add_trace(
                go.Scatter(
                    x=[data.dt[i], data.dt[i]],
                    y=[100, data.jw30[i] - 0.01],
                    mode="lines",
                    marker={"color": "red"},
                    showlegend=False,
                    hoverinfo="skip",
                    name="JW30",
                ),
                row=3,
                col=1,
            )
        if data.jw30[i] < 0 and i % 5 == 0:
            fig.add_trace(
                go.Scatter(
                    x=[data.dt[i], data.dt[i]],
                    y=[0, data.jw30[i] - 0.01],
                    mode="lines",
                    marker={"color": "green"},
                    showlegend=False,
                    hoverinfo="skip",
                    name="JW30",
                ),
                row=3,
                col=1,
            )

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
        # tickformat="%Y-%m-%d %H:%M:%S",
        tickformat="%m-%d %H:%M",
        showgrid=True,
        rangebreaks=[
            # dict(bounds=[8, 16], pattern="hour"),
            dict(bounds=[4, 21.5], pattern="hour"),
            dict(bounds=[6, 1], pattern="day of week"),
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

def plot_kline(data, dt_breaks):
    fig = make_subplots(
        rows=1,
        cols=1,
        # row_heights=[1,0.5,0.5,0.5],
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(""),
        row_width=[1],
    )
    # k线图
    fig.add_trace(go.Candlestick(x=data["dt"], open=data["open"], high=data["high"],
                    low=data["low"], close=data["close"], name=""),
                    row=1, col=1)
    fig.update_yaxes(
        showline=True,
        linecolor="black",
        linewidth=1,
        gridwidth=1,
        title={"font": {"size": 18}, "text": "", "standoff": 10},
        automargin=True,
    )
    fig.update_xaxes(
        # tickformat="%Y-%m-%d %H:%M:%S",
        tickformat="%m-%d %H:%M",
        showgrid=True,
        rangebreaks=[
            # dict(bounds=[8, 16], pattern="hour"),
            dict(bounds=[4, 21.5], pattern="hour"),
            dict(bounds=[6, 1], pattern="day of week"),
            dict(bounds=["sat", "sun"]),
        ],
    )

    return fig

def parse_req_list(code,s_date):
    # 定义起始和终止日期
    start_date = s_date.strftime("%Y-%m-%d")
    end_date =datetime.datetime.now().strftime("%Y-%m-%d")
    # 使用pandas的date_range生成日期序列
    date_range = pd.date_range(start=start_date, end=end_date, inclusive='both')
    ret = []
    for d in date_range:
        ret.append(code+'/'+d.strftime("%Y%m%d")+'.csv')
    return ret

# 设置Streamlit页面标题
fig = None
st.title("NB666NB")

# 获取用户输入的股票代码
# ticker_symbol = st.text_input("请输入股票代码:", "105.TSLA")

skt_options = ["TSLA", "MSFT", "NVDA", "其他"]

# 使用st.selectbox创建下拉选择菜单
selected_option = st.selectbox("请选择一个选项:", skt_options)
s_date = st.date_input("展示起始时间")
req_data_list = parse_req_list(selected_option,s_date)
st.write("你选择了:", selected_option,";展示起始时间:", s_date,"请求数据",req_data_list)


code_symbols = {"TSLA": "105.TSLA", "MSFT": "105.MSFT", "NVDA": "105.NVDA"}

# 使用yfinance获取股票数据
if st.button("获取数据"):
    try:
        hist = ak.stock_us_hist_min_em(symbol=code_symbols[selected_option])
        hist.columns = ["dt", "open", "close", "high", "low", "vol", "cje", "zxj"]
        print(hist)
        # hist = get_data_ib()
        # print(hist)
        zhicheng = ZhiCheng()
        hist = zhicheng.calc_point(hist, date_mode="ib")
        hist2 = zhicheng.calc_point_2_jw_1(hist)
        fig = plot_cand_volume(hist2, "")
        fig_kline = plot_kline(hist,"")
        st.write(f"获取到 {code_symbols[selected_option]} 的数据")
    except Exception as e:
        st.error(f"无法获取 {code_symbols[selected_option]} 的数据: {e}")
        hist2 = None

    # 如果成功获取到数据，绘制并展示分时图
if fig is not None:
    # 自定义CSS来尝试实现全屏和居中
    custom_css = """
    body {
        margin: 0;
        padding: 0;
        overflow-x: hidden; /* 防止水平滚动条 */
        display: flex;
        justify-content: center; /* 水平居中 */
        align-items: center; /* 垂直居中 */
        min-height: 100vh; /* 设置最小高度为视口高度，接近全屏 */
    }
    .stApp {
        max-width: 150%;
    }
    """

    # 应用CSS
    st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.plotly_chart(fig_kline)
