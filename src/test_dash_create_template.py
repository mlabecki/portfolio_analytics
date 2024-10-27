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
sort_by = ['Total Length', '% Drawdown']

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

    fig_data = analyze_prices.add_hist_price(fig_data, volume_tk, tk, target_deck = 1, secondary_y = False, plot_type = 'bar', add_title = False, price_type = 'volume', theme = theme)

    fig = fig_data['fig']
    # print(fig_data['y_min'])
    # print(fig_data['y_max'])
    # layout = fig['layout']
    # output_text = f'This is a {deck_type}-deck plot'

    # fig_div = html.Div(
    #         [dcc.Graph(id='test-graph', figure = fig)],
    #         id='fig_div',
    #     )

    # return output_text, fig

    # return fig_div
    return fig_data


#################
# html.Script(src='https://cdn.plot.ly/plotly-latest.min.js')

app.layout = html.Div([
    
    html.Div([

        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        html.Div(
            children = [
            dbc.Button(
                id = 'collapse-button-template',
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
                    'width': '220px'
                    # 'width': '185px'
                }
            )
        ]),

    dbc.Collapse(

        html.Div(
            id = 'template-controls',
            children =
            [
            html.Div([
                html.Div('Theme', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                dcc.Dropdown(
                    id = 'theme-dropdown',
                    options = ['Dark', 'Light'],
                    value = 'Dark',
                    disabled = False,
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
                html.Div('Sec Y', style = {'font-weight': 'bold', 'margin-down': '0px'}),        
                dcc.Dropdown(
                    id='secondary-y-dropdown',
                    options = ['No', 'Yes'],
                    value = 'No',
                    style = {'width': '80px', 'font-color': 'black'}
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
                    value = 150,
                    style = {'width': '160px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            ]
#        ))
        ),
        
        id = 'collapse-template',
        is_open = False
    
    )],
    style = {'font-family': 'Helvetica', 'font-weight': 'normal', 'margin-down': '5px'}

    ),

    html.Div([

        html.Div(
            children = [
            dbc.Button(
                id = 'collapse-button-drawdowns',
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
                    # 'width': '33px'
                    'width': '220px'
                }
            )
        ]),

    dbc.Collapse(

        html.Div(
            id = 'drawdown-controls',
            children =
            [
            html.Div([
                html.Div('Theme', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                dcc.Dropdown(
                    id = 'drawdowns-theme-dropdown',
                    options = ['dark', 'light'],
                    value = 'dark',
                    style = {'width': '85px'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('Ticker', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                dcc.Dropdown(
                    id='tickers-dropdown',
                    options = tickers,
                    value = 'MSFT',
                    style = {'width': '110px'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('Top DD Number', style = {'font-weight': 'bold', 'margin-down': '0px'}),        
                dcc.Dropdown(
                    id='drawdowns-number-dropdown',
                    options = [1, 2, 3, 4, 5, 6, 7, 8],
                    value = 5,
                    style = {'width': '140px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('Top DD By', style = {'font-weight': 'bold', 'margin-down': '0px'}),        
                dcc.Dropdown(
                    id='drawdowns-topby-dropdown',
                    options = ['Depth', 'Length'],
                    value = 'Depth',
                    style = {'width': '140px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('DD Display', style = {'font-weight': 'bold', 'margin-down': '0px'}),        
                dcc.Dropdown(
                    id='drawdowns-display-dropdown',
                    options = ['Peak To Trough', 'Peak To Recovery'],
                    value = 'Peak To Trough',
                    style = {'width': '190px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            html.Div([
                html.Div('DD Color', style = {'font-weight': 'bold', 'margin-down': '0px'}),        
                dcc.Dropdown(
                    id='drawdowns-color-dropdown',
                    options = drawdown_colors,
                    value = 'red',
                    style = {'width': '120px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),
            
            html.Div([
                html.Div('Price Color Theme', style = {'font-weight': 'bold', 'margin-down': '0px'}),        
                dcc.Dropdown(
                    id='drawdowns-price-color-dropdown',
                    options = overlay_color_themes,
                    value = 'magenta',
                    style = {'width': '150px', 'font-color': 'black'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                ),

            # html.Div([
                # html.Div('Overlay Theme', style = {'font-weight': 'bold', 'margin-down': '0px'}),
                # dcc.Dropdown(
                    # id='overlay-dropdown',
                    # options = overlay_color_themes,
                    # value = 'grasslands',
                    # style = {'width': '135px', 'font-color': 'black'}
                # )],
                # style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
                # )
            ]
#        ))
        ),
        
        id = 'collapse-drawdowns',
        is_open = False
        # is_open = True
    
    )], 
    style = {'display': 'inline-block', 'margin-right': '5px', 'font-family': 'Helvetica'}
    ),

    # html.Br(),
    
    dcc.Store(id = 'fig_data'),

    html.Div(
        id='fig_div',
        children = []
            # [dcc.Graph(id='test-graph', figure = {})],
    )

])

@app.callback(
    Output('collapse-button-template', 'children'),
    Output('collapse-template', 'is_open'),
    Input('collapse-button-template', 'n_clicks'),
    State('collapse-template', 'is_open')
)
def toggle_collapse_template(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'TEMPLATE OPTIONS'
    label = f'► {title}' if is_open else f'▼ {title}'
    # label = f'▼ {title}' if is_open else f'▲ {title}'
    if n:
        return label, not is_open
    else:
        # return f'▲ {title}', is_open
        return f'► {title}', is_open

@app.callback(
    Output('lower-height-dropdown', 'disabled'),
    Input('deck-type-dropdown', 'value'))
def disable_options(selected_option):
    if selected_option == 'Single':
        return True
    else:
        return False

# @app.callback(
#     # Output(component_id = 'dd-output-container', component_property = 'children'),
#     # Output(component_id = 'test-graph', component_property = 'figure'),
#     # Output(component_id = 'fig_div', component_property = 'children', allow_duplicate = True),
#     Output(component_id = 'fig_div', component_property = 'children'),
#     Input(component_id = 'theme-dropdown', component_property = 'value'),
#     Input(component_id = 'deck-type-dropdown', component_property = 'value'),
#     Input(component_id = 'secondary-y-dropdown', component_property = 'value'),
#     Input(component_id = 'width-dropdown', component_property = 'value'),
#     Input(component_id = 'upper-height-dropdown', component_property = 'value'),
#     Input(component_id = 'lower-height-dropdown', component_property = 'value'),
#     # prevent_initial_call = True
# )
# def update_template(
#         theme,
#         deck_type,
#         sec_y,
#         width,
#         upper_height,
#         lower_height
#     ):
# 
#     theme = theme.lower()
#     deck_type = deck_type.lower()
#     secondary_y = False if sec_y == 'No' else True
#     # width = int(width)
#     # upper_height = int(upper_height)
#     # lower_height = int(lower_height)
#     # fig_data = create_graph(
#     # # return create_graph(
#     #     # date_index,
#     #     theme,
#     #     deck_type,
#     #     secondary_y,
#     #     width,
#     #     upper_height,
#     #     lower_height,
#     #     lower_height
#     #     )
#     fig_data = analyze_prices.create_template(
#     # fig_data = create_template(    
#         date_index,
#         deck_type = deck_type,
#         secondary_y = secondary_y,
#         plot_width = width,
#         plot_height_1 = upper_height,
#         plot_height_2 = lower_height,
#         plot_height_3 = lower_height,
#         theme = theme
#     )

    fig = fig_data['fig']
    # fig_div = html.Div(dcc.Graph(id='template-graph', figure = fig))
    fig_div = dcc.Graph(id='template-graph', figure = fig)
    return fig_div


@app.callback(
    Output('collapse-button-drawdowns', 'children'),
    Output('collapse-drawdowns', 'is_open'),
    Input('collapse-button-drawdowns', 'n_clicks'),
    State('collapse-drawdowns', 'is_open')
)
def toggle_collapse_drawdowns(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'UPPER PLOT OPTIONS'
    label = f'► {title}' if is_open else f'▼ {title}'
    # label = f'▼ {title}' if is_open else f'▲ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open
        #return f'▼ {title}', is_open
    
    # label = '▼' if is_open else '▲'
    # if n:
    #     return label, not is_open
    # else:
    #     return '▲', is_open

@app.callback(
    # Output(component_id = 'dd-output-container', component_property = 'children'),
    # Output(component_id = 'test-graph', component_property = 'figure'),
    # Output(component_id = 'fig_div', component_property = 'children', allow_duplicate = True),
    Output(component_id = 'fig_div', component_property = 'children'),
    # Output(component_id = 'fig_div', component_property = 'children'),
    Input(component_id = 'theme-dropdown', component_property = 'value'),
    Input(component_id = 'deck-type-dropdown', component_property = 'value'),
    Input(component_id = 'secondary-y-dropdown', component_property = 'value'),
    Input(component_id = 'width-dropdown', component_property = 'value'),
    Input(component_id = 'upper-height-dropdown', component_property = 'value'),
    Input(component_id = 'lower-height-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-theme-dropdown', component_property = 'value'),
    Input(component_id = 'tickers-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-number-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-topby-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-display-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-color-dropdown', component_property = 'value'),
    Input(component_id = 'drawdowns-price-color-dropdown', component_property = 'value'),
    # prevent_initial_call=True #,
    #Input(component_id = 'overlay-dropdown', component_property = 'value')
)

def update_drawdowns(
        # template options
        theme,
        deck_type,
        sec_y,
        width,
        upper_height,
        lower_height,
        # drawdowns options
        theme_drawdowns,
        tk, 
        n_top, 
        top_by, 
        drawdown_display, 
        drawdown_color, 
        price_color_theme
    ):

    # fig_data = create_graph(theme, tk, drawdown_color, overlay_color_theme)
    theme = theme.lower()
    deck_type = deck_type.lower()
    secondary_y = False if sec_y == 'No' else True
    fig_data = analyze_prices.create_template(
        date_index,
        deck_type = deck_type,
        secondary_y = secondary_y,
        plot_width = width,
        plot_height_1 = upper_height,
        plot_height_2 = lower_height,
        plot_height_3 = lower_height,
        theme = theme
    )

    drawdown_data = analyze_prices.summarize_tk_drawdowns(df_close, tk, sort_by, n_top)
    show_trough_to_recovery = True if drawdown_display == 'Peak To Recovery' else False
    fig_data = analyze_prices.add_drawdowns(
        fig_data,
        # close_tk,
        df_close[tk],
        tk,
        drawdown_data,
        n_top_drawdowns = n_top,
        target_deck = 1,
        add_price = True,
        # add_price = False,
        price_type = 'close',
        top_by = top_by.lower(),
        show_trough_to_recovery = show_trough_to_recovery,
        add_title = True,
        theme = theme_drawdowns,
        # color_theme = 'base'
        price_color_theme = price_color_theme.lower(),
        drawdown_color = drawdown_color
    )
    # fig_div = create_graph(theme, tk, drawdown_color, overlay_color_theme)
    fig = fig_data['fig']
    # fig_div = html.Div(dcc.Graph(id='drawdowns-graph', figure = fig))
    fig_div = dcc.Graph(id='drawdowns-graph', figure = fig)
    return fig_div


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
