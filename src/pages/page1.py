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

category_option_css = {
    'display': 'block',
    'font-size': '14px',
    'font-weight': 'bold',
    'color': '#007ea7',  # This is native for the YETI theme
    'vertical-align': 'middle',
    'height': '30px',
    'margin-top': '0px',
    'margin-bottom': '2px',
    'margin-left': '10px',
    'padding-left': '10px',
    'padding-top': '3px',
    'border': '2px solid #007ea7'
}

layout = html.Div([

    html.Div(
        id = 'category-options-container',
        children = [
            html.Div(
                'BIGGEST COMPANIES',
                id = 'category-option-biggest-companies',
                style = category_option_css
            ),
            html.Div(
                'S&P 500 COMPANIES',
                id = 'category-option-sp500',
                style = category_option_css
            ),
            html.Div(
                'NASDAQ 100 COMPANIES',
                id = 'category-option-nasdaq100',
                style = category_option_css
            )
        ],
        style = {
            'width': '310px',
            'margin-top': '10px',
            'margin-left': '10px',
            'padding-left': '10px',
        }
    ),

    html.Div(
        id = 'dates-link-container',
        children = [
            dcc.Link('Go to Preliminary Ticker Selection', href='/preliminary_ticker_selection_v3'),
            html.Br(),
            # dcc.Link('Go to Ticker Info & Portfolio Selection', href='/test_ticker_input_v3'),
        ],
        style = link_container_css
    )

    # html.Div(id = 'test-output-div')

])
