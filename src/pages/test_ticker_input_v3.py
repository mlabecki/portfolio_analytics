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

import requests_cache

register_page(
    __name__,
    path = '/test_ticker_input_v3'
)

hist_info = DownloadInfo()

etf_categories = [
    'biggest_etfs',
    'fixed_income_etfs',
    'ai_etfs',
    'commodity_etfs',
    'currency_etfs',
    'crypto_etfs'
]

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

table_selected_tickers_columns = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Length*', 'Type', 'Category', 'Industry', 'Sector', 'Exchange', 'Currency']

ticker_category_info_map = {
    'biggest_companies': {
        'columns': input_table_columns_equities,
        'id_string': 'biggest-companies',
        'collapse_title': 'BIGGEST COMPANIES'
    },
    'sp500': {
        'columns': input_table_columns_equities,
        'id_string': 'sp500',
        'collapse_title': 'S&P 500 COMPANIES'
    },
    'nasdaq100': {
        'columns': input_table_columns_equities,
        'id_string': 'nasdaq100',
        'collapse_title': 'NASDAQ 100 COMPANIES'
    },
    'dow_jones': {
        'columns': input_table_columns_equities,
        'id_string': 'dow-jones',
        'collapse_title': 'DOW JONES INDUSTRIAL AVERAGE COMPANIES'
    },
    'biggest_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'biggest-etfs',
        'collapse_title': 'BIGGEST ETFs'
    },
    'fixed_income_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'fixed-income-etfs',
        'collapse_title': 'FIXED INCOME ETFs'
    },
    'ai_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'ai-etfs',
        'collapse_title': 'ARTIFICIAL INTELLIGENCE ETFs'
    },
    'commodity_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'commodity-etfs',
        'collapse_title': 'COMMODITY ETFs'
    },
    'currency_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'currency-etfs',
        'collapse_title': 'CURRENCY ETFs'
    },
    'cryptos': {
        'columns': input_table_columns_cryptos,
        'id_string': 'cryptos',
        'collapse_title': 'CRYPTOCURRENCIES'
    },
    'crypto_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'crypto-etfs',
        'collapse_title': 'CRYPTOCURRENCY ETFs'
    },
    'futures': {
        'columns': input_table_columns_futures,
        'id_string': 'futures',
        'collapse_title': 'COMMODITY FUTURES'
    },
    'precious_metals': {
        'columns': input_table_columns_futures,
        'id_string': 'precious-metals',
        'collapse_title': 'PRECIOUS METALS'
    },    
    'stock_indices': {
        'columns': input_table_columns_indices,
        'id_string': 'stock-indices',
        'collapse_title': 'STOCK INDICES'
    },
    'volatility_indices': {
        'columns': input_table_columns_indices,
        'id_string': 'volatility-indices',
        'collapse_title': 'VOLATILITY INDICES'
    },
    'benchmarks': {
        'columns': input_table_columns_indices,
        'id_string': 'benchmarks',
        'collapse_title': 'BENCHMARKS'
    }
}

#################

ticker_div_title = html.Div(
    'YOUR PORTFOLIO:',
    style = select_ticker_title_css
)

def initialize_input_table_divs(
    ticker_category_info_map
):

    input_table_collapse_div = {}
    input_table_divs = []
    
    for category in ticker_category_info_map.keys():

        id_string = ticker_category_info_map[category]['id_string']

        dash_input_table = dash_table.DataTable(
            columns = [],
            data = [],
            editable = False,
            row_selectable = 'multi',
            tooltip_data = [],
            css = [
                {
                'selector': '.dash-tooltip',
                'rule': 'border: None;'
                },
                {
                'selector': '.dash-table-tooltip',
                'rule': 'max-width: 500px; width: 500px !important; border: 1px solid rgb(67, 172, 106) !important; border-radius: 5px !important; padding: 10px; padding: 10px 12px 0px 12px; font-size: 12px; font-family: Helvetica; background-color: rgb(227, 255, 237);'
                },
                {
                'selector': '.dash-tooltip:before, .dash-tooltip:after',
                'rule': 'border-top-color: #43ac6a !important; border-bottom-color: #43ac6a !important;'
                }
            ],
            tooltip_delay = 0,
            tooltip_duration = None,
            selected_rows = [],
            style_as_list_view = True,
            style_data_conditional = [
                {'if': 
                    { 'state': 'active'},
                    'backgroundColor': 'white',
                    'border-top': '1px solid rgb(211, 211, 211)',
                    'border-bottom': '1px solid rgb(211, 211, 211)'},
                {'if': {'column_id': 'No.'}, 'width': 24},
                {'if': {'column_id': 'Ticker'}, 'width': 45},
                {'if': {'column_id': 'Currency'}, 'width': 70},
                {'if': {'column_id': 'Exchange'}, 'width': 72},
                {'if': {'column_id': 'Data Start'}, 'width': 85},
                {'if': {'column_id': 'Data End'}, 'width': 85},
            ],
            id = f'dash-table-{id_string}',
            style_header = input_table_header_css,
            style_data = input_table_data_css,
        )

        input_table_collapse_div[category] = html.Div(
            id = f'input-table-collapse-div-{id_string}',
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
                                    id = f'table-{id_string}-title',
                                    style = input_table_title_css
                                ),
                                html.Div(
                                    dash_input_table,
                                    id = f'table-{id_string}-div'
                                )
                            ],
                            style = input_table_container_css
                        ),
                    ),
                    id = f'collapse-table-{id_string}',
                    is_open = False
                ),  # dbc.Collapse
            ]
        )  # html.Div with dbc.Button and dbc.Collapse

        input_table_divs.append(input_table_collapse_div[category])
    
    return input_table_divs

