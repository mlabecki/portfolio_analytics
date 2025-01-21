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
    Output('dash-table-tickers-to-plot-div', 'children'),
    # Output('tickers-dropdown', 'options'),
    # Output('tickers-dropdown', 'value'),

    Input('final-table-selected-tickers-data-stored', 'data'),
    Input('final-selected-ticker-summaries-stored', 'data'),
    Input('final-selected-tickers-stored', 'data')
)
def display_table_selected_tickers(
    table_data,
    table_tooltip_data,
    selected_ticker_names
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
    # first_ticker = selected_tickers[0]

    dash_table_selected_tickers = dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in plots_table_selected_tickers_columns],
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
            {
            'selector': '.dash-spreadsheet tr:hover td.dash-select-cell',
            'rule': 'background-color: rgb(211, 211, 211) !important; color: black !important; border-top: 1px solid rgb(211, 211, 211) !important; border-bottom: 1px solid rgb(211, 211, 211) !important;'
            },
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
            # {'if': {'column_id': 'Length*'}, 'width': 45, 'text-align': 'right', 'padding-right': '10px'},
            {'if': {'column_id': 'No.'}, 'padding-left': '8px'},
        ],
        style_data_conditional = [
            {'if': 
                {'state': 'active'},
                'backgroundColor': 'white',
                'border-top': '1px solid rgb(211, 211, 211)',
                'border-bottom': '1px solid rgb(211, 211, 211)'},
            {'if': {'column_id': 'No.'}, 'width': 24, 'padding-left': '8px'},
            {'if': {'column_id': 'Ticker'}, 'width': 45},
            {'if': {'column_id': 'Currency'}, 'width': 70},
            {'if': {'column_id': 'Exchange'}, 'width': 72},
            # {'if': {'column_id': 'Data Start'}, 'width': 85},
            # {'if': {'column_id': 'Data End'}, 'width': 85},
            # {'if': {'column_id': 'Length*'}, 'width': 45, 'text-align': 'right', 'padding-right': '15px'},
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
            # html.Div(
            #     '* Length of the range of dates in business days excluding weekends and holidays',
            #     id = 'dates-table-selected-tickers-footnote',
            #     style = table_selected_tickers_footnote
            # )
        ],
        style = {'width': '1300px'}
    )

    dash_table_tickers_to_plot = dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in ['Ticker', 'Name']],
        data = [{'Ticker': tk, 'Name': selected_ticker_names[tk]} for tk in selected_tickers],
        editable = False,
        row_selectable = 'multi',
        selected_rows = [0],
        tooltip_data = table_tooltip_data,
        css = [
            {
                # Hide the header
               'selector': 'tr:first-child',
               'rule': 'display: none',
            },
            {
            'selector': '.dash-tooltip',
            'rule': 'border: None;'
            },
            {
            'selector': '.dash-spreadsheet tr:hover td.dash-cell',
            'rule': 'background-color: rgb(211, 211, 211) !important; color: black !important; border-top: 1px solid rgb(211, 211, 211) !important; border-bottom: 1px solid rgb(211, 211, 211) !important;'
            },
            {
            'selector': '.dash-spreadsheet tr:hover td.dash-select-cell',
            'rule': 'background-color: rgb(211, 211, 211) !important; color: black !important; border-top: 1px solid rgb(211, 211, 211) !important; border-bottom: 1px solid rgb(211, 211, 211) !important;'
            },
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
        # style_header_conditional = [
        #     {'if': {'column_id': 'No.'}, 'padding-left': '8px'},
        # ],
        style_data_conditional = [
            {'if': 
                {'state': 'active'},
                'width': '300px !important',
                'backgroundColor': 'white',
                'border-top': '1px solid rgb(211, 211, 211)',
                'border-bottom': '1px solid rgb(211, 211, 211)'},
            # {'if': {'column_id': 'No.'}, 'width': 24, 'padding-left': '8px'},
            {'if': {'column_id': 'Ticker'}, 'width': 50},
            {'if': {'column_id': 'Name'}, 'width': 200},
        ],
        id = 'dash-table-tickers-to-plot',
        # style_header = plots_selected_tickers_table_header_css,
        style_table={'overflowX': 'auto'},
        style_data = selected_tickers_table_data_css
    )

    return (
        dash_table_selected_tickers_div,
        dash_table_tickers_to_plot
        # selected_tickers,
        # first_ticker
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
overlay_color_themes = [x.title() for x in theme_style[theme]['overlay_color_theme'].keys()]
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

def deck_number(deck_type, deck_name):
    if deck_name == 'Middle':
        return 2
    elif deck_name == 'Lower':
        return 2 if deck_type == 'Double' else 3
    else:  
        # 'Upper' and all else
        return 1

ma_type_map = {
    'Simple': 'sma',
    'Exponential': 'ema',
    'Double Exponential': 'dema',
    'Triple Exponential': 'tema',
    'Weighted': 'wma',
    'Welles Wilder': 'wwma'
}


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

    dbc.Row([

    dbc.Col([  # Col 1

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

##### BEGIN TICKERS CONTROLS

    html.Div([

        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        html.Div(
            dbc.Button(
                id = 'collapse-button-tickers',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'tickers-controls',
                children = [

                    html.Div([
                        html.Div(
                            'Select Tickers To Plot',
                            style = {
                                'display': 'block',
                                'font-size': '14px',
                                'font-weight': 'bold',
                                'vertical-align': 'top',
                                'height': '20px',
                                'margin-top': '5px',
                                'margin-bottom': '5px'
                            }
                        ),
                        html.Div(
                            id = 'dash-table-tickers-to-plot-div',
                            # children = []
                        ),
                        # dcc.Dropdown(
                        #     id = 'tickers-dropdown',
                        #     className = 'plots-dropdown-button',
                        #     multi = True,
                        #     clearable = False,
                        #     style = {'width': '300px', 'vertical-align': 'middle'}
                        # )
                        ],
                        style = {
                            'display': 'block',
                            'margin-right': '0px',
                            'vertical-align': 'middle',
                            'font-family': 'Helvetica'
                        }
                    ),

                    html.Div(
                        id = 'plots-selected-ticker-names-div',
                        style = {
                            'display': 'block',
                            'width': '300px',
                            'color': 'rgb(0, 106, 240)',
                            'margin': '3px 0px 3px 5px',
                            'vertical-align': 'bottom',
                            'font-family': 'Helvetica',
                            'font-size': '14px'}
                    ),
                ]
            ),

            id = 'collapse-tickers',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ),

    ##### END TICKERS CONTROLS

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
                        html.Div('Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '3px'}),
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
                        html.Div('Deck Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '3px'}),
                        dcc.Dropdown(
                            id='deck-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = deck_types,
                            value = 'Single',
                            clearable = False, 
                            style = {'width': '108px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Secondary Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '3px'}),
                        dcc.Dropdown(
                            id='secondary-y-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '102px'}
                        )],
                        style = {'display': 'inline-block', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Width', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'width-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 1450,
                            min = 800,
                            max = 1800,
                            step = 50,
                            debounce = True,
                            style = {'width': '90px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Height Upper', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '0px'}),
                        dbc.Input(
                            id = 'upper-height-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 750,
                            min = 250,
                            max = 1000,
                            step = 50,
                            debounce = True,
                            style = {'width': '100px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'border-radius': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Height Lower', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'lower-height-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 150,
                            min = 100,
                            max = 300,
                            step = 50,
                            debounce = True,
                            style = {'width': '100px'}
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

    ##### BEGIN HISTORICAL PRICE CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-hist-price',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'hist-price-controls',
                children = [

                    html.Div([
                        html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'hist-price-deck-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Upper'],
                            value = 'Upper',
                            clearable = False,
                            style = {'width': '115px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),


                    html.Div([
                        html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='hist-price-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Close', 'High', 'Low', 'Open'],
                            value = 'Close',
                            clearable = False,
                            style = {'width': '100px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='hist-price-adjusted-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '75px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='hist-price-plot-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Line', 'Histogram'],
                            value = 'Line',
                            clearable = False,
                            style = {'width': '110px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Fill Below', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='hist-price-fill-below-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '90px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='hist-price-add-title-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '90px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='hist-price-color-theme-dropdown',
                            className = 'plots-dropdown-button',
                            options = overlay_color_themes,
                            value = 'Base',
                            clearable = False,
                            style = {'width': '130px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Plot On Secondary Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='hist-price-secondary-y-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            disabled = True,
                            style = {'width': '165px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        dbc.Button(
                            'Add To Plot',
                            id = f'add-hist-price-button',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'success',
                            size = 'sm',
                            style = plots_add_button_css
                        )],
                        # style = {'margin-bottom': '5px'}
                    ),

                ],
                # style = {'margin-left': '5px'}
            ), 

            id = 'collapse-hist-price',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END HISTORICAL PRICE CONTROLS

    ##### BEGIN CANDLESTICK CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-candlestick',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'candlestick-controls',
                children = [

                    html.Div([
                        html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'candlestick-deck-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Upper'],
                            value = 'Upper',
                            clearable = False,
                            style = {'width': '120px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='candlestick-adjusted-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '78px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px'}),
                        dcc.Dropdown(
                            id='candlestick-add-title-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '92px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Candle Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='candlestick-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Hollow', 'Traditional'],
                            value = 'Hollow',
                            clearable = False,
                            style = {'width': '135px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Candle Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='candlestick-color-theme-dropdown',
                            className = 'plots-dropdown-button',
                            # options = candlestick_color_themes,
                            options = ['Green-Red'],
                            value = 'Green-Red',
                            clearable = False,
                            style = {'width': '160px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        dbc.Button(
                            'Add To Plot',
                            id = 'add-candlestick-button',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'success',
                            size = 'sm',
                            style = plots_add_button_css
                        )],
                        # style = {'margin-bottom': '5px'}
                    ),

                ],
                # style = {'margin-left': '5px'}
            ), 

            id = 'collapse-candlestick',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END CANDLESTICK CONTROLS

    ##### BEGIN VOLUME CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-volume',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'volume-controls',
                children = [

                    html.Div([
                        html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'volume-deck-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Upper'],
                            value = 'Upper',
                            clearable = False,
                            style = {'width': '81px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    # Keep for Dollar Volume
                    #
                    # html.Div([
                    #     html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                    #     dcc.Dropdown(
                    #         id='dollar-volume-type-dropdown',
                    #         className = 'plots-dropdown-button',
                    #         options = ['Close', 'High', 'Low', 'Open'],
                    #         value = 'Close',
                    #         clearable = False,
                    #         style = {'width': '100px'}
                    #     )],
                    #     style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    # ),
# 
                    # html.Div([
                    #     html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                    #     dcc.Dropdown(
                    #         id='dollar-volume-adjusted-dropdown',
                    #         className = 'plots-dropdown-button',
                    #         options = ['Yes', 'No'],
                    #         value = 'Yes',
                    #         clearable = False,
                    #         style = {'width': '75px'}
                    #     )],
                    #     style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    # ),

                    html.Div([
                        html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                        dcc.Dropdown(
                            id='volume-plot-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Histogram', 'Line'],
                            value = 'Histogram',
                            clearable = False,
                            style = {'width': '98px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '0px'}),
                        dcc.Dropdown(
                            id='volume-color-theme-dropdown',
                            className = 'plots-dropdown-button',
                            options = overlay_color_themes,
                            value = 'Base',
                            clearable = False,
                            style = {'width': '104px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Fill Below', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='volume-fill-below-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '80px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    # Volume should not be the primary title
                    #
                    # html.Div([
                    #     html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                    #     dcc.Dropdown(
                    #         id='volume-add-title-dropdown',
                    #         className = 'plots-dropdown-button',
                    #         options = ['Yes', 'No'],
                    #         value = 'Yes',
                    #         clearable = False,
                    #         style = {'width': '90px'}
                    #     )],
                    #     style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    # ),

                    html.Div([
                        html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='volume-add-title-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '70px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Plot On Secondary Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='volume-secondary-y-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            disabled = True,
                            style = {'width': '140px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        dbc.Button(
                            'Add To Plot',
                            id = f'add-volume-button',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'success',
                            size = 'sm',
                            style = plots_add_button_css
                        )],
                        # style = {'margin-bottom': '5px'}
                    ),

                ],
                # style = {'margin-left': '5px'}
            ), 

            id = 'collapse-volume',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END VOLUME CONTROLS

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
                        html.Div('Top DD #', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'drawdowns-number-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 5,
                            min = 0,
                            step = 1,
                            debounce = True,
                            style = {'width': '63px'}
                        )],
                        style = {'display': 'inline-block', 'margin-bottom': '5px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Top DD By', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'drawdowns-topby-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['% Depth', 'Total Length'],
                            value = '% Depth',
                            clearable = False,
                            style = {'width': '112px'}
                        )],
                        style = {'display': 'inline-block', 'margin-bottom': '5px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('DD Display', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id  ='drawdowns-display-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['To Trough', 'To Recovery'],
                            value = 'To Trough',
                            clearable = False,
                            style = {'width': '115px'}
                        )],
                        style = {'display': 'inline-block', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Add Price', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'drawdowns-add-price-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '85px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'drawdowns-price-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Close', 'High', 'Open', 'Low'],
                            value = 'Close',
                            clearable = False,
                            style = {'width': '115px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'drawdowns-adjusted-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '90px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('DD Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'drawdowns-color-dropdown',
                            className = 'plots-dropdown-button',
                            options = drawdown_colors,
                            value = 'Red',
                            clearable = False,
                            style = {'width': '90px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Price Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'drawdowns-price-color-dropdown',
                            className = 'plots-dropdown-button',
                            options = overlay_color_themes,
                            value = 'Sapphire',
                            clearable = False,
                            disabled = False,
                            style = {'width': '130px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='drawdowns-add-title-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '70px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        dbc.Button(
                            'Add To Plot',
                            id = f'add-drawdowns-button',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'success',
                            size = 'sm',
                            style = plots_add_button_css
                        )],
                    ),

                ],
                # style = {'margin-left': '5px'}
            ), 

            id = 'collapse-drawdowns',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END DRAWDOWN CONTROLS

    ##### BEGIN PRICE OVERLAYS CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-price-overlays',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'price-overlays-controls',
                children = [

                    html.Div([
                        html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'price-overlays-deck-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Upper'],
                            value = 'Upper',
                            clearable = False,
                            style = {'width': '79px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                        dcc.Dropdown(
                            id='price-overlays-color-theme-dropdown',
                            className = 'plots-dropdown-button',
                            options = overlay_color_themes,
                            value = 'Gold',
                            clearable = False,
                            style = {'width': '104px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Add Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px'}),
                        dcc.Dropdown(
                            id='price-overlays-add-yaxis-title-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '106px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div('Select Price Types', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px'}),
                    html.Div(
                        id = 'price-overlays-price-list-container',
                        children = [
                            dbc.Checklist(
                                id = 'price-overlays-adj-price-list',
                                options = [
                                    {'label': 'Adjusted Close', 'value': 'Adjusted Close'},
                                    {'label': 'Adjusted Open', 'value': 'Adjusted Open'},
                                    {'label': 'Adjusted High', 'value': 'Adjusted High'},
                                    {'label': 'Adjusted Low', 'value': 'Adjusted Low'}
                                ],
                                value = [],
                                label_style = {
                                    'width': '106px',
                                    'font-family': 'Helvetica',
                                    'font-size': '14px',
                                    'color': 'black',
                                    'margin-right': '0px',
                                    'margin-bottom': '0px'
                                },
                                label_checked_style = {
                                    'width': '106px',
                                    'font-family': 'Helvetica',
                                    'font-size': '14px',
                                    'font-weight': 'bold',
                                    # 'color': 'rgb(0, 126, 255)'
                                },
                                # input_style = {'width': '24px'},
                                input_checked_style = {
                                    'background-color': 'rgb(0, 126, 255)',
                                    'border-color': 'rgb(0, 126, 255)'
                                },
                                inline = True,
                            ),
                            dbc.Checklist(
                                id = 'price-overlays-price-list',
                                options = [
                                    {'label': 'Close', 'value': 'Close'},
                                    {'label': 'Open', 'value': 'Open'},
                                    {'label': 'High', 'value': 'High'},
                                    {'label': 'Low', 'value': 'Low'}
                                ],
                                value = [],
                                label_style = {
                                    'width': '33px',
                                    'font-family': 'Helvetica',
                                    'font-size': '14px',
                                    'color': 'black',
                                    'margin-right': '0px',
                                    'margin-bottom': '0px'
                                },
                                label_checked_style = {
                                    'width': '33px',
                                    'font-family': 'Helvetica',
                                    'font-size': '14px',
                                    'font-weight': 'bold',
                                    # 'color': 'rgb(0, 126, 255)'
                                },
                                # input_style = {'width': '24px'},
                                input_checked_style = {
                                    'background-color': 'rgb(0, 126, 255)',
                                    'border-color': 'rgb(0, 126, 255)'
                                },
                                inline = True,
                            )
                        ],
                        style = {
                            'display': 'inline-block',
                            'margin-left': '5px'
                            # 'justify-content': 'space-between',
                        }
                    ),

                    # dbc.Checkbox(
                    #     id = "price-overlays-adj-close-checkbox",
                    #     label = "Adjusted Close",
                    #     value = False,
                    #     label_style = {'font-family': 'Helvetica', 'font-size': '14px', 'color': 'black', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # label_checked_style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'color': 'darkgreen', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # input_checked_style = {'color': 'darkgreen'},
                    # ),
                    # dbc.Checkbox(
                    #     id = "price-overlays-adj-open-checkbox",
                    #     label = "Adjusted Open",
                    #     value = False,
                    #     label_style = {'font-family': 'Helvetica', 'font-size': '14px', 'color': 'black', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # label_checked_style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'color': 'darkgreen', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # input_checked_style = {'color': 'darkgreen'},
                    # ),
                    # dbc.Checkbox(
                    #     id = "price-overlays-adj-high-checkbox",
                    #     label = "Adjusted High",
                    #     value = False,
                    #     label_style = {'font-family': 'Helvetica', 'font-size': '14px', 'color': 'black', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # label_checked_style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'color': 'darkgreen', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # input_checked_style = {'color': 'darkgreen'},
                    # ),
                    # dbc.Checkbox(
                    #     id = "price-overlays-adj-low-checkbox",
                    #     label = "Adjusted Low",
                    #     value = False,
                    #     label_style = {'font-family': 'Helvetica', 'font-size': '14px', 'color': 'black', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # label_checked_style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'color': 'darkgreen', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # input_checked_style = {'color': 'darkgreen'},
                    # ),
                    # dbc.Checkbox(
                    #     id = "price-overlays-close-checkbox",
                    #     label = "Close",
                    #     value = False,
                    #     label_style = {'font-family': 'Helvetica', 'font-size': '14px', 'color': 'black', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # label_checked_style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'color': 'darkgreen', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # input_checked_style = {'color': 'darkgreen'},
                    # ),
                    # dbc.Checkbox(
                    #     id = "price-overlays-open-checkbox",
                    #     label = "Open",
                    #     value = False,
                    #     label_style = {'font-family': 'Helvetica', 'font-size': '14px', 'color': 'black', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # label_checked_style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'color': 'darkgreen', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # input_checked_style = {'color': 'darkgreen'},
                    # ),
                    # dbc.Checkbox(
                    #     id = "price-overlays-high-checkbox",
                    #     label = "High",
                    #     value = False,
                    #     label_style = {'font-family': 'Helvetica', 'font-size': '14px', 'color': 'black', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # label_checked_style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'color': 'darkgreen', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # input_checked_style = {'color': 'darkgreen'},
                    # ),
                    # dbc.Checkbox(
                    #     id = "price-overlays-low-checkbox",
                    #     label = "Low",
                    #     value = False,
                    #     label_style = {'font-family': 'Helvetica', 'font-size': '14px', 'color': 'black', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # label_checked_style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'color': 'darkgreen', 'margin-right': '5px', 'margin-bottom': '5px'},
                    #     # input_checked_style = {'color': 'darkgreen'},
                    # ),

                    html.Div([
                        dbc.Button(
                            'Add To Plot',
                            id = f'add-price-overlays-button',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'success',
                            size = 'sm',
                            style = plots_add_button_css
                        )],
                        # style = {'margin-bottom': '5px'}
                    ),

                ],
                # style = {'margin-left': '5px'}
            ), 

            id = 'collapse-price-overlays',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END PRICE OVERLAYS CONTROLS

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
                        html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'bollinger-deck-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Upper'],
                            value = 'Upper',
                            clearable = False,
                            style = {'width': '115px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),


                    html.Div([
                        html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='bollinger-price-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Close', 'High', 'Low', 'Open'],
                            value = 'Close',
                            clearable = False,
                            style = {'width': '100px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='bollinger-adjusted-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '75px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('# Of Bands', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-nbands-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 1,
                            min = 1,
                            max = 5,
                            step = 1,
                            debounce = True,
                            style = {'width': '85px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Window Size', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-window-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 20,
                            min = 1,
                            max = 100,
                            step = 1,
                            debounce = True,
                            style = {'width': '100px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('St Dev Factor', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'bollinger-nstd-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 2.0,
                            min = 0,
                            max = 10,
                            step = 0.1,
                            debounce = True,
                            style = {'width': '105px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Moving Ave / St Dev Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='bollinger-ma-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Simple', 'Exponential', 'Weighted'],
                            value = 'Simple',
                            clearable = False,
                            style = {'width': '182px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='bollinger-color-theme-dropdown',
                            className = 'plots-dropdown-button',
                            options = overlay_color_themes,
                            value = 'Gold',
                            clearable = False,
                            style = {'width': '113px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        dbc.Button(
                            'Add To Plot',
                            id = f'add-bollinger-button',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'success',
                            size = 'sm',
                            style = plots_add_button_css
                        )],
                        # style = {'margin-bottom': '5px'}
                    ),

                ],
                # style = {'margin-left': '5px'}
            ), 

            id = 'collapse-bollinger',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END BOLLINGER CONTROLS

    ##### BEGIN MA ENVELOPE CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-ma-env',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'ma-env-controls',
                children = [

                    html.Div([
                        html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'ma-env-deck-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Upper'],
                            value = 'Upper',
                            clearable = False,
                            style = {'width': '115px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-env-price-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Close', 'High', 'Low', 'Open'],
                            value = 'Close',
                            clearable = False,
                            style = {'width': '100px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-env-adjusted-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '75px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('# Of Envelopes', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'ma-env-nbands-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 1,
                            min = 1,
                            max = 5,
                            step = 1,
                            debounce = True,
                            style = {'width': '120px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Window Size', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'ma-env-window-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 20,
                            min = 1,
                            max = 100,
                            step = 1,
                            debounce = True,
                            style = {'width': '100px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('% Width', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'ma-env-offset-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 5.0,
                            min = 0,
                            max = 50,
                            step = 2.5,
                            debounce = True,
                            style = {'width': '70px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Moving Average Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-env-ma-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                            value = 'Simple',
                            clearable = False,
                            style = {'width': '175px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-env-color-theme-dropdown',
                            className = 'plots-dropdown-button',
                            options = overlay_color_themes,
                            value = 'Grasslands',
                            clearable = False,
                            style = {'width': '120px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        dbc.Button(
                            'Add To Plot',
                            id = f'add-ma-env-button',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'success',
                            size = 'sm',
                            style = plots_add_button_css
                        )],
                        # style = {'margin-bottom': '5px'}
                    ),

                ],
                # style = {'margin-left': '5px'}
            ), 

            id = 'collapse-ma-env',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END MA ENVELOPE CONTROLS

    ##### BEGIN MA RIBBON CONTROLS

    html.Div([

        html.Div(
            dbc.Button(
                id = 'collapse-button-ma-ribbon',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_css
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'ma-ribbon-controls',
                children = [

                    html.Div([
                        html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id = 'ma-ribbon-deck-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Upper'],
                            value = 'Upper',
                            clearable = False,
                            style = {'width': '115px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-ribbon-price-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Close', 'High', 'Low', 'Open'],
                            value = 'Close',
                            clearable = False,
                            style = {'width': '100px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-ribbon-adjusted-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Yes', 'No'],
                            value = 'Yes',
                            clearable = False,
                            style = {'width': '75px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('# Of Bands', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'ma-ribbon-nbands-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 1,
                            min = 1,
                            max = 6,
                            step = 1,
                            debounce = True,
                            style = {'width': '82px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Window Size', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dbc.Input(
                            id = 'ma-ribbon-window-input',
                            className = 'plots-input-button',
                            type = 'number',
                            value = 10,
                            min = 1,
                            max = 200,
                            step = 1,
                            debounce = True,
                            style = {'width': '95px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Add Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-ribbon-add-yaxis-title-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['No', 'Yes'],
                            value = 'No',
                            clearable = False,
                            style = {'width': '113px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Moving Average Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-ribbon-ma-type-dropdown',
                            className = 'plots-dropdown-button',
                            options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                            value = 'Simple',
                            clearable = False,
                            style = {'width': '175px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                        dcc.Dropdown(
                            id='ma-ribbon-color-theme-dropdown',
                            className = 'plots-dropdown-button',
                            options = overlay_color_themes,
                            value = 'Lavender',
                            clearable = False,
                            style = {'width': '120px'}
                        )],
                        style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                    ),

                    html.Div([
                        dbc.Button(
                            'Add To Plot',
                            id = f'add-ma-ribbon-button',
                            n_clicks = 0,
                            class_name = 'ma-1',
                            color = 'success',
                            size = 'sm',
                            style = plots_add_button_css
                        )],
                        # style = {'margin-bottom': '5px'}
                    ),

                ],
                # style = {'margin-left': '5px'}
            ), 

            id = 'collapse-ma-ribbon',
            is_open = False,
            style = {'width': '300px'}
        )],
        style = {'margin-left': '5px'}
    ), 

    ##### END MA RIBBON CONTROLS

    ]),

    # id = 'collapse-sidebar-menu',
    # is_open = False,
    # dimension = 'width'

    ],
    style = {'display': 'inline-block', 'vertical-align': 'top'}

    ),
        
    ##### END SIDEBAR MENU ALL CONTROLS

    html.Div([

        ##### BEGIN SELECTED TICKERS TABLE

        html.Div(
            [
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
            )
            ],
            style = {'vertical-align': 'top', 'margin-bottom': '5px', 'margin-left': '0px'}
        ),

        ##### BEGIN GRAPH
        html.Div(
            id = 'fig-div-container',
            children = [],
            # [
            #     dbc.Row([  # Row
            #         
            #         dbc.Col([  # Col 1
            #             html.Div(
            #                 id = 'fig-div',
            #                 children = [],
            #                 style = {'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0px'}
            #             )
            #         ]),  # Closing Col1 
            #         ### ADD RESET AXES BUTTON
            #         dbc.Col([  # Col 2
            #             html.Div([
            #                 dbc.Button(
            #                     'Reset Axes',
            #                     id = 'reset-axes',
            #                     n_clicks = 0,
            #                     class_name = 'ma-1',
            #                     color = 'light',
            #                     size = 'sm',
            #                     style = reset_axes_button_css
            #                 )
            #             ],
            #             style = {'vertical-align': 'top'}
            #             )
            #         ],
            #         style = {'display': 'flex'}
            #         )  # Closing Col2 
            #     ],
            #     style = {'--bs-gutter-x': '0', 'flex-wrap': 'nowrap'}
            #     # --bs-gutter-x refers to the content left and right margins within each column
            #     # nowrap ensures that the Reset Axes button doesn't move to the bottom of graph when the page is resized
            #     )  # Closing Row
            # ],
        )
    ],
    style = {'display': 'inline-block', 'vertical-align': 'top'}
    
    )

    ],  # Col
    style = {'display': 'flex', 'flex-wrap': 'nowrap'}
    )  # Closing Col

    ],  # Row
    # style = {'display': 'flex', 'flex-wrap': 'nowrap'}
    )  # Closing Row

    ],

    id = 'plots-loading-wrapper',
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
    label = f'▼ {title}' if is_open else f'► {title}'
    if n:
        return label, not is_open
    else:
        return f'▼ {title}', is_open
    

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
    Output('collapse-button-tickers', 'children'),
    Output('collapse-tickers', 'is_open'),
    Input('collapse-button-tickers', 'n_clicks'),
    State('collapse-tickers', 'is_open')
)
def toggle_collapse_tickers(n, is_open):
    title = 'TICKERS'
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
    title = 'TEMPLATE'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('lower-height-input', 'disabled'),

    Output('hist-price-deck-dropdown', 'options'),
    Output('volume-deck-dropdown', 'options'),
    Output('bollinger-deck-dropdown', 'options'),
    Output('ma-env-deck-dropdown', 'options'),
    Output('ma-ribbon-deck-dropdown', 'options'),
    Output('price-overlays-deck-dropdown', 'options'),

    Output('hist-price-deck-dropdown', 'value'),
    Output('volume-deck-dropdown', 'value'),
    Output('bollinger-deck-dropdown', 'value'),
    Output('ma-env-deck-dropdown', 'value'),
    Output('ma-ribbon-deck-dropdown', 'value'),
    Output('price-overlays-deck-dropdown', 'value'),

    Input('deck-type-dropdown', 'n_clicks'),
    Input('deck-type-dropdown', 'value'),

    Input('hist-price-deck-dropdown', 'value'),
    Input('volume-deck-dropdown', 'value'),
    Input('bollinger-deck-dropdown', 'value'),
    Input('ma-env-deck-dropdown', 'value'),
    Input('ma-ribbon-deck-dropdown', 'value'),
    Input('price-overlays-deck-dropdown', 'value'),
)
def target_deck_options(
    deck_changed,
    deck_type,
    hist_price_deck,
    volume_deck,
    bollinger_deck,
    ma_env_deck,
    ma_ribbon_deck,
    price_overlays_deck
):
    n = 6  # number of deck-dropdown outputs

    deck_changed = False if deck_changed is None else deck_changed

    if deck_type == 'Single':
        return tuple([True]) + tuple([k for k in [['Upper']] * n]) + tuple(['Upper'] * n)

    elif deck_type == 'Double':
        
        hist_price_deck_value =     ['Lower'] if (hist_price_deck in ['Middle', 'Lower']) else ['Upper']
        volume_deck_value =         ['Lower'] if (volume_deck in ['Middle', 'Lower']) else ['Upper']
        bollinger_deck_value =      ['Lower'] if (bollinger_deck in ['Middle', 'Lower']) else ['Upper']
        ma_env_deck_value =         ['Lower'] if (ma_env_deck in ['Middle', 'Lower']) else ['Upper']
        ma_ribbon_deck_value =      ['Lower'] if (ma_ribbon_deck in ['Middle', 'Lower']) else ['Upper']
        price_overlays_deck_value = ['Lower'] if (price_overlays_deck in ['Middle', 'Lower']) else ['Upper']
        all_deck_values = \
            hist_price_deck_value + \
            volume_deck_value + \
            bollinger_deck_value + \
            ma_env_deck_value + \
            ma_ribbon_deck_value + \
            price_overlays_deck_value
        return tuple([False]) + tuple([k for k in [['Upper', 'Lower']] * n]) + tuple(all_deck_values)

    else:

        hist_price_deck_value =     ['Middle'] if (hist_price_deck == 'Lower') & deck_changed else [hist_price_deck]
        volume_deck_value =         ['Middle'] if (volume_deck == 'Lower') & deck_changed else [volume_deck]
        bollinger_deck_value =      ['Middle'] if (bollinger_deck == 'Lower') & deck_changed else [bollinger_deck]
        ma_env_deck_value =         ['Middle'] if (ma_env_deck == 'Lower') & deck_changed else [ma_env_deck]
        ma_ribbon_deck_value =      ['Middle'] if (ma_ribbon_deck == 'Lower') & deck_changed else [ma_ribbon_deck]
        price_overlays_deck_value = ['Middle'] if (price_overlays_deck == 'Lower') & deck_changed else [price_overlays_deck]
        all_deck_values = \
            hist_price_deck_value + \
            volume_deck_value + \
            bollinger_deck_value + \
            ma_env_deck_value + \
            ma_ribbon_deck_value + \
            price_overlays_deck_value
        return tuple([False]) + tuple([k for k in [['Upper', 'Middle', 'Lower']] * n]) + tuple(all_deck_values)


@callback(
    Output('collapse-button-hist-price', 'children'),
    Output('collapse-hist-price', 'is_open'),
    Input('collapse-button-hist-price', 'n_clicks'),
    State('collapse-hist-price', 'is_open')
)
def toggle_collapse_hist_price(n, is_open):
    title = 'HISTORICAL PRICE'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-candlestick', 'children'),
    Output('collapse-candlestick', 'is_open'),
    Input('collapse-button-candlestick', 'n_clicks'),
    State('collapse-candlestick', 'is_open')
)
def toggle_collapse_candlestick(n, is_open):
    title = 'CANDLESTICK'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-volume', 'children'),
    Output('collapse-volume', 'is_open'),
    Input('collapse-button-volume', 'n_clicks'),
    State('collapse-volume', 'is_open')
)
def toggle_collapse_volume(n, is_open):
    title = 'VOLUME'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-drawdowns', 'children'),
    Output('collapse-drawdowns', 'is_open'),
    Input('collapse-button-drawdowns', 'n_clicks'),
    State('collapse-drawdowns', 'is_open')
)
def toggle_collapse_drawdowns(n, is_open):
    title = 'DRAWDOWNS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-price-overlays', 'children'),
    Output('collapse-price-overlays', 'is_open'),
    Input('collapse-button-price-overlays', 'n_clicks'),
    State('collapse-price-overlays', 'is_open')
)
def toggle_collapse_price_overlays(n, is_open):
    title = 'PRICE OVERLAYS'
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
    Output('collapse-button-ma-env', 'children'),
    Output('collapse-ma-env', 'is_open'),
    Input('collapse-button-ma-env', 'n_clicks'),
    State('collapse-ma-env', 'is_open')
)
def toggle_collapse_ma_env(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'MOVING AVERAGE ENVELOPES'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-ma-ribbon', 'children'),
    Output('collapse-ma-ribbon', 'is_open'),
    Input('collapse-button-ma-ribbon', 'n_clicks'),
    State('collapse-ma-ribbon', 'is_open')
)
def toggle_collapse_ma_ribbon(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'MOVING AVERAGE RIBBON'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(

    # Output('test-graph', 'figure'),
    # Output('fig_div', 'children', allow_duplicate = True),
    # Output('test-graph', 'figure'),
    # Output('plots-selected-ticker-names-div', 'children'),

    Output('fig-div-container', 'children'),
    # Output('drawdown-controls', 'style'),
    # Output('bollinger-controls', 'style'),
    # Output('template-controls', 'style'),

    Output('hist-price-secondary-y-dropdown', 'disabled'),
    Output('volume-secondary-y-dropdown', 'disabled'),

    Output('drawdowns-number-input', 'max'),
    Output('drawdowns-number-input', 'value'),
    Output('drawdowns-price-color-dropdown', 'disabled'),

    Output('plots-start-date', 'children'),
    Output('plots-end-date', 'children'),

    Input('final-start-date-stored', 'data'),
    Input('final-end-date-stored', 'data'),
    Input('final-selected-tickers-stored', 'data'),

    Input({'index': ALL, 'type': 'reset-axes'}, 'n_clicks'),

    # tickers options
    ### Input('tickers-dropdown', 'value'),
    Input('dash-table-tickers-to-plot', 'selected_rows'),

    # template options
    Input('theme-dropdown', 'value'),
    Input('deck-type-dropdown', 'value'),
    Input('secondary-y-dropdown', 'value'),
    Input('width-input', 'value'),
    Input('upper-height-input', 'value'),
    Input('lower-height-input', 'value'),

    # Historical price options
    Input('hist-price-deck-dropdown', 'value'),
    Input('hist-price-type-dropdown', 'value'),
    Input('hist-price-adjusted-dropdown', 'value'),
    Input('hist-price-secondary-y-dropdown', 'value'),
    Input('hist-price-plot-type-dropdown', 'value'),
    Input('hist-price-fill-below-dropdown', 'value'),
    Input('hist-price-color-theme-dropdown', 'value'),
    Input('hist-price-add-title-dropdown', 'value'),
    Input('add-hist-price-button', 'n_clicks'),

    # Candlestick price options
    Input('candlestick-deck-dropdown', 'value'),
    Input('candlestick-adjusted-dropdown', 'value'),
    Input('candlestick-type-dropdown', 'value'),
    # Input('candlestick-color-theme-dropdown', 'value'),
    Input('candlestick-add-title-dropdown', 'value'),
    Input('add-candlestick-button', 'n_clicks'),

    # Volume options
    Input('volume-deck-dropdown', 'value'),
    Input('volume-secondary-y-dropdown', 'value'),
    Input('volume-plot-type-dropdown', 'value'),
    Input('volume-fill-below-dropdown', 'value'),
    Input('volume-color-theme-dropdown', 'value'),
    Input('volume-add-title-dropdown', 'value'),
    Input('add-volume-button', 'n_clicks'),

    # drawdowns options
    Input('drawdowns-number-input', 'value'),
    Input('drawdowns-topby-dropdown', 'value'),
    Input('drawdowns-display-dropdown', 'value'),
    Input('drawdowns-adjusted-dropdown', 'value'),
    Input('drawdowns-price-type-dropdown', 'value'),
    Input('drawdowns-color-dropdown', 'value'),
    Input('drawdowns-price-color-dropdown', 'value'),
    Input('drawdowns-add-price-dropdown', 'value'),
    Input('drawdowns-add-title-dropdown', 'value'),
    Input('add-drawdowns-button', 'n_clicks'),    

    # price overlay options
    Input('price-overlays-deck-dropdown', 'value'),
    Input('price-overlays-adj-price-list', 'value'),    
    Input('price-overlays-price-list', 'value'),
    Input('price-overlays-add-yaxis-title-dropdown', 'value'),
    Input('price-overlays-color-theme-dropdown', 'value'),
    Input('add-price-overlays-button', 'n_clicks'),

    # bollinger options
    Input('bollinger-deck-dropdown', 'value'),
    Input('bollinger-adjusted-dropdown', 'value'),
    Input('bollinger-price-type-dropdown', 'value'),
    Input('bollinger-ma-type-dropdown', 'value'),
    Input('bollinger-window-input', 'value'),
    Input('bollinger-nstd-input', 'value'),
    Input('bollinger-nbands-input', 'value'),
    Input('bollinger-color-theme-dropdown', 'value'),
    Input('add-bollinger-button', 'n_clicks'),

    # ma envelope options
    Input('ma-env-deck-dropdown', 'value'),
    Input('ma-env-adjusted-dropdown', 'value'),
    Input('ma-env-price-type-dropdown', 'value'),
    Input('ma-env-ma-type-dropdown', 'value'),
    Input('ma-env-window-input', 'value'),
    Input('ma-env-offset-input', 'value'),
    Input('ma-env-nbands-input', 'value'),
    Input('ma-env-color-theme-dropdown', 'value'),
    Input('add-ma-env-button', 'n_clicks'),
   
    # ma ribbon options
    Input('ma-ribbon-deck-dropdown', 'value'),
    Input('ma-ribbon-adjusted-dropdown', 'value'),
    Input('ma-ribbon-price-type-dropdown', 'value'),
    Input('ma-ribbon-ma-type-dropdown', 'value'),
    Input('ma-ribbon-window-input', 'value'),
    Input('ma-ribbon-nbands-input', 'value'),
    Input('ma-ribbon-add-yaxis-title-dropdown', 'value'),
    Input('ma-ribbon-color-theme-dropdown', 'value'),
    Input('add-ma-ribbon-button', 'n_clicks'),
   
)

def update_plot(

        start_date,
        end_date,
        selected_tickers_names,
        # downloaded_data,

        n_click_reset_axes,

        # ticker options
        selected_rows_tickers_to_plot,
        # tk,

        # template options
        theme,
        deck_type,
        sec_y,
        width,
        upper_height,
        lower_height,

        # historical price options
        hist_price_deck_name,
        hist_price_type,
        hist_price_adjusted,
        hist_price_secondary_y,
        hist_price_plot_type,
        hist_price_fill_below,
        hist_price_color_theme,
        hist_price_add_title,
        add_hist_price,

        # historical price options
        candlestick_deck_name,
        candlestick_adjusted,
        candlestick_type,
        # candlestick_color_theme,
        candlestick_add_title,
        add_candlestick,

        # volume options
        volume_deck_name,
        volume_secondary_y,
        volume_plot_type,
        volume_fill_below,
        volume_color_theme,
        volume_add_title,
        add_volume,
        
        # drawdowns options
        n_top, 
        drawdown_top_by, 
        drawdown_display,
        drawdown_adjusted,
        drawdown_price_type,
        drawdown_color, 
        drawdown_price_color_theme,
        drawdown_add_price,
        drawdown_add_title,
        add_drawdowns,

        # price overlays
        price_overlay_deck_name,
        price_overlay_adj_price_list,
        price_overlay_price_list,
        price_overlay_add_yaxis_title,
        price_overlay_color_theme,
        add_price_overlays,

        # bollinger options
        bollinger_deck_name,
        bollinger_adjusted,
        bollinger_price_type,
        bollinger_ma_type,
        bollinger_window,
        bollinger_nstd,
        bollinger_nbands,
        bollinger_color_theme,
        add_bollinger,

        ma_env_deck_name,
        ma_env_adjusted,
        ma_env_price_type,
        ma_env_ma_type,
        ma_env_window,
        ma_env_offset,
        ma_env_nbands,
        ma_env_color_theme,
        add_ma_env,

        ma_ribbon_deck_name,
        ma_ribbon_adjusted,
        ma_ribbon_price_type,
        ma_ribbon_ma_type,
        ma_ribbon_window,
        ma_ribbon_nbands,
        ma_ribbon_add_yaxis_title,
        ma_ribbon_color_theme,
        add_ma_ribbon

    ):

    selected_tickers = list(selected_tickers_names.keys())
    id_tk_map = {i: tk for i, tk in enumerate(selected_tickers)}

    downloaded_data = hist_data.download_yf_data(start_date, end_date, selected_tickers)

    tickers_to_plot = [id_tk_map[i] for i in selected_rows_tickers_to_plot] if selected_rows_tickers_to_plot != [] else id_tk_map[0]

    tk = tickers_to_plot[0]

    theme = theme.lower()
    secondary_y = False if sec_y == 'No' else True

    # These are in the list of outputs, so they must stay outside of the if statements
    
    hist_price_sec_y_disabled = not secondary_y
    volume_sec_y_disabled = not secondary_y

    dd_add_price_disabled = True if drawdown_add_price == 'No' else False
    n_drawdowns = 5 if n_top is None else n_top
    dd_number_value = n_drawdowns

    ################

    fig_divs = []

    for tk in tickers_to_plot:

        date_index = downloaded_data[tk]['ohlc'].index
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

        ### Add historical price
        if add_hist_price:
            
            hist_price_color_theme = hist_price_color_theme.lower() if hist_price_color_theme is not None else 'base'
            df_hist_price = downloaded_data[tk]['ohlc_adj'] if hist_price_adjusted == 'Yes' else downloaded_data[tk]['ohlc']
            hist_price = df_hist_price[hist_price_type]

            fig_data = analyze_prices.add_hist_price(
                fig_data,
                hist_price,
                tk,
                target_deck = deck_number(deck_type, hist_price_deck_name),
                secondary_y = True if hist_price_secondary_y == 'Yes' else False,
                plot_type = 'bar' if hist_price_plot_type == 'Histogram' else 'scatter',
                price_type = hist_price_type.lower(),
                add_title = True if hist_price_add_title == 'Yes' else False,
                theme = theme,
                color_theme = hist_price_color_theme,
                fill_below = True if hist_price_fill_below == 'Yes' else False
            )

        ### Add candlestick
        if add_candlestick:
            
            df_ohlc = downloaded_data[tk]['ohlc_adj'] if candlestick_adjusted == 'Yes' else downloaded_data[tk]['ohlc']

            fig_data = analyze_prices.add_candlestick(
                fig_data,
                df_ohlc,
                tk,
                candle_type = candlestick_type.lower(),
                target_deck = deck_number(deck_type, candlestick_deck_name),
                add_title = True if candlestick_add_title == 'Yes' else False,
                theme = theme #,
                # color_theme = candlestick_color_theme
            )

        ### Add volume
        if add_volume:

            volume_color_theme = volume_color_theme.lower() if volume_color_theme is not None else 'sapphire'
            df_volume = downloaded_data[tk]['volume']

            fig_data = analyze_prices.add_hist_price(
                fig_data,
                df_volume,
                tk,
                target_deck = deck_number(deck_type, volume_deck_name),
                secondary_y = True if volume_secondary_y == 'Yes' else False,
                plot_type = 'bar' if volume_plot_type == 'Histogram' else 'scatter',
                price_type = 'volume',
                add_title = True if volume_add_title == 'Yes' else False,
                theme = theme,
                color_theme = volume_color_theme,
                fill_below = True if volume_fill_below == 'Yes' else False
            )

        ### Add drawdowns
        if add_drawdowns:

            dd_add_title = True if drawdown_add_title =='Yes' else False
            drawdown_color = drawdown_color.lower() if drawdown_color is not None else 'red'
            drawdown_price_color_theme = drawdown_price_color_theme.lower() if drawdown_price_color_theme is not None else 'base'
            df_drawdown_price = downloaded_data[tk]['ohlc_adj'] if drawdown_adjusted == 'Yes' else downloaded_data[tk]['ohlc']
            drawdown_price = df_drawdown_price[drawdown_price_type]

            drawdown_data_tk = analyze_prices.summarize_tk_drawdowns(drawdown_price, drawdown_top_by)
            n_drawdowns = drawdown_data_tk['Total Drawdowns']
            dd_number_value = min(n_top, n_drawdowns)
            selected_drawdown_data = analyze_prices.select_tk_drawdowns(drawdown_data_tk, n_top)

            show_trough_to_recovery = True if 'Recovery' in drawdown_display else False
            dd_top_by = 'length' if drawdown_top_by == 'Total Length' else 'depth'

            fig_data = analyze_prices.add_drawdowns(
                fig_data,
                drawdown_price,
                tk,
                selected_drawdown_data,
                n_top_drawdowns = n_top,
                target_deck = 1,
                add_price = not dd_add_price_disabled,
                price_type = drawdown_price_type.lower(),
                top_by = dd_top_by,
                show_trough_to_recovery = show_trough_to_recovery,
                add_title = dd_add_title,
                theme = theme,
                price_color_theme = drawdown_price_color_theme,
                drawdown_color = drawdown_color
            )

        ### Add Bollinger bands
        if add_bollinger:
            df_bollinger_price = downloaded_data[tk]['ohlc_adj'] if bollinger_adjusted == 'Yes' else downloaded_data[tk]['ohlc']
            bollinger_price = df_bollinger_price[bollinger_price_type]
            bollinger_data = analyze_prices.bollinger_bands(
                bollinger_price,
                ma_type_map[bollinger_ma_type],
                bollinger_window,
                bollinger_nstd,
                bollinger_nbands
            )
            bollinger_list = bollinger_data['list']
            fig_data = analyze_prices.add_bollinger_overlays(
                fig_data,
                bollinger_list,
                target_deck = deck_number(deck_type, bollinger_deck_name),
                theme = theme,
                color_theme = bollinger_color_theme
            )

        ### Add moving average envelopes
        if add_ma_env:
            df_ma_env_price = downloaded_data[tk]['ohlc_adj'] if ma_env_adjusted == 'Yes' else downloaded_data[tk]['ohlc']
            ma_env_price = df_ma_env_price[ma_env_price_type]
            ma_env_list = analyze_prices.ma_envelopes(
                ma_env_price,
                ma_type_map[ma_env_ma_type],
                ma_env_window,
                ma_env_offset,
                ma_env_nbands
            )
            fig_data = analyze_prices.add_ma_envelopes(
                fig_data,
                ma_env_list,
                target_deck = deck_number(deck_type, ma_env_deck_name),
                theme = theme,
                color_theme = ma_env_color_theme
            )

        ### Add moving average ribbon
        if add_ma_ribbon:
            df_ma_ribbon_price = downloaded_data[tk]['ohlc_adj'] if ma_ribbon_adjusted == 'Yes' else downloaded_data[tk]['ohlc']
            ma_ribbon_price = df_ma_ribbon_price[ma_ribbon_price_type]
            ma_ribbon_list = analyze_prices.get_ma_ribbon(
                ma_type_map[ma_ribbon_ma_type],
                ma_ribbon_window,
                ma_ribbon_nbands
            )
            fig_data = analyze_prices.add_ma_overlays(
                fig_data,
                ma_ribbon_price,
                ma_ribbon_list,
                target_deck = deck_number(deck_type, ma_ribbon_deck_name),
                add_yaxis_title = True if ma_ribbon_add_yaxis_title == 'Yes' else False,
                yaxis_title = 'Moving Average',
                theme = theme,
                color_theme = ma_ribbon_color_theme
            )

        ### Add price overlays
        if add_price_overlays:
            price_list = []
            for name in ['Adjusted Close', 'Adjusted Open', 'Adjusted High', 'Adjusted Low']:
                if name in price_overlay_adj_price_list:
                    price_list.append({
                        'name': name,
                        'data': downloaded_data[tk]['ohlc_adj'][name.replace('Adjusted ', '')],
                        'show': True
                    })
            for name in ['Close', 'Open', 'High', 'Low']:
                if name in price_overlay_price_list:
                    price_list.append({
                        'name': name,
                        'data': downloaded_data[tk]['ohlc'][name],
                        'show': True
                    })
            if len(price_list) > 0:
                fig_data = analyze_prices.add_price_overlays(
                    fig_data,
                    price_list,
                    target_deck = deck_number(deck_type, price_overlay_deck_name),
                    add_yaxis_title = True if price_overlay_add_yaxis_title == 'Yes' else False,
                    yaxis_title = 'Price',
                    theme = theme,
                    color_theme = price_overlay_color_theme
                )


        ### Update graph
        fig = fig_data['fig']

        fig_div = html.Div(
            id = f'{tk}-fig-div',
            children = [
                dbc.Row([  # Row
                    dbc.Col([  # Col 1
                        html.Div(
                            id = f'{tk}-fig-div',
                            children = [
                                dcc.Graph(
                                    id = f'{tk}-main-graph',
                                    figure = fig
                                )
                            ],
                            style = {'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0px'}
                        )
                    ]),  # Closing Col1 
                    ### ADD RESET AXES BUTTON
                    dbc.Col([  # Col 2
                        html.Div([
                            dbc.Button(
                                'Reset Axes',
                                id = {'index': f'{tk}-reset-axes', 'type': 'reset-axes'},
                                n_clicks = 0,
                                class_name = 'ma-1',
                                color = 'light',
                                size = 'sm',
                                style = reset_axes_button_css
                            )
                        ],
                        style = {'vertical-align': 'top'}
                        )
                    ],
                    style = {'display': 'flex'}
                    )  # Closing Col2 
                ],
                style = {'--bs-gutter-x': '0', 'flex-wrap': 'nowrap', 'margin-bottom': '5px'}
                # --bs-gutter-x refers to the content left and right margins within each column
                # nowrap ensures that the Reset Axes button doesn't move to the bottom of graph when the page is resized
                ),  # Closing Row
                # html.Br()
            ],
        )

        fig_divs.append(fig_div)


    return (
        # selected_tickers_names[tk],
        # str([selected_tickers_names[tk] for tk in tickers_to_plot]),
        # [selected_tickers_names[tk] for tk in tickers_to_plot],

        fig_divs,
        # drawdown_div_style,
        # bollinger_div_style,
        # template_div_style,

        hist_price_sec_y_disabled,
        volume_sec_y_disabled,

        n_drawdowns,
        dd_number_value,
        dd_add_price_disabled,

        start_date,
        end_date
    )
