import dash
from dash import Dash, dcc, html, Input, Output, callback

import yfinance as yf
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta, date
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.patches as patches
from matplotlib.colors import TwoSlopeNorm
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from operator import itemgetter
from mapping_plot_attributes import *
from mapping_tickers import *
from utils import *
from download_data import DownloadData
from analyze_prices import AnalyzePrices


tickers = list(magnificent_7_tickers.keys())
print(tickers)
print(tripledeck_legendtitle)

tk = 'MSFT'
drawdown_color = 'red'
theme = 'dark'

app = dash.Dash(__name__)

def create_graph(tk, drawdown_color, theme):

    end_date = datetime.today()
    hist_years, hist_months, hist_days = 1, 0, 0
    start_date = datetime(end_date.year - hist_years, end_date.month - hist_months, end_date.day - hist_days)
    tk_market = '^GSPC'

    hist_data = DownloadData(end_date, start_date, tickers, tk_market)

    downloaded_data = hist_data.download_yh_data(start_date, end_date, tickers, tk_market)
    df_adj_close = downloaded_data['Adj Close']
    df_close = downloaded_data['Close']
    df_volume = downloaded_data['Volume']
    dict_ohlc = downloaded_data['OHLC']

    df_ohlc = dict_ohlc[tk]
    ohlc_tk = df_ohlc.copy()
    adj_close_tk = df_adj_close[tk]
    close_tk = df_close[tk]
    open_tk = ohlc_tk['Open']
    high_tk = ohlc_tk['High']
    low_tk = ohlc_tk['Low']
    volume_tk = df_volume[tk]

    analyze_prices = AnalyzePrices(end_date, start_date, [tk])
    date_index = ohlc_tk.index

    n_top = 5
    sort_by = ['Total Length', '% Drawdown']
    # sort_by = '% Drawdown'
    # sort_by = 'Peak Date'
    drawdown_data = analyze_prices.summarize_tk_drawdowns(df_adj_close, tk, sort_by, n_top)

    ma_envelope_list = analyze_prices.ma_envelopes(close_tk, window = 20, prc_offset = 5, n_bands = 2)

    ma_ribbon = analyze_prices.get_ma_ribbon(ma_type = 'sma', ma_window = 10, n_ma = 6)

    bollinger_data = analyze_prices.bollinger_bands(close_tk, window = 20, n_std = 2, n_bands = 3)
    # bollinger_data = bollinger_bands(close_tk, window = 20, n_std = 2, n_bands = 3)
    bollinger_list = bollinger_data['list']

    mvol_data = analyze_prices.moving_volatility(close_tk, window = 10)

    stochastic_data = analyze_prices.stochastic_oscillator(close_tk, high_tk, low_tk)

    atr_data = analyze_prices.average_true_rate(close_tk, high_tk, low_tk, n = 10)

    rsi_data = analyze_prices.relative_strength(close_tk)

    ##################################

    deck_type = 'triple'
    # deck_type = 'double'
    # deck_type = 'single'

    # theme = 'dark'
    # theme = 'light'
    color_theme = 'magenta'
    # color_theme = 'tableau'
    color_theme_2 = 'sapphire'
    color_theme_vol = 'rainbow'
    color_theme_vol_2 = 'sapphire'

    fig_data = analyze_prices.create_template(
    # fig_data = create_template(    
        date_index,
        deck_type = deck_type,
        secondary_y = False,
        # secondary_y = True,
        # plot_width = 1450,
        plot_width = 1450,
        plot_height_1 = 600,
        plot_height_2 = 150,
        plot_height_3 = 150,
        theme = theme
    )
    ##### NOTE: Decks need to get populated from top to bottom, i.e. from 1 to 3, otherwise the legends will end up in the wrong order

    # fig_data = analyze_prices.add_candlestick(fig_data, ohlc_tk, tk, candle_type = 'traditional', target_deck = 1, theme = theme)
    # fig_data = add_candlestick(fig_data, ohlc_tk, tk, candle_type = 'hollow', target_deck = 1, theme = theme)

    # fig_data = add_diff_stochastic(fig_data, tk, stochastic_data, target_deck = 1, reverse_diff = False, add_signal = True, signal_window = 5, add_title = True)
    # fig_data = add_diff(fig_data, tk, diff_data_stochastic, price_type_map, target_deck = 2, add_title = True)
    
    fig_data = analyze_prices.add_drawdowns(
        fig_data,
        close_tk,
        tk,
        drawdown_data,
        n_top_drawdowns = 5,
        target_deck = 1,
        add_price = True,
        # add_price = False,
        price_type = 'close',
        top_by = 'depth',
        show_trough_to_recovery = True,
        add_title = True,
        theme = theme,
        # color_theme = 'base'
        price_color_theme = 'magenta',
        drawdown_color = drawdown_color
    )
    
    fig_data = analyze_prices.add_hist_price(fig_data, volume_tk, tk, target_deck = 2, secondary_y = False, plot_type = 'bar', add_title = False, price_type = 'volume', theme = theme)
    # fig_data = analyze_prices.add_hist_price(fig_data, close_tk, tk, target_deck = 1, add_title = False, price_type = 'close', theme = theme)
    # fig_data = analyze_prices.add_price_overlays(fig_data, price_list, tk, target_deck = 1, theme = theme, color_theme = 'turquoise')
    
    # fig_data = add_ma_overlays(fig_data, close_tk, ema_list[: 6], target_deck = 1, theme = theme, color_theme = color_theme)
    # fig_data = analyze_prices.add_ma_overlays(fig_data, close_tk, ma_ribbon, target_deck = 1, theme = theme, color_theme = 'grasslands')
    fig_data = analyze_prices.add_ma_overlays(fig_data, close_tk, ma_ribbon, target_deck = 1, theme = theme, color_theme = 'silver')
    
    fig_data = analyze_prices.add_bollinger_overlays(fig_data, bollinger_list, target_deck = 1, theme = theme, color_theme = 'sapphire')
    """
    fig_data = analyze_prices.add_bollinger_width(
    # fig_data = add_bollinger_width(    
        fig_data,
        bollinger_data,
        # bollinger_type = '%B',
        bollinger_type = 'width',
        target_deck = 2,
        secondary_y = False,
        add_yaxis_title = True,
        yaxis_title = None,
        theme = theme,
        color_theme = 'magenta'
    )
    fig_data = analyze_prices.add_mvol(    
        fig_data,
        mvol_data,
        mvol_type = 'std',
        target_deck = 2,
        secondary_y = False,
        add_yaxis_title = True,
        yaxis_title = None,
        theme = theme,
        color_theme = 'lavender'
    )
    """
    fig_data = analyze_prices.add_diff_stochastic(fig_data, tk, stochastic_data, target_deck = 3, reverse_diff = False, add_signal = True, signal_window = 7, add_title = False, theme = theme)
    
    fig = fig_data['fig']
    print(fig_data['y_min'])
    print(fig_data['y_max'])
    # layout = fig['layout']
    # output_text = f'This is a {deck_type}-deck plot'

    fig_div = html.Div(
            # [dcc.Graph(id='linlogplot', figure=fig, config=_config)],
            [dcc.Graph(id='test-graph', figure = fig)],
            id='fig_div',
        )

    # return output_text, fig

    return fig_div


