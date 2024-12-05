import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table
from dash.exceptions import PreventUpdate
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
from mapping_portfolio_downloads import *
from mapping_tickers import *
from css_portfolio_analytics import *
from utils import *
from download_data import DownloadData
from analyze_prices import AnalyzePrices

end_date = datetime.today()
hist_years, hist_months, hist_days = 1, 0, 0
start_date = datetime(end_date.year - hist_years, end_date.month - hist_months, end_date.day - hist_days)

hist_data = DownloadData(end_date, start_date)

tk_market = '^GSPC'
# tk_market = 'BTC-USD'

# ticker_categories = [x for x in url_settings.keys() if x != 'global']
# print(ticker_categories)
# Ticker categories:
# 'nasdaq100', 'sp500', 'dow_jones', 'biggest_companies',
# 'biggest_etfs', 'crypto_etfs', 'cryptos', 'cryptos_coin360', 'futures'

max_tickers = 7
# ticker_category = 'crypto_etfs'
# ticker_category = 'biggest_companies'
# ticker_category = 'cryptos'
# df = hist_data.download_from_url(ticker_category, max_tickers)
# 
# category_name = url_settings[ticker_category]['category_name']
# category_sort_by = url_settings[ticker_category]['sort_by']
# title_prefix = 'Top ' if not ('Biggest' in category_name) else ''
# table_title = f'{max_tickers} {title_prefix}{category_name} by {category_sort_by}'
# print(f'\n{title_prefix}{category_name} by {category_sort_by}\n')

tickers_stock_indices = list(stock_index_tickers.keys())
tickers_magnificent_seven = list(magnificent_7_tickers.keys())
tickers_precious_metals = list(precious_metals.keys())
tickers_bond_etfs = list(bond_etf_tickers.keys())
tickers_commodity_etfs = list(commodity_etf_tickers.keys())
tickers_risk_free_treasury = list(risk_free_treasury_tickers.keys())
tickers_volatility_indices = list(volatility_tickers.keys())
tickers_currency_etfs = list(currency_etf_tickers.keys())

input_table_columns_indices = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency']
input_table_columns_futures = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency']
input_table_columns_equities = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Industry', 'Sector', 'Exchange', 'Currency']
input_table_columns_etfs = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Category', 'Exchange', 'Currency']

custom_ticker_table_columns = {
    'INDEX': ['Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency'],
    'FUTURE': ['Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency'],
    'EQUITY': ['Ticker', 'Name', 'Data Start', 'Data End', 'Industry', 'Sector', 'Exchange', 'Currency'],
    'ETF': ['Ticker', 'Name', 'Data Start', 'Data End', 'Category', 'Exchange', 'Currency']
}

# NOTE: The ticker categories and the number of tickers to download the info of in each of them will be specified by the user
#       on the page preceding the ticker selection page.

df_info_tickers_bond_etfs = pd.DataFrame(index = tickers_bond_etfs, columns = input_table_columns_etfs)
df_info_tickers_stock_indices = pd.DataFrame(index = tickers_stock_indices, columns = input_table_columns_indices)
df_info_tickers_magnificent_seven = pd.DataFrame(index = tickers_magnificent_seven, columns = input_table_columns_equities)
df_info_tickers_commodity_etfs = pd.DataFrame(index = tickers_commodity_etfs, columns = input_table_columns_etfs)
df_info_tickers_precious_metals = pd.DataFrame(index = tickers_precious_metals, columns = input_table_columns_futures)
df_info_tickers_risk_free_treasury = pd.DataFrame(index = tickers_risk_free_treasury, columns = input_table_columns_indices)
df_info_tickers_volatility_indices = pd.DataFrame(index = tickers_volatility_indices, columns = input_table_columns_indices)
df_info_tickers_currency_etfs = pd.DataFrame(index = tickers_currency_etfs, columns = input_table_columns_etfs)

row_ticker_map_bond_etfs = {}
row_ticker_map_stock_indices = {}
row_ticker_map_magnificent_seven = {}
row_ticker_map_commodity_etfs = {}
row_ticker_map_precious_metals = {}
row_ticker_map_risk_free_treasury = {}
row_ticker_map_volatility_indices = {}
row_ticker_map_currency_etfs = {}