input_table_divs = initialize_input_table_divs(ticker_category_info_map)

###########################################################################################

layout = html.Div([

    # LOADING WRAPPER
    dcc.Loading([
    
    dcc.Store(data = {}, id = 'ticker-category-info-map', storage_type = 'session'),

    dcc.Store(data = {}, id = 'ticker-info', storage_type = 'session'),

    html.Div(id = 'excluded-tickers-list', hidden = True),
    
    html.Div(id = 'ticker-output', hidden = True, style = {'font-size' : '14px'}),

    # MAIN TITLE
    html.Div(
        'Add tickers to your portfolio by selecting from the list(s) below or typing in the Add Ticker box',
        id = 'ticker-main-title',
        style = ticker_main_title_css
    ),

    html.Div(id = 'select-ticker-list', hidden = True),

    dcc.Store(data = {}, id = 'prev-table-selected-rows', storage_type = 'session'),

    # YOUR PORTFOLIO
    html.Div(
        id = 'select-ticker-container',
        hidden = True,
        children = [
            html.Div(
                id = 'select-ticker-divs-container'
            ),
            html.Div(
                id = 'select-ticker-portfolio-summary'
            ),
        ],
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
        children = input_table_divs
    )

    ],
    
    id = 'ticker-input-loading-wrapper',
    custom_spinner = html.Div([
        'Loading Ticker Info',
        html.Br(),
        html.Br(),
        dls.Fade(color = 'midnightblue'),
        html.Br(),
        'Please Wait ...'
    ],
    style = {'font-family': 'Helvetica', 'font-size': 26, 'font-weight': 'bold', 'color': 'midnightblue', 'text-align': 'center'}
    ),
    overlay_style = {'visibility': 'visible', 'opacity': 0.35, 'filter': 'blur(3px)'},
    delay_show = 1000,
    delay_hide = 1000
    
    ),  # Loading

    html.Br(),

    dcc.Link('Home Page', href='/'),
    html.Br(),
    dcc.Link('Start Over Preliminary Ticker Selection', href='/preliminary_ticker_selection_v3'),
    html.Br(),
    dcc.Link('Continue to Date Range Selection', href='/test_dates_selection')

])  # layout

####################################################################

# ticker_info = {}

