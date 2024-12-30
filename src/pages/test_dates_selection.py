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
from mapping_input_tables import *
from css_portfolio_analytics import *
from utils import *

from download_data import DownloadData

import requests_cache

register_page(
    __name__,
    path = '/test_dates_selection'
)

# hist_data = DownloadData()

def initialize_selected_ticker_table():
    
    dash_table_selected_tickers = dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in table_selected_tickers_columns],
        data = [],
        editable = False,
        row_selectable = 'multi',
        selected_rows = [],
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
        id = 'dash-table-selected-tickers',
        style_header = selected_tickers_table_header_css,
        style_data = selected_tickers_table_data_css,
    )

    dash_table_selected_tickers_div = html.Div(
        id = 'dash-table-selected-tickers-div',
        children = [
            html.Div(
                'YOUR PORTFOLIO',
                id = f'table-selected-tickers-title',
                style = input_table_title_css
            ),
            html.Div(
                id = 'dates-table-selected-tickers',
                children = [dash_table_selected_tickers]
            ),
            html.Div(
                '* Length of the range of dates in business days excluding weekends and holidays',
                id = 'dates-table-selected-tickers-footnote',
                style = table_selected_tickers_footnote
            )
        ],
        style = {'width': '1300px', 'margin-left': '5px'}
    )

    return dash_table_selected_tickers_div

# Initialize an empty table first so its id is in the layout
dash_table_selected_tickers_div = initialize_selected_ticker_table()

###########################################################################################

layout = html.Div([

    # LOADING WRAPPER
    dcc.Loading([
        
        html.Div(id = 'dates-selected-tickers', hidden = False, style = {'font-size' : '14px'}),

        # MAIN TITLE
        html.Div(
            'Confirm portfolio selection and choose the common range of dates',
            id = 'dates-main-title',
            style = ticker_main_title_css
        ),

        html.Div(
            id = 'dates-table-selected-tickers-container',
            children = [
                dash_table_selected_tickers_div
            ]
        ),

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
            dcc.Link('Start Over Preliminary Ticker Selection', href='/preliminary_ticker_selection_v3'),
            html.Br(),
            dcc.Link('Back To Ticker Info & Portfolio Selection', href='/test_ticker_input_v3'),
        ],
        style = link_container_css
    )
    # dcc.Link('Continue to Date Range Selection', href='/test_dates_selection')

])  # layout

#################################################

@callback(
    Output('dates-selected-tickers', 'children'),
    # Output('dates-table-selected-tickers', 'children'),
    Output('dash-table-selected-tickers', 'data'),
    Output('dash-table-selected-tickers', 'selected_rows'),
    Output('dash-table-selected-tickers', 'tooltip_data'),

    Input('table-selected-tickers-data-stored', 'data'),
    Input('selected-ticker-summaries-stored', 'data'),
    Input('dash-table-selected-tickers', 'selected_rows'),
)
def read_table_selected_tickers(
    table_selected_tickers_data,
    selected_ticker_summaries,
    selected_rows
):
    
    selected_rows = [k for k in range(len(table_selected_tickers_data))] if selected_rows == [] else selected_rows
    
    # selected_tickers = [row['Ticker'] for row in table_selected_tickers_data]

    tooltip_data = [
        { column: {'value': selected_ticker_summaries[row['Ticker']], 'type': 'markdown' }
        for column in row.keys() }
        for row in table_selected_tickers_data  # e.g. {'No.': 1, 'Ticker': 'AAPL', ...} etc.
    ]

    return (
        # selected_tickers,
        str(selected_rows),
        table_selected_tickers_data,
        selected_rows,
        tooltip_data
    )