ticker_category_info_map = {
    'magnificent_seven': {
        'df': df_info_tickers_magnificent_seven,
        'row': row_ticker_map_magnificent_seven,
        'dict': magnificent_7_tickers,
        'sort_by': 'marketCap',
        'id_string': 'magnificent-seven',
        'collapse_title': 'MAGNIFICENT SEVEN',
        'table_title': 'MAGNIFICENT SEVEN COMPANIES sorted by Market Capitalization'
    },
    'bond_etfs': {
        'df': df_info_tickers_bond_etfs,
        'row': row_ticker_map_bond_etfs,
        'dict': bond_etf_tickers,
        'sort_by': 'totalAssets',
        'id_string': 'bond-etfs',
        'collapse_title': 'TOP BOND ETFs',        
        'table_title': 'TOP BOND ETFs by Total Assets Under Management'
    },
    'commodity_etfs': {
        'df': df_info_tickers_commodity_etfs,
        'row': row_ticker_map_commodity_etfs,
        'dict': commodity_etf_tickers,
        'sort_by': 'totalAssets',
        'id_string': 'commodity-etfs',
        'collapse_title': 'COMMODITY ETFs',
        'table_title': 'SELECTED COMMODITY ETFs sorted by Total Assets Under Management'
    },
    'precious_metals': {
        'df': df_info_tickers_precious_metals,
        'row': row_ticker_map_precious_metals,
        'dict': precious_metals,
        'sort_by': 'openInterest',
        'id_string': 'precious-metals',
        'collapse_title': 'PRECIOUS METALS',
        'table_title': 'PRECIOUS METALS SPOT/FUTURES sorted by Open Interest'
    },
    'currency_etfs': {
        'df': df_info_tickers_currency_etfs,
        'row': row_ticker_map_currency_etfs,
        'dict': currency_etf_tickers,
        'sort_by': 'totalAssets',
        'id_string': 'currency-etfs',
        'collapse_title': 'CURRENCY ETFs',
        'table_title': 'SELECTED CURRENCY ETFs sorted by Total Assets Under Management'
    },
    'stock_indices': {
        'df': df_info_tickers_stock_indices,
        'row': row_ticker_map_stock_indices,
        'dict': stock_index_tickers,
        'sort_by': '',  # Only some indices have 'volume' in info
        'id_string': 'stock-indices',
        'collapse_title': 'STOCK INDICES',
        'table_title': 'SELECTED STOCK INDICES'
    },
    'volatility_indices': {
        'df': df_info_tickers_volatility_indices,
        'row': row_ticker_map_volatility_indices,
        'dict': volatility_tickers,
        'sort_by': '',  # No 'volume' in info
        'id_string': 'volatility-indices',
        'collapse_title': 'VOLATILITY INDICES',        
        'table_title': 'SELECTED VOLATILITY INDICES'
    },
    'risk_free_treasury': {
        'df': df_info_tickers_risk_free_treasury,
        'row': row_ticker_map_risk_free_treasury,
        'dict': risk_free_treasury_tickers,
        'sort_by': '',  # No 'volume' in info
        'id_string': 'risk-free-treasury',
        'collapse_title': 'RISK-FREE INDICES',        
        'table_title': 'RISK-FREE US TREASURY INDICES'
    }
}

ticker_info = {}  # To help user decide on tickers based on the name and data start and end dates

def create_input_table(category):

    df_info_tickers = ticker_category_info_map[category]['df']
    row_ticker_map = ticker_category_info_map[category]['row']
    dict_info_tickers = ticker_category_info_map[category]['dict']
    tk_sort_by = ticker_category_info_map[category]['sort_by']
    
    category_tickers = list(dict_info_tickers.keys())
    category_tickers_sorted = category_tickers

    # Sort ticker list by marketCap (equities), totalAssets (ETFs) or openInterest (futures)
    if tk_sort_by != '':
        dict_tickers_values = {tk: yf.Ticker(tk).info[tk_sort_by] for tk in category_tickers}
        category_tickers_sorted = [i[0] for i in sorted(dict_tickers_values.items(), key=itemgetter(1), reverse=True)]
        df_info_tickers.index = category_tickers_sorted  

    for i, tk in enumerate(category_tickers_sorted):

        if tk not in ticker_info.keys():
            
            tk_hist = yf.Ticker(tk).history(period = 'max')
            tk_info = yf.Ticker(tk).info
            # Should also check if ticker is still valid, for now assume they're all valid

            if len(tk_hist.index) > 0:

                tk_start, tk_end = str(tk_hist.index[0].date()), str(tk_hist.index[-1].date())

                df_info_tickers.at[tk, 'No.'] = i + 1
                df_info_tickers.at[tk, 'Ticker'] = tk

                if 'longName' in tk_info.keys():
                    tk_name = tk_info['longName']
                elif 'shortName' in tk_info.keys():
                    tk_name = tk_info['shortName']
                else:
                    tk_name = dict_info_tickers[tk]

                tk_type = tk_info['quoteType'] if 'quoteType' in tk_info.keys() else ''
                tk_exchange = tk_info['exchange'] if 'exchange' in tk_info.keys() else ''
                tk_currency = tk_info['currency'] if 'currency' in tk_info.keys() else ''
                tk_category = tk_info['category'] if 'category' in tk_info.keys() else ''
                tk_industry = tk_info['industry'] if 'industry' in tk_info.keys() else ''
                tk_sector = tk_info['sector'] if 'sector' in tk_info.keys() else ''

                if 'longBusinessSummary' in tk_info.keys():
                    tk_summary = tk_info['longBusinessSummary']
                elif 'description' in tk_info.keys():
                    tk_summary = tk_info['description']
                else: 
                    tk_summary = ''

                df_info_tickers.at[tk, 'Name'] = tk_name
                df_info_tickers.at[tk, 'Data Start'] = tk_start
                df_info_tickers.at[tk, 'Data End'] = tk_end
                df_info_tickers.at[tk, 'Exchange'] = tk_exchange
                df_info_tickers.at[tk, 'Currency'] = tk_currency

                if tk_type == 'ETF':
                    df_info_tickers.at[tk, 'Category'] = tk_category
                elif tk_type == 'EQUITY':
                    df_info_tickers.at[tk, 'Industry'] = tk_industry
                    df_info_tickers.at[tk, 'Sector'] = tk_sector

                ticker_info.update({
                    tk: {
                        'name': tk_name,
                        'start': tk_start,
                        'end': tk_end,
                        'type': tk_type,
                        'exchange': tk_exchange,
                        'currency': tk_currency,
                        'category': tk_category,
                        'industry': tk_industry,
                        'sector': tk_sector,
                        'summary': tk_summary
                    }
                })

            else:
                print(f'WARNING: Cannot get data for {tk} at the moment, try again later')
    
        else:

            df_info_tickers.at[tk, 'No.'] = i + 1
            df_info_tickers.at[tk, 'Ticker'] = tk
            df_info_tickers.at[tk, 'Name'] = ticker_info[tk]['name']
            df_info_tickers.at[tk, 'Data Start'] = ticker_info[tk]['start']
            df_info_tickers.at[tk, 'Data End'] = ticker_info[tk]['end']
            df_info_tickers.at[tk, 'Exchange'] = ticker_info[tk]['exchange']
            df_info_tickers.at[tk, 'Currency'] = ticker_info[tk]['currency']
            if ticker_info[tk]['type'] == 'ETF':
                df_info_tickers.at[tk, 'Category'] = ticker_info[tk]['category']
            elif ticker_info[tk]['type'] == 'EQUITY':
                df_info_tickers.at[tk, 'Industry'] = ticker_info[tk]['industry']
                df_info_tickers.at[tk, 'Sector'] = ticker_info[tk]['sector']

        row_ticker_map.update({tk: i})

    input_table_data = {
        'df': df_info_tickers,
        'row': row_ticker_map
    }

    return input_table_data


