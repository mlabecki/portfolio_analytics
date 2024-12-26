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
    path = '/test_dates_selection'
)

hist_info = DownloadInfo()

@callback(
    # Output('dates-selected-tickers', 'children'),
    Output('dates-tables-selected-tickers', 'children'),

    # Input('selected-tickers-stored', 'data'),
    Input('table-selected-tickers-stored', 'data'),
)
def read_table_selected_tickers(
    # selected_tickers,
    table_selected_tickers,
):
    # return selected_tickers, table_selected_tickers
    return table_selected_tickers


###########################################################################################

layout = html.Div([

    # LOADING WRAPPER
    dcc.Loading([
        
    html.Div(id = 'dates-selected-tickers', hidden = False, style = {'font-size' : '14px'}),

    # MAIN TITLE
    html.Div(
        'Confirm portfolio selection and choose the range of common dates',
        id = 'dates-main-title',
        style = ticker_main_title_css
    ),

    html.Div(
        id = 'dates-tables-selected-tickers',
        children = []
    ),
    html.Div(
        '* Length in business days excluding weekends and holidays',
        id = 'dates-tables-selected-tickers-footnote',
        style = {
            'font-family': 'Helvetica',
            'font-size': '12px',
            'font-style': 'italic',
            'margin-left': '10px'
        }
    )

    ],
    
    id = 'dates-loading-wrapper',
    custom_spinner = html.Div([
        'Loading Selected Tickers',
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
    dcc.Link('Back To Ticker Info & Portfolio Selection', href='/test_ticker_input_v3'),
    # dcc.Link('Continue to Date Range Selection', href='/test_dates_selection')

])  # layout
