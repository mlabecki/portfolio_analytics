from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table, _dash_renderer
from dash_extensions.pages import setup_page_components  # , setup_dynamic_components
from dash import Dash, html, page_container, dcc, page_registry
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# import yfinance as yf
# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta, date
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from operator import itemgetter
# from mapping_plot_attributes import *
# from mapping_portfolio_downloads import *
# from mapping_tickers import *
# from css_portfolio_analytics import *
# from utils import *
# from download_info import DownloadInfo
# 
# hist_info = DownloadInfo()

_dash_renderer._set_react_version('18.3.1')

# app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets = [dbc.themes.YETI])
app = Dash(__name__, use_pages=True, external_stylesheets = [dbc.themes.YETI, dmc.styles.DATES], suppress_callback_exceptions = True)
# app.suppress_callback_exceptions = True

# from pages import preliminary_ticker_selection_v3, page1, page2

app.layout = dmc.MantineProvider(

    # forceColorScheme = 'outline',

    children = [
#app.layout = html.Div([

    dcc.Location(id = 'url', refresh = False),
    page_container,  # page layout is rendered here
    # setup_page_components(), 
    # dcc.Store(data = [], id = 'preselected-updated-tickers', storage_type = 'session'),
    dcc.Store(data = [], id = 'n-preselected-stored', storage_type = 'session'),
    dcc.Store(data = [], id = 'preselected-ticker-tables-stored', storage_type = 'session'),

    # dcc.Store(data = [], id = 'selected-tickers-stored', storage_type = 'session'),
    dcc.Store(data = [], id = 'table-selected-tickers-data-stored', storage_type = 'session'),
    dcc.Store(data = [], id = 'selected-ticker-summaries-stored', storage_type = 'session'),
    dcc.Store(data = {}, id = 'selected-tickers-downloaded-data-stored', storage_type = 'session'),
    # html.Div(children = [], id = 'dash-table-selected-tickers-stored', hidden = True)

    dcc.Store(data = [], id = 'final-table-selected-tickers-data-stored', storage_type = 'session'),
    dcc.Store(data = [], id = 'final-selected-ticker-summaries-stored', storage_type = 'session'),
    dcc.Store(data = [], id = 'final-start-date-stored', storage_type = 'session'),
    dcc.Store(data = [], id = 'final-end-date-stored', storage_type = 'session'),
    dcc.Store(data = {}, id = 'final-selected-tickers-stored', storage_type = 'session'),

    # html.Div(id = 'preselected-output-list')
])

### @callback(
### Output('preselected-output-list', 'children'),
### # Input('updated-tickers-stored', 'data')
### Input('table-selected-rows-stored', 'data')
### )
### def display(table_selected_rows):
###     return str(table_selected_rows)

# @callback(Output('page-content', 'children'),
#           Input('url', 'pathname'))
# def display_page(pathname):
#     if pathname == '/preliminary_ticker_selection_v3':
#         return preliminary_ticker_selection_v3.layout
#     elif pathname == '/page2':
#         return page2.layout
#     else:
#         return page1.layout

# @app.callback(
# Output('preselected-updated-tickers', 'data'),
# Input('url', 'pathname'),
# Input('select-ticker-list', 'children'),
# # Input('preselected-updated-tickers', 'data')
# )
# def store_preselected_updated_tickers(pathname, updated_tickers):  # , stored_updated_tickers):
#     if pathname == '/preliminary_ticker_selection_v3':
#         return updated_tickers
#     else:
#         return []

# @app.callback(
# Output('page-2-preselected-updated-tickers', 'children'),
# Input('url', 'pathname'),
# Input('preselected-updated-tickers', 'data'),
# )
# def pass_preselected_updated_tickers(pathname, stored_updated_tickers):
#     if pathname == '/page2':
#         return stored_updated_tickers
#     else:
#         return []

# @callback(Output('page-content', 'children'),
#           Input('url', 'pathname'))
# def display_page(pathname):
#     if pathname == '/preliminary_ticker_selection_v3':
#         return preliminary_ticker_selection_v3.layout
#     elif pathname == '/page2':
#         return page2.layout
#     else:
#         return preliminary_ticker_selection_v3.layout
#         # return '404'
    

if __name__ == '__main__':
    app.run(debug = True, port = 8888)
    # app.run(debug = True, port = 8888, dev_tools_ui = False, dev_tools_props_check = False)
    # app.run(debug = False, port = 8888, dev_tools_ui = False, dev_tools_props_check = False)