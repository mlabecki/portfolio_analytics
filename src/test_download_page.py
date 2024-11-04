import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

import yfinance as yf
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta, date
import time
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from operator import itemgetter
from mapping_plot_attributes import *
from mapping_tickers import *
from utils import *
from download_data import DownloadData
from analyze_prices import AnalyzePrices

end_date = datetime.today()
hist_years, hist_months, hist_days = 1, 0, 0
start_date = datetime(end_date.year - hist_years, end_date.month - hist_months, end_date.day - hist_days)

hist_data = DownloadData(end_date, start_date)

# tk_market = '^GSPC'
tk_market = 'BTC-USD'

df = pd.DataFrame()
max_tickers = 10

# Ticker categories:
# 'nasdaq100', 'sp500', 'dow_jones', 'biggest_companies',
# 'biggest_etfs', 'crypto_etfs', 'cryptos_yf', 'cryptos', 'futures'

# df = hist_data.download_from_url('sp500', max_tickers)
# df = hist_data.download_from_url('futures', max_tickers)
# df = hist_data.download_from_url('cryptos', max_tickers)
# df = hist_data.download_from_url('biggest_etfs', max_tickers)
# df = hist_data.download_from_url('biggest_companies', max_tickers)

df = hist_data.download_from_url('cryptos_yf', max_tickers)
tickers = list(df['Symbol'])

# tickers = ['BTC-USD', 'USDS33039-USD', 'RENDER-USD', 'ETH-USD', 'SOLVBTC-USD', 'CBBTC32994-USD', 'XRP-USD']
# 
# # tickers = ['BTC-USD', 'ETH-USD', 'USDT-USD', 'BNB-USD', 'SOL-USD', 'USDC-USD', 'XRP-USD', 'STETH-USD', 'DOGE-USD',
# 
# tickers = ['ETH-USD', 'USDT-USD', 'BNB-USD', 'SOL-USD', 'USDC-USD', 'XRP-USD', 'STETH-USD', 'DOGE-USD',            
#     'WTRX-USD', 'TRX-USD', 'TON11419-USD', 'ADA-USD', 'WSTETH-USD', 'WBTC-USD', 'SHIB-USD', 'AVAX-USD', 'WETH-USD', 
#     'BCH-USD', 'LINK-USD', 'DOT-USD', 'USDS33039-USD', 'LEO-USD', 'DAI-USD', 'SUI20947-USD', 'LTC-USD', 'BTCB-USD', 
#     'WEETH-USD', 'NEAR-USD', 'EETH-USD', 'APT21794-USD', 'UNI7083-USD', 'WBETH-USD', 'PEPE24478-USD', 'ICP-USD', 
#     'TAO22974-USD', 'XMR-USD', 'USDE29470-USD', 'XLM-USD', 'FET-USD', 'ETC-USD', 'KAS-USD', 'FDUSD-USD', 'OKB-USD', 
#     'POL28321-USD', 'RENDER-USD', 'JITOSOL-USD', 'STX4847-USD', 'FIL-USD', 'WIF-USD', 'AAVE-USD', 'CRO-USD', 'ARB11841-USD', 
#     'MNT27075-USD', 'SUSDE-USD', 'TIA22861-USD', 'IMX10603-USD', 'OP-USD', 'RUNE-USD', 'INJ-USD', 'HBAR-USD', 'FTM-USD', 
#     'VET-USD', 'BGB-USD', 'ATOM-USD', 'BONK-USD', 'RETH-USD', 'SEI-USD', 'GRT6719-USD', 'POPCAT28782-USD', 'METH29035-USD', 
#     'PYTH-USD', 'ZBU-USD', 'JUP29210-USD', 'FLOKI-USD', 'OM-USD', 'KCS-USD', 'WZEDX-USD', 'SOLVBTC-USD', 'USDCE-USD', 'THETA-USD', 
#     'FLZ-USD', 'HNT-USD', 'MKR-USD', 'WLD-USD', 'ENA-USD', 'CBBTC32994-USD', 'EZETH-USD', 'BSV-USD', 'ALGO-USD', 'WBNB-USD', 'AR-USD', 
#     'MSOL-USD', 'LDO-USD', 'RAY-USD', 'ONDO-USD', 'FTN-USD', 'JASMY-USD', 'BTT-USD', 'VBNB-USD']
# 
# print(len(tickers))
# tickers_to_be_removed = ['USDS33039-USD', 'RENDER-USD', 'SOLVBTC-USD', 'CBBTC32994-USD']
# for tk in tickers_to_be_removed:
#     tickers.remove(tk)
# 
# print(len(tickers))
# 
# # tk = 'USDS33039-USD'

tk = 'BTC-USD'
# tickers = [tk]

