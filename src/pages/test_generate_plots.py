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
            {'if': {'column_id': 'Length*'}, 'width': 45, 'text-align': 'right', 'padding-right': '10px'},
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
                        html.Div('Ticker', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '3px', 'margin-bottom': '0px'}),
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
                            min = 1,
                            step = 1,
                            debounce = True,
                            style = {'width': '65px'}
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
                            style = {'width': '113px'}
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
            children = 
            [
                dbc.Row([  # Row
                    
                    dbc.Col([  # Col 1
                        html.Div(
                            id = 'fig-div',
                            children = [],
                            style = {'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0px'}
                        )
                    ]),  # Closing Col1 

                    ### ADD RESET AXES BUTTON
                    dbc.Col([  # Col 2
                        html.Div([
                            dbc.Button(
                                'Reset Axes',
                                id = 'reset-axes',
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
                style = {'--bs-gutter-x': '0', 'flex-wrap': 'nowrap'}
                # --bs-gutter-x refers to the content left and right margins within each column
                # nowrap ensures that the Reset Axes button doesn't move to the bottom of graph when the page is resized
                )  # Closing Row
            ],
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
    Output('bollinger-deck-dropdown', 'value'),
    Input('deck-type-dropdown', 'value'))
def disable_options(deck_type):
    if deck_type == 'Single':
        # return True, [1]
        return True, ['Upper'], 'Upper'
    elif deck_type == 'Double':
        # return False, [1, 2]
        return False, ['Upper', 'Lower'], 'Upper'
    else:
        # return False, [1, 2, 3]
        return False, ['Upper', 'Middle', 'Lower'], 'Upper'


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
    Output('drawdowns-price-color-dropdown', 'disabled'),

    Output('plots-start-date', 'children'),
    Output('plots-end-date', 'children'),

    Input('final-start-date-stored', 'data'),
    Input('final-end-date-stored', 'data'),
    Input('final-selected-tickers-stored', 'data'),

    Input('reset-axes', 'n_clicks'),
    
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
    Input('drawdowns-adjusted-dropdown', 'value'),
    Input('drawdowns-price-type-dropdown', 'value'),
    Input('drawdowns-color-dropdown', 'value'),
    Input('drawdowns-price-color-dropdown', 'value'),
    Input('drawdowns-add-price-dropdown', 'value'),
    Input('drawdowns-add-title-dropdown', 'value'),
    Input('add-drawdowns-button', 'n_clicks'),    
    # prevent_initial_call=True #,
    #Input('overlay-dropdown', 'value')

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
   
)

def update_plot(

        start_date,
        end_date,
        selected_tickers_names,
        # downloaded_data,

        n_click_reset_axes,

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
        drawdown_adjusted,
        drawdown_price_type,
        drawdown_color, 
        drawdown_price_color_theme,
        drawdown_add_price,
        drawdown_add_title,
        add_drawdowns,

        # bollinger options
        # tk_bollinger,
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
        add_ma_env

    ):

    selected_tickers = list(selected_tickers_names.keys())

    downloaded_data = hist_data.download_yf_data(start_date, end_date, selected_tickers)

    # fig_data = create_graph(theme, tk, drawdown_color, overlay_color_theme)
    date_index = downloaded_data[tk]['ohlc'].index
    theme = theme.lower()
    # deck_type = deck_type.lower()
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

    dd_add_price_disabled = True if drawdown_add_price == 'No' else False
    n_drawdowns = 5 if n_top is None else n_top
    dd_number_value = n_drawdowns

    ### Add drawdowns
    if add_drawdowns:
        
        dd_add_title = True if drawdown_add_title =='Yes' else False
        drawdown_color = drawdown_color.lower() if drawdown_color is not None else 'red'
        drawdown_price_color_theme = drawdown_price_color_theme.lower() if drawdown_price_color_theme is not None else 'base'
        df_drawdown_price = downloaded_data[tk]['ohlc_adj'] if drawdown_adjusted else downloaded_data[tk]['ohlc']
        drawdown_price = df_drawdown_price[drawdown_price_type]

        drawdown_data_tk = analyze_prices.summarize_tk_drawdowns(drawdown_price, drawdown_top_by)
        n_drawdowns = drawdown_data_tk['Total Drawdowns']
        dd_number_value = min(n_top, n_drawdowns)
        selected_drawdown_data = analyze_prices.select_tk_drawdowns(drawdown_data_tk, n_top)

        show_trough_to_recovery = True if 'Recovery' in drawdown_display else False
        drawdown_top_by = 'length' if drawdown_top_by == 'Total Length' else 'depth'

        fig_data = analyze_prices.add_drawdowns(
            fig_data,
            drawdown_price,
            tk,
            selected_drawdown_data,
            n_top_drawdowns = n_top,
            target_deck = 1,
            add_price = not dd_add_price_disabled,
            price_type = drawdown_price_type.lower(),
            top_by = drawdown_top_by,
            show_trough_to_recovery = show_trough_to_recovery,
            add_title = dd_add_title,
            theme = theme,
            price_color_theme = drawdown_price_color_theme,
            drawdown_color = drawdown_color
        )

    ### Add Bollinger bands
    if add_bollinger:
        df_bollinger_price = downloaded_data[tk]['ohlc_adj'] if bollinger_adjusted else downloaded_data[tk]['ohlc']
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
        df_ma_env_price = downloaded_data[tk]['ohlc_adj'] if ma_env_adjusted else downloaded_data[tk]['ohlc']
        ma_env_price = df_ma_env_price[ma_env_price_type]
        ma_env_list = analyze_prices.ma_envelopes(
            ma_env_price,
            ma_type_map[ma_env_ma_type],
            ma_env_window,
            ma_env_offset,
            ma_env_nbands
        )
        fig_data = analyze_prices.add_ma_envelope_overlays(
            fig_data,
            ma_env_list,
            target_deck = deck_number(deck_type, ma_env_deck_name),
            theme = theme,
            color_theme = ma_env_color_theme
        )
    
    ### Update graph
    fig = fig_data['fig']
    fig_div = dcc.Graph(id='drawdowns-graph', figure = fig)

    return (
        selected_tickers_names[tk],

        fig_div,
        # drawdown_div_style,
        # bollinger_div_style,
        # template_div_style,

        n_drawdowns,
        dd_number_value,
        dd_add_price_disabled,

        start_date,
        end_date
    )
