# from dash import dcc, html, Input, Output, callback, register_page

from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table, register_page
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import yfinance as yf
import pandas as pd
import numpy as np
from operator import itemgetter
from mapping_plot_attributes import *
from mapping_portfolio_downloads import *
from mapping_tickers import *
from css_portfolio_analytics import *
from utils import *

register_page(
    __name__,
    path = '/'
)

input_table_columns_equities = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Industry', 'Sector', 'Exchange', 'Currency']

ticker_category_info_map = {
    'volatility_indices': {
        'columns': input_table_columns_equities,
        'id_string': 'volatility-indices',
        'collapse_title': 'VOLATILITY INDICES',
        'df': pd.DataFrame().to_dict(),
        'row': {},
        'hidden': True
    }, 
    'benchmarks': {
        'columns': input_table_columns_equities,
        'id_string': 'benchmarks',
        'collapse_title': 'BENCHMARKS',
        'df': pd.DataFrame().to_dict(),
        'row': {},
        'hidden': True
    }
}

@callback(
    Output('page1-ticker-info-test', 'data'),
    Output('test-output-div', 'children'),
    Input('test-dropdown', 'value')
)
def store_data_test(val):
    
    for category in ticker_category_info_map.keys():
        cols = ticker_category_info_map[category]['columns']
        idx = ticker_category_info_map[category]['df'].keys()
        df_data = ticker_category_info_map[category]['df']
        df_ticker_category = pd.DataFrame(data = df_data, index = idx, columns = cols)
        df_ticker_category = df_ticker_category.sort_values(by = 'No.')

    if val:
        return ticker_category_info_map, str(df_ticker_category)
    else:
        return {}, ''


layout = html.Div([

    dcc.Dropdown(id='test-dropdown', options = ['Depth', 'Length'], value = 'Depth',),

    dcc.Store(data = {}, id = 'page1-ticker-info-test', storage_type = 'session'),

    dcc.Link('Go to Preliminary Ticker Selection', href='/preliminary_ticker_selection_v3'),
    html.Br(),
    dcc.Link('Go to Ticker Info & Portfolio Selection', href='/test_ticker_input_v3'),
    # dcc.Link('Go to Page 2', href='/page2')

    html.Div(id = 'test-output-div')

])


# @callback(
#     Output('page-1-display-value', 'children'),
#     Input('page-1-dropdown', 'value'))
# def display_value(value):
#     return f'You have selected {value}'