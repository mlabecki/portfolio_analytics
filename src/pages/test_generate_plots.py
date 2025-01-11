import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_loading_spinners as dls

from dash import register_page

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
from mapping_portfolio_downloads import *
from mapping_tickers import *
from mapping_input_tables import *
from css_portfolio_analytics import *
from utils import *

from download_data import DownloadData
from download_info import DownloadInfo
from analyze_prices import AnalyzePrices

register_page(
    __name__,
    path = '/test_generate_plots'
)

# end_date = datetime.today().date()
# hist_years, hist_months, hist_days = 5, 0, 0
# start_date = datetime(end_date.year - hist_years, end_date.month - hist_months, end_date.day - hist_days)
# if end_date != datetime.today().date():
#     end_date += timedelta(1) 

hist_data = DownloadData()
analyze_prices = AnalyzePrices()


@callback(
    Output('final-table-selected-tickers', 'children'),
    Output('tickers-dropdown', 'options'),
    Output('tickers-dropdown', 'value'),

    Input('final-table-selected-tickers-data-stored', 'data'),
    Input('final-selected-ticker-summaries-stored', 'data')
)
def display_table_selected_tickers(
    table_data,
    table_tooltip_data
):
    """
    table_data:
        list of dictionaries in the 'records' format
    table_tooltip_data:
        a list of ticker summaries (descriptions)
    downloaded_data:
        a dictionary of historical price and volume data with selected tickers as keys
    """
    
    selected_tickers = [row['Ticker'] for row in table_data]
    first_ticker = selected_tickers[0]

    dash_table_selected_tickers = dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in table_selected_tickers_columns],
        data = table_data,
        editable = False,
        tooltip_data = table_tooltip_data,
        css = [
            {
            'selector': '.dash-tooltip',
            'rule': 'border: None;'
            },
            {
            'selector': '.dash-spreadsheet tr:hover td.dash-cell',
            'rule': 'background-color: rgb(211, 211, 211) !important; color: black !important; border-top: 1px solid rgb(211, 211, 211) !important; border-bottom: 1px solid rgb(211, 211, 211) !important;'
            },
            # {
            # 'selector': '.dash-spreadsheet tr:hover td.dash-select-cell',
            # 'rule': 'background-color: rgb(211, 211, 211) !important; color: black !important; border-top: 1px solid rgb(211, 211, 211) !important; border-bottom: 1px solid rgb(211, 211, 211) !important;'
            # },
            {
            'selector': '.dash-table-tooltip',
            # 'rule': 'max-width: 500px; width: 500px !important; border: 1px solid rgb(67, 172, 106) !important; border-radius: 5px !important; padding: 10px; padding: 10px 12px 0px 12px; font-size: 12px; font-family: Helvetica; background-color: rgb(227, 255, 237);'
            'rule': 'max-width: 500px; width: 500px !important; border: 1px solid rgb(211, 211, 211) !important; border-radius: 5px !important; padding: 10px; padding: 10px 12px 0px 12px; font-size: 12px; font-family: Helvetica; background-color: rgb(211, 211, 211);'
            },
            {
            'selector': '.dash-tooltip:before, .dash-tooltip:after',
            # 'rule': 'border-top-color: #43ac6a !important; border-bottom-color: #43ac6a !important;'
            'rule': 'border-top-color: rgb(211, 211, 211) !important; border-bottom-color: rgb(211, 211, 211) !important;'
            }
        ],
        tooltip_delay = 0,
        tooltip_duration = None,
        style_as_list_view = True,
        style_header_conditional = [
            {'if': {'column_id': 'Length*'}, 'width': 45, 'text-align': 'right', 'padding-right': '10px'},
            {'if': {'column_id': 'No.'}, 'padding-left': '8px'},
        ],
        style_data_conditional = [
            {'if': 
                { 'state': 'active'},
                'backgroundColor': 'white',
                'border-top': '1px solid rgb(211, 211, 211)',
                'border-bottom': '1px solid rgb(211, 211, 211)'},
            {'if': {'column_id': 'No.'}, 'width': 24, 'padding-left': '8px'},
            {'if': {'column_id': 'Ticker'}, 'width': 45},
            {'if': {'column_id': 'Currency'}, 'width': 70},
            {'if': {'column_id': 'Exchange'}, 'width': 72},
            {'if': {'column_id': 'Data Start'}, 'width': 85},
            {'if': {'column_id': 'Data End'}, 'width': 85},
            {'if': {'column_id': 'Length*'}, 'width': 45, 'text-align': 'right', 'padding-right': '15px'},
        ],
        id = 'final-dash-table-selected-tickers',
        style_header = plots_selected_tickers_table_header_css,
        style_data = selected_tickers_table_data_css,
    )

    dash_table_selected_tickers_div = html.Div(
        id = 'final-dash-table-selected-tickers-div',
        children = [
            # html.Div(
            #     'YOUR PORTFOLIO',
            #     id = f'final-table-selected-tickers-title',
            #     style = input_table_title_css
            # ),
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
        style = {'width': '1300px'}
    )

    return (
        dash_table_selected_tickers_div,
        selected_tickers,
        first_ticker
    )

# Initialize an empty table first so its id is in the layout
# dash_final_table_selected_tickers_div = display_final_selected_ticker_table()

##############

#    df_adj_close = downloaded_data['Adj Close']
#    df_close = downloaded_data['Close']
#    df_volume = downloaded_data['Volume']
#    dict_ohlc = downloaded_data['OHLC']
#
#    # Refresh the list of tickers, as some of them may have been removed
#    tickers = list(df_close.columns)
#    # tk = 'MSFT'
#    # tk = tickers[0]
#
#    df_ohlc = dict_ohlc[tk]
#    ohlc_tk = df_ohlc.copy()
#    adj_close_tk = df_adj_close[tk]
#    close_tk = df_close[tk]
#    open_tk = ohlc_tk['Open']
#    high_tk = ohlc_tk['High']
#    low_tk = ohlc_tk['Low']
#    volume_tk = df_volume[tk]
#
#    # print(df_close)
#
#    # We don't want the benchmark ticker in the app menus at this point (for example, 
#    # the drawdown data will not generated) unless tk_market is explicitly selected.
#
#    if tk_market not in tickers_org:
#        tickers = tickers[:-1]  # if added by download_data, tk_market would be in the last position
#
#    analyze_prices = AnalyzePrices(end_date, start_date, tickers)
#    date_index = df_close.index
#
#    sort_by = ['Total Length', '% Depth']
#    portfolio_drawdown_data = {}
#
#    for tk in tickers:
#        drawdown_data = analyze_prices.summarize_tk_drawdowns(df_close, tk, sort_by)
#        n_drawdowns = drawdown_data['Total Drawdowns']
#        drawdown_numbers = [x for x in range(n_drawdowns + 1)[1:]]
#        portfolio_drawdown_data.update({tk: drawdown_data})
#
##############

theme = 'dark'
# overlay_color_theme = 'grasslands'
overlay_color_themes = list(theme_style[theme]['overlay_color_theme'].keys())
# overlay_color_themes = [x.title() for x in theme_style[theme]['overlay_color_theme'].keys()]
# # print(overlay_color_themes)
# # drawdown_colors = list(theme_style[theme]['drawdown_colors'].keys())
drawdown_colors = [x.title() for x in theme_style[theme]['drawdown_colors'].keys()]
# 
# # deck_type = 'triple'
# # deck_type = 'single'
# # deck_type = 'double'
# secondary_y = False
# plot_width = 1600
# plot_height_1 = 750
# plot_height_2 = 150
# plot_height_3 = 150

deck_types = ['Single', 'Double', 'Triple']


#################
# html.Script(src='https://cdn.plot.ly/plotly-latest.min.js')

select_ticker_left_css = {
    'background-color': 'rgba(0, 126, 255, .08)',
    'border-top-left-radius': '2px',
    'border-bottom-left-radius': '2px',
    'border': '1px solid rgba(0, 126, 255, .24)',
    'border-right': '0px',
    'color': '#007eff',
    'display': 'inline-block',
    'cursor': 'pointer',
    'font-family': 'Helvetica',
    'font-size': '14px',
    'line-height': '1.5',
    'padding-left': '5px',
    'padding-right': '5px',
    'margin-top': '5px',
    'vertical-align': 'center'
}
select_ticker_right_css = {
    'background-color': 'rgba(0, 126, 255, .08)',
    'border-top-right-radius': '2px',
    'border-bottom-right-radius': '2px',
    'border': '1px solid rgba(0, 126, 255, .24)',
    'color': '#007eff',
    'display': 'inline-block',
    'font-family': 'Helvetica',
    'font-size': '14px',
    'line-height': '1.5',
    'padding-left': '5px',
    'padding-right': '5px',
    'margin-top': '5px',
    'vertical-align': 'center'
}

layout = html.Div([

    # LOADING WRAPPER
    dcc.Loading([

    html.Div(id = 'plots-start-date', hidden = True, style = {'font-size' : '14px'}),
    html.Div(id = 'plots-end-date', hidden = True, style = {'font-size' : '14px'}),

    # MAIN TITLE
    html.Div(
        'Select template, ticker and plot types',
        id = 'dates-main-title',
        style = ticker_main_title_css
    ),

    ##### BEGIN SIDEBAR MENU ALL CONTROLS

    html.Div([

    ##### SIDEBAR MENU COLLAPSE

    html.Div(
        dbc.Button(
            id = 'collapse-button-sidebar-menu',
            class_name = 'ma-1',
            color = 'primary',
            size = 'sm',
            n_clicks = 0,
            style = collapse_button_menu_css
        )
        # style = {'height': '36px', 'margin-left': '5px'}
    ),

    dbc.Collapse(
        
    id = 'collapse-sidebar-menu',
    is_open = False,
    dimension = 'width',

    children =
    [

    ##### BEGIN TEMPLATE CONTROLS

    html.Div([

        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        html.Div(
            dbc.Button(
                id = 'collapse-button-template',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'template-controls',
                children = [

                    html.Div([
                        html.Div('Ticker', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'tickers-dropdown',
                            className = 'plots-dropdown-button',
                            clearable = False,
                            style = {'width': '300px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div(
                        id = 'plots-selected-ticker-name',
                        style = {
                            'display': 'inline-block',
                            'width': '300px',
                            'color': 'rgb(0, 106, 240)',
                            'margin': '3px 0px 3px 5px',
                            'vertical-align': 'top',
                            'font-family': 'Helvetica',
                            'font-size': '14px'}
                    ),

                    html.Div([
                        html.Div('Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'theme-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Dark', 'Light'],
                            value = 'Dark',
                            disabled = False,
                            clearable = False,
                            style = {'width': '80px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Deck Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='deck-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = deck_types,
                            value = 'Single',
                            clearable = False, 
                            style = {'width': '110px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Secondary Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-bottom': '0px'}),        
                        dcc.Dropdown(
                            id='secondary-y-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '100px'}
                        )],
                        style = {'display': 'inline-block', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Width', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'width-input',
                            type = 'number',
                            value = 1450,
                            min = 800,
                            max = 1600,
                            step = 50,
                            debounce = True,
                            style = {'width': '90px', 'height': '30px', 'font-size': '14px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'vertical-align': 'top'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Height Upper', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '0px'}),
                        dbc.Input(
                            id = 'upper-height-input',
                            type = 'number',
                            value = 750,
                            min = 250,
                            max = 1000,
                            step = 50,
                            debounce = True,
                            style = {'width': '100px', 'height': '30px', 'font-size': '14px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'vertical-align': 'top'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'border-radius': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Height Lower', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'lower-height-input',
                            type = 'number',
                            value = 150,
                            min = 100,
                            max = 300,
                            step = 50,
                            debounce = True,
                            style = {'width': '100px', 'height': '30px', 'font-size': '14px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'vertical-align': 'top', 'font-color': 'black'}
                        )],
                        style = {'display': 'inline-block', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                ]
            ),

            id = 'collapse-template',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ),

    ##### END TEMPLATE CONTROLS

    ##### BEGIN DRAWDOWN CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-drawdowns',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'drawdown-controls',
                children = [

                    html.Div([
                        html.Div('Top DD Number', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id='drawdowns-number-input',
                            type = 'number',
                            value = 5,
                            min = 1,
                            step = 1,
                            style = {'width': '130px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Top DD By', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-topby-dropdown',
                            options = ['% Depth', 'Total Length'],
                            value = '% Depth',
                            clearable = False,
                            style = {'width': '130px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('DD Display', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-display-dropdown',
                            options = ['Peak To Trough', 'Peak To Recovery'],
                            value = 'Peak To Trough',
                            clearable = False,
                            style = {'width': '170px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('DD Color', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-color-dropdown',
                            options = drawdown_colors,
                            value = 'Red',
                            clearable = False,
                            style = {'width': '100px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Price Color Theme', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-price-color-dropdown',
                            options = overlay_color_themes,
                            value = 'Sapphire',
                            clearable = False,
                            style = {'width': '150px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    ### ADD RESET AXES BUTTON

                    html.Div([
                        html.Div('_', style = {'color': 'white', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Button(
                            'Reset Axes',
                            id = 'reset-axes-drawdowns',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'light',
                            size = 'sm',
                            style = {
                                'display': 'inline-block',
                                'height': '36px',
                                'border-color': 'rgb(192, 192, 192)',
                                'border-radius': '5px',
                                'margin-bottom': '0px',
                                'margin-top': 'auto',
                                'text-align': 'center',
                                'font-family': 'Helvetica',
                                'font-size': '15px',
                                'width': '95px'
                            }
                        )],
                        style = {
                            'float': 'right',
                            'vertical-align': 'top',
                            'margin-bottom': '0px',
                            'margin-top': 'auto'
                        }
                    ),

                ],
                style = {'margin-left': '5px'}
            ), 

            id = 'collapse-drawdowns',
            is_open = False

        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END DRAWDOWN CONTROLS

    ##### BEGIN BOLLINGER CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-bollinger',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'bollinger-controls',
                children = [

                    html.Div([
                        html.Div('Target Deck', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),        
                        dcc.Dropdown(
                            id = 'bollinger-deck-dropdown',
                            options = [1],
                            value = 1,
                            # options = [1, 2],
                            # value = 2,
                            clearable = False,
                            style = {'width': '100px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Window Size', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-window-input',
                            type = 'number',
                            value = 20,
                            min = 1,
                            max = 100,
                            step = 1,
                            style = {'width': '120px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('St Dev Multiplier', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-nstd-input',
                            type = 'number',
                            value = 2.0,
                            min = 0,
                            max = 10,
                            step = 0.1,
                            style = {'width': '130px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Number Of Bands', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-nbands-input',
                            type = 'number',
                            value = 1,
                            min = 1,
                            max = 5,
                            step = 1,
                            style = {'width': '140px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Color Theme', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='bollinger-color-theme-dropdown',
                            options = overlay_color_themes,
                            value = 'Grasslands',
                            clearable = False,
                            style = {'width': '120px', 'font-size': '15px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    ### ADD RESET AXES BUTTON

                    html.Div([
                        html.Div('_', style = {'color': 'white', 'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Button(
                            'Reset Axes',
                            id = 'reset-axes-bollinger',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'light',
                            size = 'sm',
                            style = {
                                'display': 'inline-block',
                                'height': '36px',
                                'border-color': 'rgb(192, 192, 192)',                                
                                'border-radius': '5px',
                                'margin-bottom': '0px',
                                'margin-top': 'auto',
                                'text-align': 'center',
                                'font-family': 'Helvetica',
                                'font-size': '15px',
                                'width': '95px'
                            }
                        )],
                        style = {
                            'float': 'right',
                            # 'vertical-align': 'top',
                            'vertical-align': 'top', 
                            'margin-bottom': '0px',
                            'margin-top': 'auto'
                        }
                    ),

                ],
                style = {'margin-left': '5px'}
            ), 

            id = 'collapse-bollinger',
            is_open = False

        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END BOLLINGER CONTROLS

    ]),

    # id = 'collapse-sidebar-menu',
    # is_open = False,
    # dimension = 'width'

    ],
    style = {'display': 'inline-block', 'vertical-align': 'top'}

    ),

    ##### END SIDEBAR MENU ALL CONTROLS

    # style = {'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '5px', 'font-family': 'Helvetica'}
  
    # html.Br(),
    # dcc.Store(id = 'fig_data'),

    html.Div([

        ##### BEGIN SELECTED TICKERS TABLE

        html.Div([
            # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
            html.Div(
                dbc.Button(
                    id = 'collapse-button-final-table-selected-tickers',
                    class_name = 'ma-1',
                    color = 'primary',
                    size = 'sm',
                    n_clicks = 0,
                    style = collapse_button_css
                )
            ),
            dbc.Collapse(
                html.Div(
                    id = 'final-table-selected-tickers',
                    children = []
                ),
                id = 'collapse-final-table-selected-tickers',
                is_open = False
            )],
            style = {'vertical-align': 'top', 'margin-bottom': '5px', 'margin-left': '0px'}
        ),

        ##### BEGIN GRAPH

        html.Div(
            id = 'fig-div',
            children = [],
            style = {'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0px'}
        )
    ],
    style = {'display': 'inline-block', 'vertical-align': 'top'}
    
    )
    ],

    id = 'dates-loading-wrapper',
    custom_spinner = html.Div([
        html.Br(),
        html.Br(),
        'Updating Plot',
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

])


@callback(
    Output('collapse-button-sidebar-menu', 'children'),
    Output('collapse-sidebar-menu', 'is_open'),
    Input('collapse-button-sidebar-menu', 'n_clicks'),
    State('collapse-sidebar-menu', 'is_open')
)
def toggle_collapse_drawdowns(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = ''  # 'MENU'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open
    

@callback(
    Output('collapse-button-final-table-selected-tickers', 'children'),
    Output('collapse-final-table-selected-tickers', 'is_open'),
    Input('collapse-button-final-table-selected-tickers', 'n_clicks'),
    State('collapse-final-table-selected-tickers', 'is_open')
)
def toggle_collapse_final_table_selected_tickers(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'YOUR PORTFOLIO'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-template', 'children'),
    Output('collapse-template', 'is_open'),
    Input('collapse-button-template', 'n_clicks'),
    State('collapse-template', 'is_open')
)
def toggle_collapse_template(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'TEMPLATE AND TICKER'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('lower-height-input', 'disabled'),
    Output('bollinger-deck-dropdown', 'options'),
    Input('deck-type-dropdown', 'value'))
def disable_options(deck_type):
    if deck_type == 'Single':
        return True, [1]
    elif deck_type == 'Double':
        return False, [1, 2]
    else:
        return False, [1, 2, 3]


@callback(
    Output('collapse-button-drawdowns', 'children'),
    Output('collapse-drawdowns', 'is_open'),
    Input('collapse-button-drawdowns', 'n_clicks'),
    State('collapse-drawdowns', 'is_open')
)
def toggle_collapse_drawdowns(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'DRAWDOWNS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-bollinger', 'children'),
    Output('collapse-bollinger', 'is_open'),
    Input('collapse-button-bollinger', 'n_clicks'),
    State('collapse-bollinger', 'is_open')
)
def toggle_collapse_bollinger(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'BOLLINGER BANDS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(

    # Output('test-graph', 'figure'),
    # Output('fig_div', 'children', allow_duplicate = True),
    # Output('test-graph', 'figure'),
    Output('plots-selected-ticker-name', 'children'),

    Output('fig-div', 'children'),
    # Output('drawdown-controls', 'style'),
    # Output('bollinger-controls', 'style'),
    # Output('template-controls', 'style'),

    Output('drawdowns-number-input', 'max'),
    Output('drawdowns-number-input', 'value'),

    Output('plots-start-date', 'children'),
    Output('plots-end-date', 'children'),

    Input('final-start-date-stored', 'data'),
    Input('final-end-date-stored', 'data'),
    Input('final-selected-tickers-stored', 'data'),

    # Input('reset-axes-template', 'n_clicks'),
    Input('reset-axes-drawdowns', 'n_clicks'),
    Input('reset-axes-bollinger', 'n_clicks'),
    
    # template options
    Input('tickers-dropdown', 'value'),
    Input('theme-dropdown', 'value'),
    Input('deck-type-dropdown', 'value'),
    Input('secondary-y-dropdown', 'value'),
    Input('width-input', 'value'),
    Input('upper-height-input', 'value'),
    Input('lower-height-input', 'value'),
    
    # drawdowns options
    Input('drawdowns-number-input', 'value'),
    Input('drawdowns-topby-dropdown', 'value'),
    Input('drawdowns-display-dropdown', 'value'),
    Input('drawdowns-color-dropdown', 'value'),
    Input('drawdowns-price-color-dropdown', 'value'),
    # prevent_initial_call=True #,
    #Input('overlay-dropdown', 'value')

    # bollinger options
    Input('bollinger-deck-dropdown', 'value'),
    Input('bollinger-window-input', 'value'),
    Input('bollinger-nstd-input', 'value'),
    Input('bollinger-nbands-input', 'value'),
    Input('bollinger-color-theme-dropdown', 'value'),

   
)

def update_plot(

        start_date,
        end_date,
        selected_tickers_names,
        # downloaded_data,

        # n_click_template,
        n_click_dd,
        n_click_bollinger,

        # ticker and template options
        tk,
        theme,
        deck_type,
        sec_y,
        width,
        upper_height,
        lower_height,

        # drawdowns options
        n_top, 
        drawdown_top_by, 
        drawdown_display, 
        drawdown_color, 
        price_color_theme,

        # bollinger options
        # tk_bollinger,
        bollinger_deck,
        bollinger_window,
        bollinger_nstd,
        bollinger_nbands,
        bollinger_color_theme

    ):

    selected_tickers = list(selected_tickers_names.keys())

    downloaded_data = hist_data.download_yf_data(start_date, end_date, selected_tickers)

    drawdown_color = drawdown_color.lower() if drawdown_color is not None else 'red'
    price_color_theme = price_color_theme.lower() if price_color_theme is not None else 'base'

    # fig_data = create_graph(theme, tk, drawdown_color, overlay_color_theme)
    date_index = downloaded_data[tk]['ohlc'].index
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

    close_tk = downloaded_data[tk]['ohlc']['Close']

    # if (theme_drawdowns != theme):
    #     theme = theme_drawdowns

    # drawdown_div_style = {
    #     'width': width,
    #     # 'vertical-align': 'top',
    #     # 'margin-top': 'auto', 
    #     # 'margin-bottom': '0px'
    # }
    # bollinger_div_style = drawdown_div_style
    # template_div_style = drawdown_div_style

    drawdown_data_tk = analyze_prices.summarize_tk_drawdowns(close_tk, drawdown_top_by)
    n_drawdowns = drawdown_data_tk['Total Drawdowns']
    # dd_number_options = [x for x in range(n_drawdowns + 1)][1:]
    dd_number_value = min(n_top, n_drawdowns)
    selected_drawdown_data = analyze_prices.select_tk_drawdowns(drawdown_data_tk, n_top)

    show_trough_to_recovery = True if drawdown_display == 'Peak To Recovery' else False
    drawdown_top_by = 'length' if drawdown_top_by == 'Total Length' else 'depth'

    fig_data = analyze_prices.add_drawdowns(
        fig_data,
        close_tk,
        tk,
        selected_drawdown_data,
        n_top_drawdowns = n_top,
        target_deck = 1,
        add_price = True,
        # add_price = False,
        price_type = 'close',
        top_by = drawdown_top_by,
        show_trough_to_recovery = show_trough_to_recovery,
        add_title = True,
        # theme = theme,
        # theme = theme_drawdowns,
        # color_theme = 'base',
        price_color_theme = price_color_theme,
        drawdown_color = drawdown_color
    )
    # fig_div = create_graph(theme, tk, drawdown_color, overlay_color_theme)
    # fig = fig_data['fig']

    
    bollinger_data = analyze_prices.bollinger_bands(close_tk, bollinger_window, bollinger_nstd, bollinger_nbands)
    bollinger_list = bollinger_data['list']
    fig_data = analyze_prices.add_bollinger_overlays(
        fig_data,
        bollinger_list,
        target_deck = bollinger_deck,
        # theme = theme,
        color_theme = bollinger_color_theme
    )
    

    # target_deck = 1
    # plot_height = fig_data['plot_height'][target_deck]
    # y_min = fig_data['y_min'][target_deck]
    # y_max = fig_data['y_max'][target_deck]
    fig = fig_data['fig']
    
#     if n_click:
#         min_n_intervals = n_yintervals_map['min'][plot_height]
#         max_n_intervals = n_yintervals_map['max'][plot_height]
# 
#         y_lower_limit, y_upper_limit, y_delta = set_axis_limits(y_min, y_max, min_n_intervals, max_n_intervals)
# 
#         # y_lower_limit, y_upper_limit, y_delta = 100, 450, 50
# 
#         fig['layout']['yaxis']['range'] = (y_lower_limit, y_upper_limit)
#         fig['layout']['yaxis']['tick0'] = y_lower_limit
#         fig['layout']['yaxis']['dtick'] = y_delta
    
    # fig_div = html.Div(html.Div(dcc.Graph(id = 'drawdowns-graph', figure = fig)))
    # fig_div = html.Div(html.Div(children = [dcc.Graph(id = 'drawdowns-graph', figure = fig)]))
    fig_div = dcc.Graph(id='drawdowns-graph', figure = fig)

    return (
        selected_tickers_names[tk],

        fig_div,
        # drawdown_div_style,
        # bollinger_div_style,
        # template_div_style,

        n_drawdowns,
        dd_number_value,
        start_date,
        end_date
    )
