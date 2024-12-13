import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from operator import itemgetter
from mapping_plot_attributes import *
from mapping_portfolio_downloads import *
from mapping_tickers import *
from css_portfolio_analytics import *
from utils import *
from download_info import DownloadInfo

import requests_cache

hist_info = DownloadInfo()

max_tickers = {
    'biggest_companies': 10,
    'sp500': 10,
    'nasdaq100': 10,
    'dow_jones': 35,
    'biggest_etfs': 10,
    'fixed_income_etfs': 10,
    'ai_etfs': 30,
    'commodity_etfs': 20,
    'currency_etfs': 10,
    'cryptos': 10,
    'crypto_etfs': 10,
    'futures': 50,
    'precious_metals': 5,
    'stock_indices': 19,
    'volatility_indices': 5,
    'benchmarks': 20
}
etf_categories = [
    'biggest_etfs',
    'fixed_income_etfs',
    'ai_etfs',
    'commodity_etfs',
    'currency_etfs',
    'crypto_etfs'
]

df_url_biggest_companies = hist_info.download_from_url('biggest_companies', max_tickers['biggest_companies'])
dict_biggest_companies = df_url_biggest_companies[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_biggest_companies = list(dict_biggest_companies.keys())

df_url_sp500 = hist_info.download_from_url('sp500', max_tickers['sp500'])
dict_sp500 = df_url_sp500[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_sp500 = list(dict_sp500.keys())

df_url_nasdaq100 = hist_info.download_from_url('nasdaq100', max_tickers['nasdaq100'])  # Currently there are 101 companies
dict_nasdaq100 = df_url_nasdaq100[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_nasdaq100 = list(dict_nasdaq100.keys())

df_url_dow_jones = hist_info.download_from_url('dow_jones', max_tickers['dow_jones'])
dict_dow_jones = df_url_dow_jones[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_dow_jones = list(dict_dow_jones.keys())

df_url_biggest_etfs = hist_info.download_from_url('biggest_etfs', max_tickers['biggest_etfs'])
dict_biggest_etfs = df_url_biggest_etfs[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_biggest_etfs = list(dict_biggest_etfs.keys())

df_url_fixed_income_etfs = hist_info.download_from_url('fixed_income_etfs', max_tickers['fixed_income_etfs'])
dict_fixed_income_etfs = df_url_fixed_income_etfs[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_fixed_income_etfs = list(dict_fixed_income_etfs.keys())

df_url_ai_etfs = hist_info.download_from_url('ai_etfs', max_tickers['ai_etfs'])
dict_ai_etfs = df_url_ai_etfs[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_ai_etfs = list(dict_ai_etfs.keys())

df_url_futures = hist_info.download_from_url('futures', max_tickers['futures'])
dict_futures = df_url_futures[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_futures = list(dict_futures.keys())

df_url_cryptos = hist_info.download_from_url('cryptos', max_tickers['cryptos'])
dict_cryptos = df_url_cryptos[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_cryptos = list(dict_cryptos.keys())

df_url_crypto_etfs = hist_info.download_from_url('crypto_etfs', max_tickers['crypto_etfs'])
dict_crypto_etfs = df_url_crypto_etfs[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
tickers_crypto_etfs = list(dict_crypto_etfs.keys())

tickers_stock_indices = list(stock_index_tickers.keys())
tickers_precious_metals = list(precious_metals.keys())
tickers_commodity_etfs = list(commodity_etf_tickers.keys())
tickers_risk_free_treasury = list(risk_free_treasury_tickers.keys())
tickers_volatility_indices = list(volatility_tickers.keys())
tickers_currency_etfs = list(currency_etf_tickers.keys())
tickers_benchmarks = list(benchmark_tickers.keys())

input_table_columns_indices = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Category', 'Exchange', 'Currency']
input_table_columns_futures = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency']
input_table_columns_equities = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Industry', 'Sector', 'Exchange', 'Currency']
input_table_columns_etfs = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Category', 'Exchange', 'Currency']
input_table_columns_cryptos = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency']
input_table_columns_benchmarks = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Category', 'Exchange', 'Currency']

custom_ticker_table_columns = {
    'INDEX': ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Category', 'Exchange', 'Currency'],
    'FUTURE': ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Exchange', 'Currency'],
    'EQUITY': ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Industry', 'Sector', 'Exchange', 'Currency'],
    'ETF': ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Category', 'Exchange', 'Currency'],
    'CRYPTOCURRENCY': ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Exchange', 'Currency']
}

# NOTE: The ticker categories and the number of tickers to download the info of in each of them will be specified by the user
#       on the page preceding the ticker selection page.

df_info_url_biggest_companies = pd.DataFrame(index = tickers_biggest_companies, columns = input_table_columns_equities)
df_info_url_sp500 = pd.DataFrame(index = tickers_sp500, columns = input_table_columns_equities)
df_info_url_nasdaq100 = pd.DataFrame(index = tickers_nasdaq100, columns = input_table_columns_equities)
df_info_url_dow_jones = pd.DataFrame(index = tickers_dow_jones, columns = input_table_columns_equities)
df_info_url_biggest_etfs = pd.DataFrame(index = tickers_biggest_etfs, columns = input_table_columns_etfs)
df_info_url_fixed_income_etfs = pd.DataFrame(index = tickers_fixed_income_etfs, columns = input_table_columns_etfs)
df_info_url_ai_etfs = pd.DataFrame(index = tickers_ai_etfs, columns = input_table_columns_etfs)
df_info_url_futures = pd.DataFrame(index = tickers_futures, columns = input_table_columns_futures)
df_info_url_cryptos = pd.DataFrame(index = tickers_cryptos, columns = input_table_columns_cryptos)
df_info_url_crypto_etfs = pd.DataFrame(index = tickers_crypto_etfs, columns = input_table_columns_etfs)

df_info_tickers_stock_indices = pd.DataFrame(index = tickers_stock_indices, columns = input_table_columns_indices)
df_info_tickers_commodity_etfs = pd.DataFrame(index = tickers_commodity_etfs, columns = input_table_columns_etfs)
df_info_tickers_precious_metals = pd.DataFrame(index = tickers_precious_metals, columns = input_table_columns_futures)
df_info_tickers_risk_free_treasury = pd.DataFrame(index = tickers_risk_free_treasury, columns = input_table_columns_indices)
df_info_tickers_volatility_indices = pd.DataFrame(index = tickers_volatility_indices, columns = input_table_columns_indices)
df_info_tickers_currency_etfs = pd.DataFrame(index = tickers_currency_etfs, columns = input_table_columns_etfs)
df_info_tickers_benchmarks = pd.DataFrame(index = tickers_benchmarks, columns = input_table_columns_benchmarks)

row_ticker_map_biggest_companies = {}
row_ticker_map_sp500 = {}
row_ticker_map_nasdaq100 = {}
row_ticker_map_dow_jones = {}
row_ticker_map_biggest_etfs = {}
row_ticker_map_fixed_income_etfs = {}
row_ticker_map_ai_etfs = {}
row_ticker_map_commodity_etfs = {}
row_ticker_map_currency_etfs = {}
row_ticker_map_cryptos = {}
row_ticker_map_crypto_etfs = {}
row_ticker_map_futures = {}
row_ticker_map_precious_metals = {}
row_ticker_map_stock_indices = {}
row_ticker_map_volatility_indices = {}
row_ticker_map_benchmarks = {}

ticker_category_info_map = {
    'biggest_companies': {
        'df': df_info_url_biggest_companies,
        'row': row_ticker_map_biggest_companies,
        'dict': dict_biggest_companies,
        'sort_by': '',
        'id_string': 'biggest-companies',
        'collapse_title': 'BIGGEST COMPANIES'
    },
    'sp500': {
        'df': df_info_url_sp500,
        'row': row_ticker_map_sp500,
        'dict': dict_sp500,
        'sort_by': '',
        'id_string': 'sp500',
        'collapse_title': 'S&P 500 COMPANIES'
    },
    'nasdaq100': {
        'df': df_info_url_nasdaq100,
        'row': row_ticker_map_nasdaq100,
        'dict': dict_nasdaq100,
        'sort_by': '',
        'id_string': 'nasdaq100',
        'collapse_title': 'NASDAQ 100 COMPANIES'
    },
    'dow_jones': {
        'df': df_info_url_dow_jones,
        'row': row_ticker_map_dow_jones,
        'dict': dict_dow_jones,
        'sort_by': '',
        'id_string': 'dow-jones',
        'collapse_title': 'DOW JONES INDUSTRIAL AVERAGE COMPANIES'
    },
    'biggest_etfs': {
        'df': df_info_url_biggest_etfs,
        'row': row_ticker_map_biggest_etfs,
        'dict': dict_biggest_etfs,
        'sort_by': '',
        'id_string': 'biggest-etfs',
        'collapse_title': 'BIGGEST ETFs'
    },
    'fixed_income_etfs': {
        'df': df_info_url_fixed_income_etfs,
        'row': row_ticker_map_fixed_income_etfs,
        'dict': dict_fixed_income_etfs,
        'sort_by': '',
        'id_string': 'fixed-income-etfs',
        'collapse_title': 'FIXED INCOME ETFs'
    },
    'ai_etfs': {
        'df': df_info_url_ai_etfs,
        'row': row_ticker_map_ai_etfs,
        'dict': dict_ai_etfs,
        'sort_by': '',
        'id_string': 'ai-etfs',
        'collapse_title': 'ARTIFICIAL INTELLIGENCE ETFs'
    },
    'commodity_etfs': {
        'df': df_info_tickers_commodity_etfs,
        'row': row_ticker_map_commodity_etfs,
        'dict': commodity_etf_tickers,
        'sort_by': 'totalAssets',
        'id_string': 'commodity-etfs',
        'collapse_title': 'COMMODITY ETFs'
    },
    'currency_etfs': {
        'df': df_info_tickers_currency_etfs,
        'row': row_ticker_map_currency_etfs,
        'dict': currency_etf_tickers,
        'sort_by': 'totalAssets',
        'id_string': 'currency-etfs',
        'collapse_title': 'CURRENCY ETFs'
    },
    'cryptos': {
        'df': df_info_url_cryptos,
        'row': row_ticker_map_cryptos,
        'dict': dict_cryptos,
        'sort_by': '',
        'id_string': 'cryptos',
        'collapse_title': 'CRYPTOCURRENCIES'
    },
    'crypto_etfs': {
        'df': df_info_url_crypto_etfs,
        'row': row_ticker_map_crypto_etfs,
        'dict': dict_crypto_etfs,
        'sort_by': '',
        'id_string': 'crypto-etfs',
        'collapse_title': 'CRYPTOCURRENCY ETFs'
    },
    'futures': {
        'df': df_info_url_futures,
        'row': row_ticker_map_futures,
        'dict': dict_futures,
        'sort_by': '',
        'id_string': 'futures',
        'collapse_title': 'COMMODITY FUTURES'
    },
    'precious_metals': {
        'df': df_info_tickers_precious_metals,
        'row': row_ticker_map_precious_metals,
        'dict': precious_metals,
        'sort_by': 'openInterest',
        'id_string': 'precious-metals',
        'collapse_title': 'PRECIOUS METALS'
    },
    'stock_indices': {
        'df': df_info_tickers_stock_indices,
        'row': row_ticker_map_stock_indices,
        'dict': stock_index_tickers,
        'sort_by': '',  # Only some indices have 'volume' in info
        'id_string': 'stock-indices',
        'collapse_title': 'STOCK INDICES'
    },
    'volatility_indices': {
        'df': df_info_tickers_volatility_indices,
        'row': row_ticker_map_volatility_indices,
        'dict': volatility_tickers,
        'sort_by': '',  # No 'volume' in info
        'id_string': 'volatility-indices',
        'collapse_title': 'VOLATILITY INDICES'
    },
    'benchmarks': {
        'df': df_info_tickers_benchmarks,
        'row': row_ticker_map_benchmarks,
        'dict': benchmark_tickers,
        'sort_by': '',
        'id_string': 'benchmarks',
        'collapse_title': 'BENCHMARKS'
    }
}

ticker_info = {}  # To help user decide on tickers based on the name and data start and end dates

def create_input_table(category):

    session = requests_cache.CachedSession('cache/yfinance.cache')
    session.headers['User-agent'] = url_settings['global']['headers']

    df_info_tickers = ticker_category_info_map[category]['df']
    row_ticker_map = ticker_category_info_map[category]['row']
    dict_info_tickers = ticker_category_info_map[category]['dict']
    tk_sort_by = ticker_category_info_map[category]['sort_by']
    
    category_tickers = list(dict_info_tickers.keys())
    n_tickers = min(len(category_tickers), max_tickers[category])
    category_tickers = category_tickers[: n_tickers]
    df_info_tickers = df_info_tickers[: n_tickers]
    max_tickers[category] = n_tickers
    ### Create a function that takes max_tickers as an argument and returns category table title

    category_tickers_sorted = category_tickers

    # Sort ticker list by marketCap (equities), totalAssets (ETFs) or openInterest (futures)
    if tk_sort_by != '':
        dict_tickers_values = {tk: yf.Ticker(tk, session = session).info[tk_sort_by] for tk in category_tickers}
        category_tickers_sorted = [i[0] for i in sorted(dict_tickers_values.items(), key = itemgetter(1), reverse = True)]
        df_info_tickers.index = category_tickers_sorted

    for i, tk in enumerate(category_tickers_sorted):

        if tk not in ticker_info.keys():
            
            yf_ticker = yf.Ticker(tk, session = session)

            # The scraped response will be stored in the cache
            # yf_ticker.actions

            tk_hist = yf_ticker.history(period = 'max')
            tk_info = yf_ticker.info
            # Should also check if ticker is still valid, for now assume they're all valid

            if 'quoteType' in tk_info.keys():
                # This is meant to indicate a valid ticker
                # tk_hist may be temporarily empty for a valid ticker

                if len(tk_hist.index) > 0:
                    tk_start, tk_end = str(tk_hist.index[0].date()), str(tk_hist.index[-1].date())
                else:
                    tk_start, tk_end = 'N/A', 'N/A'

                df_info_tickers.at[tk, 'No.'] = i + 1
                df_info_tickers.at[tk, 'Ticker'] = tk

                if 'longName' in tk_info.keys():
                    tk_name = tk_info['longName']
                elif 'shortName' in tk_info.keys():
                    tk_name = tk_info['shortName']
                else:
                    tk_name = dict_info_tickers[tk]

                if category in etf_categories:
                    tk_type = 'ETF'
                else:
                    tk_type = tk_info['quoteType'] if 'quoteType' in tk_info.keys() else ''

                if category == 'crypto_etfs':
                    tk_category = 'Digital Assets'
                elif category in ['stock_indices', 'volatility_indices', 'benchmarks']:
                    if tk_type == 'INDEX':
                        tk_category = indices_custom_info[tk]['category']
                else:
                    tk_category = tk_info['category'] if 'category' in tk_info.keys() else ''

                tk_exchange = tk_info['exchange'] if 'exchange' in tk_info.keys() else ''
                tk_currency = tk_info['currency'] if 'currency' in tk_info.keys() else ''
                tk_industry = tk_info['industry'] if 'industry' in tk_info.keys() else ''
                tk_sector = tk_info['sector'] if 'sector' in tk_info.keys() else ''

                if 'longBusinessSummary' in tk_info.keys():
                    tk_summary = tk_info['longBusinessSummary']
                elif 'description' in tk_info.keys():
                    tk_summary = tk_info['description']
                elif category in ['stock_indices', 'volatility_indices', 'benchmarks']:
                    tk_summary = indices_custom_info[tk]['description']
                else: 
                    tk_summary = ''

                df_info_tickers.at[tk, 'Name'] = tk_name
                df_info_tickers.at[tk, 'Data Start'] = tk_start
                df_info_tickers.at[tk, 'Data End'] = tk_end
                df_info_tickers.at[tk, 'Exchange'] = tk_exchange
                df_info_tickers.at[tk, 'Currency'] = tk_currency

                if category == 'benchmarks':
                    df_info_tickers.at[tk, 'Type'] = tk_type

                if tk_type in ['ETF', 'INDEX']:
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

                row_ticker_map.update({tk: i})

            else:
                print(f'WARNING: Cannot get data for {tk} at the moment, try again later')
                df_info_tickers = df_info_tickers[df_info_tickers.index != tk]
    
        else:

            df_info_tickers.at[tk, 'No.'] = i + 1
            df_info_tickers.at[tk, 'Ticker'] = tk
            df_info_tickers.at[tk, 'Name'] = ticker_info[tk]['name']
            df_info_tickers.at[tk, 'Data Start'] = ticker_info[tk]['start']
            df_info_tickers.at[tk, 'Data End'] = ticker_info[tk]['end']
            df_info_tickers.at[tk, 'Exchange'] = ticker_info[tk]['exchange']
            df_info_tickers.at[tk, 'Currency'] = ticker_info[tk]['currency']

            if category == 'benchmarks':
                df_info_tickers.at[tk, 'Type'] = ticker_info[tk]['type']

            if ticker_info[tk]['type'] in ['ETF', 'INDEX']:
                df_info_tickers.at[tk, 'Category'] = ticker_info[tk]['category']
            elif ticker_info[tk]['type'] == 'EQUITY':
                df_info_tickers.at[tk, 'Industry'] = ticker_info[tk]['industry']
                df_info_tickers.at[tk, 'Sector'] = ticker_info[tk]['sector']

            row_ticker_map.update({tk: i})

    session.cache.clear()

    input_table_data = {
        'df': df_info_tickers,
        'row': row_ticker_map,
        'maxn': n_tickers
    }

    return input_table_data


for category in ticker_category_info_map.keys():
    print(f'\nProcessing info for {category} ...')
    input_table_data = create_input_table(category)
    ticker_category_info_map[category]['df'] = input_table_data['df']
    ticker_category_info_map[category]['row'] = input_table_data['row']
    max_tickers.update({category: input_table_data['maxn']})
    print(ticker_category_info_map[category]['df'])
    print(ticker_category_info_map[category]['row'])

input_table_titles = {
    'biggest_companies': f'{max_tickers["biggest_companies"]} BIGGEST COMPANIES by Market Capitalization',
    'sp500': f'TOP {max_tickers["sp500"]} S&P 500 COMPANIES by Market Capitalization',
    'nasdaq100': f'TOP {max_tickers["nasdaq100"]} NASDAQ 100 COMPANIES by Market Capitalization',
    'dow_jones': f'TOP {max_tickers["dow_jones"]} DOW JONES INDUSTRIAL AVERAGE COMPANIES by Market Capitalization',
    'biggest_etfs': f'{max_tickers["biggest_etfs"]} BIGGEST ETFs by Total Assets Under Management',
    'fixed_income_etfs': f'TOP {max_tickers["fixed_income_etfs"]} FIXED INCOME ETFs by Total Assets Under Management',
    'ai_etfs': f'TOP {max_tickers["ai_etfs"]} ARTIFICIAL INTELLIGENCE ETFs by Total Assets Under Management',
    'commodity_etfs': f'{max_tickers["commodity_etfs"]} COMMODITY ETFs sorted by Total Assets Under Management',
    'currency_etfs': f'{max_tickers["currency_etfs"]} CURRENCY ETFs sorted by Total Assets Under Management',
    'cryptos': f'TOP {max_tickers["cryptos"]} CRYPTOCURRENCIES by Market Capitalization',
    'crypto_etfs': f'TOP {max_tickers["crypto_etfs"]} CRYPTOCURRENCY ETFs by Total Assets Under Management',
    'futures': f'TOP {max_tickers["futures"]} COMMODITY FUTURES by Open Interest',
    'precious_metals': f'{max_tickers["precious_metals"]} PRECIOUS METAL SPOT / FUTURES sorted by Open Interest',
    'stock_indices': f'{max_tickers["stock_indices"]} STOCK INDICES',
    'volatility_indices': f'{max_tickers["volatility_indices"]} VOLATILITY INDICES',
    'benchmarks': f'{max_tickers["benchmarks"]} BENCHMARKS'
}
# NOTE:
# After the preliminary selection on the preceding page, the above titles will be changed to something like:
# f'{pre_n_tickers} PRE-SELECTED COMMODITY FUTURES sorted by Open Interest'
# 

print(f'\nTotal tickers: {len(ticker_info)}')

##############

ticker_div_title = html.Div(
    'YOUR PORTFOLIO:',
    style = select_ticker_title_css
)

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
                            children = input_table_titles[category],
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

###########################################################################################

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])

app.layout = html.Div([

    html.Div(id = 'ticker-output', hidden = True, style = {'font-size' : '14px'}),

    # MAIN TITLE
    html.Div(
        'Add tickers to your portfolio by typing in the Add Ticker box or selecting from the lists below',
        id = 'ticker-main-title',
        style = ticker_main_title_css
    ),

    html.Div(id = 'select-ticker-list', hidden = True),

    # html.Div(children = [], id = 'prev-table-selected-rows', hidden = True),
    dcc.Store(data = {}, id = 'prev-table-selected-rows'),

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

# row_ticker_map_biggest_companies = {}
# row_ticker_map_sp500 = {}
# row_ticker_map_nasdaq100 = {}
# row_ticker_map_dow_jones = {}
# row_ticker_map_biggest_etfs = {}
# row_ticker_map_fixed_income_etfs = {}
# row_ticker_map_ai_etfs = {}
# row_ticker_map_commodity_etfs = {}
# row_ticker_map_currency_etfs = {}
# row_ticker_map_cryptos = {}
# row_ticker_map_crypto_etfs = {}
# row_ticker_map_futures = {}
# row_ticker_map_precious_metals = {}
# row_ticker_map_stock_indices = {}
# row_ticker_map_volatility_indices = {}
# row_ticker_map_risk_free_treasury = {}

@app.callback(
    Output('select-ticker-container', 'children'),
    Output('select-ticker-container', 'hidden'),
    Output('select-ticker-list', 'children'),
    Output('custom-ticker-input', 'value'),
    Output('custom-ticker-input-message', 'hidden'),
    Output('custom-ticker-info-container', 'hidden'),
    Output('custom-ticker-input-message', 'children'),
    Output('table-custom-ticker-info', 'children'),
    Output('prev-table-selected-rows', 'data'),

    Output('table-biggest-companies', 'selected_rows'),
    Output('table-sp500', 'selected_rows'),
    Output('table-nasdaq100', 'selected_rows'),
    Output('table-dow-jones', 'selected_rows'),
    Output('table-biggest-etfs', 'selected_rows'),
    Output('table-fixed-income-etfs', 'selected_rows'),
    Output('table-ai-etfs', 'selected_rows'),
    Output('table-commodity-etfs', 'selected_rows'),
    Output('table-currency-etfs', 'selected_rows'),
    Output('table-cryptos', 'selected_rows'),
    Output('table-crypto-etfs', 'selected_rows'),
    Output('table-futures', 'selected_rows'),
    Output('table-precious-metals', 'selected_rows'),
    Output('table-stock-indices', 'selected_rows'),
    Output('table-volatility-indices', 'selected_rows'),
    Output('table-benchmarks', 'selected_rows'),

    Input('table-biggest-companies', 'data'),
    Input('table-sp500', 'data'),
    Input('table-nasdaq100', 'data'),
    Input('table-dow-jones', 'data'),    
    Input('table-biggest-etfs', 'data'),
    Input('table-fixed-income-etfs', 'data'),
    Input('table-ai-etfs', 'data'),    
    Input('table-commodity-etfs', 'data'),
    Input('table-currency-etfs', 'data'),
    Input('table-cryptos', 'data'),
    Input('table-crypto-etfs', 'data'),    
    Input('table-futures', 'data'),    
    Input('table-precious-metals', 'data'),
    Input('table-stock-indices', 'data'),
    Input('table-volatility-indices', 'data'),
    Input('table-benchmarks', 'data'),

    Input('table-biggest-companies', 'selected_rows'),
    Input('table-sp500', 'selected_rows'),
    Input('table-nasdaq100', 'selected_rows'),
    Input('table-dow-jones', 'selected_rows'),
    Input('table-biggest-etfs', 'selected_rows'),
    Input('table-fixed-income-etfs', 'selected_rows'),
    Input('table-ai-etfs', 'selected_rows'),
    Input('table-commodity-etfs', 'selected_rows'),
    Input('table-currency-etfs', 'selected_rows'),
    Input('table-cryptos', 'selected_rows'),
    Input('table-crypto-etfs', 'selected_rows'),
    Input('table-futures', 'selected_rows'),
    Input('table-precious-metals', 'selected_rows'),
    Input('table-stock-indices', 'selected_rows'),
    Input('table-volatility-indices', 'selected_rows'),
    Input('table-benchmarks', 'selected_rows'),

    Input('select-ticker-list', 'children'),
    Input('prev-table-selected-rows', 'data'),
    Input('select-ticker-container', 'children'),
    Input('custom-ticker-input', 'value'),
    Input({'index': ALL, 'type': 'ticker_icon'}, 'n_clicks')
)
def output_custom_tickers(

    table_biggest_companies_data,
    table_sp500_data,
    table_nasdaq100_data,
    table_dow_jones_data,
    table_biggest_etfs_data,
    table_fixed_income_etfs_data,
    table_ai_etfs_data,
    table_commodity_etfs_data,
    table_currency_etfs_data,
    table_cryptos_data,
    table_crypto_etfs_data,
    table_futures_data,
    table_precious_metals_data,
    table_stock_indices_data,
    table_volatility_indices_data,
    table_benchmarks_data,

    table_biggest_companies_selected_rows,
    table_sp500_selected_rows,
    table_nasdaq100_selected_rows,
    table_dow_jones_selected_rows,
    table_biggest_etfs_selected_rows,
    table_fixed_income_etfs_selected_rows,
    table_ai_etfs_selected_rows,
    table_commodity_etfs_selected_rows,
    table_currency_etfs_selected_rows,
    table_cryptos_selected_rows,
    table_crypto_etfs_selected_rows,
    table_futures_selected_rows,
    table_precious_metals_selected_rows,
    table_stock_indices_selected_rows,
    table_volatility_indices_selected_rows,
    table_benchmarks_selected_rows,

    selected_tickers,
    prev_table_selected_rows,
    ticker_divs,
    tk_input,
    n_clicks
):

    table_selected_rows = {
        'biggest_companies': table_biggest_companies_selected_rows,
        'sp500': table_sp500_selected_rows,
        'nasdaq100': table_nasdaq100_selected_rows,
        'dow_jones': table_dow_jones_selected_rows,
        'biggest_etfs': table_biggest_etfs_selected_rows,
        'fixed_income_etfs': table_fixed_income_etfs_selected_rows,
        'ai_etfs': table_ai_etfs_selected_rows,
        'commodity_etfs': table_commodity_etfs_selected_rows,
        'currency_etfs': table_currency_etfs_selected_rows,
        'cryptos': table_cryptos_selected_rows,
        'crypto_etfs': table_crypto_etfs_selected_rows,
        'futures': table_futures_selected_rows,
        'precious_metals': table_precious_metals_selected_rows,
        'stock_indices': table_stock_indices_selected_rows,
        'volatility_indices': table_volatility_indices_selected_rows,
        'benchmarks': table_benchmarks_selected_rows
    }
    # table_data = {
    #     'biggest_companies': table_biggest_companies_data,
    #     'sp500': table_sp500_data,
    #     'nasdaq100': table_nasdaq100_data,
    #     'dow_jones': table_dow_jones_data,
    #     'biggest_etfs': table_biggest_etfs_data,
    #     'fixed_income_etfs': table_fixed_income_etfs_data,
    #     'ai_etfs': table_ai_etfs_data,
    #     'commodity_etfs': table_commodity_etfs_data,
    #     'currency_etfs': table_currency_etfs_data,
    #     'cryptos': table_cryptos_data,
    #     'crypto_etfs': table_crypto_etfs_data,
    #     'futures': table_futures_data,
    #     'precious_metals': table_precious_metals_data,
    #     'stock_indices': table_stock_indices_data,
    #     'volatility_indices': table_volatility_indices_data,
    #     'benchmarks': table_benchmarks_data
    # }

    if prev_table_selected_rows == {}:
        for category in ticker_category_info_map.keys():
            prev_table_selected_rows[category] = []

    table_selected_tickers = {}
    table_nonselected_tickers = {}
    for category in ticker_category_info_map.keys():
        row_map = ticker_category_info_map[category]['row']
        table_selected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]
        table_nonselected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] not in table_selected_rows[category]]

    ctx = dash.callback_context

    added_ticker = ''
    removed_ticker = ''

    if 1 in n_clicks:
        if ctx.triggered:
            trig_id_str_list = [ctx.triggered[k]['prop_id'].split('.n_clicks')[0] for k in range(len(ctx.triggered)) if ctx.triggered[k]['value']]
            if len(trig_id_str_list) > 0:
                trig_id_str = trig_id_str_list[0]  # this is a stringified dictionary with whitespaces removed
                removed_ticker = trig_id_str.split('{"index":"')[1].split('","type"')[0].replace('select-ticker-icon-', '')  # {tk}

    ticker_divs = [ticker_div_title]

    if selected_tickers is None:
        selected_tickers = []

    updated_tickers = selected_tickers

    hide_ticker_container = False if len(updated_tickers) > 0 else True

    ##### INPUT BUTTON
    # Read in custom-specified ticker from input button

    hide_tk_input_message = True
    hide_custom_ticker_info = True
    tk_input_message = ''
    table_custom_ticker_info = []
    tk_input = tk_input.upper()

    if (tk_input != '') & (tk_input not in updated_tickers):
        
        session = requests_cache.CachedSession('cache/yfinance.cache')
        session.headers['User-agent'] = url_settings['global']['headers']

        yf_ticker_input = yf.Ticker(tk_input, session = session)
        # yf_ticker_input.actions

        # _ = yf.download(tk_input, progress = False)
        tk_hist = yf_ticker_input.history(period = 'max')
        tk_info = yf_ticker_input.info
        # Unfortunately a failure of yf.Ticker(tk).info query does not add tk to yf.shared._ERRORS
        # yf.Ticker().history() does, but unlike yf.download keeps adding invalid tickers to _ERRORS.keys()
        if 'quoteType' not in tk_info.keys():
            # No info, therefore an invalid ticker
            tk_input_message = f'ERROR: Invalid ticker {tk_input}'
            hide_tk_input_message = False

        elif tk_info['quoteType'] not in custom_ticker_table_columns.keys():
            # Info available but quoteType is unknown
            # tk_input_message = f"ERROR: Unknown ticker type {tk_info['quoteType']} for {tk_input}"
            # To avoid tickers like 'BOO', which has quoteType MUTUALFUND but only a cryptic name 79110
            tk_input_message = f'ERROR: Unknown ticker type for {tk_input}'
            hide_tk_input_message = False

        else:

            updated_tickers.append(tk_input)

            if tk_input in yf.shared._ERRORS.keys():
                tk_start, tk_end = 'N/A', 'N/A'
            else:
                tk_start, tk_end = str(tk_hist.index[0].date()), str(tk_hist.index[-1].date())

            if tk_input not in ticker_info.keys():
                
                if 'longName' in tk_info.keys():
                    tk_name = tk_info['longName']
                elif 'shortName' in tk_info.keys():
                    tk_name = tk_info['shortName']
                else:
                    tk_name = tk_input
                # if category in etf_categories:
                #     tk_type = 'ETF'
                # else:
                tk_type = tk_info['quoteType'] if 'quoteType' in tk_info.keys() else ''
                # if category == 'crypto_etfs':
                #     tk_category = 'Digital Assets'
                # elif category in ['stock_indices', 'volatility_indices']:
                #     tk_category = indices_custom_info[tk_input]['category']                    
                # else:
                tk_category = tk_info['category'] if 'category' in tk_info.keys() else ''
                tk_exchange = tk_info['exchange'] if 'exchange' in tk_info.keys() else ''
                tk_currency = tk_info['currency'] if 'currency' in tk_info.keys() else ''
                tk_industry = tk_info['industry'] if 'industry' in tk_info.keys() else ''
                tk_sector = tk_info['sector'] if 'sector' in tk_info.keys() else ''
                if 'longBusinessSummary' in tk_info.keys():
                    tk_summary = tk_info['longBusinessSummary']
                elif 'description' in tk_info.keys():
                    tk_summary = tk_info['description']
                elif category in ['stock_indices', 'volatility_indices']:
                    tk_summary = indices_custom_info[tk]['description']                    
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
                    'Type': tk_type,
                    'Category': tk_category,
                    'Exchange': tk_exchange,
                    'Currency': tk_currency
                },
                'FUTURE': {
                    'Ticker': tk_input,
                    'Name': tk_name,
                    'Data Start': tk_start,
                    'Data End': tk_end,
                    'Type': tk_type,
                    'Exchange': tk_exchange,
                    'Currency': tk_currency
                },
                'EQUITY': {
                    'Ticker': tk_input,
                    'Name': tk_name,
                    'Data Start': tk_start,
                    'Data End': tk_end,
                    'Type': tk_type,
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
                    'Type': tk_type,
                    'Category': tk_category,
                    'Exchange': tk_exchange,
                    'Currency': tk_currency
                },
                'CRYPTOCURRENCY': {
                    'Ticker': tk_input,
                    'Name': tk_name,
                    'Data Start': tk_start,
                    'Data End': tk_end,
                    'Type': tk_type,
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

        session.cache.clear()

    elif (tk_input == '') & (removed_ticker != ''):
        hide_tk_input_message = True
        for tk in selected_tickers:
            if tk == removed_ticker:
                updated_tickers.remove(tk)

    # Add tk_input to selected_rows in all relevant tables if not there yet
    for category in ticker_category_info_map.keys():
        row_map = ticker_category_info_map[category]['row']
        if tk_input != '': 
            if (tk_input in row_map.keys()) & (tk_input not in table_selected_tickers[category]):
                table_selected_rows[category].append(row_map[tk_input])
                table_selected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]

    ##### INPUT TABLES
    # Check whether a ticker was added to or removed from any table

    for category in ticker_category_info_map.keys():
        row_map = ticker_category_info_map[category]['row']
        df_info = ticker_category_info_map[category]['df']
        selected_rows = [k for k in table_selected_rows[category] if k not in prev_table_selected_rows[category]]
        if len(selected_rows) > 0:
            added_ticker = df_info.index[df_info['No.'] == 1 + selected_rows[0]][0]
            if added_ticker not in updated_tickers:
                updated_tickers.append(added_ticker)
            break
        else:
            unselected_rows = [k for k in prev_table_selected_rows[category] if k not in table_selected_rows[category]]
            if len(unselected_rows) > 0:
                removed_ticker = df_info.index[df_info['No.'] == 1 + unselected_rows[0]][0]
                if removed_ticker in updated_tickers:
                    updated_tickers.remove(removed_ticker)
                break

    # Make sure added_ticker is selected in all tables and removed_ticker is removed from all tables
    if added_ticker != '':
        for category in ticker_category_info_map.keys():
            df_info = ticker_category_info_map[category]['df']
            if added_ticker in df_info['Ticker']:
                row_map = ticker_category_info_map[category]['row']
                if row_map[added_ticker] not in table_selected_rows[category]:
                    table_selected_rows[category].append(row_map[added_ticker])

    if removed_ticker != '':
        for category in ticker_category_info_map.keys():
            df_info = ticker_category_info_map[category]['df']
            if removed_ticker in df_info['Ticker']:
                row_map = ticker_category_info_map[category]['row']
                if row_map[removed_ticker] in table_selected_rows[category]:
                    table_selected_rows[category].remove(row_map[removed_ticker])

    ##### SELECTED TICKERS
    # Set up selected tickers divs and popovers

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
        elif tk_type in ['ETF', 'INDEX']:
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
        '',  # Clear custom ticker input button value
        hide_tk_input_message,
        hide_custom_ticker_info,
        tk_input_message,
        table_custom_ticker_info,
        table_selected_rows,

        table_selected_rows['biggest_companies'],
        table_selected_rows['sp500'],
        table_selected_rows['nasdaq100'],
        table_selected_rows['dow_jones'],
        table_selected_rows['biggest_etfs'],
        table_selected_rows['fixed_income_etfs'],
        table_selected_rows['ai_etfs'],
        table_selected_rows['commodity_etfs'],
        table_selected_rows['currency_etfs'],
        table_selected_rows['cryptos'],
        table_selected_rows['crypto_etfs'],
        table_selected_rows['futures'],
        table_selected_rows['precious_metals'],
        table_selected_rows['stock_indices'],
        table_selected_rows['volatility_indices'],
        table_selected_rows['benchmarks']
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
    app.run_server(debug = True, port = 8056)
    # app.run_server(debug = False, port = 8056)