@callback(
    # preselected_table_titles
    Output('table-biggest-companies-title', 'children'),
    Output('table-sp500-title', 'children'),
    Output('table-nasdaq100-title', 'children'),
    Output('table-dow-jones-title', 'children'),
    Output('table-biggest-etfs-title', 'children'),
    Output('table-fixed-income-etfs-title', 'children'),
    Output('table-ai-etfs-title', 'children'),
    Output('table-commodity-etfs-title', 'children'),
    Output('table-currency-etfs-title', 'children'),
    Output('table-cryptos-title', 'children'),
    Output('table-crypto-etfs-title', 'children'),
    Output('table-futures-title', 'children'),
    Output('table-precious-metals-title', 'children'),
    Output('table-stock-indices-title', 'children'),
    Output('table-volatility-indices-title', 'children'),
    Output('table-benchmarks-title', 'children'),

    # Dash table columns
    Output('dash-table-biggest-companies', 'columns'),
    Output('dash-table-sp500', 'columns'),
    Output('dash-table-nasdaq100', 'columns'),
    Output('dash-table-dow-jones', 'columns'),
    Output('dash-table-biggest-etfs', 'columns'),
    Output('dash-table-fixed-income-etfs', 'columns'),
    Output('dash-table-ai-etfs', 'columns'),
    Output('dash-table-commodity-etfs', 'columns'),
    Output('dash-table-currency-etfs', 'columns'),
    Output('dash-table-cryptos', 'columns'),
    Output('dash-table-crypto-etfs', 'columns'),
    Output('dash-table-futures', 'columns'),
    Output('dash-table-precious-metals', 'columns'),
    Output('dash-table-stock-indices', 'columns'),
    Output('dash-table-volatility-indices', 'columns'),
    Output('dash-table-benchmarks', 'columns'),

    # Dash table data
    Output('dash-table-biggest-companies', 'data'),
    Output('dash-table-sp500', 'data'),
    Output('dash-table-nasdaq100', 'data'),
    Output('dash-table-dow-jones', 'data'),
    Output('dash-table-biggest-etfs', 'data'),
    Output('dash-table-fixed-income-etfs', 'data'),
    Output('dash-table-ai-etfs', 'data'),
    Output('dash-table-commodity-etfs', 'data'),
    Output('dash-table-currency-etfs', 'data'),
    Output('dash-table-cryptos', 'data'),
    Output('dash-table-crypto-etfs', 'data'),
    Output('dash-table-futures', 'data'),
    Output('dash-table-precious-metals', 'data'),
    Output('dash-table-stock-indices', 'data'),
    Output('dash-table-volatility-indices', 'data'),
    Output('dash-table-benchmarks', 'data'),

    # Dash table tooltip_data
    Output('dash-table-biggest-companies', 'tooltip_data'),
    Output('dash-table-sp500', 'tooltip_data'),
    Output('dash-table-nasdaq100', 'tooltip_data'),
    Output('dash-table-dow-jones', 'tooltip_data'),
    Output('dash-table-biggest-etfs', 'tooltip_data'),
    Output('dash-table-fixed-income-etfs', 'tooltip_data'),
    Output('dash-table-ai-etfs', 'tooltip_data'),
    Output('dash-table-commodity-etfs', 'tooltip_data'),
    Output('dash-table-currency-etfs', 'tooltip_data'),
    Output('dash-table-cryptos', 'tooltip_data'),
    Output('dash-table-crypto-etfs', 'tooltip_data'),
    Output('dash-table-futures', 'tooltip_data'),
    Output('dash-table-precious-metals', 'tooltip_data'),
    Output('dash-table-stock-indices', 'tooltip_data'),
    Output('dash-table-volatility-indices', 'tooltip_data'),
    Output('dash-table-benchmarks', 'tooltip_data'),

    # Collapse button hidden
    Output('input-table-collapse-div-biggest-companies', 'hidden'),
    Output('input-table-collapse-div-sp500', 'hidden'),
    Output('input-table-collapse-div-nasdaq100', 'hidden'),
    Output('input-table-collapse-div-dow-jones', 'hidden'),
    Output('input-table-collapse-div-biggest-etfs', 'hidden'),
    Output('input-table-collapse-div-fixed-income-etfs', 'hidden'),
    Output('input-table-collapse-div-ai-etfs', 'hidden'),
    Output('input-table-collapse-div-commodity-etfs', 'hidden'),
    Output('input-table-collapse-div-currency-etfs', 'hidden'),
    Output('input-table-collapse-div-cryptos', 'hidden'),
    Output('input-table-collapse-div-crypto-etfs', 'hidden'),
    Output('input-table-collapse-div-futures', 'hidden'),
    Output('input-table-collapse-div-precious-metals', 'hidden'),
    Output('input-table-collapse-div-stock-indices', 'hidden'),
    Output('input-table-collapse-div-volatility-indices', 'hidden'),
    Output('input-table-collapse-div-benchmarks', 'hidden'),

    Output('ticker-category-info-map', 'data'),
    Output('ticker-info', 'data'),
    Output('custom-ticker-input-message', 'hidden'),
    Output('custom-ticker-info-container', 'hidden'),
    Output('custom-ticker-input-message', 'children'),
    Output('excluded-tickers-list', 'children'),

    Input('n-preselected-stored', 'data'),              # from main app page
    Input('preselected-ticker-tables-stored', 'data'),   # from main app page

    suppress_callback_exceptions = True
)
def read_preselected_tickers(
    n_preselected,
    preselected_ticker_tables
):

    # preselected_ticker_tables = {}  # {category: [{tk: tk_name}]}
    ticker_info = {}
    dash_input_tables = {}
    excluded_tickers = []

    for category in n_preselected.keys():
    
        if n_preselected[category] != 0:
    
            session = requests_cache.CachedSession('cache/yfinance.cache')
            session.headers['User-agent'] = url_settings['global']['headers']

            category_tickers = list(preselected_ticker_tables[category][0].keys())  # {category: [{tk: tk_name}]}

            df_info_tickers = pd.DataFrame(index = category_tickers, columns = ticker_category_info_map[category]['columns'])
            row_ticker_map = {}

            for i, tk in enumerate(category_tickers):

                if tk not in ticker_info.keys():

                    yf_ticker = yf.Ticker(tk, session = session)

                    tk_hist = yf_ticker.history(period = 'max')
                    tk_info = yf_ticker.info
                    # Should also check if ticker is still valid, for now assume they're all valid

                    tk_length = len(tk_hist.index)

                    if ('quoteType' in tk_info.keys()) & ( tk_length > 0):
                        # - quoteType is meant to indicate a valid ticker
                        # - tk_hist may be temporarily empty for a valid ticker, but then it must also be excluded
                        
                        tk_start, tk_end = str(tk_hist.index[0].date()), str(tk_hist.index[-1].date())

                        df_info_tickers.at[tk, 'No.'] = i + 1
                        df_info_tickers.at[tk, 'Ticker'] = tk

                        if 'longName' in tk_info.keys():
                            tk_name = tk_info['longName']
                        elif 'shortName' in tk_info.keys():
                            tk_name = tk_info['shortName']
                        else:
                            tk_name = preselected_ticker_tables[category][0][tk]

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
                        elif len(tk_hist.index) == 0:
                            tk_summary = f'WARNING: No historical data available for {tk}, ticker cannot be added to portfolio'
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
                                'length': tk_length,
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
                        
                        excluded_tickers.append(tk)
                        n_preselected[category] -= 1
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

            # Update df_info_tickers and row_ticker_map to account for excluded tickers
            for i, tk in enumerate(df_info_tickers.index):
                df_info_tickers.at[tk, 'No.'] = i + 1
                row_ticker_map.update({tk: i})
            
            # Update ticker_category_info_map
            ticker_category_info_map[category]['df'] = df_info_tickers.to_dict()  # Dictionary !
            dash_table_data = df_info_tickers.to_dict('records')  # List of dictionaries !
            ticker_category_info_map[category]['row'] = row_ticker_map
            ticker_category_info_map[category]['hidden'] = False

            session.cache.clear()

        else:
            ticker_category_info_map[category]['df'] = {}
            dash_table_data = [{}]
            ticker_category_info_map[category]['row'] = {}
            ticker_category_info_map[category]['hidden'] = True

        ####################

        dash_input_tables[category] = {}
        dash_input_tables[category]['columns'] = [{'name': i, 'id': i} for i in ticker_category_info_map[category]['columns']]
        dash_input_tables[category]['data'] = dash_table_data   # A list of dictionaries
        dash_input_tables[category]['tooltip_data'] = [
            { column: {'value': ticker_info[row['Ticker']]['summary'], 'type': 'markdown' }
            for column in row.keys() }
            for row in dash_table_data  # e.g. {'No.': 1, 'Ticker': 'AAPL', ...} etc.
        ]
    
    if len(excluded_tickers) > 0:
        excluded_tickers_str = ", ".join(excluded_tickers)
        plural_adjustment = 'ticker has' if len(excluded_tickers) == 1 else 'tickers have'
        excluded_tickers_message = f'WARNING: No historical data available for {excluded_tickers_str} — {plural_adjustment} been removed from list'
        hide_tk_input_message = False
        hide_custom_ticker_info = True
        # hide_custom_ticker_info = False
    else:
        excluded_tickers_message = ''
        hide_tk_input_message = True
        hide_custom_ticker_info = False

    #################################

    preselected_table_titles = {
        'biggest_companies': f'{n_preselected["biggest_companies"]} PRE-SELECTED BIGGEST COMPANIES by Market Capitalization',
        'sp500': f'{n_preselected["sp500"]} PRE-SELECTED S&P 500 COMPANIES by Market Capitalization',
        'nasdaq100': f'{n_preselected["nasdaq100"]} PRE-SELECTED NASDAQ 100 COMPANIES by Market Capitalization',
        'dow_jones': f'{n_preselected["dow_jones"]} PRE-SELECTED DOW JONES INDUSTRIAL AVERAGE COMPANIES by Market Capitalization',
        'biggest_etfs': f'{n_preselected["biggest_etfs"]} PRE-SELECTED BIGGEST ETFs by Total Assets Under Management',
        'fixed_income_etfs': f'{n_preselected["fixed_income_etfs"]} PRE-SELECTED FIXED INCOME ETFs by Total Assets Under Management',
        'ai_etfs': f'{n_preselected["ai_etfs"]} PRE-SELECTED ARTIFICIAL INTELLIGENCE ETFs by Total Assets Under Management',
        'commodity_etfs': f'{n_preselected["commodity_etfs"]} PRE-SELECTED COMMODITY ETFs sorted by Total Assets Under Management',
        'currency_etfs': f'{n_preselected["currency_etfs"]} PRE-SELECTED CURRENCY ETFs sorted by Total Assets Under Management',
        'cryptos': f'{n_preselected["cryptos"]} PRE-SELECTED CRYPTOCURRENCIES by Market Capitalization',
        'crypto_etfs': f'{n_preselected["crypto_etfs"]} PRE-SELECTED CRYPTOCURRENCY ETFs by Total Assets Under Management',
        'futures': f'{n_preselected["futures"]} PRE-SELECTED COMMODITY FUTURES by Open Interest',
        'precious_metals': f'{n_preselected["precious_metals"]} PRE-SELECTED PRECIOUS METAL SPOT / FUTURES sorted by Open Interest',
        'stock_indices': f'{n_preselected["stock_indices"]} PRE-SELECTED STOCK INDICES',
        'volatility_indices': f'{n_preselected["volatility_indices"]} PRE-SELECTED VOLATILITY INDICES',
        'benchmarks': f'{n_preselected["benchmarks"]} PRE-SELECTED BENCHMARKS'
    }
   
    return (
        preselected_table_titles['biggest_companies'],
        preselected_table_titles['sp500'],
        preselected_table_titles['nasdaq100'],
        preselected_table_titles['dow_jones'],
        preselected_table_titles['biggest_etfs'],
        preselected_table_titles['fixed_income_etfs'],
        preselected_table_titles['ai_etfs'],
        preselected_table_titles['commodity_etfs'],
        preselected_table_titles['currency_etfs'],
        preselected_table_titles['cryptos'],
        preselected_table_titles['crypto_etfs'],
        preselected_table_titles['futures'],
        preselected_table_titles['precious_metals'],
        preselected_table_titles['stock_indices'],
        preselected_table_titles['volatility_indices'],
        preselected_table_titles['benchmarks'],

        dash_input_tables['biggest_companies']['columns'],
        dash_input_tables['sp500']['columns'],
        dash_input_tables['nasdaq100']['columns'],
        dash_input_tables['dow_jones']['columns'],
        dash_input_tables['biggest_etfs']['columns'],
        dash_input_tables['fixed_income_etfs']['columns'],
        dash_input_tables['ai_etfs']['columns'],
        dash_input_tables['commodity_etfs']['columns'],
        dash_input_tables['currency_etfs']['columns'],
        dash_input_tables['cryptos']['columns'],
        dash_input_tables['crypto_etfs']['columns'],
        dash_input_tables['futures']['columns'],
        dash_input_tables['precious_metals']['columns'],
        dash_input_tables['stock_indices']['columns'],
        dash_input_tables['volatility_indices']['columns'],
        dash_input_tables['benchmarks']['columns'],

        dash_input_tables['biggest_companies']['data'],
        dash_input_tables['sp500']['data'],
        dash_input_tables['nasdaq100']['data'],
        dash_input_tables['dow_jones']['data'],
        dash_input_tables['biggest_etfs']['data'],
        dash_input_tables['fixed_income_etfs']['data'],
        dash_input_tables['ai_etfs']['data'],
        dash_input_tables['commodity_etfs']['data'],
        dash_input_tables['currency_etfs']['data'],
        dash_input_tables['cryptos']['data'],
        dash_input_tables['crypto_etfs']['data'],
        dash_input_tables['futures']['data'],
        dash_input_tables['precious_metals']['data'],
        dash_input_tables['stock_indices']['data'],
        dash_input_tables['volatility_indices']['data'],
        dash_input_tables['benchmarks']['data'],

        dash_input_tables['biggest_companies']['tooltip_data'],
        dash_input_tables['sp500']['tooltip_data'],
        dash_input_tables['nasdaq100']['tooltip_data'],
        dash_input_tables['dow_jones']['tooltip_data'],
        dash_input_tables['biggest_etfs']['tooltip_data'],
        dash_input_tables['fixed_income_etfs']['tooltip_data'],
        dash_input_tables['ai_etfs']['tooltip_data'],
        dash_input_tables['commodity_etfs']['tooltip_data'],
        dash_input_tables['currency_etfs']['tooltip_data'],
        dash_input_tables['cryptos']['tooltip_data'],
        dash_input_tables['crypto_etfs']['tooltip_data'],
        dash_input_tables['futures']['tooltip_data'],
        dash_input_tables['precious_metals']['tooltip_data'],
        dash_input_tables['stock_indices']['tooltip_data'],
        dash_input_tables['volatility_indices']['tooltip_data'],
        dash_input_tables['benchmarks']['tooltip_data'],

        ticker_category_info_map['biggest_companies']['hidden'],
        ticker_category_info_map['sp500']['hidden'],
        ticker_category_info_map['nasdaq100']['hidden'],
        ticker_category_info_map['dow_jones']['hidden'],
        ticker_category_info_map['biggest_etfs']['hidden'],
        ticker_category_info_map['fixed_income_etfs']['hidden'],
        ticker_category_info_map['ai_etfs']['hidden'],
        ticker_category_info_map['commodity_etfs']['hidden'],
        ticker_category_info_map['currency_etfs']['hidden'],
        ticker_category_info_map['cryptos']['hidden'],
        ticker_category_info_map['crypto_etfs']['hidden'],
        ticker_category_info_map['futures']['hidden'],
        ticker_category_info_map['precious_metals']['hidden'],
        ticker_category_info_map['stock_indices']['hidden'],
        ticker_category_info_map['volatility_indices']['hidden'],
        ticker_category_info_map['benchmarks']['hidden'],

        ticker_category_info_map,
        ticker_info,
        hide_tk_input_message,
        hide_custom_ticker_info,
        excluded_tickers_message,
        excluded_tickers
    )

