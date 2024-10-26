import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

import yfinance as yf
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta, date
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import matplotlib.patches as patches
from matplotlib.colors import TwoSlopeNorm
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from operator import itemgetter
from mapping_plot_attributes import *
from mapping_tickers import *
from utils import *
from download_data import DownloadData
from analyze_prices import AnalyzePrices


tickers = list(magnificent_7_tickers.keys())
print(tickers)
print(tripledeck_legendtitle)

tk = 'MSFT'
drawdown_color = 'red'
theme = 'dark'
overlay_color_theme = 'grasslands'
overlay_color_themes = list(theme_style[theme]['overlay_color_theme'].keys())
drawdown_colors = list(theme_style[theme]['drawdown_colors'].keys())

deck_type = 'triple'
secondary_y = False
plot_width = 1600
plot_height_1 = 600
plot_height_2 = 150
plot_height_3 = 150
plot_widths = [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800]
upper_deck_heights = [750, 600, 450, 300]
lower_deck_heights = [300, 250, 200, 150, 100]
deck_types = ['Single', 'Double', 'Triple']

end_date = datetime.today()
hist_years, hist_months, hist_days = 1, 0, 0
start_date = datetime(end_date.year - hist_years, end_date.month - hist_months, end_date.day - hist_days)
tk_market = '^GSPC'
hist_data = DownloadData(end_date, start_date, tickers, tk_market)
downloaded_data = hist_data.download_yh_data(start_date, end_date, tickers, tk_market)
df_adj_close = downloaded_data['Adj Close']
df_close = downloaded_data['Close']
df_volume = downloaded_data['Volume']
dict_ohlc = downloaded_data['OHLC']
df_ohlc = dict_ohlc[tk]
ohlc_tk = df_ohlc.copy()
adj_close_tk = df_adj_close[tk]
close_tk = df_close[tk]
open_tk = ohlc_tk['Open']
high_tk = ohlc_tk['High']
low_tk = ohlc_tk['Low']
volume_tk = df_volume[tk]

analyze_prices = AnalyzePrices(end_date, start_date, [tk])
date_index = ohlc_tk.index

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])     # sharp corners

def create_graph(
    # date_index,
    theme,
    deck_type,
    secondary_y,
    plot_width,
    plot_height_1,
    plot_height_2,
    plot_height_3
):

    fig_data = analyze_prices.create_template(
    # fig_data = create_template(    
        date_index,
        deck_type = deck_type,
        secondary_y = secondary_y,
        plot_width = plot_width,
        plot_height_1 = plot_height_1,
        plot_height_2 = plot_height_2,
        plot_height_3 = plot_height_3,
        theme = theme
    )

    fig = fig_data['fig']
    # print(fig_data['y_min'])
    # print(fig_data['y_max'])
    # layout = fig['layout']
    # output_text = f'This is a {deck_type}-deck plot'

    fig_div = html.Div(
            [dcc.Graph(id='test-graph', figure = fig)],
            id='fig_div',
        )

    # return output_text, fig

    return fig_div


#################
# html.Script(src='https://cdn.plot.ly/plotly-latest.min.js')

app.layout = html.Div([
    
    html.Div([

        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        html.Div(
            children = [
            dbc.Button(
                id = 'collapse-button',
                class_name = 'ma-1',
                color = 'primary',
                # color = 'dark',
                size = 'sm',
                n_clicks = 0,
                # n_clicks = 1,
                style = {
                    'display': 'inline-block',
                    'margin-right': '5px',
                    'text-align': 'left',
                    'font-family': 'Helvetica',
                    'font-weight': 'bold',
                    'width': '185px'
                }
            )
        ]),

    dbc.Collapse(

        html.Div(
            id = 'controls-container',
            children =
            [
            html.Div([
                html.Div('Theme', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                dcc.Dropdown(
                    id = 'theme-dropdown',
                    options = ['Dark', 'Light'],
                    value = 'Dark',
                    style = {'width': '90px'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('Deck Type', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                dcc.Dropdown(
                    id='deck-type-dropdown',
                    options = deck_types,
                    value = 'Triple',
                    style = {'width': '110px'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('Secondary Y', style = {'font-weight': 'bold', 'margin-down': '0px'}),        
                dcc.Dropdown(
                    id='secondary-y-dropdown',
                    options = ['No', 'Yes'],
                    value = 'No',
                    style = {'width': '120px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('Plot Width', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                dcc.Dropdown(
                    id='width-dropdown',
                    options = plot_widths,
                    value = 1600,
                    style = {'width': '100px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('Upper Deck Height', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                dcc.Dropdown(
                    id='upper-height-dropdown',
                    options = upper_deck_heights,
                    value = 600,
                    style = {'width': '160px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('Lower Deck Height', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                dcc.Dropdown(
                    id='lower-height-dropdown',
                    options = lower_deck_heights,
                    value = 200,
                    style = {'width': '160px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            ]
#        ))
        ),
        
        id = 'collapse',
        is_open = True
    
    )],
    style = {
        'display': 'inline-block',
        'margin-right': '5px',
        'verticalAlign': 'middle',
        'font-family': 'Helvetica'
    }
    ),

    # style = {'font-family': 'Helvetica', 'font-weight': 'normal', 'margin-down': '5px'}

    html.Br(),

    create_graph(
        # date_index,
        theme,
        deck_type,
        secondary_y,
        plot_width,
        plot_height_1,
        plot_height_2,
        plot_height_3)

])

@app.callback(
    Output('collapse-button', 'children'),
    Output('collapse', 'is_open'),
    Input('collapse-button', 'n_clicks'),
    State('collapse', 'is_open')
)
def toggle_collapse(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'CREATE TEMPLATE'
    label = f'▼ {title}' if is_open else f'▲ {title}'
    if n:
        return label, not is_open
    else:
        return f'▲ {title}', is_open

@app.callback(
    # Output(component_id = 'dd-output-container', component_property = 'children'),
    # Output(component_id = 'test-graph', component_property = 'figure'),
    Output(component_id = 'fig_div', component_property = 'children'),
    Input(component_id = 'theme-dropdown', component_property = 'value'),
    Input(component_id = 'deck-type-dropdown', component_property = 'value'),
    Input(component_id = 'secondary-y-dropdown', component_property = 'value'),
    Input(component_id = 'width-dropdown', component_property = 'value'),
    Input(component_id = 'upper-height-dropdown', component_property = 'value'),
    Input(component_id = 'lower-height-dropdown', component_property = 'value'),
)
def update_graph(
        theme,
        deck_type,
        sec_y,
        width,
        upper_height,
        lower_height
    ):
    theme = theme.lower()
    deck_type = deck_type.lower()
    secondary_y = False if sec_y == 'No' else True
    # width = int(width)
    # upper_height = int(upper_height)
    # lower_height = int(lower_height)
    return create_graph(
        # date_index,
        theme,
        deck_type,
        secondary_y,
        width,
        upper_height,
        lower_height,
        lower_height
        )

# app.layout = html.Div(children=[
#    dcc.Graph(
#        id='example-graph',
#        figure = fig
#    )
# ])


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
