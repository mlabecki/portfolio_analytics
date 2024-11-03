import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

import yfinance as yf
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta, date
import time
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from operator import itemgetter
from mapping_plot_attributes import *
from mapping_tickers import *
from utils import *
from download_data import DownloadData
from analyze_prices import AnalyzePrices

end_date = datetime.today()
hist_years, hist_months, hist_days = 1, 0, 0
start_date = datetime(end_date.year - hist_years, end_date.month - hist_months, end_date.day - hist_days)

hist_data = DownloadData(end_date, start_date)


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])

app.layout = html.Div([
    
    ##### BEGIN TEMPLATE CONTROLS

    html.Div([

        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        html.Div(
            dbc.Button(
                id = 'collapse-button-tickers',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = {
                    'display': 'inline-block',
                    'margin-right': '5px',
                    'text-align': 'left',
                    'font-family': 'Helvetica',
                    'font-weight': 'bold',
                    'width': '250px'
                }
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'ticker-selection',
                children = [

                    html.Div([
                        html.Div('Ticker', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='tickers-dropdown',
                            options = tickers,
                            value = tickers[0],
                            clearable = False,
                            style = {'width': '180px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Theme', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'theme-dropdown',
                            options = ['Dark', 'Light'],
                            value = 'Dark',
                            disabled = False,
                            clearable = False,
                            style = {'width': '90px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Deck Type', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='deck-type-dropdown',
                            options = deck_types,
                            value = 'Single',
                            clearable = False,
                            style = {'width': '110px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Sec Y', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),        
                        dcc.Dropdown(
                            id='secondary-y-dropdown',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '80px', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Plot Width', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'width-input',
                            type = 'number',
                            value = 1450,
                            min = 800,
                            max = 1800,
                            step = 50,
                            style = {'width': '100px', 'height': '36px', 'vertical-align': 'bottom', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'bottom', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Upper Deck Height', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'upper-height-input',
                            type = 'number',
                            value = 750,
                            min = 250,
                            max = 1000,
                            step = 50,
                            style = {'width': '160px', 'height': '36px', 'vertical-align': 'bottom', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'bottom', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Lower Deck Height', style = {'font-weight': 'bold', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'lower-height-input',
                            type = 'number',
                            value = 150,
                            min = 100,
                            max = 300,
                            step = 50,
                            style = {'width': '160px', 'height': '36px', 'vertical-align': 'bottom', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'bottom', 'font-family': 'Helvetica'}
                    ),
                ]  # 'ticker_selection' children
            ),  # html.Div id 'ticker_selection'
                    
            id = 'collapse-tickers',
            is_open = False

        )  # dbc.Collapse
    ]),  # html.Div with dbc.Button and dbc.Collapse


])  # app.layout


@app.callback(
    Output('collapse-button-tickers', 'children'),
    Output('collapse-tickers', 'is_open'),
    Input('collapse-button-tickers', 'n_clicks'),
    State('collapse-tickers', 'is_open')
)
def toggle_collapse_tickers(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'PORTFOLIO TICKER SELECTION'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open