###################################################################

@callback(
    Output('select-ticker-divs-container', 'children'),
    Output('select-ticker-container', 'hidden'),
    Output('select-ticker-list', 'children'),
    Output('select-ticker-portfolio-summary', 'children'),
    Output('custom-ticker-input', 'value'),
    Output('custom-ticker-input-message', 'hidden', allow_duplicate = True),
    Output('custom-ticker-info-container', 'hidden', allow_duplicate = True),
    Output('custom-ticker-input-message', 'children', allow_duplicate = True),
    Output('table-custom-ticker-info', 'children'),
    Output('ticker-info', 'data', allow_duplicate = True),
    Output('prev-table-selected-rows', 'data'),

    Output('dash-table-biggest-companies', 'selected_rows'),
    Output('dash-table-sp500', 'selected_rows'),
    Output('dash-table-nasdaq100', 'selected_rows'),
    Output('dash-table-dow-jones', 'selected_rows'),
    Output('dash-table-biggest-etfs', 'selected_rows'),
    Output('dash-table-fixed-income-etfs', 'selected_rows'),
    Output('dash-table-ai-etfs', 'selected_rows'),
    Output('dash-table-commodity-etfs', 'selected_rows'),
    Output('dash-table-currency-etfs', 'selected_rows'),
    Output('dash-table-cryptos', 'selected_rows'),
    Output('dash-table-crypto-etfs', 'selected_rows'),
    Output('dash-table-futures', 'selected_rows'),
    Output('dash-table-precious-metals', 'selected_rows'),
    Output('dash-table-stock-indices', 'selected_rows'),
    Output('dash-table-volatility-indices', 'selected_rows'),
    Output('dash-table-benchmarks', 'selected_rows'),

    Output('table-selected-tickers-stored', 'data'),

    Input('ticker-category-info-map', 'data'),
    Input('ticker-info', 'data'),
    Input('excluded-tickers-list', 'children'),

    Input('dash-table-biggest-companies', 'selected_rows'),
    Input('dash-table-sp500', 'selected_rows'),
    Input('dash-table-nasdaq100', 'selected_rows'),
    Input('dash-table-dow-jones', 'selected_rows'),
    Input('dash-table-biggest-etfs', 'selected_rows'),
    Input('dash-table-fixed-income-etfs', 'selected_rows'),
    Input('dash-table-ai-etfs', 'selected_rows'),
    Input('dash-table-commodity-etfs', 'selected_rows'),
    Input('dash-table-currency-etfs', 'selected_rows'),
    Input('dash-table-cryptos', 'selected_rows'),
    Input('dash-table-crypto-etfs', 'selected_rows'),
    Input('dash-table-futures', 'selected_rows'),
    Input('dash-table-precious-metals', 'selected_rows'),
    Input('dash-table-stock-indices', 'selected_rows'),
    Input('dash-table-volatility-indices', 'selected_rows'),
    Input('dash-table-benchmarks', 'selected_rows'),

    Input('select-ticker-list', 'children'),
    Input('prev-table-selected-rows', 'data'),
    Input('select-ticker-divs-container', 'children'),
    Input('custom-ticker-input', 'value'),
    Input({'index': ALL, 'type': 'ticker_icon'}, 'n_clicks'),
    Input('custom-ticker-input-message', 'children'),

    prevent_initial_call = True,
    suppress_callback_exceptions = True
)
def output_custom_tickers(

    ticker_category_info_map,
    ticker_info,
    excluded_tickers,

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
    n_clicks,
    tk_input_message
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

    selected_categories = [cat for cat in ticker_category_info_map.keys() if 'Ticker' in ticker_category_info_map[cat]['df'].keys()]

    if prev_table_selected_rows == {}:
        for category in selected_categories:
            prev_table_selected_rows[category] = []

    table_selected_tickers = {}
    for category in selected_categories:
        row_map = ticker_category_info_map[category]['row']
        table_selected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]

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

    hide_custom_ticker_info = True
    if tk_input_message is None:
        tk_input_message = ''
        hide_tk_input_message = True
    else:
        hide_tk_input_message = False

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

            hide_tk_input_message = True
            tk_input_message = ''

            if tk_input in yf.shared._ERRORS.keys():
                tk_start, tk_end = 'N/A', 'N/A'
                tk_length = 0
            else:
                tk_start, tk_end = str(tk_hist.index[0].date()), str(tk_hist.index[-1].date())
                updated_tickers.append(tk_input)
                tk_length = len(tk_hist.index)

            if tk_input not in ticker_info.keys():
                
                if 'longName' in tk_info.keys():
                    tk_name = tk_info['longName']
                elif 'shortName' in tk_info.keys():
                    tk_name = tk_info['shortName']
                else:
                    tk_name = tk_input

                tk_type = tk_info['quoteType'] if 'quoteType' in tk_info.keys() else ''
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
                        'length': tk_length,
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
                css = [
                    { 
                    'selector': '.dash-spreadsheet tr:hover td.dash-cell',
                    'rule': 'background-color: white !important; border-bottom: None !important; border-top: 1px solid rgb(211, 211, 211) !important; color: black !important;'
                    }
                ],
                style_header = table_custom_ticker_header_css,
                style_data = table_custom_ticker_data_css
            )

        session.cache.clear()

    elif (tk_input == '') & (removed_ticker != ''):
        hide_tk_input_message = True
        # for tk in selected_tickers:
        for tk in updated_tickers:
            if tk == removed_ticker:
                updated_tickers.remove(tk)

    # Add tk_input to selected_rows in all relevant tables if not there yet
    for category in selected_categories:
        row_map = ticker_category_info_map[category]['row']
        if tk_input != '': 
            if (tk_input in row_map.keys()) & (tk_input not in table_selected_tickers[category]):
                table_selected_rows[category].append(row_map[tk_input])
                table_selected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]

    ##### INPUT TABLES
    # Check whether a ticker was added to or removed from any table

    for category in selected_categories:
        row_map = ticker_category_info_map[category]['row']
        df_info = ticker_category_info_map[category]['df']  ## This is a dictionary !!!
        selected_rows = [k for k in table_selected_rows[category] if k not in prev_table_selected_rows[category]]
        if len(selected_rows) > 0:
            for tk in df_info['No.'].keys():
                # if (df_info['Data Start'][tk] != 'N/A') & (df_info['No.'][tk] == 1 + selected_rows[0]):
                if df_info['No.'][tk] == 1 + selected_rows[0]:
                    added_ticker = df_info['Ticker'][tk]
                    if added_ticker not in updated_tickers:
                        updated_tickers.append(added_ticker)
                    break
        else:
            unselected_rows = [k for k in prev_table_selected_rows[category] if k not in table_selected_rows[category]]
            if len(unselected_rows) > 0:
                for tk in df_info['No.'].keys():
                    if df_info['No.'][tk] == 1 + unselected_rows[0]:
                        removed_ticker = df_info['Ticker'][tk]
                        # if (removed_ticker in updated_tickers) & (removed_ticker not in excluded_tickers):
                        if (removed_ticker in updated_tickers):
                            updated_tickers.remove(removed_ticker)
                        break

    # Make sure added_ticker is selected in all tables and removed_ticker is removed from all tables
    if added_ticker != '':
        for category in selected_categories:
            df_info = ticker_category_info_map[category]['df']  ## This is a dictionary!
            if added_ticker in df_info['Ticker'].keys():  # or values(), they're the same as keys()
                row_map = ticker_category_info_map[category]['row']
                if row_map[added_ticker] not in table_selected_rows[category]:
                    table_selected_rows[category].append(row_map[added_ticker])

    if removed_ticker != '':
        for category in selected_categories:
            df_info = ticker_category_info_map[category]['df']  ## This is a dictionary !
            if removed_ticker in df_info['Ticker'].keys():  # or values(), they're the same as keys()
                row_map = ticker_category_info_map[category]['row']
                if row_map[removed_ticker] in table_selected_rows[category]:
                    table_selected_rows[category].remove(row_map[removed_ticker])

    ##### SELECTED TICKERS
    # Set up selected tickers divs, popovers and table

    table_selected_tickers = pd.DataFrame(index = updated_tickers, columns = table_selected_tickers_columns)

    for i, tk in enumerate(updated_tickers):

        tk_id = f'select-ticker-{tk}'
        tk_icon_id = f'select-ticker-icon-{tk}'
        name = ticker_info[tk]['name'] if tk in ticker_info.keys() is not None else tk
        tk_start = ticker_info[tk]['start']
        tk_end = ticker_info[tk]['end']

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

        ##########################

        table_selected_tickers.at[tk, 'No.'] = i + 1
        table_selected_tickers.at[tk, 'Ticker'] = tk
        table_selected_tickers.at[tk, 'Name'] = name
        table_selected_tickers.at[tk, 'Data Start'] = tk_start
        table_selected_tickers.at[tk, 'Data End'] = tk_end
        table_selected_tickers.at[tk, 'Length*'] = ticker_info[tk]['length']
        table_selected_tickers.at[tk, 'Type'] = tk_type
        table_selected_tickers.at[tk, 'Category'] = ticker_info[tk]['category']
        table_selected_tickers.at[tk, 'Industry'] = ticker_info[tk]['industry']
        table_selected_tickers.at[tk, 'Sector'] = ticker_info[tk]['sector']
        table_selected_tickers.at[tk, 'Exchange'] = ticker_info[tk]['exchange']
        table_selected_tickers.at[tk, 'Currency'] = ticker_info[tk]['currency']

    ########################

    dash_table_selected_tickers_data = table_selected_tickers.to_dict('records')

    dash_table_selected_tickers = dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in table_selected_tickers_columns],
        data = dash_table_selected_tickers_data,
        editable = False,
        row_deletable = True,
        tooltip_data = [
            { column: {'value': ticker_info[row['Ticker']]['summary'], 'type': 'markdown' }
            for column in row.keys() }
            for row in dash_table_selected_tickers_data  # e.g. {'No.': 1, 'Ticker': 'AAPL', ...} etc.
        ],
        css = [
            {
            'selector': '.dash-spreadsheet tr',
            'rule': 'border-top: 2px solid rgb(211, 211, 211) !important;'
            },
            {
            'selector': '.dash-tooltip',
            'rule': 'border: None;'
            },
            {
            'selector': '.dash-spreadsheet tr:hover td.dash-cell',
            'rule': 'background-color: rgb(211, 211, 211) !important; border-top: 2px solid rgb(211, 211, 211) !important; border-bottom: 2px solid rgb(211, 211, 211) !important; color: black !important' 
            },
            {
            'selector': '.dash-spreadsheet td.dash-delete-cell',
            'rule': 'background-color: white !important; border-top: 2px solid rgb(211, 211, 211) !important; border-bottom: 2px solid rgb(211, 211, 211) !important; text-align: center !important; color: darkred !important; font-size: 20px !important; font-weight: bold !important;' 
            },
            {
            'selector': '.dash-spreadsheet tr:hover td.dash-delete-cell',
            'rule': 'background-color: rgb(211, 211, 211) !important; border-top: 2px solid rgb(211, 211, 211) !important; border-bottom: 2px solid rgb(211, 211, 211) !important; color: darkred !important; font-weight: bold;' 
            },
            {
            'selector': '.dash-tooltip:before, .dash-tooltip:after',
            'rule': 'border-top-color: rgb(211, 211, 211) !important; border-bottom-color: rgb(211, 211, 211) !important;'
            },
            {
            'selector': '.dash-table-tooltip',
            'rule': 'max-width: 500px; width: 500px !important; border: 1px solid rgb(211, 211, 211) !important; border-radius: 5px !important; padding: 10px; padding: 10px 12px 0px 12px; font-size: 12px; font-family: Helvetica;'
            }
        ],
        tooltip_delay = 0,
        tooltip_duration = None,
        style_as_list_view = True,
        style_data_conditional = [
            {'if': 
                { 'state': 'active'},
                'backgroundColor': 'white',
                'border-top': '1px solid rgb(211, 211, 211)',
                'border-bottom': '1px solid rgb(211, 211, 211)'},
            {'if': {'column_id': 'No.'}, 'width': 24},
            {'if': {'column_id': 'Ticker'}, 'width': 45},
            {'if': {'column_id': 'Currency'}, 'width': 70},
            {'if': {'column_id': 'Exchange'}, 'width': 72},
            {'if': {'column_id': 'Data Start'}, 'width': 85},
            {'if': {'column_id': 'Data End'}, 'width': 85},
            {'if': {'column_id': 'Length*'}, 'width': 80},
        ],
        id = f'dash-table-selected-tickers',
        style_header = selected_tickers_table_header_css,
        style_data = selected_tickers_table_data_css,
    )

    ################################

    n_tickers = len(updated_tickers)

    if n_tickers > 0:
        
        hide_ticker_container = False

        # portfolio_data_start = f"{min([ticker_info[tk]['start'] for tk in updated_tickers if ticker_info[tk]['start'] != 'N/A'])}"
        # portfolio_data_end = f"{max([ticker_info[tk]['end'] for tk in updated_tickers if ticker_info[tk]['end'] != 'N/A'])}"
        # portfolio_overlap_data_start = f"{max([ticker_info[tk]['start'] for tk in updated_tickers if ticker_info[tk]['start'] != 'N/A'])}"
        # portfolio_overlap_data_end = f"{min([ticker_info[tk]['end'] for tk in updated_tickers if ticker_info[tk]['end'] != 'N/A'])}"

        portfolio_data_start = f"{min([ticker_info[tk]['start'] for tk in updated_tickers])}"
        portfolio_data_end = f"{max([ticker_info[tk]['end'] for tk in updated_tickers])}"
        # portfolio_data_length = f'{len(pd.bdate_range(portfolio_data_start, portfolio_data_end))} business days'

        portfolio_overlap_data_start = f"{max([ticker_info[tk]['start'] for tk in updated_tickers])}"
        portfolio_overlap_data_end = f"{min([ticker_info[tk]['end'] for tk in updated_tickers])}"
        # portfolio_overlap_data_length = f'{len(pd.bdate_range(portfolio_overlap_data_start, portfolio_overlap_data_end))} business days'

        # test_max_length = max([ticker_info[tk]['length'] for tk in updated_tickers])
        # test_overlap_length = min([ticker_info[tk]['length'] for tk in updated_tickers])

        no_overlap_message = 'WARNING: No overlapping dates in the selection'

        portfolio_summary_keys = [
            html.B('Portfolio Ticker Count'), html.Br(),
            html.B('Portfolio Overlapping Dates'), html.Br(),
            html.B('Portfolio All Dates'), html.Br(),
        ]

        if portfolio_overlap_data_start <= portfolio_overlap_data_end:

            portfolio_summary_values_from = [
                html.Span(f'{n_tickers}'), html.Br(),
                html.B('From: '), html.Span(portfolio_overlap_data_start), html.Br(),
                html.B('From: '), html.Span(portfolio_data_start), html.Br()
            ]
            portfolio_summary_values_to = [
                html.Br(),
                html.B('To: '), html.Span(portfolio_overlap_data_end), html.Br(),
                html.B('To: '), html.Span(portfolio_data_end), html.Br()
            ]
        #    portfolio_summary_values_length_key = [
        #        html.Br(),
        #        html.B('Length: '), html.Br(),
        #        html.B('Length: '), html.Br()
        #    ]
        #    portfolio_summary_values_length_value = [
        #        html.Br(),
        #        # html.Span(f'{test_overlap_length} business days'), html.Br(),
        #        # html.Span(f'{test_max_length} business days'), html.Br()
        #        # html.Span(portfolio_overlap_data_length), html.Br(),
        #        # html.Span(portfolio_data_length), html.Br()
        #    ]

        else:
            portfolio_summary_values_from = [
                html.Span(f'{n_tickers}'), html.Br(),
                html.B(no_overlap_message), html.Br(),
                html.B('From: '), html.Span(portfolio_data_start), html.Br()
            ]
            portfolio_summary_values_to = [
                html.Br(),
                html.Br(),
                html.B('To: '), html.Span(portfolio_data_end), html.Br()
            ]
        #    portfolio_summary_values_length_key = [
        #        html.Br(),
        #        html.B('Length: '), html.Br(),
        #        html.B('Length: '), html.Br()
        #    ]
        #    portfolio_summary_values_length_value = [
        #        html.Br(),
        #        html.Span(portfolio_data_length), html.Br(),
        #        html.Span(portfolio_data_length), html.Br()
        #    ]

        select_ticker_portfolio_summary = html.Div(
            [
            html.Div(
                portfolio_summary_keys,
                id = 'portfolio-summary-keys',
                style = portfolio_summary_keys_css
            ),
            html.Div(
                portfolio_summary_values_from,
                id = 'portfolio-summary-values-from',
                style = portfolio_summary_values_from_css
            ),
            html.Div(
                portfolio_summary_values_to,
                id = 'portfolio-summary-values-to',
                style = portfolio_summary_values_to_css
            ),
            # html.Div(
            #     portfolio_summary_values_length_key,
            #     id = 'portfolio-summary-values-length',
            #     style = portfolio_summary_values_length_key_css
            # ),
            # html.Div(
            #     portfolio_summary_values_length_value,
            #     id = 'portfolio-summary-values-length',
            #     style = portfolio_summary_values_length_value_css
            # )
            ],
            style = {'display': 'block'}
        )

    else:
        
        select_ticker_portfolio_summary = html.Div([])
        hide_ticker_container = True

    return (
        ticker_divs,
        hide_ticker_container,
        updated_tickers,
        select_ticker_portfolio_summary,
        '',  # Clear custom ticker input button value
        hide_tk_input_message,
        hide_custom_ticker_info,
        tk_input_message,
        table_custom_ticker_info,
        ticker_info,
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
        table_selected_rows['benchmarks'],

        dash_table_selected_tickers
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
    callback(
        Output(f'collapse-button-table-{id_string}', 'children'),
        Output(f'collapse-table-{id_string}', 'is_open'),
        Input(f'collapse-button-title-{id_string}', 'children'),
        Input(f'collapse-button-table-{id_string}', 'n_clicks'),
        State(f'collapse-table-{id_string}', 'is_open'),

        suppress_callback_exceptions = True
    )(toggle_collapse_tickers)