for category in ticker_category_info_map.keys():
    print(f'\nProcessing info for {category} ...')
    input_table_data = create_input_table(category)
    ticker_category_info_map[category]['df'] = input_table_data['df']
    ticker_category_info_map[category]['row'] = input_table_data['row']
    print(ticker_category_info_map[category]['df'])
    print(ticker_category_info_map[category]['row'])

print(f'\nTotal tickers: {len(ticker_info)}')
# print(df_info_tickers_magnificent_seven)

# import sys
# sys.exit()
# 
# for i, tk in enumerate(tickers_bond_etfs):
#     
#     yf_tk_hist = yf.Ticker(tk).history(period = 'max')
#     yf_tk_info = yf.Ticker(tk).info
# 
#     if len(yf_tk_hist.index) > 0:
# 
#         tk_start, tk_end = str(yf_tk_hist.index[0].date()), str(yf_tk_hist.index[-1].date())
# 
#         df_info_tickers_bond_etfs.at[tk, 'No.'] = i + 1
#         df_info_tickers_bond_etfs.at[tk, 'Ticker'] = tk
# 
#         if 'longName' in yf_tk_info.keys():
#             tk_name = yf_tk_info['longName']
#         elif 'shortName' in yf_tk_info.keys():
#             tk_name = yf_tk_info['shortName']
#         else:
#             tk_name = bond_etf_tickers[tk]
# 
#         tk_type = yf_tk_info['quoteType'] if 'quoteType' in yf_tk_info.keys() else ''
#         tk_exchange = yf_tk_info['exchange'] if 'exchange' in yf_tk_info.keys() else ''
#         tk_currency = yf_tk_info['currency'] if 'currency' in yf_tk_info.keys() else ''
#         if 'longBusinessSummary' in yf_tk_info.keys():
#             tk_summary = yf_tk_info['longBusinessSummary']
#         elif 'description' in yf_tk_info.keys():
#             tk_summary = yf_tk_info['description']
#         else: 
#             tk_summary = ''
# 
#         df_info_tickers_bond_etfs.at[tk, 'Name'] = tk_name
#         df_info_tickers_bond_etfs.at[tk, 'Data Start'] = tk_start
#         df_info_tickers_bond_etfs.at[tk, 'Data End'] = tk_end
#         df_info_tickers_bond_etfs.at[tk, 'Type'] = tk_type
#         df_info_tickers_bond_etfs.at[tk, 'Exchange'] = tk_exchange
#         df_info_tickers_bond_etfs.at[tk, 'Currency'] = tk_currency
# 
#         row_ticker_map_bond_etfs.update({tk: i})
# 
#         ticker_info.update({
#             tk: {
#                 'name': tk_name,
#                 'start': tk_start,
#                 'end': tk_end,
#                 'type': tk_type,
#                 'exchange': tk_exchange,
#                 'currency': tk_currency,
#                 'summary': tk_summary
#             }
#         })
# 
#     else:
#         print(f'WARNING: Cannot get data for {tk} at the moment, try again later')