#################

app.layout = html.Div(children = [

    # html.H1(children='Hello Dash'),
    # html.Script(src="https://cdn.plot.ly/plotly-latest.min.js"),
    html.Div(
    [
        dcc.Dropdown(
            id='tickers-dropdown',
            options = tickers,
            value = 'MSFT',
            style = {'width': '100px'}
        )
    # html.Div(id='graphDiv'),
    # create_graph(tk, drawdown_color),
    #html.Div(children = [dcc.Graph(id = 'test-graph', figure = {})])
    ],
    style={
        "display": "inline-block",
        # "margin-top": "10px",
        # "margin-left": "10px",
        "verticalAlign": "middle",
        "font-family": "Helvetica"
    }),

    html.Div(
    [
        dcc.Dropdown(
            id='drawdowns-dropdown',
            options = ['yellow', 'orange', 'blue', 'purple', 'silver', 'red', 'green'],
            value = 'red',
            style = {'width': '100px'}
        ),
        # html.Div(id = 'dd-output-container', children = []),

        # html.Div(id='graphDiv'),
        # create_graph(tk, drawdown_color),
        #html.Div(children = [dcc.Graph(id = 'test-graph', figure = {})])
    ],
    style={
        "display": "inline-block",
        # "margin-top": "10px",
        # "margin-left": "10px",
        "verticalAlign": "middle",
        "font-family": "Helvetica"
    }),

    html.Div(
    [
        dcc.Dropdown(
            id='theme-dropdown',
            options = ['dark', 'light'],
            value = 'dark',
            style = {'width': '100px'}
        ),
        # html.Div(id = 'dd-output-container', children = []),

        # html.Div(id='graphDiv'),
        # create_graph(tk, drawdown_color),
        #html.Div(children = [dcc.Graph(id = 'test-graph', figure = {})])
    ],
    style={
        "display": "inline-block",
        # "margin-top": "10px",
        # "margin-left": "10px",
        "verticalAlign": "middle",
        "font-family": "Helvetica"
    }),

    create_graph(tk, drawdown_color, theme)
])

@app.callback(
    # Output(component_id = 'dd-output-container', component_property = 'children'),
    # Output(component_id = 'test-graph', component_property = 'figure'),
    Output(component_id = 'fig_div', component_property = 'children'),
    Input(component_id = 'tickers-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-dropdown', component_property = 'value'),
    Input(component_id = 'theme-dropdown', component_property = 'value')
)
def update_graph(tk, drawdown_color, theme):
    return create_graph(tk, drawdown_color, theme)

# app.layout = html.Div(children=[
#    dcc.Graph(
#        id='example-graph',
#        figure = fig
#    )
# ])


# dcc.Graph(figure=fig)

# fig.show()

# fig.update_layout(hovermode='x')

# fig.show()

# plotly_chart(fig)

# print(fig_data['overlays'])

# fig_data = analyze_prices.update_color_theme(fig_data, theme, new_color_theme = 'gold', invert = False, overlay_name = 'OV2')
# fig_data = update_color_theme(fig_data, theme, new_color_theme = 'sapphire',  invert = False, overlay_name = 'OV2')
# fig_data['fig'].show()
# print(fig_data['overlays'])

if __name__ == '__main__':
    app.run_server(debug=True)
