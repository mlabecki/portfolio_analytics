import dash
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

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
from mapping_portfolio_downloads import *
from mapping_tickers import *
from utils import *
from download_data import DownloadData
from analyze_prices import AnalyzePrices

# tickers = list(magnificent_7_tickers.keys())

end_date = datetime.today().date()
hist_years, hist_months, hist_days = 5, 0, 0
start_date = datetime(end_date.year - hist_years, end_date.month - hist_months, end_date.day - hist_days)
if end_date != datetime.today().date():
    end_date += timedelta(1)  # Both yf.download and yf.Ticker[tk].history() cut the data one day before end_date
    
tk_market = '^GSPC'
# tk_market = 'BTC-USD'

df = pd.DataFrame()
hist_data = DownloadData(end_date, start_date)

ticker_categories = [x for x in url_settings.keys() if x != 'global']
print(ticker_categories)
# Ticker categories:
# 'nasdaq100', 'sp500', 'dow_jones', 'biggest_companies',
# 'biggest_etfs', 'crypto_etfs', 'cryptos_yf', 'cryptos', 'futures'

max_tickers = 10
ticker_category = 'futures'
df = hist_data.download_from_url(ticker_category, max_tickers)

category_name = url_settings[ticker_category]['category_name']
category_sort_by = url_settings[ticker_category]['sort_by']
title_prefix = 'Top ' if not ('Biggest' in category_name) else ''
print(f'\n{title_prefix}{category_name} by {category_sort_by}\n')

# tickers = ['ZF=F', 'GC=F', 'YM=F']
# df_ticker_info = pd.DataFrame(index = df['Symbol'], columns = ['No.', 'Name', 'Data Start', 'Data End'])
df_ticker_info = pd.DataFrame(index = df['Symbol'], columns = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End'])
# df_ticker_info = pd.DataFrame(index = tickers, columns = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End'])

ticker_menu_info = {}
for i, tk in enumerate(df['Symbol']):
# for i, tk in enumerate(tickers):
    yf_tk_hist = yf.Ticker(tk).history(period = 'max')
    yf_tk_info = yf.Ticker(tk).info
    if len(yf_tk_hist.index) > 0:
        tk_start, tk_end = str(yf_tk_hist.index[0].date()), str(yf_tk_hist.index[-1].date())
        # tk_info_full = f"{i + 1}. {tk}: {df.loc[i, 'Name']}, {tk_start}, {tk_end}"
        
        # print(tk_info)
        # print(f"{i + 1}. {tk}:\t\t{df.loc[i, 'Name']}, {tk_start}-{tk_end}")

        df_ticker_info.loc[tk, 'No.'] = i + 1
        df_ticker_info.loc[tk, 'Ticker'] = tk

        if 'longName' in yf_tk_info.keys():
            tk_name = yf_tk_info['longName']
        elif 'shortName' in yf_tk_info.keys():
            tk_name = yf_tk_info['shortName']
        else:
            tk_name = df.loc[i, 'Name']
        df_ticker_info.loc[tk, 'Name'] = tk_name

        df_ticker_info.loc[tk, 'Data Start'] = tk_start
        df_ticker_info.loc[tk, 'Data End'] = tk_end

        tk_info = f"{tk}: {tk_name}"
        ticker_menu_info.update({tk_info: tk})

    else:
        print(f'SORRY: Cannot get data for {tk}')

df_ticker_info = df_ticker_info.dropna()

print(df_ticker_info)
print(df_ticker_info['Data End'].min())

tickers = list(df['Symbol'])

tk = tickers[0]
ticker_menu_info_list = list(ticker_menu_info.keys())
# ticker_names = list(df['Name'])

"""
tickers = [  # Spot and futures
    'GC=F',  # Gold, Comex
    'SI=F',  # Silver, Comex
    'HG=F',  # Copper, Comex
    'PL=F',  # Platinum, NY Mercantile
    'PA=F',  # Palladium, NY Mercantile
    ]
"""

tickers_org = tickers.copy()  #

print(f'tickers_org = {tickers_org}')

##############

dict_info = hist_data.download_yh_info(tickers, tk_market)
# print(hist_data.start_date)

# for tk in dict_info:
    # print(f'{tk}:')
    # dict_info_tk = dict_info[tk]
    # for field in dict_info_tk.keys():
        # print(f'\t{field}:\t{dict_info_tk[field]}')
    # print('')

##############

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

    if tk_market not in tickers_org:
        tickers = tickers[:-1]  # if added by download_data, tk_market would be in the last position

    analyze_prices = AnalyzePrices(end_date, start_date, tickers)
    date_index = df_close.index

    sort_by = ['Total Length', '% Depth']
    portfolio_drawdown_data = {}

    for tk in tickers:
        drawdown_data = analyze_prices.summarize_tk_drawdowns(df_close, tk, sort_by)
        n_drawdowns = drawdown_data['Total Drawdowns']
        drawdown_numbers = [x for x in range(n_drawdowns + 1)[1:]]
        portfolio_drawdown_data.update({tk: drawdown_data})

##############

drawdown_color = 'red'
theme = 'dark'
overlay_color_theme = 'grasslands'
# overlay_color_themes = list(theme_style[theme]['overlay_color_theme'].keys())
overlay_color_themes = [x.title() for x in theme_style[theme]['overlay_color_theme'].keys()]
# print(overlay_color_themes)
# drawdown_colors = list(theme_style[theme]['drawdown_colors'].keys())
drawdown_colors = [x.title() for x in theme_style[theme]['drawdown_colors'].keys()]

# deck_type = 'triple'
# deck_type = 'single'
# deck_type = 'double'
secondary_y = False
plot_width = 1600
plot_height_1 = 750
plot_height_2 = 150
plot_height_3 = 150
deck_types = ['Single', 'Double', 'Triple']

##############

df_ticker_info.insert(0, ' ', '⬜')

table = html.Div([
    dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in df_ticker_info.columns],
        data = df_ticker_info.to_dict('records'),
        editable = False,
        style_as_list_view = True,
        style_data_conditional = [
            # {'if': {'state': 'active'},'backgroundColor': 'white', 'border': '1px solid white'},
            {'if': {
                'state': 'active'},
                'backgroundColor': 'white',
                'border-top': '1px solid rgb(211, 211, 211)',
                'border-bottom': '1px solid rgb(211, 211, 211)'},
            {'if': {'column_id': ' '}, 'cursor': 'pointer'},
            # {'if': {'column_id': 'Name'}, 'textAlign': 'left', 'text-indent': '10px', 'width': 300},
        ],
        fixed_rows = {'headers': True},
        id = 'ticker-table',
        style_header = {
            'font-family': 'Helvetica',
            'font-size' : '13px',
            'font-weight' : 'bold',
            'width': '15px',
            'background': 'white',
            'text-align': 'left'
            # 'text-align': 'center'
        },
        style_data = {
            # 'cursor': 'pointer',
            'font-family': 'Helvetica',
            'font-size' : '13px',
            'width': '15px',
            'background': 'white',
            'text-align': 'left',
            'border-top': '1px solid rgb(211, 211, 211)',
            'border-bottom': '1px solid rgb(211, 211, 211)'
            # 'text-align': 'center'
        },
    )
])

