import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table, _dash_renderer
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
import dash_mantine_components as dmc
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

# app = dash.Dash(__name__, external_stylesheets = [dmc.styles.ALL, dbc.themes.YETI])
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI, dmc.styles.DATES])

_dash_renderer._set_react_version('18.3.1')
# _dash_renderer._available_react_versions

app.layout = dmc.MantineProvider([

    dmc.Alert(
       'Hi from Dash Mantine Components. You can create some great looking dashboards using me!',
       title = 'Welcome!',
       color = 'violet',
    ),

    html.Div(
        'End Date',
        style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '10px'}
    ),
    dmc.DatePickerInput(
        # minDate = datetime.now(),
        id = 'end-date-input-dmc',
        maxDate = datetime.today(),
        # placeholder = 'Select End Date',
        # label = 'Select End Date',
        # placeholder = 'YYYY-MM-DD',
        valueFormat = 'YYYY-MM-DD',
        highlightToday = True,
        # pointer = False,  # no effect
        # mod = { 'data-size': 'xl' },  # no effect
        size = 'sm',
        w = 100,
        # h = 60,
        style = {
            # 'font-family': 'Helvetica',  # no effect
            # 'font-size': '14px',  # no effect
            # 'font-weight': 'bold',
            'margin-left': '10px'
        }
    ),

    html.Div(
        'Start Date',
        style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '10px'}
    ),
    dmc.DatePickerInput(
        # minDate = datetime.now(),
        id = 'start-date-input-dmc',
        maxDate = datetime.today(),
        # placeholder = 'Select Start Date',
        # label = 'Select Start Date',
        # placeholder = 'YYYY-MM-DD, ddd',
        valueFormat = 'YYYY-MM-DD',
        highlightToday = True,
        # pointer = True,  # no effect
        size = 'sm',
        w = 100,
        # h = 60,
        style = {
            'font-family': 'Times',
            'font-size': '14px',
            # 'font-weight': 'bold',
            # 'text-align': 'right',  # no effect
            'margin-left': '10px'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug = True, port = 8887)