# print(df_info_tickers_bond_etfs)

ticker_names_org = pd.Series(index = df_info_tickers_bond_etfs.index, data = df_info_tickers_bond_etfs['Name'])

tickers = df_info_tickers_bond_etfs.index
# ticker_menu_info_list = list(ticker_menu_info.keys())

tickers_org = tickers.copy()  #
print(f'tickers_org = {tickers_org}')

# We don't want the benchmark ticker in the app menus at this point (for example, 
# the drawdown data will not generated) unless tk_market is explicitly selected.

# downloaded_data = hist_data.download_yh_data(start_date, end_date, tickers, tk_market)
# error_msg = downloaded_data['error_msg']
# 
# if error_msg:
#     print(error_msg)
# 
# else:
# 
#     df_adj_close = downloaded_data['Adj Close']
#     df_close = downloaded_data['Close']
#     df_volume = downloaded_data['Volume']
#     dict_ohlc = downloaded_data['OHLC']
# 
#     # Refresh the list of tickers, as some of them may have been removed
#     tickers = list(df_close.columns)
# 
#     # We don't want the benchmark ticker in the app menus at this point (for example, 
#     # the drawdown data will not generated) unless tk_market is explicitly selected.
# 
#     if tk_market not in tickers_org:
#         tickers = tickers[:-1]  # if added by download_data, tk_market would be in the last position
# 
#     ticker_names = ticker_names_org[tickers]
# 
#     print(tickers)
#     # print(ticker_names)

##############

ticker_div_title = html.Div(
    'YOUR PORTFOLIO:',
    style = select_ticker_title_css
)

# def create_ticker_divs(ticker_names: pd.Series, ticker_div_title):
# 
#     ticker_divs = [ticker_div_title]
# 
#     for tk in ticker_names.index:
#         name = ticker_names[tk]
#         tk_id = f'select-ticker-{tk}'
#         tk_icon_id = f'select-ticker-icon-{tk}'
#         tk_div = html.Div(
#             id = tk_id,
#             hidden = True,
#             children = [
#                 html.Div('x', id = tk_icon_id, n_clicks = 0, style = select_ticker_left_css),
#                 html.Div(children = [
#                     html.B(tk, id = f'select-ticker-label-tk-{tk}', style = {'margin-right': '6px'}),
#                     html.Span(name, id = f'select-ticker-label-name-{tk}')
#                     ],
#                     id = f'select-ticker-label-{tk}',
#                     style = select_ticker_right_css
#                 )
#             ],
#             style = {
#                 'display': 'inline-block',
#                 'margin-right': '5px',
#                 'margin-bottom': '5px',
#                 # 'margin-top': '0px',
#                 'line-height': '1',
#                 'vertical-align': 'top'
#             }
#         )
#         ticker_divs.append(tk_div)
# 
#     return ticker_divs


# ticker_divs = create_ticker_divs(ticker_names, ticker_div_title)

input_table = {}  # A dictionary mapping ticker category to the corresponding input table
input_table_collapse_div = {}
static_tables = []

for category in ticker_category_info_map.keys():
    
    id_string = ticker_category_info_map[category]['id_string']

    input_table[category] = html.Div([
        dash_table.DataTable(
            columns = [{'name': i, 'id': i} for i in ticker_category_info_map[category]['df'].columns],
            data = ticker_category_info_map[category]['df'].to_dict('records'),
            editable = False,
            row_selectable = 'multi',
            # column_selectable = 'multi',
            selected_rows = [],
            style_as_list_view = True,
            style_data_conditional = [
                # {'if': {'state': 'active'},'backgroundColor': 'white', 'border': '1px solid white'},
                {'if': {
                    'state': 'active'},
                    'backgroundColor': 'white',
                    'border-top': '1px solid rgb(211, 211, 211)',
                    'border-bottom': '1px solid rgb(211, 211, 211)'},
                # {'if': {'column_id': ' '}, 'cursor': 'pointer'},
                {'if': {'column_id': 'No.'}, 'width': 24},
                {'if': {'column_id': 'Ticker'}, 'width': 45},
                # {'if': {'column_id': 'Type'}, 'width': 38},
                {'if': {'column_id': 'Currency'}, 'width': 70},
                {'if': {'column_id': 'Exchange'}, 'width': 72},
                {'if': {'column_id': 'Data Start'}, 'width': 85},
                {'if': {'column_id': 'Data End'}, 'width': 85},
                # {'if': {'column_id': 'Category'}, 'width': 125},
                # {'if': {'column_id': 'Industry'}, 'width': 130},
                # {'if': {'column_id': 'Sector'}, 'width': 130},
            ],
            id = f'table-{id_string}',
            style_header = input_table_header_css,
            style_data = input_table_data_css,
        )
    ])

    input_table_collapse_div[category] = html.Div(
        hidden = False,
        children =
        [
            html.Div(
                ticker_category_info_map[category]['collapse_title'],
                id = f'collapse-button-title-{id_string}',
                hidden = True
            ),
            html.Div(
                dbc.Button(
                    id = f'collapse-button-table-{id_string}',
                    class_name = 'ma-1',
                    color = 'primary',
                    size = 'sm',
                    n_clicks = 0,
                    style = collapse_button_table_css
                )
            ),
            dbc.Collapse(
                html.Div(
                    html.Div(
                        id = f'table-{id_string}-container',
                        children = [
                        html.Div(
                            children = ticker_category_info_map[category]['table_title'],
                            id = f'table-{id_string}-title',
                            style = input_table_title_css
                        ),
                        input_table[category]
                        ],
                        style = input_table_container_css
                    ),
                ),
                id = f'collapse-table-{id_string}',
                is_open = False
            ),  # dbc.Collapse
        ]
    )  # html.Div with dbc.Button and dbc.Collapse

    static_tables.append(input_table_collapse_div[category])