#################

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])     # sharp corners

#################
# html.Script(src='https://cdn.plot.ly/plotly-latest.min.js')

select_ticker_left_css = {
    'background-color': 'rgba(0, 126, 255, .08)',
    'border-top-left-radius': '2px',
    'border-bottom-left-radius': '2px',
    'border': '1px solid rgba(0, 126, 255, .24)',
    'border-right': '0px',
    'color': '#007eff',
    'display': 'inline-block',
    'cursor': 'pointer',
    'font-family': 'Helvetica',
    'font-size': '14px',
    'line-height': '1.5',
    'padding-left': '5px',
    'padding-right': '5px',
    'margin-top': '5px',
    'vertical-align': 'center'
}
select_ticker_right_css = {
    'background-color': 'rgba(0, 126, 255, .08)',
    'border-top-right-radius': '2px',
    'border-bottom-right-radius': '2px',
    'border': '1px solid rgba(0, 126, 255, .24)',
    'color': '#007eff',
    'display': 'inline-block',
    'font-family': 'Helvetica',
    'font-size': '14px',
    'line-height': '1.5',
    'padding-left': '5px',
    'padding-right': '5px',
    'margin-top': '5px',
    'vertical-align': 'center'
}

app.layout = html.Div([

    html.Div([
            html.Div(html.Span('x'), id = 'select-ticker-icon', style = select_ticker_left_css),
            html.Div(children = [
                # html.B(ticker_menu_info[ticker_menu_info_list[0]], id = 'select-ticker-label-tk'),  # ticker corresponding to the first menu item
                # html.Span(f': {ticker_menu_info_list[0].split(": ")[1]}', id = 'select-ticker-label-name')  # the first menu item
                html.B(id = 'select-ticker-label-tk', style = {'margin-right': '10px'}),
                html.Span(id = 'select-ticker-label-name')
                ],
                id = 'select-ticker-label',
                style = select_ticker_right_css
            ),
        ],
        id = 'select-ticker',
        hidden = True,
        style = {
            # 'width': '400px',
            'border': '1px solid rgba(0, 126, 255, .24)',
            'border-radius': '2px',
            'margin-right': '5px'
        }
    ),

    html.Div(
        table,
        style = {
            'width': '550px',
            'font-family': 'Helvetica',
            'font-size' : '13px',
        }
    ),

    ##### BEGIN TEMPLATE CONTROLS

    html.Div([

        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        html.Div(
            dbc.Button(
                id = 'collapse-button-template',
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

                id = 'template-controls',
                children = [

                    html.Div([
                        html.Div('Ticker', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='tickers-dropdown',
                            # options = tickers,
                            # value = tickers[0],
                            options = ticker_menu_info_list,
                            value = ticker_menu_info_list[0],
                            clearable = False,
                            # clearable = True,
                            # multi = True,
                            # style = {'width': '180px'}
                            style = {'width': '450px', 'font-size': '15px', 'border-radius': '5px', 'vertical-align': 'top', 'margin-bottom': '0px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Theme', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'theme-dropdown',
                            options = ['Dark', 'Light'],
                            value = 'Dark',
                            disabled = False,
                            clearable = False,
                            style = {'width': '90px', 'font-size': '15px', 'border-radius': '5px', 'vertical-align': 'top', 'margin-bottom': '0px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Deck Type', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='deck-type-dropdown',
                            options = deck_types,
                            value = 'Single',
                            clearable = False, 
                            style = {'width': '110px', 'font-size': '15px', 'border-radius': '5px', 'vertical-align': 'top', 'margin-bottom': '0px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Sec Y', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),        
                        dcc.Dropdown(
                            id='secondary-y-dropdown',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '80px', 'font-size': '15px', 'border-radius': '5px', 'vertical-align': 'top', 'margin-bottom': '0px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Plot Width', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'width-input',
                            type = 'number',
                            value = 1450,
                            min = 800,
                            max = 1800,
                            step = 50,
                            style = {'width': '100px', 'height': '36px', 'font-size': '15px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'vertical-align': 'top'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Upper Deck Height', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px'}),
                        dbc.Input(
                            id = 'upper-height-input',
                            type = 'number',
                            value = 750,
                            min = 250,
                            max = 1000,
                            step = 50,
                            style = {'width': '160px', 'height': '36px', 'font-size': '15px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'vertical-align': 'top'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'border-radius': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Lower Deck Height', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'lower-height-input',
                            type = 'number',
                            value = 150,
                            min = 100,
                            max = 300,
                            step = 50,
                            style = {'width': '160px', 'height': '36px', 'font-size': '15px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'vertical-align': 'top', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    ### ADD RESET AXES BUTTON

                    html.Div([
                        html.Div('_', style = {'color': 'white', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Button(
                            'Reset Axes',
                            id = 'reset-axes-template',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'light',
                            size = 'sm',
                            style = {
                                'display': 'inline-block',
                                'height': '36px',
                                'border-color': 'rgb(192, 192, 192)', 
                                'border-radius': '5px',
                                'margin-bottom': '0px',
                                'margin-top': 'auto',
                                'text-align': 'center',
                                'font-family': 'Helvetica',
                                'font-size': '15px',
                                'width': '95px'
                            }
                        )],
                        style = {
                            'float': 'right',
                            'vertical-align': 'top',
                            'margin-bottom': '0px',
                            'margin-top': 'auto'
                        }
                    ),

                ]
            ),
        
            id = 'collapse-template',
            is_open = False
        )
    
    ]),

    ##### END TEMPLATE CONTROLS

    ##### BEGIN DRAWDOWN CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-drawdowns',
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

                id = 'drawdown-controls',
                children = [

                    html.Div([
                        html.Div('Top DD Number', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id='drawdowns-number-input',
                            type = 'number',
                            value = 5,
                            min = 1,
                            step = 1,
                            style = {'width': '130px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Top DD By', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-topby-dropdown',
                            options = ['% Depth', 'Total Length'],
                            value = '% Depth',
                            clearable = False,
                            style = {'width': '130px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('DD Display', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-display-dropdown',
                            options = ['Peak To Trough', 'Peak To Recovery'],
                            value = 'Peak To Trough',
                            clearable = False,
                            style = {'width': '170px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('DD Color', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-color-dropdown',
                            options = drawdown_colors,
                            value = 'Red',
                            clearable = False,
                            style = {'width': '100px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Price Color Theme', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-price-color-dropdown',
                            options = overlay_color_themes,
                            value = 'Sapphire',
                            clearable = False,
                            style = {'width': '150px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    ### ADD RESET AXES BUTTON

                    html.Div([
                        html.Div('_', style = {'color': 'white', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Button(
                            'Reset Axes',
                            id = 'reset-axes-drawdowns',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'light',
                            size = 'sm',
                            style = {
                                'display': 'inline-block',
                                'height': '36px',
                                'border-color': 'rgb(192, 192, 192)',
                                'border-radius': '5px',
                                'margin-bottom': '0px',
                                'margin-top': 'auto',
                                'text-align': 'center',
                                'font-family': 'Helvetica',
                                'font-size': '15px',
                                'width': '95px'
                            }
                        )],
                        style = {
                            'float': 'right',
                            'vertical-align': 'top',
                            'margin-bottom': '0px',
                            'margin-top': 'auto'
                        }
                    ),

                ],
            ), 

            id = 'collapse-drawdowns',
            is_open = False

        )]
    ), 

    ##### END DRAWDOWN CONTROLS

    ##### BEGIN BOLLINGER CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-bollinger',
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

                id = 'bollinger-controls',
                children = [

                    html.Div([
                        html.Div('Target Deck', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),        
                        dcc.Dropdown(
                            id = 'bollinger-deck-dropdown',
                            options = [1],
                            value = 1,
                            # options = [1, 2],
                            # value = 2,
                            clearable = False,
                            style = {'width': '100px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Window Size', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-window-input',
                            type = 'number',
                            value = 20,
                            min = 1,
                            max = 100,
                            step = 1,
                            style = {'width': '120px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('St Dev Multiplier', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-nstd-input',
                            type = 'number',
                            value = 2.0,
                            min = 0,
                            max = 10,
                            step = 0.1,
                            style = {'width': '130px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Number Of Bands', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-nbands-input',
                            type = 'number',
                            value = 1,
                            min = 1,
                            max = 5,
                            step = 1,
                            style = {'width': '140px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Color Theme', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='bollinger-color-theme-dropdown',
                            options = overlay_color_themes,
                            value = 'Grasslands',
                            clearable = False,
                            style = {'width': '120px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    ### ADD RESET AXES BUTTON

                    html.Div([
                        html.Div('_', style = {'color': 'white', 'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Button(
                            'Reset Axes',
                            id = 'reset-axes-bollinger',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'light',
                            size = 'sm',
                            style = {
                                'display': 'inline-block',
                                'height': '36px',
                                'border-color': 'rgb(192, 192, 192)',                                
                                'border-radius': '5px',
                                'margin-bottom': '0px',
                                'margin-top': 'auto',
                                'text-align': 'center',
                                'font-family': 'Helvetica',
                                'font-size': '15px',
                                'width': '95px'
                            }
                        )],
                        style = {
                            'float': 'right',
                            # 'vertical-align': 'top',
                            'vertical-align': 'top', 
                            'margin-bottom': '0px',
                            'margin-top': 'auto'
                        }
                    ),

                ],
            ), 

            id = 'collapse-bollinger',
            is_open = False

        )]
    ), 

    ##### END BOLLINGER CONTROLS

    # style = {'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '5px', 'font-family': 'Helvetica'}
  
    # html.Br(),
    # dcc.Store(id = 'fig_data'),

    html.Div(id = 'fig-div', children = [])
            # [dcc.Graph(id='test-graph', figure = {})],)

])

@app.callback(
    Output('select-ticker-label-tk', 'children'),
    Output('select-ticker-label-name', 'children'),
    # Output('select-ticker', 'hidden'),
    Input('tickers-dropdown', 'value'),
    # State('select-ticker', 'hidden')
    # Input('select-ticker-icon', 'n_clicks')
)
def add_ticker_select(tk_info):
    tk = ticker_menu_info[tk_info]
    name = tk_info.split(': ')[1]
    return tk, name

@app.callback(
    # Output('select-ticker_label', 'children'),
    Output('select-ticker', 'hidden'),
    # Input('tickers-dropdown', 'value'),
    Input('select-ticker-icon', 'n_clicks')
)
def remove_ticker_select(n):
    if n:
        return True
    else:
        return False
    
@app.callback(
    Output('collapse-button-template', 'children'),
    Output('collapse-template', 'is_open'),
    Input('collapse-button-template', 'n_clicks'),
    State('collapse-template', 'is_open')
)
def toggle_collapse_template(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'TICKER AND TEMPLATE'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open

@app.callback(
    Output('lower-height-input', 'disabled'),
    Output('bollinger-deck-dropdown', 'options'),
    Input('deck-type-dropdown', 'value'))
def disable_options(deck_type):
    if deck_type == 'Single':
        return True, [1]
    elif deck_type == 'Double':
        return False, [1, 2]
    else:
        return False, [1, 2, 3]

@app.callback(
    Output('collapse-button-drawdowns', 'children'),
    Output('collapse-drawdowns', 'is_open'),
    Input('collapse-button-drawdowns', 'n_clicks'),
    State('collapse-drawdowns', 'is_open')
)
def toggle_collapse_drawdowns(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'DRAWDOWNS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open

@app.callback(
    Output('collapse-button-bollinger', 'children'),
    Output('collapse-bollinger', 'is_open'),
    Input('collapse-button-bollinger', 'n_clicks'),
    State('collapse-bollinger', 'is_open')
)
def toggle_collapse_bollinger(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'BOLLINGER BANDS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open

@app.callback(
    # Output(component_id = 'drawdowns-number-dropdown', component_property = 'options'),
    # Output(component_id = 'drawdowns-number-dropdown', component_property = 'value'),
    Output(component_id = 'drawdowns-number-input', component_property = 'max'),
    Output(component_id = 'drawdowns-number-input', component_property = 'value'),
    Input(component_id = 'tickers-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-number-input', component_property = 'value')
)
def update_drawdowns_number_dropdown(tk_menu_info, dd_number):
    tk = ticker_menu_info[tk_menu_info]
    n_drawdowns = portfolio_drawdown_data[tk]['Total Drawdowns']
    # dd_number_options = [x for x in range(n_drawdowns + 1)][1:]
    dd_number_value = min(dd_number, n_drawdowns)
    return n_drawdowns, dd_number_value
    # return dd_number_options, dd_number_value

@app.callback(

    # Output(component_id = 'test-graph', component_property = 'figure'),
    # Output(component_id = 'fig_div', component_property = 'children', allow_duplicate = True),
    # Output(component_id = 'test-graph', component_property = 'figure'),
    Output(component_id = 'fig-div', component_property = 'children'),
    Output(component_id = 'drawdown-controls', component_property = 'style'),
    Output(component_id = 'bollinger-controls', component_property = 'style'),
    Output(component_id = 'template-controls', component_property = 'style'),

    Input(component_id = 'reset-axes-template', component_property = 'n_clicks'),
    Input(component_id = 'reset-axes-drawdowns', component_property = 'n_clicks'),
    Input(component_id = 'reset-axes-bollinger', component_property = 'n_clicks'),
    
    # template options
    Input(component_id = 'tickers-dropdown', component_property = 'value'),
    Input(component_id = 'theme-dropdown', component_property = 'value'),
    Input(component_id = 'deck-type-dropdown', component_property = 'value'),
    Input(component_id = 'secondary-y-dropdown', component_property = 'value'),
    Input(component_id = 'width-input', component_property = 'value'),
    Input(component_id = 'upper-height-input', component_property = 'value'),
    Input(component_id = 'lower-height-input', component_property = 'value'),
    
    # drawdowns options
    Input(component_id = 'drawdowns-number-input', component_property = 'value'),
    Input(component_id = 'drawdowns-topby-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-display-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-color-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-price-color-dropdown', component_property = 'value'),
    # prevent_initial_call=True #,
    #Input(component_id = 'overlay-dropdown', component_property = 'value')

    # bollinger options
    Input(component_id = 'bollinger-deck-dropdown', component_property = 'value'),
    Input(component_id = 'bollinger-window-input', component_property = 'value'),
    Input(component_id = 'bollinger-nstd-input', component_property = 'value'),
    Input(component_id = 'bollinger-nbands-input', component_property = 'value'),
    Input(component_id = 'bollinger-color-theme-dropdown', component_property = 'value'),

    
)

def update_plot(
        n_click_template,
        n_click_dd,
        n_click_bollinger,

        # ticker and template options
        # tk,
        tk_menu_info,
        theme,
        deck_type,
        sec_y,
        width,
        upper_height,
        lower_height,

        # drawdowns options
        n_top, 
        drawdown_top_by, 
        drawdown_display, 
        drawdown_color, 
        price_color_theme,

        # bollinger options
        # tk_bollinger,
        bollinger_deck,
        bollinger_window,
        bollinger_nstd,
        bollinger_nbands,
        bollinger_color_theme

    ):

    # fig_data = create_graph(theme, tk, drawdown_color, overlay_color_theme)
    tk = ticker_menu_info[tk_menu_info]
    theme = theme.lower()
    deck_type = deck_type.lower()
    secondary_y = False if sec_y == 'No' else True
    fig_data = analyze_prices.create_template(
        date_index,
        deck_type = deck_type,
        secondary_y = secondary_y,
        plot_width = width,
        plot_height_1 = upper_height,
        plot_height_2 = lower_height,
        plot_height_3 = lower_height,
        theme = theme
    )

    # if (theme_drawdowns != theme):
    #     theme = theme_drawdowns

    drawdown_div_style = {
        'width': width,
        # 'vertical-align': 'top',
        # 'margin-top': 'auto', 
        # 'margin-bottom': '0px'
    }
    bollinger_div_style = drawdown_div_style
    template_div_style = drawdown_div_style

    drawdown_data = portfolio_drawdown_data[tk]
    selected_drawdown_data = analyze_prices.select_tk_drawdowns(drawdown_data, n_top)
    # n_drawdowns = len(drawdown_data['Drawdown Stats'])
    # n_drawdown_list = [x for x in range(n_drawdowns + 1)][1:]

    show_trough_to_recovery = True if drawdown_display == 'Peak To Recovery' else False
    drawdown_top_by = 'length' if drawdown_top_by == 'Total Length' else 'depth'
    fig_data = analyze_prices.add_drawdowns(
        fig_data,
        df_close[tk],
        tk,
        selected_drawdown_data,
        n_top_drawdowns = n_top,
        target_deck = 1,
        add_price = True,
        # add_price = False,
        price_type = 'close',
        top_by = drawdown_top_by,
        show_trough_to_recovery = show_trough_to_recovery,
        add_title = True,
        theme = theme,
        # theme = theme_drawdowns,
        # color_theme = 'base',
        price_color_theme = price_color_theme.lower(),
        drawdown_color = drawdown_color.lower()
    )
    # fig_div = create_graph(theme, tk, drawdown_color, overlay_color_theme)
    # fig = fig_data['fig']

    
    bollinger_data = analyze_prices.bollinger_bands(df_close[tk], bollinger_window, bollinger_nstd, bollinger_nbands)
    bollinger_list = bollinger_data['list']
    fig_data = analyze_prices.add_bollinger_overlays(
        fig_data,
        bollinger_list,
        target_deck = bollinger_deck,
        theme = theme,
        color_theme = bollinger_color_theme.lower()
    )
    

    # target_deck = 1
    # plot_height = fig_data['plot_height'][target_deck]
    # y_min = fig_data['y_min'][target_deck]
    # y_max = fig_data['y_max'][target_deck]
    fig = fig_data['fig']
    
#     if n_click:
#         min_n_intervals = n_yintervals_map['min'][plot_height]
#         max_n_intervals = n_yintervals_map['max'][plot_height]
# 
#         y_lower_limit, y_upper_limit, y_delta = set_axis_limits(y_min, y_max, min_n_intervals, max_n_intervals)
# 
#         # y_lower_limit, y_upper_limit, y_delta = 100, 450, 50
# 
#         fig['layout']['yaxis']['range'] = (y_lower_limit, y_upper_limit)
#         fig['layout']['yaxis']['tick0'] = y_lower_limit
#         fig['layout']['yaxis']['dtick'] = y_delta
    
    # fig_div = html.Div(html.Div(dcc.Graph(id = 'drawdowns-graph', figure = fig)))
    # fig_div = html.Div(html.Div(children = [dcc.Graph(id = 'drawdowns-graph', figure = fig)]))
    fig_div = dcc.Graph(id='drawdowns-graph', figure = fig)

    return fig_div, drawdown_div_style, bollinger_div_style, template_div_style
    

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
    # app.run_server(debug=False, port=8052)
