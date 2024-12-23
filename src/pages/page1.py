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

layout = html.Div([

    dcc.Link('Go to Preliminary Ticker Selection', href='/preliminary_ticker_selection_v3'),
    html.Br(),
    dcc.Link('Go to Ticker Info & Portfolio Selection', href='/test_ticker_input_v3'),

    # html.Div(id = 'test-output-div')

])