# table_bond_etfs_title = 'Top Bond ETFs by Total Assets'
# table_bond_etfs_title = 'TOP BOND ETFs by Total Assets Under Management'

###########################################################################################

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])
# app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.Div(id = 'ticker-output', hidden = True, style = {'font-size' : '14px'}),

    # MAIN TITLE
    html.Div(
        'Add tickers to your portfolio by typing in the Add Ticker box or selecting from the lists below',
        id = 'ticker-main-title',
        style = ticker_main_title_css
    ),

    html.Div(id = 'select-ticker-list', hidden = True),

    # YOUR PORTFOLIO
    html.Div(
        id = 'select-ticker-container',
        hidden = True,
        style = select_ticker_container_css
    ),

    html.Div(
        id = 'custom-ticker-all-container',
        children = [

            html.Div(
                id = 'custom-ticker-input-container',
                children = [
                    html.Div([
                        html.Div(
                            'Add Ticker:',
                            id = 'custom-ticker-input-title',
                            style = custom_ticker_input_title_css
                        ),
                        dbc.Input(
                            id = 'custom-ticker-input',
                            type = 'text',
                            value = '',
                            debounce = True,
                            placeholder = '',
                            style = custom_ticker_input_css
                        )
                    ]),
                ],
                style = custom_ticker_input_container
            ),

            html.Div(
                id = 'custom-ticker-input-message',
                hidden = True,
                style = custom_ticker_input_message_css
            ),

            html.Div(
                id = 'custom-ticker-info-container',
                hidden = False,
                children = [
                    html.Div(
                        id = 'table-custom-ticker-info',
                        style = table_custom_ticker_info_css
                    ),
                ],
                style = custom_ticker_info_container_css
            )
        ],
        style = custom_ticker_all_container_css
    ),

    ################

    html.Div(
        id = 'all-tables-container',
        children = static_tables
    ),

    html.Br()

])  # app.layout

####################################################################