"""
tickers = [  # Spot and futures
    'GC=F',  # Gold, Comex
    'SI=F',  # Silver, Comex
    'HG=F',  # Copper, Comex
    'PL=F',  # Platinum, NY Mercantile
    'PA=F',  # Palladium, NY Mercantile
    ]
"""
# tickers = ['SHIB-USD']
# tickers = ['PEPE24478-USD']
# crypto_names = list(df['Name'])
# tickers = ['GF=F', 'B0=F', 'PA=F', 'SIL=F']
# tickers = ['PA=F']
tickers_org = tickers.copy()  #

print(f'tickers_org = {tickers_org}')


downloaded_data = hist_data.download_yh_data(start_date, end_date, tickers, tk_market)

df_adj_close = downloaded_data['Adj Close']
df_close = downloaded_data['Close']
df_volume = downloaded_data['Volume']
dict_ohlc = downloaded_data['OHLC']

# Refresh the list of tickers, as some of them may have been removed
tickers = list(df_close.columns)
# tk = 'MSFT'
tk = tickers[0]  # 'BTC-USD'

df_ohlc = dict_ohlc[tk]
ohlc_tk = df_ohlc.copy()
adj_close_tk = df_adj_close[tk]
close_tk = df_close[tk]
open_tk = ohlc_tk['Open']
high_tk = ohlc_tk['High']
low_tk = ohlc_tk['Low']
volume_tk = df_volume[tk]

# print(df_close)

# We don't want the benchmark ticker in the app menus at this point (for example, 
# the drawdown data will not generated) unless tk_market is explicitly selected.

if tk_market not in tickers_org:
    tickers = tickers[:-1]  # if added by download_data, tk_market would be in the last position

downloaded_data = hist_data.download_yh_data(start_date, end_date, tickers, tk_market)
error_msg = downloaded_data['error_msg']

if error_msg:
    print(error_msg)

else:

    df_adj_close = downloaded_data['Adj Close']
    df_close = downloaded_data['Close']
    df_volume = downloaded_data['Volume']
    dict_ohlc = downloaded_data['OHLC']

    # Refresh the list of tickers, as some of them may have been removed
    tickers = list(df_close.columns)
    # tk = 'MSFT'
    # tk = tickers[0]

    df_ohlc = dict_ohlc[tk]
    ohlc_tk = df_ohlc.copy()
    adj_close_tk = df_adj_close[tk]
    close_tk = df_close[tk]
    open_tk = ohlc_tk['Open']
    high_tk = ohlc_tk['High']
    low_tk = ohlc_tk['Low']
    volume_tk = df_volume[tk]

    # print(df_close)

    # We don't want the benchmark ticker in the app menus at this point (for example, 
    # the drawdown data will not generated) unless tk_market is explicitly selected.

###########################################################################################

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])

app.layout = html.Div([
    
    ##### BEGIN TEMPLATE CONTROLS

    html.Div([

        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        html.Div(
            dbc.Button(
                id = 'collapse-button-tickers',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = {
                    'display': 'inline-block',
                    'margin-right': '5px',
                    'text-align': 'left',
                    'font-family': 'Helvetica',
                    'font-weight': 'bold',
                    'width': '250px'
                }
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'ticker-selection',
                children = [

                    html.Div([
                        html.Div('Ticker', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='tickers-dropdown',
                            options = tickers,
                            value = tickers[0],
                            clearable = False,
                            style = {'width': '180px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Theme', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'theme-dropdown',
                            options = ['Dark', 'Light'],
                            value = 'Dark',
                            disabled = False,
                            clearable = False,
                            style = {'width': '90px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Deck Type', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='deck-type-dropdown',
                            options = deck_types,
                            value = 'Single',
                            clearable = False,
                            style = {'width': '110px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Sec Y', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),        
                        dcc.Dropdown(
                            id='secondary-y-dropdown',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '80px', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Plot Width', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'width-input',
                            type = 'number',
                            value = 1450,
                            min = 800,
                            max = 1800,
                            step = 50,
                            style = {'width': '100px', 'height': '36px', 'vertical-align': 'bottom', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'bottom', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Upper Deck Height', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'upper-height-input',
                            type = 'number',
                            value = 750,
                            min = 250,
                            max = 1000,
                            step = 50,
                            style = {'width': '160px', 'height': '36px', 'vertical-align': 'bottom', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'bottom', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Lower Deck Height', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'lower-height-input',
                            type = 'number',
                            value = 150,
                            min = 100,
                            max = 300,
                            step = 50,
                            style = {'width': '160px', 'height': '36px', 'vertical-align': 'bottom', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'bottom', 'font-family': 'Helvetica'}
                    ),
                ]  # 'ticker_selection' children
            ),  # html.Div id 'ticker_selection'
                    
            id = 'collapse-tickers',
            is_open = False

        )  # dbc.Collapse
    ]),  # html.Div with dbc.Button and dbc.Collapse


])  # app.layout


@app.callback(
    Output('collapse-button-tickers', 'children'),
    Output('collapse-tickers', 'is_open'),
    Input('collapse-button-tickers', 'n_clicks'),
    State('collapse-tickers', 'is_open')
)
def toggle_collapse_tickers(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'PORTFOLIO TICKER SELECTION'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open