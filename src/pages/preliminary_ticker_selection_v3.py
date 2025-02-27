import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls

from dash import register_page

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


register_page(
    __name__,
    path = '/preliminary_ticker_selection_v3'
    # page_components = [html.Div('')]
)

hist_info = DownloadInfo()

max_tickers = {
    'biggest_companies': 100,
    'sp500': 100,
    'nasdaq100': 120,
    'dow_jones': 35,
    # 'car_companies': 75,
    'car_companies': 10,
    'rare_metals_companies': 20,
    'biggest_etfs': 100,
    'fixed_income_etfs': 100,
    'ai_etfs': 50,
    'commodity_etfs': 20,
    'currency_etfs': 10,
    'cryptos': 100, 
    'crypto_etfs': 100,
    'futures': 100,
    'precious_metals': 5,
    'stock_indices': 20,
    'volatility_indices': 10,
    'benchmarks': 30
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

tickers_car_companies = list(car_companies.keys())
tickers_rare_metals_companies = list(rare_metals_companies.keys())
tickers_stock_indices = list(stock_index_tickers.keys())
tickers_precious_metals = list(precious_metals.keys())
tickers_commodity_etfs = list(commodity_etf_tickers.keys())
tickers_risk_free_treasury = list(risk_free_treasury_tickers.keys())
tickers_volatility_indices = list(volatility_tickers.keys())
tickers_currency_etfs = list(currency_etf_tickers.keys())
tickers_benchmarks = list(benchmark_tickers.keys())

pre_table_columns = ['No.', 'Ticker', 'Name']

# NOTE: The ticker categories and the number of tickers to download the info of in each of them will be specified by the user
#       on the page preceding the ticker selection page.

df_pre_url_biggest_companies = pd.DataFrame(index = tickers_biggest_companies, columns = pre_table_columns)
df_pre_url_sp500 = pd.DataFrame(index = tickers_sp500, columns = pre_table_columns)
df_pre_url_nasdaq100 = pd.DataFrame(index = tickers_nasdaq100, columns = pre_table_columns)
df_pre_url_dow_jones = pd.DataFrame(index = tickers_dow_jones, columns = pre_table_columns)
df_pre_url_biggest_etfs = pd.DataFrame(index = tickers_biggest_etfs, columns = pre_table_columns)
df_pre_url_fixed_income_etfs = pd.DataFrame(index = tickers_fixed_income_etfs, columns = pre_table_columns)
df_pre_url_ai_etfs = pd.DataFrame(index = tickers_ai_etfs, columns = pre_table_columns)
df_pre_url_futures = pd.DataFrame(index = tickers_futures, columns = pre_table_columns)
df_pre_url_cryptos = pd.DataFrame(index = tickers_cryptos, columns = pre_table_columns)
df_pre_url_crypto_etfs = pd.DataFrame(index = tickers_crypto_etfs, columns = pre_table_columns)

df_pre_tickers_car_companies = pd.DataFrame(index = tickers_car_companies, columns = pre_table_columns)
df_pre_tickers_rare_metals_companies = pd.DataFrame(index = tickers_rare_metals_companies, columns = pre_table_columns)
df_pre_tickers_stock_indices = pd.DataFrame(index = tickers_stock_indices, columns = pre_table_columns)
df_pre_tickers_commodity_etfs = pd.DataFrame(index = tickers_commodity_etfs, columns = pre_table_columns)
df_pre_tickers_precious_metals = pd.DataFrame(index = tickers_precious_metals, columns = pre_table_columns)
df_pre_tickers_risk_free_treasury = pd.DataFrame(index = tickers_risk_free_treasury, columns = pre_table_columns)
df_pre_tickers_volatility_indices = pd.DataFrame(index = tickers_volatility_indices, columns = pre_table_columns)
df_pre_tickers_currency_etfs = pd.DataFrame(index = tickers_currency_etfs, columns = pre_table_columns)
df_pre_tickers_benchmarks = pd.DataFrame(index = tickers_benchmarks, columns = pre_table_columns)

row_ticker_map_biggest_companies = {}
row_ticker_map_sp500 = {}
row_ticker_map_nasdaq100 = {}
row_ticker_map_dow_jones = {}
row_ticker_map_car_companies = {}
row_ticker_map_rare_metals_companies = {}
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

ticker_category_info_map = {}
ticker_category_info_map = {
    # 'car_companies': {
    #     'df': df_pre_tickers_car_companies,
    #     'row': row_ticker_map_car_companies,
    #     'dict': car_companies,
    #     'sort_by': 'marketCap',
    #     'id_string': 'car-companies',
    #     'collapse_title': 'CAR COMPANIES'
    # },
    # 'rare_metals_companies': {
    #     'df': df_pre_tickers_rare_metals_companies,
    #     'row': row_ticker_map_rare_metals_companies,
    #     'dict': rare_metals_companies,
    #     'sort_by': 'marketCap',
    #     'id_string': 'rare-metals-companies',
    #     'collapse_title': 'RARE METALS COMPANIES'
    # },
    'biggest_companies': {
        'df': df_pre_url_biggest_companies,
        'row': row_ticker_map_biggest_companies,
        'dict': dict_biggest_companies,
        'sort_by': '',
        'id_string': 'biggest-companies',
        'collapse_title': 'BIGGEST COMPANIES'
    },
    'sp500': {
        'df': df_pre_url_sp500,
        'row': row_ticker_map_sp500,
        'dict': dict_sp500,
        'sort_by': '',
        'id_string': 'sp500',
        'collapse_title': 'S&P 500 COMPANIES'
    },
    'nasdaq100': {
        'df': df_pre_url_nasdaq100,
        'row': row_ticker_map_nasdaq100,
        'dict': dict_nasdaq100,
        'sort_by': '',
        'id_string': 'nasdaq100',
        'collapse_title': 'NASDAQ 100 COMPANIES'
    },
    'dow_jones': {
        'df': df_pre_url_dow_jones,
        'row': row_ticker_map_dow_jones,
        'dict': dict_dow_jones,
        'sort_by': '',
        'id_string': 'dow-jones',
        'collapse_title': 'DOW JONES INDUSTRIAL AVERAGE COMPANIES'
    },
    'car_companies': {
        'df': df_pre_tickers_car_companies,
        'row': row_ticker_map_car_companies,
        'dict': car_companies,
        'sort_by': 'marketCap',
        'id_string': 'car-companies',
        'collapse_title': 'CAR COMPANIES'
    },
    'rare_metals_companies': {
        'df': df_pre_tickers_rare_metals_companies,
        'row': row_ticker_map_rare_metals_companies,
        'dict': rare_metals_companies,
        'sort_by': 'marketCap',
        'id_string': 'rare-metals-companies',
        'collapse_title': 'RARE METALS COMPANIES'
    },
    'biggest_etfs': {
        'df': df_pre_url_biggest_etfs,
        'row': row_ticker_map_biggest_etfs,
        'dict': dict_biggest_etfs,
        'sort_by': '',
        'id_string': 'biggest-etfs',
        'collapse_title': 'BIGGEST ETFs'
    },
    'fixed_income_etfs': {
        'df': df_pre_url_fixed_income_etfs,
        'row': row_ticker_map_fixed_income_etfs,
        'dict': dict_fixed_income_etfs,
        'sort_by': '',
        'id_string': 'fixed-income-etfs',
        'collapse_title': 'FIXED INCOME ETFs'
    },
    'ai_etfs': {
        'df': df_pre_url_ai_etfs,
        'row': row_ticker_map_ai_etfs,
        'dict': dict_ai_etfs,
        'sort_by': '',
        'id_string': 'ai-etfs',
        'collapse_title': 'ARTIFICIAL INTELLIGENCE ETFs'
    },
    'commodity_etfs': {
        'df': df_pre_tickers_commodity_etfs,
        'row': row_ticker_map_commodity_etfs,
        'dict': commodity_etf_tickers,
        'sort_by': 'totalAssets',
        'id_string': 'commodity-etfs',
        'collapse_title': 'COMMODITY ETFs'
    },
    'currency_etfs': {
        'df': df_pre_tickers_currency_etfs,
        'row': row_ticker_map_currency_etfs,
        'dict': currency_etf_tickers,
        'sort_by': 'totalAssets',
        'id_string': 'currency-etfs',
        'collapse_title': 'CURRENCY ETFs'
    },
    'cryptos': {
        'df': df_pre_url_cryptos,
        'row': row_ticker_map_cryptos,
        'dict': dict_cryptos,
        'sort_by': '',
        'id_string': 'cryptos',
        'collapse_title': 'CRYPTOCURRENCIES'
    },
    'crypto_etfs': {
        'df': df_pre_url_crypto_etfs,
        'row': row_ticker_map_crypto_etfs,
        'dict': dict_crypto_etfs,
        'sort_by': '',
        'id_string': 'crypto-etfs',
        'collapse_title': 'CRYPTOCURRENCY ETFs'
    },
    'futures': {
        'df': df_pre_url_futures,
        'row': row_ticker_map_futures,
        'dict': dict_futures,
        'sort_by': '',
        'id_string': 'futures',
        'collapse_title': 'COMMODITY FUTURES'
    },
    'precious_metals': {
        'df': df_pre_tickers_precious_metals,
        'row': row_ticker_map_precious_metals,
        'dict': precious_metals,
        'sort_by': 'openInterest',
        'id_string': 'precious-metals',
        'collapse_title': 'PRECIOUS METALS'
    },
    'stock_indices': {
        'df': df_pre_tickers_stock_indices,
        'row': row_ticker_map_stock_indices,
        'dict': stock_index_tickers,
        'sort_by': '',  # Only some indices have 'volume' in info
        'id_string': 'stock-indices',
        'collapse_title': 'STOCK INDICES'
    },
    'volatility_indices': {
        'df': df_pre_tickers_volatility_indices,
        'row': row_ticker_map_volatility_indices,
        'dict': volatility_tickers,
        'sort_by': '',  # No 'volume' in info
        'id_string': 'volatility-indices',
        'collapse_title': 'VOLATILITY INDICES'
    },
    'benchmarks': {
        'df': df_pre_tickers_benchmarks,
        'row': row_ticker_map_benchmarks,
        'dict': benchmark_tickers,
        'sort_by': '',
        'id_string': 'benchmarks',
        'collapse_title': 'BENCHMARKS'
    }
}

ticker_names = {}  # To help user decide on tickers based on the name =

def create_pre_table(category):

    df_pre_tickers = ticker_category_info_map[category]['df']
    row_ticker_map = ticker_category_info_map[category]['row']
    dict_info_tickers = ticker_category_info_map[category]['dict']
    tk_sort_by = ticker_category_info_map[category]['sort_by']
    
    category_tickers = list(dict_info_tickers.keys())
    n_tickers = min(len(category_tickers), max_tickers[category])
    category_tickers = category_tickers[: n_tickers]
    df_pre_tickers = df_pre_tickers[: n_tickers]
    max_tickers[category] = n_tickers
    ### Create a function that takes max_tickers as an argument and returns category table title

    category_tickers_sorted = category_tickers

    # Sort ticker list by marketCap (equities), totalAssets (ETFs) or openInterest (futures)

    if tk_sort_by != '':
    # The above means that the tickers are NOT from a URL

        dict_tickers_values = {}
        dict_currency_fx_rates = {}
        for tk in category_tickers:
            tk_info = yf.Ticker(tk).info
            currency = tk_info['currency']
            if currency != 'USD':
                if currency in dict_currency_fx_rates.keys():
                    dict_tickers_values.update({currency: dict_currency_fx_rates[currency]})
                else:
                    fx_rate = hist_info.get_usd_fx_rate(currency)
                    fx_rate = 1 if fx_rate == 0 else fx_rate
                    dict_tickers_values.update({tk: tk_info[tk_sort_by] / fx_rate})
                    dict_currency_fx_rates.update({tk: fx_rate})
            else:
                dict_tickers_values.update({tk: tk_info[tk_sort_by]})

        category_tickers_sorted = [i[0] for i in sorted(dict_tickers_values.items(), key=itemgetter(1), reverse=True)]
        df_pre_tickers.index = category_tickers_sorted  

    for i, tk in enumerate(category_tickers_sorted):

        if tk not in ticker_names.keys():
            
            df_pre_tickers.at[tk, 'No.'] = i + 1
            df_pre_tickers.at[tk, 'Ticker'] = tk
            tk_name = dict_info_tickers[tk]
            df_pre_tickers.at[tk, 'Name'] = tk_name
            ticker_names.update({tk: tk_name})
    
        else:

            df_pre_tickers.at[tk, 'No.'] = i + 1
            df_pre_tickers.at[tk, 'Ticker'] = tk
            if tk in bond_etf_tickers.keys():
                # To avoid corrupt names at https://8marketcap.com/etfs/
                df_pre_tickers.at[tk, 'Name'] = bond_etf_tickers[tk]
            else:
                df_pre_tickers.at[tk, 'Name'] = ticker_names[tk]

        row_ticker_map.update({tk: i})

    pre_table_data = {
        'df': df_pre_tickers,
        'row': row_ticker_map,
        'maxn': n_tickers
    }

    return pre_table_data


for category in ticker_category_info_map.keys():
    print(f'\nProcessing {category} ...')
    pre_table_data = create_pre_table(category)
    ticker_category_info_map[category]['df'] = pre_table_data['df']
    ticker_category_info_map[category]['row'] = pre_table_data['row']
    max_tickers.update({category: pre_table_data['maxn']})
    print(ticker_category_info_map[category]['df'])
    print(ticker_category_info_map[category]['row'])

pre_table_titles = {
    'biggest_companies': f'{max_tickers["biggest_companies"]} BIGGEST COMPANIES by Market Capitalization',
    'sp500': f'TOP {max_tickers["sp500"]} S&P 500 COMPANIES by Market Capitalization',
    'nasdaq100': f'TOP {max_tickers["nasdaq100"]} NASDAQ 100 COMPANIES by Market Capitalization',
    'dow_jones': f'TOP {max_tickers["dow_jones"]} DOW JONES INDUSTRIAL AVERAGE COMPANIES by Market Capitalization',
    'car_companies': f'TOP {max_tickers["car_companies"]} CAR COMPANIES by Market Capitalization',
    'rare_metals_companies': f'TOP {max_tickers["rare_metals_companies"]} RARE METALS COMPANIES by Market Capitalization',
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

print(f'\nTotal tickers: {len(ticker_names)}')

##############

ticker_div_title = html.Div(
    'YOUR PORTFOLIO:',
    style = select_ticker_title_css
)

pre_selection_table = {}  # A dictionary mapping ticker category to the corresponding pre-selection table
pre_selection_table_collapse_div = {}
pre_tables = []

for category in ticker_category_info_map.keys():
    
    id_string = ticker_category_info_map[category]['id_string']

    pre_selection_table[category] = html.Div([
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
            ],
            id = f'pre-dash-table-{id_string}',
            style_header = input_table_header_css,
            style_data = input_table_data_css,
        )
    ])

    pre_selection_table_collapse_div[category] = html.Div(
        hidden = False,
        children =
        [
            html.Div(
                ticker_category_info_map[category]['collapse_title'],
                id = f'pre-collapse-button-title-{id_string}',
                hidden = True
            ),

            html.Div([
                dbc.Button(
                    id = f'pre-collapse-button-table-{id_string}',
                    class_name = 'ma-1',
                    color = 'primary',
                    size = 'sm',
                    n_clicks = 0,
                    style = collapse_button_pre_table_css
                ),
                html.Div(
                    id = f'n-preselected-{id_string}-container',
                    children = [
                        html.Div(
                            id = f'n-preselected-{id_string}',
                            hidden = False,
                            style = n_selected_category_css
                        ),
                        html.Div(
                            f'/ {max_tickers[category]}',
                            hidden = False,
                            style = n_tickers_category_css
                        ),
                        html.Div(
                            'pre-selected',
                            hidden = False,
                            style = selected_string_css
                        )
                    ],
                    style = {'display': 'inline-block'}
                )
            ]),

            dbc.Collapse(
                html.Div(
                    html.Div(
                        id = f'pre-category-{id_string}-container',
                        children = [
                            
                            html.Div(
                                id = f'pre-menu-{id_string}-container',
                                children = [

                                    ### Select buttons
                                    html.Div(
                                        id = f'pre-menu-{id_string}-select-buttons-container',
                                        style = {'margin-bottom': '10px', 'margin-left': '10px'},
                                        children = [
                                            dbc.Button(
                                                'Select All',
                                                id = f'pre-menu-{id_string}-select-all-button',
                                                n_clicks = 0,
                                                class_name = 'ma-1',
                                                color = 'success',
                                                size = 'sm',
                                                style = pre_menu_select_all_button_css
                                            ),
                                            html.Div(
                                                id = 'pre-menu-{id_string}-select-first-last-tickers-container',
                                                children = [
                                                    html.Div('Select Ticker Range', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                                    html.Div([
                                                        html.Div(
                                                            'First No.',
                                                            style = {
                                                                'font-size': '14px',
                                                                'vertical-align': 'top',
                                                                'margin-bottom': '0px',
                                                                'margin-left': '2px',
                                                                'margin-right': '0px'
                                                            }
                                                        ),
                                                        dbc.Input(
                                                            id = f'pre-menu-{id_string}-select-first-ticker-input',
                                                            type = 'number',
                                                            min = 1,
                                                            max = max_tickers[category],
                                                            step = 1,
                                                            debounce = True,
                                                            style = pre_menu_input_css
                                                        )],
                                                        style = pre_menu_item_css
                                                    ),
                                                    html.Div([
                                                        html.Div(
                                                            'Last No.',
                                                            style = {
                                                                'font-size': '14px',
                                                                'vertical-align': 'top',
                                                                'margin-bottom': '0px',
                                                                'margin-left': '2px',
                                                                'margin-right': '4px'
                                                            }
                                                        ),
                                                        dbc.Input(
                                                            id = f'pre-menu-{id_string}-select-last-ticker-input',
                                                            type = 'number',
                                                            min = 1,
                                                            max = max_tickers[category],
                                                            step = 1,
                                                            debounce = True,
                                                            style = pre_menu_input_css
                                                        )],
                                                        style = pre_menu_item_css
                                                    )
                                                ]
                                            )
                                        ]
                                    ),

                                    ### Unselect buttons
                                    html.Div(
                                        id = f'pre-menu-{id_string}-unselect-buttons-container',
                                        style = {'margin-bottom': '10px', 'margin-left': '10px'},
                                        children = [
                                            dbc.Button(
                                                'Unselect All',
                                                id = f'pre-menu-{id_string}-unselect-all-button',
                                                n_clicks = 0,
                                                class_name = 'ma-1',
                                                color = 'danger',
                                                size = 'sm',
                                                style = pre_menu_select_all_button_css
                                            ),
                                            html.Div(
                                                id = 'pre-menu-{id_string}-unselect-first-last-tickers-container',
                                                children = [
                                                    html.Div('Unselect Ticker Range', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                                    html.Div([
                                                        html.Div(
                                                            'First No.',
                                                            style = {
                                                                'font-size': '14px',
                                                                'vertical-align': 'top',
                                                                'margin-bottom': '0px',
                                                                'margin-left': '2px',
                                                                'margin-right': '0px'
                                                            }
                                                        ),
                                                        dbc.Input(
                                                            id = f'pre-menu-{id_string}-unselect-first-ticker-input',
                                                            type = 'number',
                                                            min = 1,
                                                            max = max_tickers[category],
                                                            step = 1,
                                                            debounce = True,
                                                            style = pre_menu_input_css
                                                        )],
                                                        style = pre_menu_item_css
                                                    ),
                                                    html.Div([
                                                        html.Div(
                                                            'Last No.',
                                                            style = {
                                                                'font-size': '14px',
                                                                'vertical-align': 'top',
                                                                'margin-bottom': '0px',
                                                                'margin-left': '2px',
                                                                'margin-right': '4px'
                                                            }
                                                        ),
                                                        dbc.Input(
                                                            id = f'pre-menu-{id_string}-unselect-last-ticker-input',
                                                            type = 'number',
                                                            min = 1,
                                                            max = max_tickers[category],
                                                            step = 1,
                                                            debounce = True,
                                                            style = pre_menu_input_css
                                                        )],
                                                        style = pre_menu_item_css
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ],
                                style = pre_menu_container_css
                            ),

                            html.Div(
                                id = f'pre-table-{id_string}-container',
                                children = [
                                html.Div(
                                    children = pre_table_titles[category],
                                    id = f'pre-table-{id_string}-title',
                                    style = input_table_title_css
                                ),
                                pre_selection_table[category]
                                ],
                                style = pre_table_container_css
                            )
                        ],
                        # style = {'display': 'inline-block'}
                    ),
                ),
                id = f'pre-collapse-table-{id_string}',
                is_open = False
            ),  # dbc.Collapse
        ]
    )  # html.Div with dbc.Button and dbc.Collapse

    pre_tables.append(pre_selection_table_collapse_div[category])

###########################################################################################

# app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])

# app.layout = html.Div([
layout = html.Div([

    # LOADING WRAPPER
    dcc.Loading([

    html.Div(id = 'ticker-output', hidden = True, style = {'font-size' : '14px'}),

    # MAIN TITLE
    html.Div(
        'Pre-select ticker categories or individual tickers to extract more details about',
        id = 'ticker-main-title',
        style = ticker_main_title_css
    ),

    html.Div(id = 'pre-select-ticker-list', hidden = True),
    html.Div(id = 'pre-select-ticker-list-check', hidden = False),

    # html.Div(children = [], id = 'prev-table-selected-rows', hidden = True),
    # dcc.Store(data = {}, id = 'pre-prev-table-selected-rows', storage_type = 'session'),
    # dcc.Store(data = {}, id = 'tk-selected-category-map', storage_type = 'session'),
    # dcc.Store(data = [], id = 'preselected-categories', storage_type = 'session'),
    dcc.Store(data = {}, id = 'pre-prev-table-selected-rows', storage_type = 'memory'),
    dcc.Store(data = {}, id = 'tk-selected-category-map', storage_type = 'memory'),
    dcc.Store(data = [], id = 'preselected-categories', storage_type = 'memory'),

    # YOUR PORTFOLIO
    html.Div(
        id = 'pre-select-ticker-container',
        hidden = True,
        style = select_ticker_container_css
    ),

    ################
    html.Div([
        html.Div(
            'Total distinct tickers pre-selected:',
            style = {
                'display': 'inline-block',
                'font-family': 'Helvetica',
                'font-size': '16px',
                'font-weight': 'bold',
                'text-align': 'left',
                'vertical-align': 'middle',
                # 'margin-top': '5px',
                'margin-bottom': '5px',
                'margin-left': '5px'
            }
        ),
        html.Div(
            id = 'pre-selected-tickers-total',
            # hidden = True,
            style = {
                'display': 'inline-block',
                'font-family': 'Helvetica',
                'font-size': '16px',
                'font-weight': 'bold',
                'text-align': 'left',
                'color': 'darkgreen',
                'vertical-align': 'middle',
                # 'margin-top': '5px',
                'margin-bottom': '5px',
                'margin-left': '5px'
            }
        ),
    ]),

    ################

    html.Div(
        id = 'pre-all-tables-container',
        children = pre_tables
    ),

],
    
    id = 'ticker-input-loading-wrapper',
    custom_spinner = html.Div([
        'Loading Ticker Categories',
        html.Br(),
        html.Br(),
        dls.Fade(color = 'midnightblue'),
        html.Br(),
        'Please Wait ...'
    ],
    style = page_loading_wrapper_css
    ),
    overlay_style = {'visibility': 'visible', 'opacity': 0.35, 'filter': 'blur(3px)'},
    delay_show = 1000,
    delay_hide = 1000

    ),  # Loading

    html.Br(),

    html.Div(
        id = 'dates-link-container',
        children = [
            dcc.Link('Home Page', href='/'),
            html.Br(),
            dcc.Link('Continue to Ticker Info & Portfolio Selection', href='/test_ticker_input_v3')
        ],
        style = link_container_css
    )

])  # app.layout

####################################################################

# @app.callback(
@callback(        
    Output('pre-select-ticker-container', 'children'),
    Output('pre-select-ticker-container', 'hidden'),
    Output('pre-select-ticker-list', 'children'),
    Output('pre-prev-table-selected-rows', 'data'),

    Output('pre-menu-biggest-companies-select-all-button', 'n_clicks'),
    Output('pre-menu-sp500-select-all-button', 'n_clicks'),
    Output('pre-menu-nasdaq100-select-all-button', 'n_clicks'),
    Output('pre-menu-dow-jones-select-all-button', 'n_clicks'),
    Output('pre-menu-car-companies-select-all-button', 'n_clicks'),
    Output('pre-menu-rare-metals-companies-select-all-button', 'n_clicks'),
    Output('pre-menu-biggest-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-fixed-income-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-ai-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-commodity-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-currency-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-cryptos-select-all-button', 'n_clicks'),
    Output('pre-menu-crypto-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-futures-select-all-button', 'n_clicks'),
    Output('pre-menu-precious-metals-select-all-button', 'n_clicks'),
    Output('pre-menu-stock-indices-select-all-button', 'n_clicks'),
    Output('pre-menu-volatility-indices-select-all-button', 'n_clicks'),
    Output('pre-menu-benchmarks-select-all-button', 'n_clicks'),
     
    Output('pre-menu-biggest-companies-unselect-all-button', 'n_clicks'),
    Output('pre-menu-sp500-unselect-all-button', 'n_clicks'),
    Output('pre-menu-nasdaq100-unselect-all-button', 'n_clicks'),
    Output('pre-menu-dow-jones-unselect-all-button', 'n_clicks'),
    Output('pre-menu-car-companies-unselect-all-button', 'n_clicks'),
    Output('pre-menu-rare-metals-companies-unselect-all-button', 'n_clicks'),
    Output('pre-menu-biggest-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-fixed-income-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-ai-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-commodity-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-currency-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-cryptos-unselect-all-button', 'n_clicks'),
    Output('pre-menu-crypto-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-futures-unselect-all-button', 'n_clicks'),
    Output('pre-menu-precious-metals-unselect-all-button', 'n_clicks'),
    Output('pre-menu-stock-indices-unselect-all-button', 'n_clicks'),
    Output('pre-menu-volatility-indices-unselect-all-button', 'n_clicks'),
    Output('pre-menu-benchmarks-unselect-all-button', 'n_clicks'),

    Output('pre-menu-biggest-companies-select-first-ticker-input', 'value'),
    Output('pre-menu-sp500-select-first-ticker-input', 'value'),
    Output('pre-menu-nasdaq100-select-first-ticker-input', 'value'),
    Output('pre-menu-dow-jones-select-first-ticker-input', 'value'),
    Output('pre-menu-car-companies-select-first-ticker-input', 'value'),
    Output('pre-menu-rare-metals-companies-select-first-ticker-input', 'value'),
    Output('pre-menu-biggest-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-fixed-income-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-ai-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-commodity-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-currency-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-cryptos-select-first-ticker-input', 'value'),
    Output('pre-menu-crypto-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-futures-select-first-ticker-input', 'value'),
    Output('pre-menu-precious-metals-select-first-ticker-input', 'value'),
    Output('pre-menu-stock-indices-select-first-ticker-input', 'value'),
    Output('pre-menu-volatility-indices-select-first-ticker-input', 'value'),
    Output('pre-menu-benchmarks-select-first-ticker-input', 'value'),

    Output('pre-menu-biggest-companies-select-last-ticker-input', 'value'),
    Output('pre-menu-sp500-select-last-ticker-input', 'value'),
    Output('pre-menu-nasdaq100-select-last-ticker-input', 'value'),
    Output('pre-menu-dow-jones-select-last-ticker-input', 'value'),
    Output('pre-menu-car-companies-select-last-ticker-input', 'value'),
    Output('pre-menu-rare-metals-companies-select-last-ticker-input', 'value'),
    Output('pre-menu-biggest-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-fixed-income-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-ai-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-commodity-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-currency-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-cryptos-select-last-ticker-input', 'value'),
    Output('pre-menu-crypto-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-futures-select-last-ticker-input', 'value'),
    Output('pre-menu-precious-metals-select-last-ticker-input', 'value'),
    Output('pre-menu-stock-indices-select-last-ticker-input', 'value'),
    Output('pre-menu-volatility-indices-select-last-ticker-input', 'value'),
    Output('pre-menu-benchmarks-select-last-ticker-input', 'value'),

    Output('pre-menu-biggest-companies-unselect-first-ticker-input', 'value'),
    Output('pre-menu-sp500-unselect-first-ticker-input', 'value'),
    Output('pre-menu-nasdaq100-unselect-first-ticker-input', 'value'),
    Output('pre-menu-dow-jones-unselect-first-ticker-input', 'value'),
    Output('pre-menu-car-companies-unselect-first-ticker-input', 'value'),
    Output('pre-menu-rare-metals-companies-unselect-first-ticker-input', 'value'),
    Output('pre-menu-biggest-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-fixed-income-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-ai-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-commodity-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-currency-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-cryptos-unselect-first-ticker-input', 'value'),
    Output('pre-menu-crypto-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-futures-unselect-first-ticker-input', 'value'),
    Output('pre-menu-precious-metals-unselect-first-ticker-input', 'value'),
    Output('pre-menu-stock-indices-unselect-first-ticker-input', 'value'),
    Output('pre-menu-volatility-indices-unselect-first-ticker-input', 'value'),
    Output('pre-menu-benchmarks-unselect-first-ticker-input', 'value'),

    Output('pre-menu-biggest-companies-unselect-last-ticker-input', 'value'),
    Output('pre-menu-sp500-unselect-last-ticker-input', 'value'),
    Output('pre-menu-nasdaq100-unselect-last-ticker-input', 'value'),
    Output('pre-menu-dow-jones-unselect-last-ticker-input', 'value'),
    Output('pre-menu-car-companies-unselect-last-ticker-input', 'value'),
    Output('pre-menu-rare-metals-companies-unselect-last-ticker-input', 'value'),
    Output('pre-menu-biggest-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-fixed-income-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-ai-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-commodity-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-currency-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-cryptos-unselect-last-ticker-input', 'value'),
    Output('pre-menu-crypto-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-futures-unselect-last-ticker-input', 'value'),
    Output('pre-menu-precious-metals-unselect-last-ticker-input', 'value'),
    Output('pre-menu-stock-indices-unselect-last-ticker-input', 'value'),
    Output('pre-menu-volatility-indices-unselect-last-ticker-input', 'value'),
    Output('pre-menu-benchmarks-unselect-last-ticker-input', 'value'),

    Output('pre-dash-table-biggest-companies', 'selected_rows'),
    Output('pre-dash-table-sp500', 'selected_rows'),
    Output('pre-dash-table-nasdaq100', 'selected_rows'),
    Output('pre-dash-table-dow-jones', 'selected_rows'),
    Output('pre-dash-table-car-companies', 'selected_rows'),
    Output('pre-dash-table-rare-metals-companies', 'selected_rows'),
    Output('pre-dash-table-biggest-etfs', 'selected_rows'),
    Output('pre-dash-table-fixed-income-etfs', 'selected_rows'),
    Output('pre-dash-table-ai-etfs', 'selected_rows'),
    Output('pre-dash-table-commodity-etfs', 'selected_rows'),
    Output('pre-dash-table-currency-etfs', 'selected_rows'),
    Output('pre-dash-table-cryptos', 'selected_rows'),
    Output('pre-dash-table-crypto-etfs', 'selected_rows'),
    Output('pre-dash-table-futures', 'selected_rows'),
    Output('pre-dash-table-precious-metals', 'selected_rows'),
    Output('pre-dash-table-stock-indices', 'selected_rows'),
    Output('pre-dash-table-volatility-indices', 'selected_rows'),
    Output('pre-dash-table-benchmarks', 'selected_rows'),

    Output('n-preselected-biggest-companies', 'children'),
    Output('n-preselected-sp500', 'children'),
    Output('n-preselected-nasdaq100', 'children'),
    Output('n-preselected-dow-jones', 'children'),
    Output('n-preselected-car-companies', 'children'),
    Output('n-preselected-rare-metals-companies', 'children'),
    Output('n-preselected-biggest-etfs', 'children'),
    Output('n-preselected-fixed-income-etfs', 'children'),
    Output('n-preselected-ai-etfs', 'children'),
    Output('n-preselected-commodity-etfs', 'children'),
    Output('n-preselected-currency-etfs', 'children'),
    Output('n-preselected-cryptos', 'children'),
    Output('n-preselected-crypto-etfs', 'children'),
    Output('n-preselected-futures', 'children'),
    Output('n-preselected-precious-metals', 'children'),
    Output('n-preselected-stock-indices', 'children'),
    Output('n-preselected-volatility-indices', 'children'),
    Output('n-preselected-benchmarks', 'children'),

    Output('pre-selected-tickers-total', 'children'),
    Output('tk-selected-category-map', 'data'),
    Output('preselected-categories', 'data'),

    Input('pre-menu-biggest-companies-select-all-button', 'n_clicks'),
    Input('pre-menu-sp500-select-all-button', 'n_clicks'),
    Input('pre-menu-nasdaq100-select-all-button', 'n_clicks'),
    Input('pre-menu-dow-jones-select-all-button', 'n_clicks'),
    Input('pre-menu-car-companies-select-all-button', 'n_clicks'),
    Input('pre-menu-rare-metals-companies-select-all-button', 'n_clicks'),
    Input('pre-menu-biggest-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-fixed-income-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-ai-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-commodity-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-currency-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-cryptos-select-all-button', 'n_clicks'),
    Input('pre-menu-crypto-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-futures-select-all-button', 'n_clicks'),
    Input('pre-menu-precious-metals-select-all-button', 'n_clicks'),
    Input('pre-menu-stock-indices-select-all-button', 'n_clicks'),
    Input('pre-menu-volatility-indices-select-all-button', 'n_clicks'),
    Input('pre-menu-benchmarks-select-all-button', 'n_clicks'),

    Input('pre-menu-biggest-companies-unselect-all-button', 'n_clicks'),
    Input('pre-menu-sp500-unselect-all-button', 'n_clicks'),
    Input('pre-menu-nasdaq100-unselect-all-button', 'n_clicks'),
    Input('pre-menu-dow-jones-unselect-all-button', 'n_clicks'),
    Input('pre-menu-car-companies-unselect-all-button', 'n_clicks'),
    Input('pre-menu-rare-metals-companies-unselect-all-button', 'n_clicks'),
    Input('pre-menu-biggest-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-fixed-income-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-ai-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-commodity-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-currency-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-cryptos-unselect-all-button', 'n_clicks'),
    Input('pre-menu-crypto-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-futures-unselect-all-button', 'n_clicks'),
    Input('pre-menu-precious-metals-unselect-all-button', 'n_clicks'),
    Input('pre-menu-stock-indices-unselect-all-button', 'n_clicks'),
    Input('pre-menu-volatility-indices-unselect-all-button', 'n_clicks'),
    Input('pre-menu-benchmarks-unselect-all-button', 'n_clicks'),

    State('pre-menu-biggest-companies-select-first-ticker-input', 'value'),
    State('pre-menu-sp500-select-first-ticker-input', 'value'),
    State('pre-menu-nasdaq100-select-first-ticker-input', 'value'),
    State('pre-menu-dow-jones-select-first-ticker-input', 'value'),
    State('pre-menu-car-companies-select-first-ticker-input', 'value'),
    State('pre-menu-rare-metals-companies-select-first-ticker-input', 'value'),
    State('pre-menu-biggest-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-fixed-income-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-ai-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-commodity-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-currency-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-cryptos-select-first-ticker-input', 'value'),
    State('pre-menu-crypto-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-futures-select-first-ticker-input', 'value'),
    State('pre-menu-precious-metals-select-first-ticker-input', 'value'),
    State('pre-menu-stock-indices-select-first-ticker-input', 'value'),
    State('pre-menu-volatility-indices-select-first-ticker-input', 'value'),
    State('pre-menu-benchmarks-select-first-ticker-input', 'value'),

    Input('pre-menu-biggest-companies-select-last-ticker-input', 'value'),
    Input('pre-menu-sp500-select-last-ticker-input', 'value'),
    Input('pre-menu-nasdaq100-select-last-ticker-input', 'value'),
    Input('pre-menu-dow-jones-select-last-ticker-input', 'value'),
    Input('pre-menu-car-companies-select-last-ticker-input', 'value'),
    Input('pre-menu-rare-metals-companies-select-last-ticker-input', 'value'),
    Input('pre-menu-biggest-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-fixed-income-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-ai-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-commodity-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-currency-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-cryptos-select-last-ticker-input', 'value'),
    Input('pre-menu-crypto-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-futures-select-last-ticker-input', 'value'),
    Input('pre-menu-precious-metals-select-last-ticker-input', 'value'),
    Input('pre-menu-stock-indices-select-last-ticker-input', 'value'),
    Input('pre-menu-volatility-indices-select-last-ticker-input', 'value'),
    Input('pre-menu-benchmarks-select-last-ticker-input', 'value'),

    State('pre-menu-biggest-companies-unselect-first-ticker-input', 'value'),
    State('pre-menu-sp500-unselect-first-ticker-input', 'value'),
    State('pre-menu-nasdaq100-unselect-first-ticker-input', 'value'),
    State('pre-menu-dow-jones-unselect-first-ticker-input', 'value'),
    State('pre-menu-car-companies-unselect-last-ticker-input', 'value'),
    State('pre-menu-rare-metals-companies-unselect-last-ticker-input', 'value'),
    State('pre-menu-biggest-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-fixed-income-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-ai-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-commodity-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-currency-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-cryptos-unselect-first-ticker-input', 'value'),
    State('pre-menu-crypto-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-futures-unselect-first-ticker-input', 'value'),
    State('pre-menu-precious-metals-unselect-first-ticker-input', 'value'),
    State('pre-menu-stock-indices-unselect-first-ticker-input', 'value'),
    State('pre-menu-volatility-indices-unselect-first-ticker-input', 'value'),
    State('pre-menu-benchmarks-unselect-first-ticker-input', 'value'),

    Input('pre-menu-biggest-companies-unselect-last-ticker-input', 'value'),
    Input('pre-menu-sp500-unselect-last-ticker-input', 'value'),
    Input('pre-menu-nasdaq100-unselect-last-ticker-input', 'value'),
    Input('pre-menu-dow-jones-unselect-last-ticker-input', 'value'),
    Input('pre-menu-car-companies-unselect-last-ticker-input', 'value'),
    Input('pre-menu-rare-metals-companies-unselect-last-ticker-input', 'value'),
    Input('pre-menu-biggest-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-fixed-income-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-ai-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-commodity-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-currency-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-cryptos-unselect-last-ticker-input', 'value'),
    Input('pre-menu-crypto-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-futures-unselect-last-ticker-input', 'value'),
    Input('pre-menu-precious-metals-unselect-last-ticker-input', 'value'),
    Input('pre-menu-stock-indices-unselect-last-ticker-input', 'value'),
    Input('pre-menu-volatility-indices-unselect-last-ticker-input', 'value'),
    Input('pre-menu-benchmarks-unselect-last-ticker-input', 'value'),

    Input('pre-dash-table-biggest-companies', 'data'),
    Input('pre-dash-table-sp500', 'data'),
    Input('pre-dash-table-nasdaq100', 'data'),
    Input('pre-dash-table-dow-jones', 'data'),
    Input('pre-dash-table-car-companies', 'data'),
    Input('pre-dash-table-rare-metals-companies', 'data'),
    Input('pre-dash-table-biggest-etfs', 'data'),
    Input('pre-dash-table-fixed-income-etfs', 'data'),
    Input('pre-dash-table-ai-etfs', 'data'),    
    Input('pre-dash-table-commodity-etfs', 'data'),
    Input('pre-dash-table-currency-etfs', 'data'),
    Input('pre-dash-table-cryptos', 'data'),
    Input('pre-dash-table-crypto-etfs', 'data'),    
    Input('pre-dash-table-futures', 'data'),    
    Input('pre-dash-table-precious-metals', 'data'),
    Input('pre-dash-table-stock-indices', 'data'),
    Input('pre-dash-table-volatility-indices', 'data'),
    Input('pre-dash-table-benchmarks', 'data'),

    Input('pre-dash-table-biggest-companies', 'selected_rows'),
    Input('pre-dash-table-sp500', 'selected_rows'),
    Input('pre-dash-table-nasdaq100', 'selected_rows'),
    Input('pre-dash-table-dow-jones', 'selected_rows'),
    Input('pre-dash-table-car-companies', 'selected_rows'),
    Input('pre-dash-table-rare-metals-companies', 'selected_rows'),
    Input('pre-dash-table-biggest-etfs', 'selected_rows'),
    Input('pre-dash-table-fixed-income-etfs', 'selected_rows'),
    Input('pre-dash-table-ai-etfs', 'selected_rows'),
    Input('pre-dash-table-commodity-etfs', 'selected_rows'),
    Input('pre-dash-table-currency-etfs', 'selected_rows'),
    Input('pre-dash-table-cryptos', 'selected_rows'),
    Input('pre-dash-table-crypto-etfs', 'selected_rows'),
    Input('pre-dash-table-futures', 'selected_rows'),
    Input('pre-dash-table-precious-metals', 'selected_rows'),
    Input('pre-dash-table-stock-indices', 'selected_rows'),
    Input('pre-dash-table-volatility-indices', 'selected_rows'),
    Input('pre-dash-table-benchmarks', 'selected_rows'),

    Input('pre-select-ticker-list', 'children'),
    Input('pre-prev-table-selected-rows', 'data'),
    Input('pre-select-ticker-container', 'children'),
    Input({'index': ALL, 'type': 'ticker_icon'}, 'n_clicks'),

    State('tk-selected-category-map', 'data'),
    # Input('tk-selected-category-map', 'data'),

    suppress_callback_exceptions = True
)
def output_custom_tickers(

    select_all_biggest_companies,
    select_all_sp500,
    select_all_nasdaq100,
    select_all_dow_jones,
    select_all_car_companies,
    select_all_rare_metals_companies,
    select_all_biggest_etfs,
    select_all_fixed_income_etfs,
    select_all_ai_etfs,
    select_all_commodity_etfs,
    select_all_currency_etfs,
    select_all_cryptos,
    select_all_crypto_etfs,
    select_all_futures,
    select_all_precious_metals,
    select_all_stock_indices,
    select_all_volatility_indices,
    select_all_benchmarks,

    unselect_all_biggest_companies,
    unselect_all_sp500,
    unselect_all_nasdaq100,
    unselect_all_dow_jones,
    unselect_all_car_companies,
    unselect_all_rare_metals_companies,
    unselect_all_biggest_etfs,
    unselect_all_fixed_income_etfs,
    unselect_all_ai_etfs,
    unselect_all_commodity_etfs,
    unselect_all_currency_etfs,
    unselect_all_cryptos,
    unselect_all_crypto_etfs,
    unselect_all_futures,
    unselect_all_precious_metals,
    unselect_all_stock_indices,
    unselect_all_volatility_indices,
    unselect_all_benchmarks,

    select_first_ticker_biggest_companies,
    select_first_ticker_sp500,
    select_first_ticker_nasdaq100,
    select_first_ticker_dow_jones,
    select_first_ticker_car_companies,
    select_first_ticker_rare_metals_companies,
    select_first_ticker_biggest_etfs,
    select_first_ticker_fixed_income_etfs,
    select_first_ticker_ai_etfs,
    select_first_ticker_commodity_etfs,
    select_first_ticker_currency_etfs,
    select_first_ticker_cryptos,
    select_first_ticker_crypto_etfs,
    select_first_ticker_futures,
    select_first_ticker_precious_metals,
    select_first_ticker_stock_indices,
    select_first_ticker_volatility_indices,
    select_first_ticker_benchmarks,

    select_last_ticker_biggest_companies,
    select_last_ticker_sp500,
    select_last_ticker_nasdaq100,
    select_last_ticker_dow_jones,
    select_last_ticker_car_companies,
    select_last_ticker_rare_metals_companies,
    select_last_ticker_biggest_etfs,
    select_last_ticker_fixed_income_etfs,
    select_last_ticker_ai_etfs,
    select_last_ticker_commodity_etfs,
    select_last_ticker_currency_etfs,
    select_last_ticker_cryptos,
    select_last_ticker_crypto_etfs,
    select_last_ticker_futures,
    select_last_ticker_precious_metals,
    select_last_ticker_stock_indices,
    select_last_ticker_volatility_indices,
    select_last_ticker_benchmarks,

    unselect_first_ticker_biggest_companies,
    unselect_first_ticker_sp500,
    unselect_first_ticker_nasdaq100,
    unselect_first_ticker_dow_jones,
    unselect_first_ticker_car_companies,
    unselect_first_ticker_rare_metals_companies,
    unselect_first_ticker_biggest_etfs,
    unselect_first_ticker_fixed_income_etfs,
    unselect_first_ticker_ai_etfs,
    unselect_first_ticker_commodity_etfs,
    unselect_first_ticker_currency_etfs,
    unselect_first_ticker_cryptos,
    unselect_first_ticker_crypto_etfs,
    unselect_first_ticker_futures,
    unselect_first_ticker_precious_metals,
    unselect_first_ticker_stock_indices,
    unselect_first_ticker_volatility_indices,
    unselect_first_ticker_benchmarks,

    unselect_last_ticker_biggest_companies,
    unselect_last_ticker_sp500,
    unselect_last_ticker_nasdaq100,
    unselect_last_ticker_dow_jones,
    unselect_last_ticker_car_companies,
    unselect_last_ticker_rare_metals_companies,
    unselect_last_ticker_biggest_etfs,
    unselect_last_ticker_fixed_income_etfs,
    unselect_last_ticker_ai_etfs,
    unselect_last_ticker_commodity_etfs,
    unselect_last_ticker_currency_etfs,
    unselect_last_ticker_cryptos,
    unselect_last_ticker_crypto_etfs,
    unselect_last_ticker_futures,
    unselect_last_ticker_precious_metals,
    unselect_last_ticker_stock_indices,
    unselect_last_ticker_volatility_indices,
    unselect_last_ticker_benchmarks,

    table_biggest_companies_data,
    table_sp500_data,
    table_nasdaq100_data,
    table_dow_jones_data,
    table_car_companies_data,
    table_rare_metals_companies_data,
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
    table_car_companies_selected_rows,
    table_rare_metals_companies_selected_rows,
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
    n_clicks,

    tk_selected_category_map
):

    table_selected_rows = {
        'biggest_companies': table_biggest_companies_selected_rows,
        'sp500': table_sp500_selected_rows,
        'nasdaq100': table_nasdaq100_selected_rows,
        'dow_jones': table_dow_jones_selected_rows,
        'car_companies': table_car_companies_selected_rows,
        'rare_metals_companies': table_rare_metals_companies_selected_rows,
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
    table_data = {
        'biggest_companies': table_biggest_companies_data,
        'sp500': table_sp500_data,
        'nasdaq100': table_nasdaq100_data,
        'dow_jones': table_dow_jones_data,
        'car_companies': table_car_companies_data,
        'rare_metals_companies': table_rare_metals_companies_data,
        'biggest_etfs': table_biggest_etfs_data,
        'fixed_income_etfs': table_fixed_income_etfs_data,
        'ai_etfs': table_ai_etfs_data,
        'commodity_etfs': table_commodity_etfs_data,
        'currency_etfs': table_currency_etfs_data,
        'cryptos': table_cryptos_data,
        'crypto_etfs': table_crypto_etfs_data,
        'futures': table_futures_data,
        'precious_metals': table_precious_metals_data,
        'stock_indices': table_stock_indices_data,
        'volatility_indices': table_volatility_indices_data,
        'benchmarks': table_benchmarks_data
    }
    select_all_button_nclicks = {
        'biggest_companies': select_all_biggest_companies,
        'sp500': select_all_sp500,
        'nasdaq100': select_all_nasdaq100,
        'dow_jones': select_all_dow_jones,
        'car_companies': select_all_car_companies,
        'rare_metals_companies': select_all_rare_metals_companies,
        'biggest_etfs': select_all_biggest_etfs,
        'fixed_income_etfs': select_all_fixed_income_etfs,
        'ai_etfs': select_all_ai_etfs,
        'commodity_etfs': select_all_commodity_etfs,
        'currency_etfs': select_all_currency_etfs,
        'cryptos': select_all_cryptos,
        'crypto_etfs': select_all_crypto_etfs,
        'futures': select_all_futures,
        'precious_metals': select_all_precious_metals,
        'stock_indices': select_all_stock_indices,
        'volatility_indices': select_all_volatility_indices,
        'benchmarks': select_all_benchmarks
    }
    unselect_all_button_nclicks = {
        'biggest_companies': unselect_all_biggest_companies,
        'sp500': unselect_all_sp500,
        'nasdaq100': unselect_all_nasdaq100,
        'dow_jones': unselect_all_dow_jones,
        'car_companies': unselect_all_car_companies,
        'rare_metals_companies': unselect_all_rare_metals_companies,
        'biggest_etfs': unselect_all_biggest_etfs,
        'fixed_income_etfs': unselect_all_fixed_income_etfs,
        'ai_etfs': unselect_all_ai_etfs,
        'commodity_etfs': unselect_all_commodity_etfs,
        'currency_etfs': unselect_all_currency_etfs,
        'cryptos': unselect_all_cryptos,
        'crypto_etfs': unselect_all_crypto_etfs,
        'futures': unselect_all_futures,
        'precious_metals': unselect_all_precious_metals,
        'stock_indices': unselect_all_stock_indices,
        'volatility_indices': unselect_all_volatility_indices,
        'benchmarks': unselect_all_benchmarks
    }
    select_first_ticker = {
        'biggest_companies': select_first_ticker_biggest_companies,
        'sp500': select_first_ticker_sp500,
        'nasdaq100': select_first_ticker_nasdaq100,
        'dow_jones': select_first_ticker_dow_jones,
        'car_companies': select_first_ticker_car_companies,
        'rare_metals_companies': select_first_ticker_rare_metals_companies,
        'biggest_etfs': select_first_ticker_biggest_etfs,
        'fixed_income_etfs': select_first_ticker_fixed_income_etfs,
        'ai_etfs': select_first_ticker_ai_etfs,
        'commodity_etfs': select_first_ticker_commodity_etfs,
        'currency_etfs': select_first_ticker_currency_etfs,
        'cryptos': select_first_ticker_cryptos,
        'crypto_etfs': select_first_ticker_crypto_etfs,
        'futures': select_first_ticker_futures,
        'precious_metals': select_first_ticker_precious_metals,
        'stock_indices': select_first_ticker_stock_indices,
        'volatility_indices': select_first_ticker_volatility_indices,
        'benchmarks': select_first_ticker_benchmarks
    }
    select_last_ticker = {
        'biggest_companies': select_last_ticker_biggest_companies,
        'sp500': select_last_ticker_sp500,
        'nasdaq100': select_last_ticker_nasdaq100,
        'dow_jones': select_last_ticker_dow_jones,
        'car_companies': select_last_ticker_car_companies,
        'rare_metals_companies': select_last_ticker_rare_metals_companies,
        'biggest_etfs': select_last_ticker_biggest_etfs,
        'fixed_income_etfs': select_last_ticker_fixed_income_etfs,
        'ai_etfs': select_last_ticker_ai_etfs,
        'commodity_etfs': select_last_ticker_commodity_etfs,
        'currency_etfs': select_last_ticker_currency_etfs,
        'cryptos': select_last_ticker_cryptos,
        'crypto_etfs': select_last_ticker_crypto_etfs,
        'futures': select_last_ticker_futures,
        'precious_metals': select_last_ticker_precious_metals,
        'stock_indices': select_last_ticker_stock_indices,
        'volatility_indices': select_last_ticker_volatility_indices,
        'benchmarks': select_last_ticker_benchmarks
    }
    unselect_first_ticker = {
        'biggest_companies': unselect_first_ticker_biggest_companies,
        'sp500': unselect_first_ticker_sp500,
        'nasdaq100': unselect_first_ticker_nasdaq100,
        'dow_jones': unselect_first_ticker_dow_jones,
        'car_companies': unselect_first_ticker_car_companies,
        'rare_metals_companies': unselect_first_ticker_rare_metals_companies,
        'biggest_etfs': unselect_first_ticker_biggest_etfs,
        'fixed_income_etfs': unselect_first_ticker_fixed_income_etfs,
        'ai_etfs': unselect_first_ticker_ai_etfs,
        'commodity_etfs': unselect_first_ticker_commodity_etfs,
        'currency_etfs': unselect_first_ticker_currency_etfs,
        'cryptos': unselect_first_ticker_cryptos,
        'crypto_etfs': unselect_first_ticker_crypto_etfs,
        'futures': unselect_first_ticker_futures,
        'precious_metals': unselect_first_ticker_precious_metals,
        'stock_indices': unselect_first_ticker_stock_indices,
        'volatility_indices': unselect_first_ticker_volatility_indices,
        'benchmarks': unselect_first_ticker_benchmarks
    }
    unselect_last_ticker = {
        'biggest_companies': unselect_last_ticker_biggest_companies,
        'sp500': unselect_last_ticker_sp500,
        'nasdaq100': unselect_last_ticker_nasdaq100,
        'dow_jones': unselect_last_ticker_dow_jones,
        'car_companies': unselect_last_ticker_car_companies,
        'rare_metals_companies': unselect_last_ticker_rare_metals_companies,
        'biggest_etfs': unselect_last_ticker_biggest_etfs,
        'fixed_income_etfs': unselect_last_ticker_fixed_income_etfs,
        'ai_etfs': unselect_last_ticker_ai_etfs,
        'commodity_etfs': unselect_last_ticker_commodity_etfs,
        'currency_etfs': unselect_last_ticker_currency_etfs,
        'cryptos': unselect_last_ticker_cryptos,
        'crypto_etfs': unselect_last_ticker_crypto_etfs,
        'futures': unselect_last_ticker_futures,
        'precious_metals': unselect_last_ticker_precious_metals,
        'stock_indices': unselect_last_ticker_stock_indices,
        'volatility_indices': unselect_last_ticker_volatility_indices,
        'benchmarks': unselect_last_ticker_benchmarks
    }

    n_preselected = {}

    if selected_tickers is None:
        selected_tickers = []

    updated_tickers = selected_tickers

    if prev_table_selected_rows == {}:
        for category in ticker_category_info_map.keys():
            prev_table_selected_rows[category] = []

    for category in ticker_category_info_map.keys():

        n_category_tickers = len(table_data[category])

        if select_all_button_nclicks[category]:
            table_selected_rows[category] = list(range(n_category_tickers))

        elif unselect_all_button_nclicks[category]:
            table_selected_rows[category] = []
            select_first_ticker[category] = None
            select_last_ticker[category] = None

        elif (select_first_ticker[category] is not None):
            if (select_last_ticker[category] is not None):
                select_first_row = select_first_ticker[category] - 1
                if select_last_ticker[category] < select_first_ticker[category]:
                    select_last_row = select_first_ticker[category]
                else:
                    select_last_row = select_last_ticker[category]
                select_rows_range = [k for k in range(select_first_row, select_last_row)]
                for row in select_rows_range:
                    if row not in table_selected_rows[category]:
                        table_selected_rows[category].append(row)
                select_last_ticker[category] = None 
        
        elif (unselect_first_ticker[category] is not None):
            if (unselect_last_ticker[category] is not None):
                unselect_first_row = unselect_first_ticker[category] - 1
                if unselect_last_ticker[category] < unselect_first_ticker[category]:
                    unselect_last_row = unselect_first_ticker[category]
                else:
                    unselect_last_row = unselect_last_ticker[category]
                unselect_rows_range = [k for k in range(unselect_first_row, unselect_last_row)]
                for row in unselect_rows_range:
                    if row in table_selected_rows[category]:
                        table_selected_rows[category].remove(row)
                unselect_last_ticker[category] = None

        else:
            select_last_ticker[category] = None
            unselect_last_ticker[category] = None

    #########

    # table_selected_tickers = {}
    # table_nonselected_tickers = {}
    # for category in ticker_category_info_map.keys():
    #     row_map = ticker_category_info_map[category]['row']
    #     table_selected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]
    #     table_nonselected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] not in table_selected_rows[category]]

    ctx = dash.callback_context

    # Should change to added tickers in this format
    added_tickers = []
    removed_tickers = []
    if 1 in n_clicks:
        if ctx.triggered:
            trig_id_str_list = [ctx.triggered[k]['prop_id'].split('.n_clicks')[0] for k in range(len(ctx.triggered)) if ctx.triggered[k]['value']]
            if len(trig_id_str_list) > 0:
                trig_id_str = trig_id_str_list[0]  # this is a stringified dictionary with whitespaces removed
                removed_ticker = trig_id_str.split('{"index":"')[1].split('","type"')[0].replace('select-ticker-icon-', '')  # {tk}
                removed_tickers.append(removed_ticker)

    for removed_ticker in removed_tickers:
        if removed_ticker in updated_tickers:
            updated_tickers.remove(removed_ticker)

    ticker_divs = [ticker_div_title]

    hide_ticker_container = False if len(updated_tickers) > 0 else True

    ##### INPUT TABLES
    # Check whether a ticker was added to or removed from any table

    # Construct the final list of categories from which the user has selected tickers
    # This is to prevent passing to next page other categories containing the same tickers

    # tk_selected_cat_map = {}

    for category in ticker_category_info_map.keys():
        row_map = ticker_category_info_map[category]['row']
        df_pre = ticker_category_info_map[category]['df']
        selected_rows = [k for k in table_selected_rows[category] if k not in prev_table_selected_rows[category]]
        if len(selected_rows) > 0:
            # preselected_categories.append(category)
            for row in selected_rows:
                added_ticker = df_pre.index[df_pre['No.'] == row + 1][0]
                if added_ticker not in added_tickers:
                    added_tickers.append(added_ticker)
                if added_ticker not in updated_tickers:
                    updated_tickers.append(added_ticker)
                    if added_ticker not in tk_selected_category_map.keys():
                        tk_selected_category_map[added_ticker] = category
            break
        else:
            unselected_rows = [k for k in prev_table_selected_rows[category] if k not in table_selected_rows[category]]
            if len(unselected_rows) > 0:
                for row in unselected_rows:
                    removed_ticker = df_pre.index[df_pre['No.'] == row + 1][0]
                    if removed_ticker not in removed_tickers:
                        removed_tickers.append(removed_ticker)
                    if removed_ticker in updated_tickers:
                        updated_tickers.remove(removed_ticker)
                        if removed_ticker in tk_selected_category_map.keys():
                            del tk_selected_category_map[removed_ticker]
                break
        # Check if category is empty and remove it from preselected_categories if it is
        # if (len(table_selected_rows[category]) == 0) & (category in preselected_categories):
        #     preselected_categories.remove(category)

    preselected_categories = list(set(tk_selected_category_map.values()))  # Set removes duplicates

    # Make sure added_ticker is selected in all tables and removed_ticker is removed from all tables
    if added_tickers != []:
        for category in ticker_category_info_map.keys():
            df_pre = ticker_category_info_map[category]['df']
            for added_ticker in added_tickers:
                if added_ticker in df_pre['Ticker']:
                    row_map = ticker_category_info_map[category]['row']
                    if row_map[added_ticker] not in table_selected_rows[category]:
                        table_selected_rows[category].append(row_map[added_ticker])

    if removed_tickers != []:
        for category in ticker_category_info_map.keys():
            df_pre = ticker_category_info_map[category]['df']
            for removed_ticker in removed_tickers:
                if removed_ticker in df_pre['Ticker']:
                    row_map = ticker_category_info_map[category]['row']
                    if row_map[removed_ticker] in table_selected_rows[category]:
                        table_selected_rows[category].remove(row_map[removed_ticker])

    ##### SELECTED TICKERS
    # Set up selected tickers divs

    for tk in updated_tickers:
        
        tk_id = f'select-ticker-{tk}'
        tk_icon_id = f'select-ticker-icon-{tk}'
        name = ticker_names[tk] if tk in ticker_names.keys() is not None else tk

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
            ],
            style = select_ticker_div_css
        )
        ticker_divs.append(tk_div)

    for category in table_selected_rows.keys():
        n_preselected[category] = len(table_selected_rows[category])

    n_preselected_total = len(updated_tickers)

    # hide_ticker_container = True if len(updated_tickers) == 0 else False
    hide_ticker_container = True

    return (
        ticker_divs,
        hide_ticker_container,
        updated_tickers,
        table_selected_rows,

        # select_all_button_nclicks
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # unselect_all_button_nclicks
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # select_first_ticker
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        # select_last_ticker
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        # unselect_first_ticker
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        # unselect_last_ticker
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,

        table_selected_rows['biggest_companies'],
        table_selected_rows['sp500'],
        table_selected_rows['nasdaq100'],
        table_selected_rows['dow_jones'],
        table_selected_rows['car_companies'],
        table_selected_rows['rare_metals_companies'],
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
        table_selected_rows['benchmarks'],

        n_preselected['biggest_companies'],
        n_preselected['sp500'],
        n_preselected['nasdaq100'],
        n_preselected['dow_jones'],
        n_preselected['car_companies'],
        n_preselected['rare_metals_companies'],
        n_preselected['biggest_etfs'],
        n_preselected['fixed_income_etfs'],
        n_preselected['ai_etfs'],
        n_preselected['commodity_etfs'],
        n_preselected['currency_etfs'],
        n_preselected['cryptos'],
        n_preselected['crypto_etfs'],
        n_preselected['futures'],
        n_preselected['precious_metals'],
        n_preselected['stock_indices'],
        n_preselected['volatility_indices'],
        n_preselected['benchmarks'],

        n_preselected_total,
        tk_selected_category_map,
        preselected_categories
    )


def toggle_collapse_tickers(title, n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


for category in ticker_category_info_map.keys():
    id_string = ticker_category_info_map[category]['id_string']
    callback(
    # app.callback(        
        Output(f'pre-collapse-button-table-{id_string}', 'children'),
        Output(f'pre-collapse-table-{id_string}', 'is_open'),
        Input(f'pre-collapse-button-title-{id_string}', 'children'),
        Input(f'pre-collapse-button-table-{id_string}', 'n_clicks'),
        State(f'pre-collapse-table-{id_string}', 'is_open')
    )(toggle_collapse_tickers)

########## MULTIPAGE APP CALLBACKS

# @callback(
# Output('pre-select-ticker-list-check', 'children'),
# Input('preselected-updated-tickers', 'data'),
# # State('pre-select-ticker-list', 'children'),
# suppress_callback_exceptions = True
# )
# # def store_preselected_updated_tickers(pathname, updated_tickers):  # , stored_updated_tickers):
# def retrieve_preselected_updated_tickers(stored_updated_tickers): # , updated_tickers):
#     # if (stored_updated_tickers != []) & (updated_tickers == []):
#     # if stored_updated_tickers != []:
#     # if pathname == '/test_multipage_app':
#     return stored_updated_tickers

@callback(
Output('n-preselected-stored', 'data'),
Output('preselected-ticker-tables-stored', 'data'),

Input('pre-dash-table-biggest-companies', 'selected_rows'),
Input('pre-dash-table-sp500', 'selected_rows'),
Input('pre-dash-table-nasdaq100', 'selected_rows'),
Input('pre-dash-table-dow-jones', 'selected_rows'),
Input('pre-dash-table-car-companies', 'selected_rows'),
Input('pre-dash-table-rare-metals-companies', 'selected_rows'),
Input('pre-dash-table-biggest-etfs', 'selected_rows'),
Input('pre-dash-table-fixed-income-etfs', 'selected_rows'),
Input('pre-dash-table-ai-etfs', 'selected_rows'),
Input('pre-dash-table-commodity-etfs', 'selected_rows'),
Input('pre-dash-table-currency-etfs', 'selected_rows'),
Input('pre-dash-table-cryptos', 'selected_rows'),
Input('pre-dash-table-crypto-etfs', 'selected_rows'),
Input('pre-dash-table-futures', 'selected_rows'),
Input('pre-dash-table-precious-metals', 'selected_rows'),
Input('pre-dash-table-stock-indices', 'selected_rows'),
Input('pre-dash-table-volatility-indices', 'selected_rows'),
Input('pre-dash-table-benchmarks', 'selected_rows'),

Input('preselected-categories', 'data')
)
def store_preselected_tickers(
    table_biggest_companies_selected_rows,
    table_sp500_selected_rows,
    table_nasdaq100_selected_rows,
    table_dow_jones_selected_rows,
    table_car_companies_selected_rows,
    table_rare_metals_companies_selected_rows,
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

    preselected_categories
):
    table_selected_rows = {
        'biggest_companies': table_biggest_companies_selected_rows,
        'sp500': table_sp500_selected_rows,
        'nasdaq100': table_nasdaq100_selected_rows,
        'dow_jones': table_dow_jones_selected_rows,
        'car_companies': table_car_companies_selected_rows,
        'rare_metals_companies': table_rare_metals_companies_selected_rows,
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

    # n_preselected will only be non-zero if the user has selected from that particular category
    n_preselected = {}
    preselected_ticker_tables = {}

    for category in ticker_category_info_map.keys():
        
        if category in preselected_categories:
            n_preselected[category] = len(table_selected_rows[category])
        else:
            n_preselected[category] = 0

        row_map = ticker_category_info_map[category]['row']
        # preselected_ticker_tables[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]
        preselected_ticker_tables[category] = [{tk: ticker_names[tk] for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]}]

    return (
        n_preselected,
        preselected_ticker_tables
    )
    
##########################################################################