@app.callback(
    Output('select-ticker-container', 'children'),
    Output('select-ticker-container', 'hidden'),
    Output('select-ticker-list', 'children'),
    Output('custom-ticker-input', 'value'),
    Output('custom-ticker-input-message', 'hidden'),
    Output('custom-ticker-info-container', 'hidden'),
    Output('custom-ticker-input-message', 'children'),
    Output('table-custom-ticker-info', 'children'),

    Output('table-bond-etfs', 'selected_rows'),
    Output('table-stock-indices', 'selected_rows'),
    Output('table-magnificent-seven', 'selected_rows'),
    Output('table-commodity-etfs', 'selected_rows'),
    Output('table-precious-metals', 'selected_rows'),
    Output('table-risk-free-treasury', 'selected_rows'),
    Output('table-volatility-indices', 'selected_rows'),
    Output('table-currency-etfs', 'selected_rows'),

    Input('table-bond-etfs', 'data'),
    Input('table-stock-indices', 'data'),
    Input('table-magnificent-seven', 'data'),
    Input('table-commodity-etfs', 'data'),
    Input('table-precious-metals', 'data'),
    Input('table-risk-free-treasury', 'data'),
    Input('table-volatility-indices', 'data'),
    Input('table-currency-etfs', 'data'),

    Input('table-bond-etfs', 'selected_rows'),
    Input('table-stock-indices', 'selected_rows'),
    Input('table-magnificent-seven', 'selected_rows'),
    Input('table-commodity-etfs', 'selected_rows'),
    Input('table-precious-metals', 'selected_rows'),
    Input('table-risk-free-treasury', 'selected_rows'),
    Input('table-volatility-indices', 'selected_rows'),
    Input('table-currency-etfs', 'selected_rows'),

    Input('select-ticker-list', 'children'),
    Input('select-ticker-container', 'children'),
    Input('custom-ticker-input', 'value'),
    Input({'index': ALL, 'type': 'ticker_icon'}, 'n_clicks')
)
def output_custom_tickers(

    table_bond_etfs_data,
    table_stock_indices_data,
    table_magnificent_seven_data,
    table_commodity_etfs_data,
    table_precious_metals_data,
    table_risk_free_treasury_data,
    table_volatility_indices_data,
    table_currency_etfs_data,

    table_bond_etfs_selected_rows,
    table_stock_indices_selected_rows,
    table_magnificent_seven_selected_rows,
    table_commodity_etfs_selected_rows,
    table_precious_metals_selected_rows,
    table_risk_free_treasury_selected_rows,
    table_volatility_indices_selected_rows,
    table_currency_etfs_selected_rows,

    selected_tickers,
    ticker_divs,
    tk_input,
    n_clicks
):

    table_selected_rows = {
        'bond_etfs': table_bond_etfs_selected_rows,
        'stock_indices': table_stock_indices_selected_rows,
        'magnificent_seven': table_magnificent_seven_selected_rows,
        'commodity_etfs': table_commodity_etfs_selected_rows,
        'precious_metals':  table_precious_metals_selected_rows,
        'risk_free_treasury': table_risk_free_treasury_selected_rows,
        'volatility_indices': table_volatility_indices_selected_rows,
        'currency_etfs': table_currency_etfs_selected_rows
    }
    table_data = {
        'bond_etfs': table_bond_etfs_data,
        'stock_indices': table_stock_indices_data,
        'magnificent_seven': table_magnificent_seven_data,
        'commodity_etfs': table_commodity_etfs_data,
        'precious_metals':  table_precious_metals_data,
        'risk_free_treasury': table_risk_free_treasury_data,
        'volatility_indices': table_volatility_indices_data,
        'currency_etfs': table_currency_etfs_data
    }

    table_selected_tickers = {}
    table_nonselected_tickers = {}
    for category in ticker_category_info_map.keys():
        row_map = ticker_category_info_map[category]['row']
        table_selected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]
        table_nonselected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] not in table_selected_rows[category]]

    ctx = dash.callback_context
    # if tk_input is None:
    #     tk_input = ''
    remove_tk = ''

    if 1 in n_clicks:
        if ctx.triggered:
            trig_id_str_list = [ctx.triggered[k]['prop_id'].split('.n_clicks')[0] for k in range(len(ctx.triggered)) if ctx.triggered[k]['value']]
            if len(trig_id_str_list) > 0:
                trig_id_str = trig_id_str_list[0]  # this is a stringified dictionary with whitespaces removed
                remove_tk = trig_id_str.split('{"index":"')[1].split('","type"')[0].replace('select-ticker-icon-', '')  # {tk}

    ticker_divs = [ticker_div_title]

    if selected_tickers is None:
        selected_tickers = []

    updated_tickers = selected_tickers

    hide_ticker_container = False if len(updated_tickers) > 0 else True

    #####
    # Read in ticker from input button

    hide_tk_input_message = True
    hide_custom_ticker_info = True
    tk_input_message = ''
    table_custom_ticker_info = []
    tk_input = tk_input.upper()

    if (tk_input != '') & (tk_input not in selected_tickers):
        
        # _ = yf.download(tk_input, progress = False)
        tk_hist = yf.Ticker(tk_input).history(period = 'max')
        # Unfortunately a failure of yf.Ticker(tk).info query does not add tk to yf.shared._ERRORS
        # yf.Ticker().history() does, but unlike yf.download keeps adding invalid tickers to _ERRORS.keys()
        if tk_input in yf.shared._ERRORS.keys():
            tk_input_message = f'ERROR: Invalid ticker {tk_input}'
            hide_tk_input_message = False
        else:
            updated_tickers.append(tk_input)

            if tk_input not in ticker_info.keys():
                
                tk_start, tk_end = str(tk_hist.index[0].date()), str(tk_hist.index[-1].date())
                tk_info = yf.Ticker(tk_input).info

                if 'longName' in tk_info.keys():
                    tk_name = tk_info['longName']
                elif 'shortName' in tk_info.keys():
                    tk_name = tk_info['shortName']
                else:
                    tk_name = tk_input

                tk_type = tk_info['quoteType'] if 'quoteType' in tk_info.keys() else ''
                tk_exchange = tk_info['exchange'] if 'exchange' in tk_info.keys() else ''
                tk_currency = tk_info['currency'] if 'currency' in tk_info.keys() else ''
                tk_category = tk_info['category'] if 'category' in tk_info.keys() else ''
                tk_industry = tk_info['industry'] if 'industry' in tk_info.keys() else ''
                tk_sector = tk_info['sector'] if 'sector' in tk_info.keys() else ''

                if 'longBusinessSummary' in tk_info.keys():
                    tk_summary = tk_info['longBusinessSummary']
                elif 'description' in tk_info.keys():
                    tk_summary = tk_info['description']
                else: 
                    tk_summary = ''

                ticker_info.update({
                    tk_input: {
                        'name': tk_name,
                        'start': tk_start,
                        'end': tk_end,
                        'type': tk_type,
                        'exchange': tk_exchange,
                        'currency': tk_currency,
                        'category': tk_category,
                        'industry': tk_industry,
                        'sector': tk_sector,
                        'summary': tk_summary
                    }
                })

            else:
                tk_name = ticker_info[tk_input]['name']
                tk_start = ticker_info[tk_input]['start']
                tk_end = ticker_info[tk_input]['end']
                tk_type = ticker_info[tk_input]['type']
                tk_exchange = ticker_info[tk_input]['exchange']
                tk_currency = ticker_info[tk_input]['currency']
                tk_category = ticker_info[tk_input]['category']
                tk_industry = ticker_info[tk_input]['industry']
                tk_sector = ticker_info[tk_input]['sector']
            
            hide_custom_ticker_info = False

            custom_table_data = {
                'INDEX': {
                    'Ticker': tk_input,
                    'Name': tk_name,
                    'Data Start': tk_start,
                    'Data End': tk_end,
                    'Exchange': tk_exchange,
                    'Currency': tk_currency
                },
                'FUTURE': {
                    'Ticker': tk_input,
                    'Name': tk_name,
                    'Data Start': tk_start,
                    'Data End': tk_end,
                    'Exchange': tk_exchange,
                    'Currency': tk_currency
                },
                'EQUITY': {
                    'Ticker': tk_input,
                    'Name': tk_name,
                    'Data Start': tk_start,
                    'Data End': tk_end,
                    'Industry': tk_industry,
                    'Sector': tk_sector,
                    'Exchange': tk_exchange,
                    'Currency': tk_currency
                },
                'ETF': {
                    'Ticker': tk_input,
                    'Name': tk_name,
                    'Data Start': tk_start,
                    'Data End': tk_end,
                    'Category': tk_category,
                    'Exchange': tk_exchange,
                    'Currency': tk_currency
                }
            }

            table_custom_ticker_info = dash_table.DataTable(
                columns = [{'name': i, 'id': i} for i in custom_ticker_table_columns[tk_type]],
                data = [custom_table_data[tk_type]],
                id = 'table-custom-ticker',
                style_header = table_custom_ticker_header_css,
                style_data = table_custom_ticker_data_css
            )
                
    elif (tk_input == '') & (remove_tk != ''):
        hide_tk_input_message = True
        for tk in selected_tickers:
            if tk == remove_tk:
                updated_tickers.remove(tk)

    # Map tk_input to the corresponding row_id and add the latter to selected_rows in all relevant tables

    # table_selected_tickers = {}
    # table_nonselected_tickers = {}
    
    for category in ticker_category_info_map.keys():

        # Must check updated_tickers for tk_input, add it to table_selected_rows if absent    
        row_map = ticker_category_info_map[category]['row']
        if tk_input != '': 
            if (tk_input in row_map.keys()) & (tk_input not in table_selected_tickers[category]):
                table_selected_rows[category].append(row_map[tk_input])
                table_selected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]
    ###
    ###    # table_bond_etfs_selected_tickers = [tk for tk in row_ticker_map_bond_etfs.keys() if row_ticker_map_bond_etfs[tk] in table_bond_etfs_selected_rows]
    ###    # if (tk_input != '') & (tk_input in row_ticker_map_bond_etfs.keys()) & (tk_input not in table_bond_etfs_selected_tickers):
    ###    #     table_bond_etfs_selected_rows.append(row_ticker_map_bond_etfs[tk_input])
    ###    # Remove tickers that are not selected in the table
    ###    # table_bond_etfs_nonselected_tickers = [tk for tk in row_ticker_map_bond_etfs.keys() if row_ticker_map_bond_etfs[tk] not in table_bond_etfs_selected_rows]
    ###    


    table_tickers_remove = []  # This should suffice for all tables
    for tk in updated_tickers:
        for category in ticker_category_info_map.keys():
            row_map = ticker_category_info_map[category]['row']
            if tk in row_map.keys():
                table_nonselected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] not in table_selected_rows[category]]
                if tk in table_nonselected_tickers[category]:
                    if tk not in table_tickers_remove:
                        table_tickers_remove.append(tk)
#     
    for tk in table_tickers_remove:
        # if tk in updated_tickers:  # -- this shouldn't be necessary
        updated_tickers.remove(tk)

    # Read in tickers from all tables

    for category in ticker_category_info_map.keys():
        
        for row_id in range(len(table_data[category])):  # All rows

            tk = table_data[category][row_id]['Ticker']
            # tk_name = table_data[category][row_id]['Name']

            if row_id in table_selected_rows[category]:

                if tk == remove_tk:
                    table_selected_rows[category].remove(row_id)
                    if tk in updated_tickers:
                        updated_tickers.remove(tk)

                elif tk not in updated_tickers:
                    updated_tickers.append(tk)
                    # if tk not in ticker_info.keys():
                    #     ticker_info.update({tk: tk_name})

    #######


    #######

    for tk in updated_tickers:
        
        tk_id = f'select-ticker-{tk}'
        tk_icon_id = f'select-ticker-icon-{tk}'
        name = ticker_info[tk]['name'] if tk in ticker_info.keys() is not None else tk

        tk_type = ticker_info[tk]['type']
        popover_ticker_keys = [
            html.B('Data Start:'), html.Br(),
            html.B('Data End:'), html.Br(),
            html.B('Type:'), html.Br(),
            html.B('Exchange:'), html.Br(),
            html.B('Currency:')
        ]
        popover_ticker_values = [
            html.Span(f"{ticker_info[tk]['start']}"), html.Br(),
            html.Span(f"{ticker_info[tk]['end']}"), html.Br(),
            html.Span(f"{ticker_info[tk]['type']}"), html.Br(),
            html.Span(f"{ticker_info[tk]['exchange']}"), html.Br(),
            html.Span(f"{ticker_info[tk]['currency']}")
        ]
        if tk_type == 'EQUITY':
            popover_ticker_keys.insert(6, html.B('Industry:'))
            popover_ticker_keys.insert(7, html.Br())
            popover_ticker_keys.insert(8, html.B('Sector:'))
            popover_ticker_keys.insert(9, html.Br())
            popover_ticker_values.insert(6, html.Span(f"{ticker_info[tk]['industry']}"))
            popover_ticker_values.insert(7, html.Br())
            popover_ticker_values.insert(8, html.Span(f"{ticker_info[tk]['sector']}"))
            popover_ticker_values.insert(9, html.Br())
        elif tk_type == 'ETF':
            popover_ticker_keys.insert(6, html.B('Category:'))
            popover_ticker_keys.insert(7, html.Br())
            popover_ticker_values.insert(6, html.Span(f"{ticker_info[tk]['category']}"))
            popover_ticker_values.insert(7, html.Br())

        tk_div = html.Div(
            id = tk_id,
            children = [
                html.Div(
                    'x',
                    id = {'index': tk_icon_id, 'type': 'ticker_icon'},
                    n_clicks = 0,
                    style = select_ticker_left_css
                ),
                html.Div(children = [
                    html.B(tk, id = f'select-ticker-label-tk-{tk}', style = {'margin-right': '6px'}),
                    html.Span(name, id = f'select-ticker-label-name-{tk}')
                    ],
                    id = f'select-ticker-label-{tk}',
                    style = select_ticker_right_css
                ),
                dbc.Popover(
                    [
                        html.B(tk, style = popover_select_ticker_header), 
                        html.Div([
                            html.Div(
                                popover_ticker_keys,
                                id = 'popover-select-ticker-keys',
                                style = popover_select_ticker_keys_css
                            ),
                            html.Div(
                                popover_ticker_values,
                                id = 'popover-select-ticker-values',
                                style = popover_select_ticker_values_css
                            )
                            ],
                            style = {'display': 'block'}
                        ),
                        # html.Br(),
                        html.Div(
                            f"{ticker_info[tk]['summary']}",
                            id = 'popover-select-ticker-summary',
                            style = popover_select_ticker_summary
                        )
                    ],
                    id = 'popover-select-ticker',
                    target = f'select-ticker-label-{tk}',
                    body = True,
                    trigger = 'hover',
                    style = popover_select_ticker_css
                ),
            ],
            style = select_ticker_div_css
        )
        ticker_divs.append(tk_div)

    hide_ticker_container = True if len(updated_tickers) == 0 else False

    return (
        ticker_divs,
        hide_ticker_container,
        updated_tickers,
        '',
        hide_tk_input_message,
        hide_custom_ticker_info,
        tk_input_message,
        # custom_ticker_info,
        table_custom_ticker_info,

        table_selected_rows['bond_etfs'],
        table_selected_rows['stock_indices'],
        table_selected_rows['magnificent_seven'],
        table_selected_rows['commodity_etfs'],
        table_selected_rows['precious_metals'],
        table_selected_rows['risk_free_treasury'],
        table_selected_rows['volatility_indices'],
        table_selected_rows['currency_etfs']
    )


def toggle_collapse_tickers(title, n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    # title = 'TOP BOND ETFs'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open

for category in ticker_category_info_map.keys():
    id_string = ticker_category_info_map[category]['id_string']
    app.callback(
        Output(f'collapse-button-table-{id_string}', 'children'),
        Output(f'collapse-table-{id_string}', 'is_open'),
        Input(f'collapse-button-title-{id_string}', 'children'),
        Input(f'collapse-button-table-{id_string}', 'n_clicks'),
        State(f'collapse-table-{id_string}', 'is_open')
    )(toggle_collapse_tickers)


#######################################################################

if __name__ == '__main__':
    app.run_server(debug = True, port = 8055)

