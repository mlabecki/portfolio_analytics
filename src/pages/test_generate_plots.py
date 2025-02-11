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
from build_dash_html import BuildDashHtml

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
build_dash_html = BuildDashHtml()


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
        # selected_rows = [],
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
                'width': '310px !important',
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
#    portfolio_drawdowns_data = {}
#
#    for tk in tickers:
#        drawdowns_data = analyze_prices.summarize_tk_drawdowns(df_close, tk, sort_by)
#        n_drawdowns = drawdowns_data['Total Drawdowns']
#        drawdowns_numbers = [x for x in range(n_drawdowns + 1)[1:]]
#        portfolio_drawdowns_data.update({tk: drawdowns_data})
#
##############

theme = 'dark'
# overlay_color_theme = 'grasslands'
candle_colors = [x.title() for x in theme_style[theme]['candle_colors'].keys()]
overlay_color_themes = [x.title() for x in theme_style[theme]['overlay_color_theme'].keys()]
# overlay_color_themes = [x.title() for x in theme_style[theme]['overlay_color_theme'].keys()]
# # print(overlay_color_themes)
# # drawdowns_colors = list(theme_style[theme]['drawdowns_colors'].keys())
drawdowns_colors = [x.title() for x in theme_style[theme]['drawdown_colors'].keys()]
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

    ###########################################

    ##### BEGIN GENERAL SETTINGS TAB

    html.Div([

        html.Div([
            dbc.Button(
                id = 'collapse-button-general-tab',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_general_settings_tab_css
            ),
        ],
        # style = {'width': '315px', 'display': 'flex', 'flex-wrap': 'nowrap'}
        style = {'width': '310px'}
        ),
        dbc.Popover([
            # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
            dcc.Markdown("""<DIV>► TICKERS<BR/>► DATE RANGE<BR/>► THEME & TEMPLATE</DIV>""", dangerously_allow_html = True)
            ], 
            id = 'popover-collapse-button-general-tab',
            target = 'collapse-button-general-tab',
            body = False,
            trigger = 'hover',
            # trigger = 'click',
            hide_arrow = True,
            style = popover_menu_tab_collapse_button_css
        ),

        dbc.Collapse(

            html.Div([

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
                            style = collapse_button_general_settings_css
                        )
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'tickers-controls',
                            children = [
                            
                                html.Div([
                                    html.Div(
                                        id = 'select-tickers-to-plot-title',
                                        children= ['Select Tickers To Plot'],
                                        style = {
                                            'display': 'block',
                                            'font-size': '14px',
                                            'font-weight': 'bold',
                                            'vertical-align': 'top',
                                            'height': '20px',
                                            'margin-top': '5px',
                                            'margin-bottom': '5px',
                                            'margin-left': '2px'
                                        }
                                    ),
                                    dbc.Popover(
                                        [
                                        html.Span(
                                            """Tickers will be plotted individually on separate graphs with common plot features as selected below.""",
                                            style = popover_menu_collapse_button_header_css
                                            )
                                        ], 
                                        id = 'popover-select-tickers-to-plot-title',
                                        target = 'select-tickers-to-plot-title',
                                        body = False,
                                        trigger = 'hover',
                                        hide_arrow = True,
                                        style = popover_menu_button_css
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
                                    #     style = {'width': '310px', 'vertical-align': 'middle'}
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
                                        'width': '305px',
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
                        style = {'width': '305px'}
                    )],
                    style = {'margin-left': '5px'}
                ),

            ##### END TICKERS CONTROLS

            ##### BEGIN DATES CONTROLS

                html.Div([
                
                    # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
                    html.Div(
                        dbc.Button(
                            id = 'collapse-button-dates',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_general_settings_css
                        )
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'dates-controls',
                            children = [
                            
                                html.Div([
                                    html.Div(
                                        'NARROW DOWN RANGE OF DATES',
                                        style = {
                                            'display': 'block',
                                            'font-size': '14px',
                                            'font-weight': 'bold',
                                            'color': '#007ea7',  # This is native for the YETI theme
                                            'vertical-align': 'top',
                                            'height': '20px',
                                            'margin-top': '5px',
                                            'margin-bottom': '0px',
                                            'margin-left': '7px'
                                        }
                                    ),

                                    # Dates selection
                                    html.Div(
                                        id = 'plots-dates-selection-container',
                                        children = [
                                            # Start date
                                            html.Div(
                                                id = 'plots-start-date-select-container',
                                                children = [
                                                    html.Div(
                                                        'New Start Date',
                                                        style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '2px'}
                                                    ),
                                                    dmc.DatePickerInput(
                                                        id = 'plots-start-date-input-dmc',
                                                        # maxDate = datetime.today().date(),
                                                        valueFormat = 'YYYY-MM-DD',
                                                        highlightToday = False,
                                                        size = 'sm',
                                                        variant = 'filled',
                                                        w = 140,
                                                        style = {
                                                            'text-align': 'center',
                                                            'border': '1px solid rgb(0, 126, 255)',
                                                            'border-radius': '5px',
                                                            'margin-right': '10px'
                                                        }
                                                    )
                                                ],
                                                style = {'display': 'inline-block', 'vertical-align': 'top'}
                                            ),
                                            # End date
                                            html.Div(
                                                id = 'plots-end-date-select-container',
                                                children = [
                                                    html.Div(
                                                        'New End Date',
                                                        style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '2px'}
                                                    ),
                                                    dmc.DatePickerInput(
                                                        id = 'plots-end-date-input-dmc',
                                                        # maxDate = datetime.today().date(),
                                                        # value = datetime.today().date(),
                                                        valueFormat = 'YYYY-MM-DD',
                                                        highlightToday = False,
                                                        size = 'sm',
                                                        variant = 'filled',
                                                        w = 140,
                                                        style = {
                                                            'text-align': 'center',
                                                            'border': '1px solid rgb(0, 126, 255)',
                                                            'border-radius': '5px',
                                                            'margin-left': '0px'
                                                        }
                                                    )
                                                ],
                                                style = {'display': 'inline-block', 'margin-left': '0px', 'vertical-align': 'top'}
                                            )
                                        ],
                                        style = {'margin-right': '5px', 'margin-bottom': '10px', 'margin-left': '5px'}
                                    )
                                ])
                            ]
                        ),

                        id = 'collapse-dates',
                        is_open = False,
                        style = {'width': '305px'}
                    )],
                    style = {'margin-left': '5px'}
                ),

                ##### END DATES CONTROLS

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
                            style = collapse_button_general_settings_css
                        )
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'template-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Dark', 'Light'],
                                        value = 'Dark',
                                        disabled = False,
                                        clearable = False,
                                        style = {'width': '83px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Deck Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '3px', 'margin-left': '2px'}),
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
                                    html.Div('Secondary Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '104px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis can be added to the Upper Deck only.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-secondary-y-dropdown',
                                    target = 'secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Width', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'width-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 1350,
                                        min = 800,
                                        max = 1800,
                                        step = 50,
                                        debounce = True,
                                        style = {'width': '89px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '0px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Height Upper', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'upper-height-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 750,
                                        min = 250,
                                        max = 1000,
                                        step = 50,
                                        debounce = True,
                                        style = {'width': '103px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '0px', 'border-radius': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Height of the Upper Deck',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-upper-height-input',
                                    target = 'upper-height-input',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Height Lower', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'height': '20px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'lower-height-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 150,
                                        min = 100,
                                        max = 300,
                                        step = 50,
                                        debounce = True,
                                        style = {'width': '103px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '0px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Height of the Lower/Middle Deck if Double/Triple deck type is selected.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-lower-height-input',
                                    target = 'lower-height-input',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                            ]
                        ),

                        id = 'collapse-template',
                        is_open = False,
                        style = {'width': '305px'}
                    )],
                    style = {'margin-left': '5px'}
                ),

                ##### END TEMPLATE CONTROLS

            ]),
            id = 'collapse-general-tab',
            is_open = False,
            style = {'width': '310px'}
        )],
        style = {'width': '310px', 'margin-left': '5px', 'margin-bottom': '5px'}
    ), 

    ##### END GENERAL SETTINGS TAB

    #############################################################

    ##### BEGIN PRICES TAB

    html.Div([

        html.Div([
            dbc.Button(
                id = 'collapse-button-prices-tab',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_plot_category_css
            ),
            html.Div(
                id = 'added-to-plot-indicator-prices-tab',
                style = not_added_to_plot_indicator_css
            )
        ],
        style = {'width': '315px', 'display': 'flex', 'flex-wrap': 'nowrap'}
        ),
        dbc.Popover([
            # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
            dcc.Markdown("""<DIV>► PRICE<BR/>► CANDLESTICK<BR/>► PRICE OVERLAYS<BR/>► DRAWDOWNS</DIV>""", dangerously_allow_html = True)
            ], 
            id = 'popover-collapse-button-prices-tab',
            target = 'collapse-button-prices-tab',
            body = False,
            trigger = 'hover',
            hide_arrow = True,
            style = popover_menu_tab_collapse_button_css
        ),

        dbc.Collapse(

            html.Div([

                ##### BEGIN HISTORICAL PRICE CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-hist-price',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-hist-price',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'hist-price-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'hist-price-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '110px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='hist-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '97px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='hist-price-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '88px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is the price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-hist-price-adjusted-dropdown',
                                    target = 'hist-price-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='hist-price-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Line', 'Histogram'],
                                        value = 'Line',
                                        clearable = False,
                                        style = {'width': '180px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Fill Below', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='hist-price-fill-below-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='hist-price-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '82px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('On Sec Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='hist-price-secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '83px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis must first be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS in order to plot on it.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-hist-price-secondary-y-dropdown',
                                    target = 'hist-price-secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        # 'ADD TO PLOT',
                                        # '🗸',
                                        # '✓',
                                        # '✔',
                                        # https://www.w3schools.com/charsets/ref_utf_dingbats.asp
                                        id = f'add-hist-price-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        # https://www.w3schools.com/charsets/ref_utf_dingbats.asp
                                        id = f'remove-hist-price-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-hist-price',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END HISTORICAL PRICE CONTROLS

                ##### BEGIN CANDLESTICK CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-candlestick',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-candlestick',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'candlestick-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'candlestick-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '122px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='candlestick-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Are the underlying prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-candlestick-adjusted-dropdown',
                                    target = 'candlestick-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='candlestick-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '93px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Candle Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='candlestick-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Hollow', 'Traditional'],
                                        value = 'Hollow',
                                        clearable = False,
                                        style = {'width': '100px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='candlestick-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = candle_colors,
                                        value = 'Green-Red',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '0px'}),
                                    dcc.Dropdown(
                                        id='candlestick-add-yaxis-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '75px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-candlestick-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-candlestick-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-candlestick',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END CANDLESTICK CONTROLS

                ##### BEGIN PRICE OVERLAYS CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-price-overlays',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-price-overlays',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
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
                                        style = {'width': '100px'}
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
                                        style = {'width': '115px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='price-overlays-add-yaxis-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div('Select Price Types', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-price-overlays-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-price-overlays-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-price-overlays',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END PRICE OVERLAYS CONTROLS

                ##### BEGIN DRAWDOWN CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-drawdowns',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-drawdowns',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'drawdown-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id = 'drawdowns-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '115px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Drawdown Display', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id  ='drawdowns-display-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Peak To Trough', 'Peak To Recovery'],
                                        value = 'Peak To Trough',
                                        clearable = False,
                                        style = {'width': '185px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '0px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('# Of Top Drawdowns', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-bottom': '0px'}),
                                    dbc.Input(
                                        id = 'drawdowns-number-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 5,
                                        min = 0,
                                        max = 20,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '150px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '5px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Sort Drawdowns By', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'drawdowns-topby-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['% Depth', 'Total Length'],
                                        value = '% Depth',
                                        clearable = False,
                                        style = {'width': '150px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '0px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'drawdowns-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Open', 'Low'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'drawdowns-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '70px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is the underlying price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-drawdowns-adjusted-dropdown',
                                    target = 'drawdowns-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Price', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'drawdowns-add-price-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '70px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),


                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='drawdowns-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Drawdown Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'drawdowns-color-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = drawdowns_colors,
                                        value = 'Red',
                                        clearable = False,
                                        style = {'width': '150px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Price Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'drawdowns-price-color-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Sapphire',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '150px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-drawdowns-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-drawdowns-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-drawdowns',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END DRAWDOWN CONTROLS

            ]),
            id = 'collapse-prices-tab',
            is_open = False,
            style = {'width': '315px'}
        )],
        style = {'margin-left': '5px', 'margin-bottom': '5px'}
    ), 

    ##### END PRICES TAB

    ###########################################################################

    ##### BEGIN VOLUME TAB

    html.Div([

        html.Div([
            dbc.Button(
                id = 'collapse-button-volume-tab',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_plot_category_css
            ),
            html.Div(
                id = 'added-to-plot-indicator-volume-tab',
                style = not_added_to_plot_indicator_css
            )
        ],
        style = {'width': '315px', 'display': 'flex', 'flex-wrap': 'nowrap'}
        ),
        dbc.Popover([
            # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
            dcc.Markdown("""<DIV>► VOLUME<BR/>► DOLLAR VOLUME<BR/>► ON-BALANCE VOLUME</DIV>""", dangerously_allow_html = True)
            ], 
            id = 'popover-collapse-button-volume-tab',
            target = 'collapse-button-volume-tab',
            body = False,
            trigger = 'hover',
            hide_arrow = True,
            style = popover_menu_tab_collapse_button_css
        ),

        dbc.Collapse(

            html.Div([

                ##### BEGIN VOLUME CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-volume',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-volume',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                                """NOTE: Volume can only be plotted on the Secondary Y-Axis or on the Middle/Lower Deck
                                if the Primary Y-Axis is populated. 
                                """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-volume',
                        target = 'collapse-button-volume',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
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
                                        style = {'width': '95px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='volume-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Fill Below', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='volume-fill-below-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='volume-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Base',
                                        clearable = False,
                                        style = {'width': '130px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='volume-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('On Sec Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id='volume-secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis must first be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS in order to plot on it.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-volume-secondary-y-dropdown',
                                    target = 'volume-secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-volume-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-volume-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-volume',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END VOLUME CONTROLS

                ##### BEGIN DOLLAR VOLUME CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-dollar-volume',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-dollar-volume',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                                """NOTE: Volume can only be plotted on the Secondary Y-Axis or on the Middle/Lower deck
                                if the Primary Y-Axis is populated. 
                                """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-dollar-volume',
                        target = 'collapse-button-dollar-volume',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'dollar-volume-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id = 'dollar-volume-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '95px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='dollar-volume-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Fill Below', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='dollar-volume-fill-below-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id='dollar-volume-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '60px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is the underlying price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-dollar-volume-adjusted-dropdown',
                                    target = 'dollar-volume-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '0px'}),
                                    dcc.Dropdown(
                                        id='dollar-volume-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '60px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='dollar-volume-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Base',
                                        clearable = False,
                                        style = {'width': '105px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('On Sec Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id='dollar-volume-secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis must first be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS in order to plot on it.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-dollar-volume-secondary-y-dropdown',
                                    target = 'dollar-volume-secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-dollar-volume-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-dollar-volume-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-dollar-volume',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END DOLLAR VOLUME CONTROLS

                ##### BEGIN ON-BALANCE VOLUME CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-obv',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-obv',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                                """NOTE: Volume can only be plotted on the Secondary Y-Axis or on the Middle/Lower deck
                                if the Primary Y-Axis is populated. 
                                """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-obv',
                        target = 'collapse-button-obv',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'obv-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id = 'obv-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '95px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='obv-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Fill Below', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='obv-fill-below-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id='obv-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '60px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is the underlying price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-obv-adjusted-dropdown',
                                    target = 'obv-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '0px'}),
                                    dcc.Dropdown(
                                        id='obv-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '60px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='obv-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Base',
                                        clearable = False,
                                        style = {'width': '105px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('On Sec Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id='obv-secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis must first be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS in order to plot on it.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-obv-secondary-y-dropdown',
                                    target = 'obv-secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-obv-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-obv-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-obv',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END ON-BALANCE VOLUME CONTROLS

            ]),
            id = 'collapse-volume-tab',
            is_open = False,
            style = {'width': '315px'}
        )],
        style = {'margin-left': '5px', 'margin-bottom': '5px'}
    ), 

    ##### END VOLUME TAB

    ###########################################################################

    ##### BEGIN TREND INDICATORS TAB

    html.Div([

        html.Div([
            dbc.Button(
                id = 'collapse-button-trend-tab',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_plot_category_css
            ),
            html.Div(
                id = 'added-to-plot-indicator-trend-tab',
                style = not_added_to_plot_indicator_css
            )
        ],
        style = {'width': '315px', 'display': 'flex', 'flex-wrap': 'nowrap'}
        ),
        dbc.Popover([
            # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
            dcc.Markdown("""<DIV>► MOVING AVERAGE ENVELOPES<BR/>
                ► DOLLAR VOLUME<BR/>
                ► MOVING AVERAGE RIBBON<BR/>
                ► MACD / MACD-V<BR/>
                ► IMPULSE MACD</DIV>""",
                dangerously_allow_html = True)
            ], 
            id = 'popover-collapse-button-trend-tab',
            target = 'collapse-button-trend-tab',
            body = False,
            trigger = 'hover',
            hide_arrow = True,
            style = popover_menu_tab_collapse_button_css
        ),

        dbc.Collapse(

            html.Div([

                ##### BEGIN MA ENVELOPE CONTROLS
                # Category: TREND INDICATORS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-ma-env',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-ma-env',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'ma-env-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
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
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
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
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
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
                                dbc.Popover([
                                    html.Span(
                                        'Are the underlying prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-ma-env-adjusted-dropdown',
                                    target = 'ma-env-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('# Of Envelopes', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('% Width', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-ma-env-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-ma-env-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-ma-env',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END MA ENVELOPE CONTROLS

                ##### BEGIN MA RIBBON CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-ma-ribbon',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-ma-ribbon',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'ma-ribbon-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
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
                                dbc.Popover([
                                    html.Span(
                                        'Are the underlying prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-ma-ribbon-adjusted-dropdown',
                                    target = 'ma-ribbon-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('# Of Bands', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
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
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-ma-ribbon-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-ma-ribbon-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-ma-ribbon',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END MA RIBBON CONTROLS

                ##### BEGIN MACD CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-macd',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-macd',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                               """NOTE: Moving Average Convergence Divergence cannot be plotted on the Upper Deck 
                               if the Primary Y-Axis of the Upper Deck is populated.
                               """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-macd',
                        target = 'collapse-button-macd',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'macd-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id = 'macd-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '98px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id = 'macd-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '78px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is MACD based on prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-macd-adjusted-dropdown',
                                    target = 'macd-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Vol Normalized', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px'}),
                                    dcc.Dropdown(
                                        id = 'macd-vol-normalized-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '114px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        """MACD-V, or Volatility-Normalized MACD, takes into account High, Low and Close prices,
                                        as well as the Average True Rate.""",
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-macd-vol-normalized-dropdown',
                                    class_name = 'popover-menu-button',
                                    target = 'macd-vol-normalized-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Signal', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top'}),
                                    dcc.Dropdown(
                                        id = 'macd-add-signal-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '75px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Signal Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                                    dbc.Input(
                                        id = 'macd-signal-window-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 9,
                                        min = 1,
                                        max = 200,
                                        step = 1,
                                        debounce = True,
                                        disabled = False,
                                        style = {'width': '102px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Signal Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'macd-signal-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Gold',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '113px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'macd-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Filled Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '103px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        """NOTE: Histogram will plot the accurate daily data. Filled Line will plot at zero whenever MACD/MACD-V 
                                        changes sign, which is to avoid both positive and negative line fills on any given day.""",
                                        style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-macd-plot-type-dropdown',
                                    target = 'macd-plot-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Oscillator Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top'}),
                                    dcc.Dropdown(
                                        id = 'macd-histogram-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['MACD-Signal', 'MACD-Zero'],
                                        value = 'MACD-Signal',
                                        clearable = False,
                                        style = {'width': '125px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
                                    dcc.Markdown("""<DIV>MACD-Signal: MACD and Signal are plotted as lines and Histogram / Filled Line is based on their difference.<BR/>
                                        MACD-Zero: MACD is plotted as Histogram / Filled Line and the Signal is added if selected.</DIV>""", dangerously_allow_html = True),
                                    ], 
                                    id = 'popover-macd-histogram-type-dropdown',
                                    target = 'macd-histogram-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    # trigger = 'click',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top'}),
                                    dcc.Dropdown(
                                        id='macd-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '62px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'macd-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = candle_colors,
                                        value = 'Green-Red',
                                        clearable = False,
                                        style = {'width': '116px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Price', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top'}),
                                    dcc.Dropdown(
                                        id = 'macd-add-price-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '67px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Price can only be added to Secondary Y-Axis on the Upper Deck. Secondary Y-Axis must be first activated from the THEME & TEMPLATE menu under GENERAL SETTINGS.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-macd-add-price-dropdown',
                                    target = 'macd-add-price-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Price Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='macd-price-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Magenta',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '107px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-macd-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-macd-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-macd',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END MACD CONTROLS

                ##### BEGIN IMPULSE MACD CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-impulse-macd',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-impulse-macd',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                               """NOTE: Impulse Moving Average Convergence Divergence cannot be plotted on the Upper Deck 
                               if the Primary Y-Axis of the Upper Deck is populated.
                               """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-impulse-macd',
                        target = 'collapse-button-impulse-macd',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'impulse-macd-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'impulse-macd-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '98px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'impulse-macd-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '78px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is Impulse MACD based on prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-impulse-macd-adjusted-dropdown',
                                    target = 'impulse-macd-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('SMMA Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'impulse-macd-smma-window-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 34,
                                        min = 1,
                                        max = 200,
                                        step = 1,
                                        debounce = True,
                                        disabled = False,
                                        style = {'width': '114px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'The length of the Smoothed Moving Average (SMMA) period used in the Impulse MACD calculation..',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-impulse-macd-smma-window-input',
                                    target = 'impulse-macd-smma-window-input',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Signal', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top'}),
                                    dcc.Dropdown(
                                        id = 'impulse-macd-add-signal-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '75px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Signal Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
                                    dbc.Input(
                                        id = 'impulse-macd-signal-window-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 9,
                                        min = 1,
                                        max = 200,
                                        step = 1,
                                        debounce = True,
                                        disabled = False,
                                        style = {'width': '102px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Signal Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'impulse-macd-signal-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Gold',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '113px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'impulse-macd-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Filled Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '103px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        """NOTE: Histogram will plot the accurate daily data. Filled Line will plot at zero whenever MACD/MACD-V 
                                        changes sign, which is to avoid both positive and negative line fills on any given day.""",
                                        style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-impulse-macd-plot-type-dropdown',
                                    target = 'impulse-macd-plot-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Oscillator Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'impulse-macd-histogram-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['MACD-Signal', 'MACD-Zero'],
                                        value = 'MACD-Signal',
                                        clearable = False,
                                        style = {'width': '125px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
                                    dcc.Markdown("""<DIV>MACD-Signal: Impulse MACD and Signal are plotted as lines and the Histogram / Filled Line is based on their difference.<BR/>
                                        MACD-Zero: Impulse MACD is plotted as Histogram / Filled Line and the Signal is added if selected.</DIV>""", dangerously_allow_html = True),
                                    ], 
                                    id = 'popover-impulse-macd-histogram-type-dropdown',
                                    target = 'impulse-macd-histogram-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    # trigger = 'click',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top'}),
                                    dcc.Dropdown(
                                        id='impulse-macd-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '62px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'impulse-macd-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = candle_colors,
                                        value = 'Green-Red',
                                        clearable = False,
                                        style = {'width': '116px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Price', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top'}),
                                    dcc.Dropdown(
                                        id = 'impulse-macd-add-price-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '67px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Price can only be added to Secondary Y-Axis on the Upper Deck. Secondary Y-Axis must be first activated from the THEME & TEMPLATE menu under GENERAL SETTINGS.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-impulse-macd-add-price-dropdown',
                                    target = 'impulse-macd-add-price-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Price Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='impulse-macd-price-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Magenta',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '107px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-impulse-macd-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-impulse-macd-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-impulse-macd',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END IMPULSE MACD CONTROLS

            ]),
            id = 'collapse-trend-tab',
            is_open = False,
            style = {'width': '315px'}
        )],
        style = {'margin-left': '5px', 'margin-bottom': '5px'}
    ), 

    ##### END TREND INDICATORS TAB

    ####################################################

    ##### BEGIN VOLATILITY INDICATORS TAB

    html.Div([

        html.Div([
            dbc.Button(
                id = 'collapse-button-volatility-tab',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_plot_category_css
            ),
            html.Div(
                id = 'added-to-plot-indicator-volatility-tab',
                style = not_added_to_plot_indicator_css
            )
        ],
        style = {'width': '315px', 'display': 'flex', 'flex-wrap': 'nowrap'}
        ),
        dbc.Popover([
            # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
            dcc.Markdown("""<DIV>► BOLLINGER BANDS<BR/>
                ► BOLLINGER BANDWIDTH / %B<BR/>
                ► AVERAGE TRUE RATE<BR/>
                ► MOVING VOLATILITY<BR/>
                ► ULCER INDEX</DIV>""",
                dangerously_allow_html = True)
            ], 
            id = 'popover-collapse-button-volatility-tab',
            target = 'collapse-button-volatility-tab',
            body = False,
            trigger = 'hover',
            hide_arrow = True,
            style = popover_menu_tab_collapse_button_css
        ),

        dbc.Collapse(

            html.Div([

                ##### BEGIN BOLLINGER CONTROLS
                # Category: VOLATILITY INDICATORS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-bollinger',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-bollinger',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'bollinger-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
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
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
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
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='bollinger-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Are the underlying prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-bollinger-adjusted-dropdown',
                                    target = 'bollinger-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('# Of Bands', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'bollinger-nbands-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 1,
                                        min = 1,
                                        max = 5,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '90px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('SD Factor', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
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
                                    html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='bollinger-ma-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Simple', 'Exponential', 'Weighted'],
                                        value = 'Simple',
                                        clearable = False,
                                        style = {'width': '175px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='bollinger-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Gold',
                                        clearable = False,
                                        style = {'width': '125px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-bollinger-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-bollinger-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-bollinger',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END BOLLINGER CONTROLS

                ##### BEGIN BOLL WIDTH CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-boll-width',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-boll-width',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                                """NOTE: Bollinger Bandwidth / %B can only be plotted on Secondary Y-Axis or on the Middle/Lower deck
                                if the Primary Y-Axis is populated. 
                                """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-boll-width',
                        target = 'collapse-button-boll-width',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'boll-width-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'boll-width-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='boll-width-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '75px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='boll-width-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Are the underlying prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-boll-width-adjusted-dropdown',
                                    target = 'boll-width-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('On Sec Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='boll-width-secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'No',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis must first be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS in order to plot on it.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-boll-width-secondary-y-dropdown',
                                    target = 'boll-width-secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Indicator Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='boll-width-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Bandwidth', '%B'],
                                        value = 'Bandwidth',
                                        clearable = False,
                                        style = {'width': '135px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
                                    dcc.Markdown("""<DIV>Bollinger Bandwith =<BR/> (Upper Band - Lower Band) / Middle Band<BR/>
                                        %B =<BR/> (Price - Lower Band) / (Upper Band - Lower Band)</DIV>""", dangerously_allow_html = True),
                                    ], 
                                    id = 'popover-boll-width-type-dropdown',
                                    target = 'boll-width-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    # trigger = 'click',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'boll-width-window-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 20,
                                        min = 1,
                                        max = 100,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('SD Factor', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'boll-width-nstd-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 2.0,
                                        min = 0,
                                        max = 10,
                                        step = 0.1,
                                        debounce = True,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='boll-width-ma-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Simple', 'Exponential', 'Weighted'],
                                        value = 'Simple',
                                        clearable = False,
                                        style = {'width': '112px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='boll-width-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Gold',
                                        clearable = False,
                                        style = {'width': '108px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '0px'}),
                                    dcc.Dropdown(
                                        id='boll-width-add-yaxis-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '75px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Add y-axis title?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-boll-width-add-yaxis-title-dropdown',
                                    target = 'boll-width-add-yaxis-title-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-boll-width-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-boll-width-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-boll-width',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END BOLL WIDTH CONTROLS

                ##### BEGIN ATR CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-atr',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-atr',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                                """NOTE: Average True Rate can only be plotted on the Secondary Y-Axis or on the Middle/Lower deck
                                if the Primary Y-Axis is populated. 
                                """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-atr',
                        target = 'collapse-button-atr',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'atr-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'atr-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '90px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='atr-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '70px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Are the underlying prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-atr-adjusted-dropdown',
                                    target = 'atr-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Periods', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'atr-periods-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 14,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '5px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Number of periods (days) used in the Average True Rate calculation',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-atr-periods-input',
                                    target = 'atr-periods-input',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('On Sec Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='atr-secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'No',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis must first be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS in order to plot on it.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-atr-secondary-y-dropdown',
                                    target = 'atr-secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('ATR Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='atr-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Regular', 'Percent'],
                                        value = 'Regular',
                                        clearable = False,
                                        style = {'width': '93px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='atr-add-yaxis-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '82px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Add y-axis title?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-atr-add-yaxis-title-dropdown',
                                    target = 'atr-add-yaxis-title-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='atr-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Base',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        # 'ADD TO PLOT',
                                        # '🗸',
                                        # '✓',
                                        # '✔',
                                        # https://www.w3schools.com/charsets/ref_utf_dingbats.asp
                                        id = f'add-atr-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        # https://www.w3schools.com/charsets/ref_utf_dingbats.asp
                                        id = f'remove-atr-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-atr',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END ATR CONTROLS

                ##### BEGIN MVOL CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-mvol',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-mvol',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                                """NOTE: Moving Volatility / Standard Deviation can only be plotted on Secondary Y-Axis or on the Middle/Lower Deck
                                if the Primary Y-Axis is populated. 
                                """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-mvol',
                        target = 'collapse-button-mvol',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'mvol-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'mvol-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='mvol-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '75px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='mvol-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is the underlying price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-mvol-adjusted-dropdown',
                                    target = 'mvol-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('On Sec Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='mvol-secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'No',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis must first be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS in order to plot on it.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-mvol-secondary-y-dropdown',
                                    target = 'mvol-secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Indicator Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='mvol-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Volatility', 'Standard Deviation'],
                                        value = 'Volatility',
                                        clearable = False,
                                        style = {'width': '155px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '1px'}),
                                    dcc.Dropdown(
                                        id='mvol-ma-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Simple', 'Exponential', 'Weighted'],
                                        value = 'Simple',
                                        clearable = False,
                                        style = {'width': '145px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'mvol-window-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 10,
                                        min = 1,
                                        max = 100,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '92px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='mvol-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Gold',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='mvol-add-yaxis-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '83px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Add y-axis title?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-mvol-add-yaxis-title-dropdown',
                                    target = 'mvol-add-yaxis-title-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-mvol-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-mvol-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-mvol',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END MVOL CONTROLS

                ##### BEGIN ULCER INDEX CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-ulcer',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-ulcer',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                                """NOTE: Ulcer Index can only be plotted on Secondary Y-Axis or on the Middle/Lower Deck
                                if the Primary Y-Axis is populated. Ulcer Index data is part of the drawdown analysis
                                and can be plotted alongside DRAWDOWNS from the PRICES PLOTS tab.
                                """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-ulcer',
                        target = 'collapse-button-ulcer',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'ulcer-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'ulcer-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='ulcer-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '75px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='ulcer-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is the underlying price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-ulcer-adjusted-dropdown',
                                    target = 'ulcer-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('On Sec Y', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '1px'}),
                                    dcc.Dropdown(
                                        id='ulcer-secondary-y-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'No',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Secondary Y-Axis must first be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS in order to plot on it.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-ulcer-secondary-y-dropdown',
                                    target = 'ulcer-secondary-y-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'ulcer-window-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 14,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '92px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='ulcer-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Gold',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Y-Axis Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='ulcer-add-yaxis-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '83px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Add y-axis title?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-ulcer-add-yaxis-title-dropdown',
                                    target = 'ulcer-add-yaxis-title-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-ulcer-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-ulcer-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-ulcer',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END ULCER INDEX CONTROLS

            ]),
            id = 'collapse-volatility-tab',
            is_open = False,
            style = {'width': '315px'}
        )],
        style = {'margin-left': '5px', 'margin-bottom': '5px'}
    ), 

    ##### END VOLATILITY INDICATORS TAB

    ###########################################

    ##### BEGIN MOMENTUM INDICATORS TAB

    html.Div([

        html.Div([
            dbc.Button(
                id = 'collapse-button-momentum-tab',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_plot_category_css
            ),
            html.Div(
                id = 'added-to-plot-indicator-momentum-tab',
                style = not_added_to_plot_indicator_css
            )
        ],
        style = {'width': '315px', 'display': 'flex', 'flex-wrap': 'nowrap'}
        ),
        dbc.Popover([
            # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
            dcc.Markdown("""<DIV>► RELATIVE STRENGTH INDEX<BR/>► STOCHASTIC OSCILLATOR</DIV>""",
                dangerously_allow_html = True)
            ], 
            id = 'popover-collapse-button-momentum-tab',
            target = 'collapse-button-momentum-tab',
            body = False,
            trigger = 'hover',
            hide_arrow = True,
            style = popover_menu_tab_collapse_button_css
        ),

        dbc.Collapse(

            html.Div([

                ##### BEGIN RSI CONTROLS
                # Category: MOMENTUM INDICATORS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-rsi',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-rsi',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                               """NOTE: Relative Strength Index cannot be plotted on the Upper Deck 
                               if the Primary Y-Axis of the Upper Deck is populated.
                               """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-rsi',
                        target = 'collapse-button-rsi',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'rsi-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'rsi-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '90px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'rsi-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'Adjusted Close'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '130px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is RSI based on prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-rsi-price-type-dropdown',
                                    target = 'rsi-price-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'rsi-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '70px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('# Of Periods', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'rsi-periods-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 14,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '110px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '5px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Overbought/Oversold', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'rsi-add-overbought-oversold-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '185px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('% Overbought Level', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'rsi-overbought-level-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 70,
                                        min = 1,
                                        max = 99,
                                        step = 1,
                                        debounce = True,
                                        disabled = False,
                                        style = {'width': '155px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('% Oversold Level', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'rsi-oversold-level-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 30,
                                        min = 1,
                                        max = 99,
                                        step = 1,
                                        debounce = True,
                                        disabled = False,
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('RSI Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'rsi-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Gold',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '110px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Price', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'rsi-add-price-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '70px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Price can only be added to Secondary Y-Axis on the Upper Deck. Secondary Y-Axis must be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS for this option to be available.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-rsi-add-price-dropdown',
                                    target = 'rsi-add-price-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Price Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='rsi-price-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Base',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '110px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-rsi-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-rsi-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-rsi',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END RSI CONTROLS

                ##### BEGIN STOCHASTIC CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-stochastic',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-stochastic',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                               """NOTE: Stochastic Oscillator cannot be plotted on the Upper Deck 
                               if the Primary Y-Axis of the Upper Deck is populated.
                               """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-stochastic',
                        target = 'collapse-button-stochastic',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'stochastic-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'stochastic-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '95px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='stochastic-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '75px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Are the underlying prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-stochastic-adjusted-dropdown',
                                    target = 'stochastic-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Stochastic Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'stochastic-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Fast', 'Slow', 'Full'],
                                        value = 'Slow',
                                        clearable = False,
                                        style = {'width': '120px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
                                    dcc.Markdown("""<DIV>Fast Stochastic: [...].<BR/>
                                        Slow Stochastic: [...].<BR/>
                                        Full Stochastic: [...].<BR/></DIV>""", dangerously_allow_html = True),
                                    ], 
                                    id = 'popover-stochastic-type-dropdown',
                                    target = 'stochastic-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('%K Line Period', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'stochastic-fast-k-period-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 14,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '127px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '5px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('%K Smoothing Period', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'stochastic-k-smoothing-period-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 3,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '168px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '0px', 'margin-right': '0px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('%D Line Period', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'stochastic-d-period-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 3,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '115px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '5px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Overbought/Oversold', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'stochastic-add-overbought-oversold-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '180px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('% Overbought Level', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'stochastic-overbought-level-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 80,
                                        min = 1,
                                        max = 99,
                                        step = 1,
                                        debounce = True,
                                        disabled = False,
                                        style = {'width': '155px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('% Oversold Level', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'stochastic-oversold-level-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 20,
                                        min = 1,
                                        max = 99,
                                        step = 1,
                                        debounce = True,
                                        disabled = False,
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('%K Line Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'stochastic-k-line-color-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = drawdowns_colors,
                                        value = 'Orange',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '148px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('%D Line Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'stochastic-d-line-color-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = drawdowns_colors,
                                        value = 'Purple',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '147px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'stochastic-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Price', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'stochastic-add-price-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Price can only be added to Secondary Y-Axis on the Upper Deck. Secondary Y-Axis must be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS for this option to be available.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-stochastic-add-price-dropdown',
                                    target = 'stochastic-add-price-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Price Color', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='stochastic-price-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Base',
                                        clearable = False,
                                        disabled = False,
                                        style = {'width': '125px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-stochastic-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-stochastic-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-stochastic',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END STOCHASTIC CONTROLS

            ]),
            id = 'collapse-momentum-tab',
            is_open = False,
            style = {'width': '315px'}
        )],
        style = {'margin-left': '5px', 'margin-bottom': '5px'}
    ), 

    ##### END MOMENTUM INDICATORS TAB

    #######################################################

    ##### BEGIN DIFFERENTIAL PLOTS TAB

    html.Div([

        html.Div([
            dbc.Button(
                id = 'collapse-button-differential-tab',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_plot_category_css
            ),
            html.Div(
                id = 'added-to-plot-indicator-differential-tab',
                style = not_added_to_plot_indicator_css
            )
        ],
        style = {'width': '315px', 'display': 'flex', 'flex-wrap': 'nowrap'}
        ),
        dbc.Popover([
            # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
            dcc.Markdown("""<DIV>► DIFFERENTIAL No. 1<BR/>
                ► DIFFERENTIAL No. 2<BR/>
                ► DIFFERENTIAL No. 3<BR/>
                ► STOCHASTIC DIFFERENTIAL</DIV>""",
                dangerously_allow_html = True)
            ], 
            id = 'popover-collapse-button-differential-tab',
            target = 'collapse-button-differential-tab',
            body = False,
            trigger = 'hover',
            hide_arrow = True,
            style = popover_menu_tab_collapse_button_css
        ),

        dbc.Collapse(

            html.Div([

                ##### BEGIN DIFFERENTIAL PLOT 1 CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-diff-1',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-diff-1',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                               """NOTE: Differential plot cannot be placed on the Upper Deck 
                               if the Primary Y-Axis of the Upper Deck is populated.
                               """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-diff-1',
                        target = 'collapse-button-diff-1',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'diff-1-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id = 'diff-1-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-1-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Filled Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '97px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        """NOTE: Histogram will plot the accurate daily data. Filled Line will plot at zero whenever the Differential 
                                        changes sign, which is to avoid both positive and negative line fills on any given day.""",
                                        style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-1-plot-type-dropdown',
                                    target = 'diff-1-plot-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-1-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = candle_colors,
                                        value = 'Green-Red',
                                        clearable = False,
                                        style = {'width': '113px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Line 1', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-1-add-price-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Line 1 can only be added to Secondary Y-Axis on the Upper Deck. Secondary Y-Axis must be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS for this option to be available.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-1-add-price-dropdown',
                                    target = 'diff-1-add-price-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                html.Div([
                                    html.Div('Line 1 Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-1-price-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Sapphire',
                                        clearable = False,
                                        disabled = False,
                                        #style = {'width': '107px'}
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-1-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '70px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ### Signal Line, Row 1
                                # html.Div('Signal Line', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'text-decoration': 'underline', 'width': '310px', 'padding-left': '2px', 'vertical-align': 'top'}),                            
                                html.Div([
                                    html.Div('Add Signal', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-1-add-signal-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '90px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Signal MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-1-signal-ma-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                        value = 'Simple',
                                        clearable = False,
                                        style = {'width': '205px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),                    
                                ### Signal Line, Row 2
                                html.Div(
                                    id = 'diff-1-signal-line-row-2-container',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('Signal Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-1-signal-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '135px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Signal Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-1-signal-color-theme-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = overlay_color_themes,
                                                value = 'Gold',
                                                clearable = False,
                                                disabled = False,
                                                style = {'width': '160px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                    ]
                                ),

                                ### Line 1, Row 1
                                html.Div('Define Line 1', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'text-decoration': 'underline', 'width': '310px', 'padding-left': '2px', 'vertical-align': 'top'}),
                                html.Div([
                                    html.Div('Line Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-1-line-1-line-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Price', 'Moving Average'],
                                        value = 'Price',
                                        clearable = False,
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-1-line-1-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-1-line-1-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is Line 1 base price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-1-line-1-adjusted-dropdown',
                                    target = 'diff-1-line-1-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                ### Line 1, Row 2
                                html.Div(
                                    id = 'diff-1-line-1-ma-options',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-1-line-1-ma-type-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                                value = 'Simple',
                                                clearable = False,
                                                style = {'width': '180px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-1-line-1-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '115px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        )
                                    ]
                                ),

                                ### Line 2, Row 1
                                html.Div(
                                    'Define Line 2',
                                    id = 'diff-1-define-line-2',
                                    style = {
                                        'font-family': 'Helvetica',
                                        'font-size': '14px',
                                        'font-weight': 'bold',
                                        'text-decoration': 'underline',
                                        'width': '310px',
                                        'padding-left': '2px',
                                        'vertical-align': 'top'
                                    }
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Line 2 must differ from Line 1',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-1-define-line-2',
                                    target = 'diff-1-define-line-2',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Line Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-1-line-2-line-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Price', 'Moving Average'],
                                        value = 'Price',
                                        clearable = False,
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-1-line-2-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-1-line-2-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is Line 2 base price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-1-line-2-adjusted-dropdown',
                                    target = 'diff-1-line-2-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                ### Line 2, Row 2
                                html.Div(
                                    id = 'diff-1-line-2-ma-options',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-1-line-2-ma-type-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                                value = 'Simple',
                                                clearable = False,
                                                style = {'width': '180px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-1-line-2-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '115px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        )
                                    ]
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-diff-1-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-diff-1-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-diff-1',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END DIFFERENTIAL No. 1 CONTROLS

                ##### BEGIN DIFFERENTIAL PLOT 2 CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-diff-2',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-diff-2',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                               """NOTE: Differential plot cannot be placed on the Upper Deck 
                               if the Primary Y-Axis of the Upper Deck is populated.
                               """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-diff-2',
                        target = 'collapse-button-diff-2',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'diff-2-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id = 'diff-2-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-2-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Filled Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '97px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        """NOTE: Histogram will plot the accurate daily data. Filled Line will plot at zero whenever the Differential 
                                        changes sign, which is to avoid both positive and negative line fills on any given day.""",
                                        style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-2-plot-type-dropdown',
                                    target = 'diff-2-plot-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-2-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = candle_colors,
                                        value = 'Green-Red',
                                        clearable = False,
                                        style = {'width': '113px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Line 1', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-2-add-price-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Line 1 can only be added to Secondary Y-Axis on the Upper Deck. Secondary Y-Axis must be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS for this option to be available.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-2-add-price-dropdown',
                                    target = 'diff-2-add-price-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                html.Div([
                                    html.Div('Line 1 Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-2-price-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Sapphire',
                                        clearable = False,
                                        disabled = False,
                                        #style = {'width': '107px'}
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-2-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '70px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ### Signal Line, Row 1
                                # html.Div('Signal Line', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'text-decoration': 'underline', 'width': '310px', 'padding-left': '2px', 'vertical-align': 'top'}),                            
                                html.Div([
                                    html.Div('Add Signal', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-2-add-signal-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '90px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Signal MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-2-signal-ma-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                        value = 'Simple',
                                        clearable = False,
                                        style = {'width': '205px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),                    
                                ### Signal Line, Row 2
                                html.Div(
                                    id = 'diff-2-signal-line-row-2-container',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('Signal Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-2-signal-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '135px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Signal Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-2-signal-color-theme-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = overlay_color_themes,
                                                value = 'Gold',
                                                clearable = False,
                                                disabled = False,
                                                style = {'width': '160px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                    ]
                                ),

                                ### Line 1, Row 1
                                html.Div('Define Line 1', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'text-decoration': 'underline', 'width': '310px', 'padding-left': '2px', 'vertical-align': 'top'}),
                                html.Div([
                                    html.Div('Line Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-2-line-1-line-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Price', 'Moving Average'],
                                        value = 'Price',
                                        clearable = False,
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-2-line-1-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-2-line-1-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is Line 1 base price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-2-line-1-adjusted-dropdown',
                                    target = 'diff-2-line-1-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                ### Line 1, Row 2
                                html.Div(
                                    id = 'diff-2-line-1-ma-options',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-2-line-1-ma-type-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                                value = 'Simple',
                                                clearable = False,
                                                style = {'width': '180px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-2-line-1-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '115px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        )
                                    ]
                                ),

                                ### Line 2, Row 1
                                html.Div(
                                    'Define Line 2',
                                    id = 'diff-2-define-line-2',
                                    style = {
                                        'font-family': 'Helvetica',
                                        'font-size': '14px',
                                        'font-weight': 'bold',
                                        'text-decoration': 'underline',
                                        'width': '310px',
                                        'padding-left': '2px',
                                        'vertical-align': 'top'
                                    }
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Line 2 must differ from Line 1',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-2-define-line-2',
                                    target = 'diff-2-define-line-2',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Line Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-2-line-2-line-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Price', 'Moving Average'],
                                        value = 'Price',
                                        clearable = False,
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-2-line-2-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-2-line-2-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is Line 2 base price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-2-line-2-adjusted-dropdown',
                                    target = 'diff-2-line-2-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                ### Line 2, Row 2
                                html.Div(
                                    id = 'diff-2-line-2-ma-options',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-2-line-2-ma-type-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                                value = 'Simple',
                                                clearable = False,
                                                style = {'width': '180px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-2-line-2-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '115px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        )
                                    ]
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-diff-2-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-diff-2-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-diff-2',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END DIFFERENTIAL No. 2 CONTROLS

                ##### BEGIN DIFFERENTIAL PLOT 3 CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-diff-3',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-diff-3',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                               """NOTE: Differential plot cannot be placed on the Upper Deck 
                               if the Primary Y-Axis of the Upper Deck is populated.
                               """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-diff-3',
                        target = 'collapse-button-diff-3',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'diff-3-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-bottom': '0px'}),
                                    dcc.Dropdown(
                                        id = 'diff-3-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-3-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Filled Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '97px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        """NOTE: Histogram will plot the accurate daily data. Filled Line will plot at zero whenever the Differential 
                                        changes sign, which is to avoid both positive and negative line fills on any given day.""",
                                        style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-2-plot-type-dropdown',
                                    target = 'diff-3-plot-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-3-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = candle_colors,
                                        value = 'Green-Red',
                                        clearable = False,
                                        style = {'width': '113px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Line 1', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-3-add-price-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Line 1 can only be added to Secondary Y-Axis on the Upper Deck. Secondary Y-Axis must be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS for this option to be available.',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-3-add-price-dropdown',
                                    target = 'diff-3-add-price-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                html.Div([
                                    html.Div('Line 1 Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-3-price-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Sapphire',
                                        clearable = False,
                                        disabled = False,
                                        #style = {'width': '107px'}
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-3-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '70px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ### Signal Line, Row 1
                                # html.Div('Signal Line', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'text-decoration': 'underline', 'width': '310px', 'padding-left': '2px', 'vertical-align': 'top'}),                            
                                html.Div([
                                    html.Div('Add Signal', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-3-add-signal-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '90px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Signal MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-3-signal-ma-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                        value = 'Simple',
                                        clearable = False,
                                        style = {'width': '205px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),                    
                                ### Signal Line, Row 2
                                html.Div(
                                    id = 'diff-3-signal-line-row-2-container',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('Signal Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-3-signal-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '135px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Signal Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-3-signal-color-theme-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = overlay_color_themes,
                                                value = 'Gold',
                                                clearable = False,
                                                disabled = False,
                                                style = {'width': '160px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                    ]
                                ),

                                ### Line 1, Row 1
                                html.Div('Define Line 1', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'text-decoration': 'underline', 'width': '310px', 'padding-left': '2px', 'vertical-align': 'top'}),
                                html.Div([
                                    html.Div('Line Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-3-line-1-line-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Price', 'Moving Average'],
                                        value = 'Price',
                                        clearable = False,
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-3-line-1-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-3-line-1-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is Line 1 base price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-3-line-1-adjusted-dropdown',
                                    target = 'diff-3-line-1-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                ### Line 1, Row 2
                                html.Div(
                                    id = 'diff-3-line-1-ma-options',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-3-line-1-ma-type-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                                value = 'Simple',
                                                clearable = False,
                                                style = {'width': '180px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-3-line-1-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '115px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        )
                                    ]
                                ),

                                ### Line 2, Row 1
                                html.Div(
                                    'Define Line 2',
                                    id = 'diff-3-define-line-2',
                                    style = {
                                        'font-family': 'Helvetica',
                                        'font-size': '14px',
                                        'font-weight': 'bold',
                                        'text-decoration': 'underline',
                                        'width': '310px',
                                        'padding-left': '2px',
                                        'vertical-align': 'top'
                                    }
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Line 2 must differ from Line 1',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-3-define-line-2',
                                    target = 'diff-3-define-line-2',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Line Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-3-line-2-line-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Price', 'Moving Average'],
                                        value = 'Price',
                                        clearable = False,
                                        style = {'width': '140px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Price Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-3-line-2-price-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Close', 'High', 'Low', 'Open'],
                                        value = 'Close',
                                        clearable = False,
                                        style = {'width': '85px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-3-line-2-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '65px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Is Line 2 base price adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-3-line-2-adjusted-dropdown',
                                    target = 'diff-3-line-2-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                ### Line 2, Row 2
                                html.Div(
                                    id = 'diff-3-line-2-ma-options',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-3-line-2-ma-type-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                                value = 'Simple',
                                                clearable = False,
                                                style = {'width': '180px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-3-line-2-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '115px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        )
                                    ]
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = f'add-diff-3-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = f'remove-diff-3-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm'
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-diff-3',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END DIFFERENTIAL No. 3 CONTROLS

                ##### BEGIN STOCHASTIC DIFFERENTIAL CONTROLS

                html.Div([
                
                    html.Div([
                        dbc.Button(
                            id = 'collapse-button-diff-stochastic',
                            class_name = 'ma-1',
                            color = 'primary',
                            size = 'sm',
                            n_clicks = 0,
                            style = collapse_button_css
                        ),
                        html.Div(
                            id = 'added-to-plot-indicator-diff-stochastic',
                            style = not_added_to_plot_indicator_css
                        )
                    ],
                    style = {'width': '310px', 'display': 'flex', 'flex-wrap': 'nowrap'}
                    ),
                    dbc.Popover(
                        [
                        html.Span(
                               """NOTE: Stochastic Differential cannot be plotted on the Upper Deck 
                               if the Primary Y-Axis of the Upper Deck is populated.
                               """,
                                style = popover_menu_collapse_button_header_css
                            )
                        ], 
                        id = 'popover-collapse-button-diff-stochastic',
                        target = 'collapse-button-diff-stochastic',
                        body = False,
                        trigger = 'hover',
                        hide_arrow = True,
                        style = popover_menu_collapse_button_css
                    ),

                    dbc.Collapse(
                    
                        html.Div(
                        
                            id = 'diff-stochastic-controls',
                            children = [
                            
                                html.Div([
                                    html.Div('Target Deck', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-deck-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Upper'],
                                        value = 'Upper',
                                        clearable = False,
                                        style = {'width': '90px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Plot Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-plot-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Histogram', 'Filled Line'],
                                        value = 'Histogram',
                                        clearable = False,
                                        style = {'width': '102px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        """NOTE: Histogram will plot the accurate daily data. Filled Line will plot at zero whenever the Stochastic Differential 
                                        changes sign, which is to avoid both positive and negative line fills on any given day.""",
                                        style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-stochastic-plot-type-dropdown',
                                    target = 'diff-stochastic-plot-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Differential', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '3px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-sign-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['%K − %D', '%D − %K'],
                                        value = '%K − %D',
                                        clearable = False,
                                        style = {'width': '98px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = candle_colors,
                                        value = 'Green-Red',
                                        clearable = False,
                                        style = {'width': '130px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Add Title', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-add-title-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Adjusted', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-stochastic-adjusted-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Yes', 'No'],
                                        value = 'Yes',
                                        clearable = False,
                                        style = {'width': '80px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span(
                                        'Are the underlying prices adjusted for stock splits and dividends?',
                                         style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-stochastic-adjusted-dropdown',
                                    target = 'diff-stochastic-adjusted-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('Stochastic Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Fast', 'Slow', 'Full'],
                                        value = 'Slow',
                                        clearable = False,
                                        style = {'width': '150px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    # NOTE: Must use <BR/>, not <BR>, to break the line inside the popover
                                    dcc.Markdown("""<DIV>Fast Stochastic: [...].<BR/>
                                        Slow Stochastic: [...].<BR/>
                                        Full Stochastic: [...].<BR/></DIV>""", dangerously_allow_html = True),
                                    ], 
                                    id = 'popover-diff-stochastic-type-dropdown',
                                    target = 'diff-stochastic-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),

                                html.Div([
                                    html.Div('%K Line Period', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'diff-stochastic-fast-k-period-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 14,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '145px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '5px', 'margin-right': '0px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('%K Smoothing Period', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'diff-stochastic-k-smoothing-period-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 3,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '170px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '0px', 'margin-right': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('%D Line Period', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                                    dbc.Input(
                                        id = 'diff-stochastic-d-period-input',
                                        className = 'plots-input-button',
                                        type = 'number',
                                        value = 3,
                                        min = 1,
                                        step = 1,
                                        debounce = True,
                                        style = {'width': '125px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-bottom': '0px', 'margin-right': '0px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                html.Div([
                                    html.Div('Add Line', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-add-line-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '69px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span("""%K Line, %D Line or Price can be added to Secondary Y-Axis on the Upper Deck. 
                                        Secondary Y-Axis must be activated from the THEME & TEMPLATE menu under GENERAL SETTINGS for this option to be available.""",
                                        style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-stochastic-add-line-dropdown',
                                    target = 'diff-stochastic-add-line-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),
                                html.Div([
                                    html.Div('Line Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-stochastic-added-line-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['%K Line', '%D Line', 'Price'],
                                        value = '%K Line',
                                        clearable = False,
                                        style = {'width': '93px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                dbc.Popover([
                                    html.Span('%K Line, %D Line or Price',
                                        style = popover_menu_collapse_button_header_css
                                        )
                                    ], 
                                    id = 'popover-diff-stochastic-added-line-type-dropdown',
                                    target = 'diff-stochastic-added-line-type-dropdown',
                                    body = False,
                                    trigger = 'hover',
                                    hide_arrow = False,
                                    style = popover_menu_button_css
                                ),                    
                                html.Div([
                                    html.Div('Line Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id='diff-stochastic-added-line-color-theme-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = overlay_color_themes,
                                        value = 'Base',
                                        clearable = False,
                                        disabled = True,
                                        style = {'width': '128px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),

                                ### Signal Line, Row 1
                                # html.Div('Signal Line', style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'text-decoration': 'underline', 'width': '310px', 'padding-left': '2px', 'vertical-align': 'top'}),                            
                                html.Div([
                                    html.Div('Add Signal', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-add-signal-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['No', 'Yes'],
                                        value = 'No',
                                        clearable = False,
                                        style = {'width': '90px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),
                                html.Div([
                                    html.Div('Signal MA Type', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                    dcc.Dropdown(
                                        id = 'diff-stochastic-signal-ma-type-dropdown',
                                        className = 'plots-dropdown-button',
                                        options = ['Simple', 'Exponential', 'Double Exponential', 'Triple Exponential', 'Weighted', 'Welles Wilder'],
                                        value = 'Simple',
                                        clearable = False,
                                        style = {'width': '205px'}
                                    )],
                                    style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                ),                    
                                ### Signal Line, Row 2
                                html.Div(
                                    id = 'diff-stochastic-signal-line-row-2-container',
                                    hidden = False,
                                    children = [
                                        html.Div([
                                            html.Div('Signal Window', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dbc.Input(
                                                id = 'diff-stochastic-signal-window-input',
                                                className = 'plots-input-button',
                                                type = 'number',
                                                value = 10,
                                                min = 1,
                                                max = 200,
                                                step = 1,
                                                debounce = True,
                                                disabled = False,
                                                style = {'width': '135px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                        html.Div([
                                            html.Div('Signal Color Theme', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-left': '2px'}),
                                            dcc.Dropdown(
                                                id = 'diff-stochastic-signal-color-theme-dropdown',
                                                className = 'plots-dropdown-button',
                                                options = overlay_color_themes,
                                                value = 'Gold',
                                                clearable = False,
                                                disabled = False,
                                                style = {'width': '160px'}
                                            )],
                                            style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                                        ),
                                    ]
                                ),

                                ##### Add / Remove buttons
                                html.Div([
                                    dbc.Button(
                                        'Add To Plot',
                                        id = 'add-diff-stochastic-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'success',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div([
                                    dbc.Button(
                                        # '✕',
                                        'Remove',
                                        id = 'remove-diff-stochastic-button',
                                        n_clicks = 0,
                                        class_name = 'ma-1',
                                        color = 'danger',
                                        size = 'sm',
                                        style = {'margin-bottom': '0px'}
                                    )],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                        ), 

                        id = 'collapse-diff-stochastic',
                        is_open = False,
                        style = {'width': '310px'}
                    )],
                    style = {'margin-left': '5px'}
                ), 

                ##### END STOCHASTIC DIFFERENTIAL CONTROLS

            ]),
            id = 'collapse-differential-tab',
            is_open = False,
            style = {'width': '315px'}
        )],
        style = {'margin-left': '5px', 'margin-bottom': '5px'}
    ), 

    ##### END DIFFERENTIAL PLOTS TAB

    #################################################################

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
            html.Div([
                dbc.Button(
                    id = 'collapse-button-final-table-selected-tickers',
                    class_name = 'ma-1',
                    color = 'primary',
                    size = 'sm',
                    n_clicks = 0,
                    style = collapse_button_right_margin_css
                ),
                html.Div(
                    build_dash_html.display_color_themes(),
                    style = {'display': 'inline-block'}
                )
            ]),

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
    Output('collapse-button-dates', 'children'),
    Output('collapse-dates', 'is_open'),
    Input('collapse-button-dates', 'n_clicks'),
    State('collapse-dates', 'is_open')
)
def toggle_collapse_dates(n, is_open):
    title = 'DATE RANGE'
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
    title = 'THEME & TEMPLATE'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('lower-height-input', 'disabled'),

    Output('hist-price-deck-dropdown', 'options'),
    Output('candlestick-deck-dropdown', 'options'),
    Output('drawdowns-deck-dropdown', 'options'),
    Output('volume-deck-dropdown', 'options'),
    Output('dollar-volume-deck-dropdown', 'options'),
    Output('obv-deck-dropdown', 'options'),   
    Output('bollinger-deck-dropdown', 'options'),
    Output('boll-width-deck-dropdown', 'options'),
    Output('ma-env-deck-dropdown', 'options'),
    Output('ma-ribbon-deck-dropdown', 'options'),
    Output('price-overlays-deck-dropdown', 'options'),
    Output('macd-deck-dropdown', 'options'),
    Output('impulse-macd-deck-dropdown', 'options'),
    Output('atr-deck-dropdown', 'options'),
    Output('mvol-deck-dropdown', 'options'),
    Output('ulcer-deck-dropdown', 'options'),
    Output('rsi-deck-dropdown', 'options'),
    Output('stochastic-deck-dropdown', 'options'),
    Output('diff-1-deck-dropdown', 'options'),
    Output('diff-2-deck-dropdown', 'options'),
    Output('diff-3-deck-dropdown', 'options'),
    Output('diff-stochastic-deck-dropdown', 'options'),

    Output('hist-price-deck-dropdown', 'value'),
    Output('candlestick-deck-dropdown', 'value'),
    Output('drawdowns-deck-dropdown', 'value'),
    Output('volume-deck-dropdown', 'value'),
    Output('dollar-volume-deck-dropdown', 'value'),
    Output('obv-deck-dropdown', 'value'),
    Output('bollinger-deck-dropdown', 'value'),
    Output('boll-width-deck-dropdown', 'value'),
    Output('ma-env-deck-dropdown', 'value'),
    Output('ma-ribbon-deck-dropdown', 'value'),
    Output('price-overlays-deck-dropdown', 'value'),
    Output('macd-deck-dropdown', 'value'),
    Output('impulse-macd-deck-dropdown', 'value'),
    Output('atr-deck-dropdown', 'value'),
    Output('mvol-deck-dropdown', 'value'),
    Output('ulcer-deck-dropdown', 'value'),    
    Output('rsi-deck-dropdown', 'value'),
    Output('stochastic-deck-dropdown', 'value'),
    Output('diff-1-deck-dropdown', 'value'),
    Output('diff-2-deck-dropdown', 'value'),
    Output('diff-3-deck-dropdown', 'value'),
    Output('diff-stochastic-deck-dropdown', 'value'),

    Input('deck-type-dropdown', 'n_clicks'),
    Input('deck-type-dropdown', 'value'),

    Input('hist-price-deck-dropdown', 'value'),
    Input('candlestick-deck-dropdown', 'value'),
    Input('drawdowns-deck-dropdown', 'value'),
    Input('volume-deck-dropdown', 'value'),
    Input('dollar-volume-deck-dropdown', 'value'),
    Input('obv-deck-dropdown', 'value'),
    Input('bollinger-deck-dropdown', 'value'),
    Input('boll-width-deck-dropdown', 'value'),
    Input('ma-env-deck-dropdown', 'value'),
    Input('ma-ribbon-deck-dropdown', 'value'),
    Input('price-overlays-deck-dropdown', 'value'),
    Input('macd-deck-dropdown', 'value'),
    Input('impulse-macd-deck-dropdown', 'value'),
    Input('atr-deck-dropdown', 'value'),
    Input('mvol-deck-dropdown', 'value'),
    Input('ulcer-deck-dropdown', 'value'),
    Input('rsi-deck-dropdown', 'value'),
    Input('stochastic-deck-dropdown', 'value'),
    Input('diff-1-deck-dropdown', 'value'),
    Input('diff-2-deck-dropdown', 'value'),
    Input('diff-3-deck-dropdown', 'value'),
    Input('diff-stochastic-deck-dropdown', 'value')
)
def target_deck_options(
    deck_changed,
    deck_type,
    hist_price_deck,
    candlestick_deck,
    drawdowns_deck,
    volume_deck,
    dollar_volume_deck,
    obv_deck,
    bollinger_deck,
    boll_width_deck,
    ma_env_deck,
    ma_ribbon_deck,
    price_overlays_deck,
    macd_deck,
    impulse_macd_deck,    
    atr_deck,
    mvol_deck,
    ulcer_deck,
    rsi_deck,
    stochastic_deck,
    diff_1_deck,
    diff_2_deck,
    diff_3_deck,
    diff_stochastic_deck
):
    # Number of deck-dropdown inputs
    n = target_deck_options.__code__.co_argcount - 2

    deck_changed = False if deck_changed is None else deck_changed

    if deck_type == 'Single':
        return tuple([True]) + tuple([k for k in [['Upper']] * n]) + tuple(['Upper'] * n)

    elif deck_type == 'Double':
        
        hist_price_deck_value =         ['Lower'] if (hist_price_deck in ['Middle', 'Lower']) else ['Upper']
        candlestick_deck_value =        ['Lower'] if (candlestick_deck in ['Middle', 'Lower']) else ['Upper']
        drawdowns_deck_value =          ['Lower'] if (drawdowns_deck in ['Middle', 'Lower']) else ['Upper']
        volume_deck_value =             ['Lower'] if (volume_deck in ['Middle', 'Lower']) else ['Upper']
        dollar_volume_deck_value =      ['Lower'] if (dollar_volume_deck in ['Middle', 'Lower']) else ['Upper']
        obv_deck_value =                ['Lower'] if (obv_deck in ['Middle', 'Lower']) else ['Upper']
        bollinger_deck_value =          ['Lower'] if (bollinger_deck in ['Middle', 'Lower']) else ['Upper']
        boll_width_deck_value =         ['Lower'] if (boll_width_deck in ['Middle', 'Lower']) else ['Upper']
        ma_env_deck_value =             ['Lower'] if (ma_env_deck in ['Middle', 'Lower']) else ['Upper']
        ma_ribbon_deck_value =          ['Lower'] if (ma_ribbon_deck in ['Middle', 'Lower']) else ['Upper']
        price_overlays_deck_value =     ['Lower'] if (price_overlays_deck in ['Middle', 'Lower']) else ['Upper']
        macd_deck_value =               ['Lower'] if (macd_deck in ['Middle', 'Lower']) else ['Upper']
        impulse_macd_deck_value =       ['Lower'] if (impulse_macd_deck in ['Middle', 'Lower']) else ['Upper']        
        atr_deck_value =                ['Lower'] if (atr_deck in ['Middle', 'Lower']) else ['Upper']
        mvol_deck_value =               ['Lower'] if (mvol_deck in ['Middle', 'Lower']) else ['Upper']
        ulcer_deck_value =              ['Lower'] if (ulcer_deck in ['Middle', 'Lower']) else ['Upper']
        rsi_deck_value =                ['Lower'] if (rsi_deck in ['Middle', 'Lower']) else ['Upper']
        stochastic_deck_value =         ['Lower'] if (stochastic_deck in ['Middle', 'Lower']) else ['Upper']
        diff_1_deck_value =             ['Lower'] if (diff_1_deck in ['Middle', 'Lower']) else ['Upper']
        diff_2_deck_value =             ['Lower'] if (diff_2_deck in ['Middle', 'Lower']) else ['Upper']
        diff_3_deck_value =             ['Lower'] if (diff_3_deck in ['Middle', 'Lower']) else ['Upper']
        diff_stochastic_deck_value =    ['Lower'] if (diff_stochastic_deck in ['Middle', 'Lower']) else ['Upper']
        all_deck_values = \
            hist_price_deck_value + \
            candlestick_deck_value + \
            drawdowns_deck_value + \
            volume_deck_value + \
            dollar_volume_deck_value + \
            obv_deck_value + \
            bollinger_deck_value + \
            boll_width_deck_value + \
            ma_env_deck_value + \
            ma_ribbon_deck_value + \
            price_overlays_deck_value + \
            macd_deck_value + \
            impulse_macd_deck_value + \
            atr_deck_value + \
            mvol_deck_value + \
            ulcer_deck_value + \
            rsi_deck_value + \
            stochastic_deck_value + \
            diff_1_deck_value + \
            diff_2_deck_value + \
            diff_3_deck_value + \
            diff_stochastic_deck_value
        return tuple([False]) + tuple([k for k in [['Upper', 'Lower']] * n]) + tuple(all_deck_values)

    else:

        hist_price_deck_value =         ['Middle'] if (hist_price_deck == 'Lower') & deck_changed else [hist_price_deck]
        candlestick_deck_value =        ['Middle'] if (candlestick_deck == 'Lower') & deck_changed else [candlestick_deck]
        drawdowns_deck_value =          ['Middle'] if (drawdowns_deck == 'Lower') & deck_changed else [drawdowns_deck]
        volume_deck_value =             ['Middle'] if (volume_deck == 'Lower') & deck_changed else [volume_deck]
        dollar_volume_deck_value =      ['Middle'] if (dollar_volume_deck == 'Lower') & deck_changed else [dollar_volume_deck]
        obv_deck_value =                ['Middle'] if (obv_deck == 'Lower') & deck_changed else [obv_deck]
        bollinger_deck_value =          ['Middle'] if (bollinger_deck == 'Lower') & deck_changed else [bollinger_deck]
        boll_width_deck_value =         ['Middle'] if (boll_width_deck in ['Middle', 'Lower']) else ['boll_width_deck']
        ma_env_deck_value =             ['Middle'] if (ma_env_deck == 'Lower') & deck_changed else [ma_env_deck]
        ma_ribbon_deck_value =          ['Middle'] if (ma_ribbon_deck == 'Lower') & deck_changed else [ma_ribbon_deck]
        price_overlays_deck_value =     ['Middle'] if (price_overlays_deck == 'Lower') & deck_changed else [price_overlays_deck]
        macd_deck_value =               ['Middle'] if (macd_deck == 'Lower') & deck_changed else [macd_deck]
        impulse_macd_deck_value =       ['Middle'] if (impulse_macd_deck == 'Lower') & deck_changed else [impulse_macd_deck]        
        atr_deck_value =                ['Middle'] if (atr_deck == 'Lower') & deck_changed else [atr_deck]
        mvol_deck_value =               ['Middle'] if (mvol_deck == 'Lower') & deck_changed else [mvol_deck]
        ulcer_deck_value =              ['Middle'] if (ulcer_deck == 'Lower') & deck_changed else [ulcer_deck]        
        rsi_deck_value =                ['Middle'] if (rsi_deck == 'Lower') & deck_changed else [rsi_deck]
        stochastic_deck_value =         ['Middle'] if (stochastic_deck == 'Lower') & deck_changed else [stochastic_deck]
        diff_1_deck_value =             ['Middle'] if (diff_1_deck == 'Lower') & deck_changed else [diff_1_deck]
        diff_2_deck_value =             ['Middle'] if (diff_2_deck == 'Lower') & deck_changed else [diff_2_deck]
        diff_3_deck_value =             ['Middle'] if (diff_3_deck == 'Lower') & deck_changed else [diff_3_deck]
        diff_stochastic_deck_value =    ['Middle'] if (diff_stochastic_deck == 'Lower') & deck_changed else [diff_stochastic_deck]
        all_deck_values = \
            hist_price_deck_value + \
            candlestick_deck_value + \
            drawdowns_deck_value + \
            volume_deck_value + \
            dollar_volume_deck_value + \
            obv_deck_value + \
            bollinger_deck_value + \
            boll_width_deck_value + \
            ma_env_deck_value + \
            ma_ribbon_deck_value + \
            price_overlays_deck_value + \
            macd_deck_value + \
            impulse_macd_deck_value + \
            atr_deck_value + \
            mvol_deck_value + \
            ulcer_deck_value + \
            rsi_deck_value + \
            stochastic_deck_value + \
            diff_1_deck_value + \
            diff_2_deck_value + \
            diff_3_deck_value + \
            diff_stochastic_deck_value
        return tuple([False]) + tuple([k for k in [['Upper', 'Middle', 'Lower']] * n]) + tuple(all_deck_values)


@callback(
    Output('collapse-button-general-tab', 'children'),
    Output('collapse-general-tab', 'is_open'),
    Input('collapse-button-general-tab', 'n_clicks'),
    State('collapse-general-tab', 'is_open')
)
def toggle_collapse_general_tab(n, is_open):
    title = 'GENERAL SETTINGS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-prices-tab', 'children'),
    Output('collapse-prices-tab', 'is_open'),
    Input('collapse-button-prices-tab', 'n_clicks'),
    State('collapse-prices-tab', 'is_open')
)
def toggle_collapse_prices_tab(n, is_open):
    title = 'PRICE PLOTS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-volume-tab', 'children'),
    Output('collapse-volume-tab', 'is_open'),
    Input('collapse-button-volume-tab', 'n_clicks'),
    State('collapse-volume-tab', 'is_open')
)
def toggle_collapse_volume_tab(n, is_open):
    title = 'VOLUME PLOTS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-trend-tab', 'children'),
    Output('collapse-trend-tab', 'is_open'),
    Input('collapse-button-trend-tab', 'n_clicks'),
    State('collapse-trend-tab', 'is_open')
)
def toggle_collapse_trend_tab(n, is_open):
    title = 'TREND INDICATOR PLOTS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-differential-tab', 'children'),
    Output('collapse-differential-tab', 'is_open'),
    Input('collapse-button-differential-tab', 'n_clicks'),
    State('collapse-differential-tab', 'is_open')
)
def toggle_collapse_differential_tab(n, is_open):
    title = 'DIFFERENTIAL PLOTS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-volatility-tab', 'children'),
    Output('collapse-volatility-tab', 'is_open'),
    Input('collapse-button-volatility-tab', 'n_clicks'),
    State('collapse-volatility-tab', 'is_open')
)
def toggle_collapse_volatility_tab(n, is_open):
    title = 'VOLATILITY INDICATOR PLOTS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-momentum-tab', 'children'),
    Output('collapse-momentum-tab', 'is_open'),
    Input('collapse-button-momentum-tab', 'n_clicks'),
    State('collapse-momentum-tab', 'is_open')
)
def toggle_collapse_momentum_tab(n, is_open):
    title = 'MOMENTUM INDICATOR PLOTS'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


##########################################################

@callback(
    Output('collapse-button-hist-price', 'children'),
    Output('collapse-hist-price', 'is_open'),
    Input('collapse-button-hist-price', 'n_clicks'),
    State('collapse-hist-price', 'is_open')
)
def toggle_collapse_hist_price(n, is_open):
    title = 'PRICE'
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
    Output('collapse-button-dollar-volume', 'children'),
    Output('collapse-dollar-volume', 'is_open'),
    Input('collapse-button-dollar-volume', 'n_clicks'),
    State('collapse-dollar-volume', 'is_open')
)
def toggle_collapse_dollar_volume(n, is_open):
    title = 'DOLLAR VOLUME'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-obv', 'children'),
    Output('collapse-obv', 'is_open'),
    Input('collapse-button-obv', 'n_clicks'),
    State('collapse-obv', 'is_open')
)
def toggle_collapse_obv(n, is_open):
    title = 'ON-BALANCE VOLUME'
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
    Output('collapse-button-boll-width', 'children'),
    Output('collapse-boll-width', 'is_open'),
    Input('collapse-button-boll-width', 'n_clicks'),
    State('collapse-boll-width', 'is_open')
)
def toggle_collapse_boll_width(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'BOLLINGER BANDWIDTH / %B'
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
    Output('collapse-button-macd', 'children'),
    Output('collapse-macd', 'is_open'),
    Input('collapse-button-macd', 'n_clicks'),
    State('collapse-macd', 'is_open')
)
def toggle_collapse_macd(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'MACD / MACD-V'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-impulse-macd', 'children'),
    Output('collapse-impulse-macd', 'is_open'),
    Input('collapse-button-impulse-macd', 'n_clicks'),
    State('collapse-impulse-macd', 'is_open')
)
def toggle_collapse_impulse_macd(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'IMPULSE MACD'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-diff-1', 'children'),
    Output('collapse-diff-1', 'is_open'),
    Input('collapse-button-diff-1', 'n_clicks'),
    State('collapse-diff-1', 'is_open')
)
def toggle_collapse_diff_1(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'DIFFERENTIAL No. 1'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-diff-2', 'children'),
    Output('collapse-diff-2', 'is_open'),
    Input('collapse-button-diff-2', 'n_clicks'),
    State('collapse-diff-2', 'is_open')
)
def toggle_collapse_diff_2(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'DIFFERENTIAL No. 2'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-diff-3', 'children'),
    Output('collapse-diff-3', 'is_open'),
    Input('collapse-button-diff-3', 'n_clicks'),
    State('collapse-diff-3', 'is_open')
)
def toggle_collapse_diff_3(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'DIFFERENTIAL No. 3'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-diff-stochastic', 'children'),
    Output('collapse-diff-stochastic', 'is_open'),
    Input('collapse-button-diff-stochastic', 'n_clicks'),
    State('collapse-diff-stochastic', 'is_open')
)
def toggle_collapse_diff_stochastic(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'STOCHASTIC DIFFERENTIAL'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


# @callback(
#     Output('collapse-button-diff', 'children'),
#     Output('collapse-diff', 'is_open'),
#     Input('collapse-button-diff', 'n_clicks'),
#     State('collapse-diff', 'is_open')
# )
# def toggle_collapse_diff(n, is_open):
#     # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
#     title = 'DIFFERENTIAL PLOT'
#     label = f'► {title}' if is_open else f'▼ {title}'
#     if n:
#         return label, not is_open
#     else:
#         return f'► {title}', is_open


@callback(
    Output('collapse-button-atr', 'children'),
    Output('collapse-atr', 'is_open'),
    Input('collapse-button-atr', 'n_clicks'),
    State('collapse-atr', 'is_open')
)
def toggle_collapse_atr(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'AVERAGE TRUE RATE'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-mvol', 'children'),
    Output('collapse-mvol', 'is_open'),
    Input('collapse-button-mvol', 'n_clicks'),
    State('collapse-mvol', 'is_open')
)
def toggle_collapse_mvol(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'MOVING VOLATILITY'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-ulcer', 'children'),
    Output('collapse-ulcer', 'is_open'),
    Input('collapse-button-ulcer', 'n_clicks'),
    State('collapse-ulcer', 'is_open')
)
def toggle_collapse_ulcer(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'ULCER INDEX'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-rsi', 'children'),
    Output('collapse-rsi', 'is_open'),
    Input('collapse-button-rsi', 'n_clicks'),
    State('collapse-rsi', 'is_open')
)
def toggle_collapse_rsi(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'RELATIVE STRENGTH INDEX'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(
    Output('collapse-button-stochastic', 'children'),
    Output('collapse-stochastic', 'is_open'),
    Input('collapse-button-stochastic', 'n_clicks'),
    State('collapse-stochastic', 'is_open')
)
def toggle_collapse_stochastic(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'STOCHASTIC OSCILLATOR'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


@callback(

    Output('fig-div-container', 'children'),

    # Add To Plot buttons
    Output('add-hist-price-button', 'n_clicks'),
    Output('add-candlestick-button', 'n_clicks'),
    Output('add-volume-button', 'n_clicks'),
    Output('add-dollar-volume-button', 'n_clicks'),
    Output('add-obv-button', 'n_clicks'),
    Output('add-drawdowns-button', 'n_clicks'),
    Output('add-price-overlays-button', 'n_clicks'),
    Output('add-bollinger-button', 'n_clicks'),
    Output('add-boll-width-button', 'n_clicks'),
    Output('add-ma-env-button', 'n_clicks'),
    Output('add-ma-ribbon-button', 'n_clicks'),
    Output('add-macd-button', 'n_clicks'),
    Output('add-impulse-macd-button', 'n_clicks'),    
    Output('add-atr-button', 'n_clicks'),
    Output('add-mvol-button', 'n_clicks'),
    Output('add-ulcer-button', 'n_clicks'),
    Output('add-rsi-button', 'n_clicks'),
    Output('add-stochastic-button', 'n_clicks'),
    Output('add-diff-1-button', 'n_clicks'),
    Output('add-diff-2-button', 'n_clicks'),
    Output('add-diff-3-button', 'n_clicks'),
    Output('add-diff-stochastic-button', 'n_clicks'),
    
    # Remove From Plot buttons
    Output('remove-hist-price-button', 'n_clicks'),
    Output('remove-candlestick-button', 'n_clicks'),
    Output('remove-volume-button', 'n_clicks'),
    Output('remove-dollar-volume-button', 'n_clicks'),
    Output('remove-obv-button', 'n_clicks'),    
    Output('remove-drawdowns-button', 'n_clicks'),
    Output('remove-price-overlays-button', 'n_clicks'),
    Output('remove-bollinger-button', 'n_clicks'),
    Output('remove-boll-width-button', 'n_clicks'),
    Output('remove-ma-env-button', 'n_clicks'),
    Output('remove-ma-ribbon-button', 'n_clicks'),
    Output('remove-macd-button', 'n_clicks'),
    Output('remove-impulse-macd-button', 'n_clicks'),    
    Output('remove-atr-button', 'n_clicks'),
    Output('remove-mvol-button', 'n_clicks'),
    Output('remove-ulcer-button', 'n_clicks'),
    Output('remove-rsi-button', 'n_clicks'),
    Output('remove-stochastic-button', 'n_clicks'),
    Output('remove-diff-1-button', 'n_clicks'),
    Output('remove-diff-2-button', 'n_clicks'),
    Output('remove-diff-3-button', 'n_clicks'),
    Output('remove-diff-stochastic-button', 'n_clicks'),

    # Added To plot Indicators
    Output('added-to-plot-indicator-prices-tab', 'style'),
    Output('added-to-plot-indicator-volume-tab', 'style'),
    Output('added-to-plot-indicator-trend-tab', 'style'),
    Output('added-to-plot-indicator-differential-tab', 'style'),
    Output('added-to-plot-indicator-volatility-tab', 'style'),
    Output('added-to-plot-indicator-momentum-tab', 'style'),

    Output('added-to-plot-indicator-hist-price', 'style'),
    Output('added-to-plot-indicator-candlestick', 'style'),
    Output('added-to-plot-indicator-volume', 'style'),
    Output('added-to-plot-indicator-dollar-volume', 'style'),
    Output('added-to-plot-indicator-obv', 'style'),    
    Output('added-to-plot-indicator-drawdowns', 'style'),
    Output('added-to-plot-indicator-price-overlays', 'style'),
    Output('added-to-plot-indicator-bollinger', 'style'),
    Output('added-to-plot-indicator-boll-width', 'style'),
    Output('added-to-plot-indicator-ma-env', 'style'),
    Output('added-to-plot-indicator-ma-ribbon', 'style'),
    Output('added-to-plot-indicator-macd', 'style'),
    Output('added-to-plot-indicator-impulse-macd', 'style'),
    Output('added-to-plot-indicator-atr', 'style'),
    Output('added-to-plot-indicator-mvol', 'style'),
    Output('added-to-plot-indicator-ulcer', 'style'),
    Output('added-to-plot-indicator-rsi', 'style'),
    Output('added-to-plot-indicator-stochastic', 'style'),
    Output('added-to-plot-indicator-diff-1', 'style'),
    Output('added-to-plot-indicator-diff-2', 'style'),
    Output('added-to-plot-indicator-diff-3', 'style'),
    Output('added-to-plot-indicator-diff-stochastic', 'style'),

    #
    Output('macd-signal-window-input', 'disabled'),
    Output('macd-signal-color-theme-dropdown', 'disabled'),
    Output('impulse-macd-signal-window-input', 'disabled'),
    Output('impulse-macd-signal-color-theme-dropdown', 'disabled'),
    Output('rsi-overbought-level-input', 'disabled'),
    Output('rsi-oversold-level-input', 'disabled'),
    Output('stochastic-overbought-level-input', 'disabled'),
    Output('stochastic-oversold-level-input', 'disabled'),

    Output('diff-1-signal-ma-type-dropdown', 'disabled'),
    Output('diff-1-signal-window-input', 'disabled'),
    Output('diff-1-signal-color-theme-dropdown', 'disabled'),
    Output('diff-1-signal-line-row-2-container', 'hidden'),
    Output('diff-1-line-1-ma-options', 'hidden'),
    Output('diff-1-line-2-ma-options', 'hidden'),
    Output('diff-2-signal-ma-type-dropdown', 'disabled'),
    Output('diff-2-signal-window-input', 'disabled'),
    Output('diff-2-signal-color-theme-dropdown', 'disabled'),
    Output('diff-2-signal-line-row-2-container', 'hidden'),
    Output('diff-2-line-1-ma-options', 'hidden'),
    Output('diff-2-line-2-ma-options', 'hidden'),
    Output('diff-3-signal-ma-type-dropdown', 'disabled'),
    Output('diff-3-signal-window-input', 'disabled'),
    Output('diff-3-signal-color-theme-dropdown', 'disabled'),
    Output('diff-3-signal-line-row-2-container', 'hidden'),
    Output('diff-3-line-1-ma-options', 'hidden'),
    Output('diff-3-line-2-ma-options', 'hidden'),

    Output('diff-stochastic-signal-ma-type-dropdown', 'disabled'),
    Output('diff-stochastic-signal-window-input', 'disabled'),
    Output('diff-stochastic-signal-color-theme-dropdown', 'disabled'),
    Output('diff-stochastic-signal-line-row-2-container', 'hidden'),

    Output('stochastic-k-smoothing-period-input', 'disabled'),
    Output('stochastic-type-dropdown', 'value'),
    Output('diff-stochastic-k-smoothing-period-input', 'disabled'),
    Output('diff-stochastic-type-dropdown', 'value'),

    Output('drawdowns-number-input', 'max'),
    Output('drawdowns-number-input', 'value'),
    Output('drawdowns-price-color-dropdown', 'disabled'),

    Output('plots-start-date-input-dmc', 'value'),
    Output('plots-end-date-input-dmc', 'value'),
    Output('plots-start-date-input-dmc', 'minDate'),
    Output('plots-start-date-input-dmc', 'maxDate'),
    Output('plots-end-date-input-dmc', 'minDate'),
    Output('plots-end-date-input-dmc', 'maxDate'),

    # Secondary y disabled outputs
    Output('hist-price-secondary-y-dropdown', 'disabled'),
    Output('volume-secondary-y-dropdown', 'disabled'),
    Output('dollar-volume-secondary-y-dropdown', 'disabled'),
    Output('obv-secondary-y-dropdown', 'disabled'),
    Output('atr-secondary-y-dropdown', 'disabled'),
    Output('boll-width-secondary-y-dropdown', 'disabled'),
    Output('mvol-secondary-y-dropdown', 'disabled'),
    Output('ulcer-secondary-y-dropdown', 'disabled'),
    Output('macd-add-price-dropdown', 'disabled'),
    Output('macd-price-color-theme-dropdown', 'disabled'),
    Output('impulse-macd-add-price-dropdown', 'disabled'),
    Output('impulse-macd-price-color-theme-dropdown', 'disabled'),
    Output('rsi-add-price-dropdown', 'disabled'),
    Output('rsi-price-color-theme-dropdown', 'disabled'),
    Output('stochastic-add-price-dropdown', 'disabled'),
    Output('stochastic-price-color-theme-dropdown', 'disabled'),
    Output('diff-1-add-price-dropdown', 'disabled'),
    Output('diff-1-price-color-theme-dropdown', 'disabled'),
    Output('diff-2-add-price-dropdown', 'disabled'),
    Output('diff-2-price-color-theme-dropdown', 'disabled'),
    Output('diff-3-add-price-dropdown', 'disabled'),
    Output('diff-3-price-color-theme-dropdown', 'disabled'),
    Output('diff-stochastic-add-line-dropdown', 'disabled'),
    Output('diff-stochastic-added-line-type-dropdown', 'disabled'),
    Output('diff-stochastic-added-line-color-theme-dropdown', 'disabled'),

    ##### Inputs

    Input('final-start-date-stored', 'data'),
    Input('final-end-date-stored', 'data'),
    Input('final-selected-tickers-stored', 'data'),
    
    Input({'index': ALL, 'type': 'reset-axes'}, 'n_clicks'),

    # Tickers inputs
    ### Input('tickers-dropdown', 'value'),
    Input('dash-table-tickers-to-plot', 'selected_rows'),

    Input('plots-start-date-input-dmc', 'value'),
    Input('plots-end-date-input-dmc', 'value'),

    # Theme & Template inputs
    Input('theme-dropdown', 'value'),
    Input('deck-type-dropdown', 'value'),
    Input('secondary-y-dropdown', 'value'),
    Input('width-input', 'value'),
    Input('upper-height-input', 'value'),
    Input('lower-height-input', 'value'),

    # Historical Price inputs
    Input('hist-price-deck-dropdown', 'value'),
    Input('hist-price-type-dropdown', 'value'),
    Input('hist-price-adjusted-dropdown', 'value'),
    Input('hist-price-secondary-y-dropdown', 'value'),
    Input('hist-price-plot-type-dropdown', 'value'),
    Input('hist-price-fill-below-dropdown', 'value'),
    Input('hist-price-color-theme-dropdown', 'value'),
    Input('hist-price-add-title-dropdown', 'value'),
    Input('add-hist-price-button', 'n_clicks'),
    Input('remove-hist-price-button', 'n_clicks'),

    # Candlestick inputs
    Input('candlestick-deck-dropdown', 'value'),
    Input('candlestick-adjusted-dropdown', 'value'),
    Input('candlestick-type-dropdown', 'value'),
    Input('candlestick-color-theme-dropdown', 'value'),
    Input('candlestick-add-title-dropdown', 'value'),
    Input('candlestick-add-yaxis-title-dropdown', 'value'),
    Input('add-candlestick-button', 'n_clicks'),
    Input('remove-candlestick-button', 'n_clicks'),    

    # Volume inputs
    Input('volume-deck-dropdown', 'value'),
    Input('volume-secondary-y-dropdown', 'value'),
    Input('volume-plot-type-dropdown', 'value'),
    Input('volume-fill-below-dropdown', 'value'),
    Input('volume-color-theme-dropdown', 'value'),
    Input('volume-add-title-dropdown', 'value'),
    Input('add-volume-button', 'n_clicks'),
    Input('remove-volume-button', 'n_clicks'),

    # Dollar Volume inputs
    Input('dollar-volume-deck-dropdown', 'value'),
    Input('dollar-volume-adjusted-dropdown', 'value'),
    Input('dollar-volume-secondary-y-dropdown', 'value'),
    Input('dollar-volume-plot-type-dropdown', 'value'),
    Input('dollar-volume-fill-below-dropdown', 'value'),
    Input('dollar-volume-color-theme-dropdown', 'value'),
    Input('dollar-volume-add-title-dropdown', 'value'),
    Input('add-dollar-volume-button', 'n_clicks'),
    Input('remove-dollar-volume-button', 'n_clicks'),

    # On-Balance Volume inputs
    Input('obv-deck-dropdown', 'value'),
    Input('obv-adjusted-dropdown', 'value'),
    Input('obv-secondary-y-dropdown', 'value'),
    Input('obv-plot-type-dropdown', 'value'),
    Input('obv-fill-below-dropdown', 'value'),
    Input('obv-color-theme-dropdown', 'value'),
    Input('obv-add-title-dropdown', 'value'),
    Input('add-obv-button', 'n_clicks'),
    Input('remove-obv-button', 'n_clicks'),

    # Drawdowns inputs
    Input('drawdowns-number-input', 'value'),
    Input('drawdowns-deck-dropdown', 'value'),
    Input('drawdowns-topby-dropdown', 'value'),
    Input('drawdowns-display-dropdown', 'value'),
    Input('drawdowns-adjusted-dropdown', 'value'),
    Input('drawdowns-price-type-dropdown', 'value'),
    Input('drawdowns-color-dropdown', 'value'),
    Input('drawdowns-price-color-dropdown', 'value'),
    Input('drawdowns-add-price-dropdown', 'value'),
    Input('drawdowns-add-title-dropdown', 'value'),
    Input('add-drawdowns-button', 'n_clicks'),
    Input('remove-drawdowns-button', 'n_clicks'),

    # Price Overlay options
    Input('price-overlays-deck-dropdown', 'value'),
    Input('price-overlays-adj-price-list', 'value'),    
    Input('price-overlays-price-list', 'value'),
    Input('price-overlays-add-yaxis-title-dropdown', 'value'),
    Input('price-overlays-color-theme-dropdown', 'value'),
    Input('add-price-overlays-button', 'n_clicks'),
    Input('remove-price-overlays-button', 'n_clicks'),

    # Bollinger Bands inputs
    Input('bollinger-deck-dropdown', 'value'),
    Input('bollinger-adjusted-dropdown', 'value'),
    Input('bollinger-price-type-dropdown', 'value'),
    Input('bollinger-ma-type-dropdown', 'value'),
    Input('bollinger-window-input', 'value'),
    Input('bollinger-nstd-input', 'value'),
    Input('bollinger-nbands-input', 'value'),
    Input('bollinger-color-theme-dropdown', 'value'),
    Input('add-bollinger-button', 'n_clicks'),
    Input('remove-bollinger-button', 'n_clicks'),

    # Bollinger Width inputs
    Input('boll-width-deck-dropdown', 'value'),
    Input('boll-width-adjusted-dropdown', 'value'),
    Input('boll-width-price-type-dropdown', 'value'),
    Input('boll-width-type-dropdown', 'value'),    
    Input('boll-width-ma-type-dropdown', 'value'),
    Input('boll-width-window-input', 'value'),
    Input('boll-width-nstd-input', 'value'),
    Input('boll-width-secondary-y-dropdown', 'value'),
    Input('boll-width-add-yaxis-title-dropdown', 'value'),
    Input('boll-width-color-theme-dropdown', 'value'),
    Input('add-boll-width-button', 'n_clicks'),
    Input('remove-boll-width-button', 'n_clicks'),

    # MA Envelopes inputs
    Input('ma-env-deck-dropdown', 'value'),
    Input('ma-env-adjusted-dropdown', 'value'),
    Input('ma-env-price-type-dropdown', 'value'),
    Input('ma-env-ma-type-dropdown', 'value'),
    Input('ma-env-window-input', 'value'),
    Input('ma-env-offset-input', 'value'),
    Input('ma-env-nbands-input', 'value'),
    Input('ma-env-color-theme-dropdown', 'value'),
    Input('add-ma-env-button', 'n_clicks'),
    Input('remove-ma-env-button', 'n_clicks'),
   
    # MA Ribbon inputs
    Input('ma-ribbon-deck-dropdown', 'value'),
    Input('ma-ribbon-adjusted-dropdown', 'value'),
    Input('ma-ribbon-price-type-dropdown', 'value'),
    Input('ma-ribbon-ma-type-dropdown', 'value'),
    Input('ma-ribbon-window-input', 'value'),
    Input('ma-ribbon-nbands-input', 'value'),
    Input('ma-ribbon-add-yaxis-title-dropdown', 'value'),
    Input('ma-ribbon-color-theme-dropdown', 'value'),
    Input('add-ma-ribbon-button', 'n_clicks'),
    Input('remove-ma-ribbon-button', 'n_clicks'),

    # MACD inputs
    Input('macd-deck-dropdown', 'value'),
    Input('macd-adjusted-dropdown', 'value'),
    Input('macd-add-price-dropdown', 'value'),
    Input('macd-add-signal-dropdown', 'value'),
    Input('macd-signal-window-input', 'value'),
    Input('macd-plot-type-dropdown', 'value'),
    Input('macd-histogram-type-dropdown', 'value'),
    Input('macd-vol-normalized-dropdown', 'value'),
    Input('macd-add-title-dropdown', 'value'),    
    Input('macd-color-theme-dropdown', 'value'),
    Input('macd-signal-color-theme-dropdown', 'value'),
    Input('macd-price-color-theme-dropdown', 'value'),
    Input('add-macd-button', 'n_clicks'),
    Input('remove-macd-button', 'n_clicks'),

    # Impulse MACD inputs
    Input('impulse-macd-deck-dropdown', 'value'),
    Input('impulse-macd-adjusted-dropdown', 'value'),
    Input('impulse-macd-add-price-dropdown', 'value'),
    Input('impulse-macd-smma-window-input', 'value'),    
    Input('impulse-macd-add-signal-dropdown', 'value'),
    Input('impulse-macd-signal-window-input', 'value'),
    Input('impulse-macd-plot-type-dropdown', 'value'),
    Input('impulse-macd-histogram-type-dropdown', 'value'),
    Input('impulse-macd-add-title-dropdown', 'value'),    
    Input('impulse-macd-color-theme-dropdown', 'value'),
    Input('impulse-macd-signal-color-theme-dropdown', 'value'),
    Input('impulse-macd-price-color-theme-dropdown', 'value'),
    Input('add-impulse-macd-button', 'n_clicks'),
    Input('remove-impulse-macd-button', 'n_clicks'),

    # Differential 1 inputs
    Input('diff-1-deck-dropdown', 'value'),
    Input('diff-1-plot-type-dropdown', 'value'),
    Input('diff-1-add-title-dropdown', 'value'),    
    Input('diff-1-color-theme-dropdown', 'value'),
    Input('diff-1-add-price-dropdown', 'value'),
    Input('diff-1-price-color-theme-dropdown', 'value'),
    Input('diff-1-add-signal-dropdown', 'value'),
    Input('diff-1-signal-ma-type-dropdown', 'value'),
    Input('diff-1-signal-window-input', 'value'),
    Input('diff-1-signal-color-theme-dropdown', 'value'),
    Input('diff-1-line-1-line-type-dropdown', 'value'),
    Input('diff-1-line-1-price-type-dropdown', 'value'),
    Input('diff-1-line-1-adjusted-dropdown', 'value'),
    Input('diff-1-line-1-ma-type-dropdown', 'value'),
    Input('diff-1-line-1-window-input', 'value'),
    Input('diff-1-line-2-line-type-dropdown', 'value'),
    Input('diff-1-line-2-price-type-dropdown', 'value'), 
    Input('diff-1-line-2-adjusted-dropdown', 'value'),
    Input('diff-1-line-2-ma-type-dropdown', 'value'),
    Input('diff-1-line-2-window-input', 'value'),
    Input('add-diff-1-button', 'n_clicks'),
    Input('remove-diff-1-button', 'n_clicks'),

    # Differential 2 inputs
    Input('diff-2-deck-dropdown', 'value'),
    Input('diff-2-plot-type-dropdown', 'value'),
    Input('diff-2-add-title-dropdown', 'value'),    
    Input('diff-2-color-theme-dropdown', 'value'),
    Input('diff-2-add-price-dropdown', 'value'),
    Input('diff-2-price-color-theme-dropdown', 'value'),
    Input('diff-2-add-signal-dropdown', 'value'),
    Input('diff-2-signal-ma-type-dropdown', 'value'),
    Input('diff-2-signal-window-input', 'value'),
    Input('diff-2-signal-color-theme-dropdown', 'value'),
    Input('diff-2-line-1-line-type-dropdown', 'value'),
    Input('diff-2-line-1-price-type-dropdown', 'value'),
    Input('diff-2-line-1-adjusted-dropdown', 'value'),
    Input('diff-2-line-1-ma-type-dropdown', 'value'),
    Input('diff-2-line-1-window-input', 'value'),
    Input('diff-2-line-2-line-type-dropdown', 'value'),
    Input('diff-2-line-2-price-type-dropdown', 'value'), 
    Input('diff-2-line-2-adjusted-dropdown', 'value'),
    Input('diff-2-line-2-ma-type-dropdown', 'value'),
    Input('diff-2-line-2-window-input', 'value'),
    Input('add-diff-2-button', 'n_clicks'),
    Input('remove-diff-2-button', 'n_clicks'),

    # Differential 3 inputs
    Input('diff-3-deck-dropdown', 'value'),
    Input('diff-3-plot-type-dropdown', 'value'),
    Input('diff-3-add-title-dropdown', 'value'),    
    Input('diff-3-color-theme-dropdown', 'value'),
    Input('diff-3-add-price-dropdown', 'value'),
    Input('diff-3-price-color-theme-dropdown', 'value'),
    Input('diff-3-add-signal-dropdown', 'value'),
    Input('diff-3-signal-ma-type-dropdown', 'value'),
    Input('diff-3-signal-window-input', 'value'),
    Input('diff-3-signal-color-theme-dropdown', 'value'),
    Input('diff-3-line-1-line-type-dropdown', 'value'),
    Input('diff-3-line-1-price-type-dropdown', 'value'),
    Input('diff-3-line-1-adjusted-dropdown', 'value'),
    Input('diff-3-line-1-ma-type-dropdown', 'value'),
    Input('diff-3-line-1-window-input', 'value'),
    Input('diff-3-line-2-line-type-dropdown', 'value'),
    Input('diff-3-line-2-price-type-dropdown', 'value'), 
    Input('diff-3-line-2-adjusted-dropdown', 'value'),
    Input('diff-3-line-2-ma-type-dropdown', 'value'),
    Input('diff-3-line-2-window-input', 'value'),
    Input('add-diff-3-button', 'n_clicks'),
    Input('remove-diff-3-button', 'n_clicks'),

    # Average True Rate inputs
    Input('atr-deck-dropdown', 'value'),
    Input('atr-adjusted-dropdown', 'value'),
    Input('atr-periods-input', 'value'),
    Input('atr-type-dropdown', 'value'),
    Input('atr-secondary-y-dropdown', 'value'),
    Input('atr-add-yaxis-title-dropdown', 'value'),
    Input('atr-color-theme-dropdown', 'value'),
    Input('add-atr-button', 'n_clicks'),
    Input('remove-atr-button', 'n_clicks'),

    # MVol / MStDev inputs
    Input('mvol-deck-dropdown', 'value'),
    Input('mvol-price-type-dropdown', 'value'),
    Input('mvol-adjusted-dropdown', 'value'),
    Input('mvol-type-dropdown', 'value'),
    Input('mvol-ma-type-dropdown', 'value'),
    Input('mvol-window-input', 'value'),
    Input('mvol-secondary-y-dropdown', 'value'),
    Input('mvol-add-yaxis-title-dropdown', 'value'),
    Input('mvol-color-theme-dropdown', 'value'),
    Input('add-mvol-button', 'n_clicks'),
    Input('remove-mvol-button', 'n_clicks'),

    # Ulcer Index inputs
    Input('ulcer-deck-dropdown', 'value'),
    Input('ulcer-price-type-dropdown', 'value'),
    Input('ulcer-adjusted-dropdown', 'value'),
    Input('ulcer-window-input', 'value'),
    Input('ulcer-secondary-y-dropdown', 'value'),
    Input('ulcer-add-yaxis-title-dropdown', 'value'),
    Input('ulcer-color-theme-dropdown', 'value'),
    Input('add-ulcer-button', 'n_clicks'),
    Input('remove-ulcer-button', 'n_clicks'),

   # MACD inputs
    Input('rsi-deck-dropdown', 'value'),
    Input('rsi-price-type-dropdown', 'value'),
    Input('rsi-add-title-dropdown', 'value'),
    Input('rsi-periods-input', 'value'),
    Input('rsi-add-overbought-oversold-dropdown', 'value'),
    Input('rsi-overbought-level-input', 'value'),
    Input('rsi-oversold-level-input', 'value'),
    Input('rsi-color-theme-dropdown', 'value'),
    Input('rsi-add-price-dropdown', 'value'),
    Input('rsi-price-color-theme-dropdown', 'value'),
    Input('add-rsi-button', 'n_clicks'),
    Input('remove-rsi-button', 'n_clicks'),

    Input('stochastic-deck-dropdown', 'value'),
    Input('stochastic-adjusted-dropdown', 'value'),
    Input('stochastic-add-title-dropdown', 'value'),
    Input('stochastic-type-dropdown', 'value'),
    Input('stochastic-fast-k-period-input', 'value'),
    Input('stochastic-k-smoothing-period-input', 'value'),
    Input('stochastic-d-period-input', 'value'),
    Input('stochastic-add-overbought-oversold-dropdown', 'value'),
    Input('stochastic-overbought-level-input', 'value'),
    Input('stochastic-oversold-level-input', 'value'),
    Input('stochastic-k-line-color-dropdown', 'value'),
    Input('stochastic-d-line-color-dropdown', 'value'),
    Input('stochastic-add-price-dropdown', 'value'),
    Input('stochastic-price-color-theme-dropdown', 'value'),
    Input('add-stochastic-button', 'n_clicks'),
    Input('remove-stochastic-button', 'n_clicks'),

    Input('diff-stochastic-deck-dropdown', 'value'),
    Input('diff-stochastic-plot-type-dropdown', 'value'),    
    Input('diff-stochastic-sign-dropdown', 'value'),
    Input('diff-stochastic-adjusted-dropdown', 'value'),
    Input('diff-stochastic-add-title-dropdown', 'value'),
    Input('diff-stochastic-color-theme-dropdown', 'value'),
    Input('diff-stochastic-type-dropdown', 'value'),
    Input('diff-stochastic-fast-k-period-input', 'value'),
    Input('diff-stochastic-k-smoothing-period-input', 'value'),
    Input('diff-stochastic-d-period-input', 'value'),
    Input('diff-stochastic-add-signal-dropdown', 'value'),
    Input('diff-stochastic-signal-ma-type-dropdown', 'value'),
    Input('diff-stochastic-signal-window-input', 'value'),
    Input('diff-stochastic-signal-color-theme-dropdown', 'value'),
    Input('diff-stochastic-add-line-dropdown', 'value'),
    Input('diff-stochastic-added-line-type-dropdown', 'value'),    
    Input('diff-stochastic-added-line-color-theme-dropdown', 'value'),
    Input('add-diff-stochastic-button', 'n_clicks'),
    Input('remove-diff-stochastic-button', 'n_clicks')

)

def update_plot(

        start_date,
        end_date,
        selected_tickers_names,

        n_click_reset_axes,

        # tickers
        selected_rows_tickers_to_plot,

        # dates
        new_start_date,
        new_end_date,

        # template parameters
        theme,
        deck_type,
        sec_y,
        width,
        upper_height,
        lower_height,

        hist_price_deck_name,
        hist_price_type,
        hist_price_adjusted,
        hist_price_secondary_y,
        hist_price_plot_type,
        hist_price_fill_below,
        hist_price_color_theme,
        hist_price_add_title,
        add_hist_price,
        remove_hist_price,

        candlestick_deck_name,
        candlestick_adjusted,
        candlestick_type,
        candlestick_color_theme,
        candlestick_add_title,
        candlestick_add_yaxis_title,
        add_candlestick,
        remove_candlestick,

        volume_deck_name,
        volume_secondary_y,
        volume_plot_type,
        volume_fill_below,
        volume_color_theme,
        volume_add_title,
        add_volume,
        remove_volume,

        dollar_volume_deck_name,
        dollar_volume_adjusted,
        dollar_volume_secondary_y,
        dollar_volume_plot_type,
        dollar_volume_fill_below,
        dollar_volume_color_theme,
        dollar_volume_add_title,
        add_dollar_volume,
        remove_dollar_volume,

        obv_deck_name,
        obv_adjusted,
        obv_secondary_y,
        obv_plot_type,
        obv_fill_below,
        obv_color_theme,
        obv_add_title,
        add_obv,
        remove_obv,

        n_top, 
        drawdowns_deck,
        drawdowns_top_by, 
        drawdowns_display,
        drawdowns_adjusted,
        drawdowns_price_type,
        drawdowns_color, 
        drawdowns_price_color_theme,
        drawdowns_add_price,
        drawdowns_add_title,
        add_drawdowns,
        remove_drawdowns,

        price_overlay_deck_name,
        price_overlay_adj_price_list,
        price_overlay_price_list,
        price_overlay_add_yaxis_title,
        price_overlay_color_theme,
        add_price_overlays,
        remove_price_overlays,

        bollinger_deck_name,
        bollinger_adjusted,
        bollinger_price_type,
        bollinger_ma_type,
        bollinger_window,
        bollinger_nstd,
        bollinger_nbands,
        bollinger_color_theme,
        add_bollinger,
        remove_bollinger,

        boll_width_deck,
        boll_width_adjusted,
        boll_width_price_type,
        boll_width_type,
        boll_width_ma_type,
        boll_width_window,
        boll_width_nstd,
        boll_width_secondary_y,
        boll_width_add_yaxis_title,
        boll_width_color_theme,
        add_boll_width,
        remove_boll_width,

        ma_env_deck_name,
        ma_env_adjusted,
        ma_env_price_type,
        ma_env_ma_type,
        ma_env_window,
        ma_env_offset,
        ma_env_nbands,
        ma_env_color_theme,
        add_ma_env,
        remove_ma_env,

        ma_ribbon_deck_name,
        ma_ribbon_adjusted,
        ma_ribbon_price_type,
        ma_ribbon_ma_type,
        ma_ribbon_window,
        ma_ribbon_nbands,
        ma_ribbon_add_yaxis_title,
        ma_ribbon_color_theme,
        add_ma_ribbon,
        remove_ma_ribbon,

        macd_deck,
        macd_adjusted,
        macd_add_price,
        macd_add_signal,
        macd_signal_window,
        macd_plot_type,
        macd_histogram_type,
        macd_vol_normalized,
        macd_add_title,
        macd_color_theme,
        macd_signal_color,
        macd_price_color,
        add_macd,
        remove_macd,

        impulse_macd_deck,
        impulse_macd_adjusted,
        impulse_macd_add_price,
        impulse_macd_smma_window,
        impulse_macd_add_signal,
        impulse_macd_signal_window,
        impulse_macd_plot_type,
        impulse_macd_histogram_type,
        impulse_macd_add_title,
        impulse_macd_color_theme,
        impulse_macd_signal_color,
        impulse_macd_price_color,
        add_impulse_macd,
        remove_impulse_macd,

        diff_1_deck,
        diff_1_plot_type,
        diff_1_add_title,
        diff_1_color_theme,
        diff_1_add_price,
        diff_1_price_color,
        diff_1_add_signal,
        diff_1_signal_ma_type,
        diff_1_signal_window,
        diff_1_signal_color,
        diff_1_line_1_line_type,
        diff_1_line_1_price_type,
        diff_1_line_1_adjusted,
        diff_1_line_1_ma_type,
        diff_1_line_1_window,
        diff_1_line_2_line_type,
        diff_1_line_2_price_type,
        diff_1_line_2_adjusted,
        diff_1_line_2_ma_type,
        diff_1_line_2_window,
        add_diff_1,
        remove_diff_1,

        diff_2_deck,
        diff_2_plot_type,
        diff_2_add_title,
        diff_2_color_theme,
        diff_2_add_price,
        diff_2_price_color,
        diff_2_add_signal,
        diff_2_signal_ma_type,
        diff_2_signal_window,
        diff_2_signal_color,
        diff_2_line_1_line_type,
        diff_2_line_1_price_type,
        diff_2_line_1_adjusted,
        diff_2_line_1_ma_type,
        diff_2_line_1_window,
        diff_2_line_2_line_type,
        diff_2_line_2_price_type,
        diff_2_line_2_adjusted,
        diff_2_line_2_ma_type,
        diff_2_line_2_window,
        add_diff_2,
        remove_diff_2,

        diff_3_deck,
        diff_3_plot_type,
        diff_3_add_title,
        diff_3_color_theme,
        diff_3_add_price,
        diff_3_price_color,
        diff_3_add_signal,
        diff_3_signal_ma_type,
        diff_3_signal_window,
        diff_3_signal_color,
        diff_3_line_1_line_type,
        diff_3_line_1_price_type,
        diff_3_line_1_adjusted,
        diff_3_line_1_ma_type,
        diff_3_line_1_window,
        diff_3_line_2_line_type,
        diff_3_line_2_price_type,
        diff_3_line_2_adjusted,
        diff_3_line_2_ma_type,
        diff_3_line_2_window,
        add_diff_3,
        remove_diff_3,

        atr_deck,
        atr_adjusted,
        atr_periods,
        atr_type,
        atr_secondary_y,
        atr_add_yaxis_title,
        atr_color_theme,
        add_atr,
        remove_atr,

        mvol_deck,
        mvol_price_type,
        mvol_adjusted,
        mvol_type,
        mvol_ma_type,
        mvol_window,
        mvol_secondary_y,
        mvol_add_yaxis_title,
        mvol_color_theme,
        add_mvol,
        remove_mvol,

        ulcer_deck,
        ulcer_price_type,
        ulcer_adjusted,
        ulcer_window,
        ulcer_secondary_y,
        ulcer_add_yaxis_title,
        ulcer_color_theme,
        add_ulcer,
        remove_ulcer,

        rsi_deck,
        rsi_price_type,
        rsi_add_title,
        rsi_periods,
        rsi_add_overbought_oversold,
        rsi_overbought_level,
        rsi_oversold_level,
        rsi_color_theme,
        rsi_add_price,
        rsi_price_color_theme,
        add_rsi,
        remove_rsi,

        stochastic_deck,
        stochastic_adjusted,
        stochastic_add_title,
        stochastic_type,
        stochastic_fast_k_period,
        stochastic_k_smoothing_period,
        stochastic_d_period,
        stochastic_add_overbought_oversold,
        stochastic_overbought_level,
        stochastic_oversold_level,
        stochastic_k_line_color,
        stochastic_d_line_color,
        stochastic_add_price,
        stochastic_price_color_theme,
        add_stochastic,
        remove_stochastic,

        diff_stochastic_deck,
        diff_stochastic_plot_type,
        diff_stochastic_sign,
        diff_stochastic_adjusted,
        diff_stochastic_add_title,
        diff_stochastic_color_theme,
        diff_stochastic_type,
        diff_stochastic_fast_k_period,
        diff_stochastic_k_smoothing_period,
        diff_stochastic_d_period,
        diff_stochastic_add_signal,
        diff_stochastic_signal_ma_type,
        diff_stochastic_signal_window,
        diff_stochastic_signal_color,
        diff_stochastic_add_line,
        diff_stochastic_added_line_type,
        diff_stochastic_added_line_color_theme,
        add_diff_stochastic,
        remove_diff_stochastic

    ):

    selected_tickers = list(selected_tickers_names.keys())
    id_tk_map = {i: tk for i, tk in enumerate(selected_tickers)}

    # NOTE: start_date, end_date, new_start_date and new_end_date are all strings, converted to datetime using strptime()
    min_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    max_start_date = datetime.strptime(new_end_date, '%Y-%m-%d').date() if new_end_date is not None else datetime.strptime(end_date, '%Y-%m-%d').date()
    min_end_date = datetime.strptime(new_start_date, '%Y-%m-%d').date() if new_start_date is not None else datetime.strptime(start_date, '%Y-%m-%d').date()
    max_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    start_date_value = start_date if new_start_date is None else new_start_date
    end_date_value = end_date if new_end_date is None else new_end_date

    downloaded_data = hist_data.download_yf_data(start_date, end_date, selected_tickers)

    tickers_to_plot = [id_tk_map[i] for i in selected_rows_tickers_to_plot] if selected_rows_tickers_to_plot != [] else [id_tk_map[0]]

    # tk = tickers_to_plot[0]
    # date_index = downloaded_data[tk_0]['ohlc'][min_start_date: max_end_date].index

    theme = theme.lower()
    secondary_y = boolean(sec_y)

    # These are in the list of outputs, so they must stay outside of the if statements
    # -- should move these to after the plot is updated, so the '_disabled' parameters
    # could take into account the trace possibly present already on the secondary y-axis
    
    dd_add_price_disabled = not boolean(drawdowns_add_price)
    # Genaralizing to the case where multiple tickers are selected to plot
    max_top_drawdowns = 5 if n_top is None else n_top
    dd_number_value = max_top_drawdowns

    macd_signal_window_disabled = not boolean(macd_add_signal)
    macd_signal_color_disabled = not boolean(macd_add_signal)
    impulse_macd_signal_window_disabled = not boolean(impulse_macd_add_signal)
    impulse_macd_signal_color_disabled = not boolean(impulse_macd_add_signal)
    rsi_overbought_level_disabled = not boolean(rsi_add_overbought_oversold)
    rsi_oversold_level_disabled = not boolean(rsi_add_overbought_oversold)
    stochastic_overbought_level_disabled = not boolean(stochastic_add_overbought_oversold)
    stochastic_oversold_level_disabled = not boolean(stochastic_add_overbought_oversold)

    diff_1_signal_ma_type_disabled = not boolean(diff_1_add_signal)
    diff_1_signal_window_disabled = not boolean(diff_1_add_signal)
    diff_1_signal_color_disabled = not boolean(diff_1_add_signal)
    diff_1_signal_line_row_2_hidden = not boolean(diff_1_add_signal)
    diff_1_line_1_ma_options_hidden = True if diff_1_line_1_line_type == 'Price' else False
    diff_1_line_2_ma_options_hidden = True if diff_1_line_2_line_type == 'Price' else False
    diff_2_signal_ma_type_disabled = not boolean(diff_2_add_signal)
    diff_2_signal_window_disabled = not boolean(diff_2_add_signal)
    diff_2_signal_color_disabled = not boolean(diff_2_add_signal)
    diff_2_signal_line_row_2_hidden = not boolean(diff_2_add_signal)
    diff_2_line_1_ma_options_hidden = True if diff_2_line_1_line_type == 'Price' else False
    diff_2_line_2_ma_options_hidden = True if diff_2_line_2_line_type == 'Price' else False
    diff_3_signal_ma_type_disabled = not boolean(diff_3_add_signal)
    diff_3_signal_window_disabled = not boolean(diff_3_add_signal)
    diff_3_signal_color_disabled = not boolean(diff_3_add_signal)
    diff_3_signal_line_row_2_hidden = not boolean(diff_3_add_signal)
    diff_3_line_1_ma_options_hidden = True if diff_3_line_1_line_type == 'Price' else False
    diff_3_line_2_ma_options_hidden = True if diff_3_line_2_line_type == 'Price' else False

    diff_stochastic_signal_ma_type_disabled = not boolean(diff_stochastic_add_signal)
    diff_stochastic_signal_window_disabled = not boolean(diff_stochastic_add_signal)
    diff_stochastic_signal_color_disabled = not boolean(diff_stochastic_add_signal)
    diff_stochastic_signal_line_row_2_hidden = not boolean(diff_stochastic_add_signal)

    # Secondary y disabled outputs

    hist_price_sec_y_disabled = not secondary_y
    volume_sec_y_disabled = not secondary_y
    dollar_volume_sec_y_disabled = not secondary_y
    obv_sec_y_disabled = not secondary_y
    atr_sec_y_disabled = not secondary_y
    boll_width_sec_y_disabled = not secondary_y
    mvol_sec_y_disabled = not secondary_y
    ulcer_sec_y_disabled = not secondary_y

    macd_price_color_disabled = False if boolean(macd_add_price) & secondary_y else True
    if (macd_deck != 'Upper') | (not secondary_y):
        macd_add_price_disabled = True
        macd_price_color_disabled = True
    else:
        macd_add_price_disabled = False

    impulse_macd_price_color_disabled = False if boolean(impulse_macd_add_price) & secondary_y else True
    if (impulse_macd_deck != 'Upper') | (not secondary_y):
        impulse_macd_add_price_disabled = True
        impulse_macd_price_color_disabled = True
    else:
        impulse_macd_add_price_disabled = False

    diff_1_price_color_disabled = False if boolean(diff_1_add_price) & secondary_y else True
    if (diff_1_deck != 'Upper') | (not secondary_y):
        diff_1_add_price_disabled = True
        diff_1_price_color_disabled = True
    else:
        diff_1_add_price_disabled = False

    diff_2_price_color_disabled = False if boolean(diff_2_add_price) & secondary_y else True
    if (diff_2_deck != 'Upper') | (not secondary_y):
        diff_2_add_price_disabled = True
        diff_2_price_color_disabled = True
    else:
        diff_2_add_price_disabled = False

    diff_3_price_color_disabled = False if boolean(diff_3_add_price) & secondary_y else True
    if (diff_3_deck != 'Upper') | (not secondary_y):
        diff_3_add_price_disabled = True
        diff_3_price_color_disabled = True
    else:
        diff_3_add_price_disabled = False

    rsi_price_color_disabled = False if boolean(rsi_add_price) & secondary_y else True
    if (rsi_deck != 'Upper') | (not secondary_y):
        rsi_add_price_disabled = True
        rsi_price_color_disabled = True
    else:
        rsi_add_price_disabled = False

    stochastic_k_smoothing_period_disabled = True if stochastic_type == 'Fast' else False
    stochastic_type = 'Full' if stochastic_k_smoothing_period != stochastic_d_period else stochastic_type
    stochastic_price_color_disabled = False if boolean(stochastic_add_price) & secondary_y else True
    if (stochastic_deck != 'Upper') | (not secondary_y):
        stochastic_add_price_disabled = True
        stochastic_price_color_disabled = True
    else:
        stochastic_add_price_disabled = False

    diff_stochastic_k_smoothing_period_disabled = True if diff_stochastic_type == 'Fast' else False
    diff_stochastic_type = 'Full' if diff_stochastic_k_smoothing_period != diff_stochastic_d_period else diff_stochastic_type
    diff_stochastic_added_line_type_disabled = False if boolean(diff_stochastic_add_line) & secondary_y else True
    diff_stochastic_added_line_color_disabled = False if boolean(diff_stochastic_add_line) & secondary_y else True
    if (diff_stochastic_deck != 'Upper') | (not secondary_y):
        diff_stochastic_add_line_disabled = True
        diff_stochastic_added_line_type_disabled = True
        diff_stochastic_added_line_color_disabled = True
    else:
        diff_stochastic_add_line_disabled = False

    # Added To plot indicators
    added_to_plot_indicator_prices_tab_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_volume_tab_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_trend_tab_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_differential_tab_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_volatility_tab_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_momentum_tab_style = not_added_to_plot_indicator_css

    added_to_plot_indicator_hist_price_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_candlestick_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_volume_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_dollar_volume_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_obv_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_drawdowns_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_price_overlays_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_bollinger_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_boll_width_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_ma_env_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_ma_ribbon_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_macd_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_impulse_macd_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_atr_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_mvol_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_ulcer_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_rsi_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_stochastic_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_diff_1_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_diff_2_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_diff_3_style = not_added_to_plot_indicator_css
    added_to_plot_indicator_diff_stochastic_style = not_added_to_plot_indicator_css

    ################

    fig_divs = []

    top_drawdowns = {}

    for tk in tickers_to_plot:

        # date_index = downloaded_data[tk]['ohlc'].index
        # new_start_date = '2024-06-01'
        # new_end_date = '2024-12-31'
        # min_date = datetime.strptime(new_start_date, '%Y-%m-%d').date()
        # max_date = datetime.strptime(new_end_date, '%Y-%m-%d').date()

        ## if (new_start_date is None) | (new_end_date is None):
        ##     min_date = min_start_date
        ##     max_date = max_end_date
        ## else:
        min_date = datetime.strptime(new_start_date, '%Y-%m-%d').date() if new_start_date is not None else datetime.strptime(start_date, '%Y-%m-%d').date()
        max_date = datetime.strptime(new_end_date, '%Y-%m-%d').date() if new_end_date is not None else datetime.strptime(end_date, '%Y-%m-%d').date()

        date_index = downloaded_data[tk]['ohlc'][min_date: max_date].index
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

        ################## PRICES TAB
        
        ### Add historical price

        # add_hist_price = 0 if remove_hist_price else add_hist_price
        if remove_hist_price & (fig_data is not None):
            add_hist_price = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':
                    if 'hist-price' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])
                        # fig_data['fig']['data'][i].clear()
            
        # NOTE: The condition 
        # if add_hist_price & (not remove_hist_price)
        # requires clicking Add To Plot twice in order to restore the plot after it has been removed.
        if add_hist_price:
            
            hist_price_color_theme = hist_price_color_theme.lower() if hist_price_color_theme is not None else 'base'
            df_hist_price = downloaded_data[tk]['ohlc_adj'] if boolean(hist_price_adjusted) else downloaded_data[tk]['ohlc']
            hist_price = df_hist_price[hist_price_type]
            if boolean(hist_price_adjusted):
                hist_price_type = 'Adjusted ' + hist_price_type

            fig_data = analyze_prices.add_hist_price(
                fig_data,
                hist_price[min_date: max_date],
                tk,
                target_deck = deck_number(deck_type, hist_price_deck_name),
                secondary_y = boolean(hist_price_secondary_y),
                plot_type = 'bar' if hist_price_plot_type == 'Histogram' else 'scatter',
                price_type = hist_price_type,
                add_title = boolean(hist_price_add_title),
                theme = theme,
                color_theme = hist_price_color_theme,
                fill_below = boolean(hist_price_fill_below)
            )

            added_to_plot_indicator_hist_price_style = added_to_plot_indicator_css
            added_to_plot_indicator_prices_tab_style = added_to_plot_indicator_css

        # for i, tr in enumerate(fig_data['fig']['data']):
        #     trace_uid_to_delete = tr['uid']
        #     print(f"tr['uid']\n {tr['uid']}")

        ### Add candlestick
        if remove_candlestick & (fig_data is not None):
            add_candlestick = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':
                    if 'candlestick' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_candlestick:
            
            df_ohlc = downloaded_data[tk]['ohlc_adj'] if boolean(candlestick_adjusted) else downloaded_data[tk]['ohlc']

            fig_data = analyze_prices.add_candlestick(
                fig_data,
                df_ohlc[min_date: max_date],
                tk,
                candle_type = candlestick_type.lower(),
                target_deck = deck_number(deck_type, candlestick_deck_name),
                add_title = boolean(candlestick_add_title),
                add_yaxis_title = boolean(candlestick_add_yaxis_title),
                adjusted_prices = boolean(candlestick_adjusted),
                theme = theme,
                color_theme = candlestick_color_theme
            )

            added_to_plot_indicator_candlestick_style = added_to_plot_indicator_css
            added_to_plot_indicator_prices_tab_style = added_to_plot_indicator_css

        ### Add price overlays
        if remove_price_overlays & (fig_data is not None):
            add_price_overlays = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'price-overlay' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_price_overlays:
            price_list = []
            for name in ['Adjusted Close', 'Adjusted Open', 'Adjusted High', 'Adjusted Low']:
                if name in price_overlay_adj_price_list:
                    price_list.append({
                        'name': name,
                        'data': downloaded_data[tk]['ohlc_adj'][name.replace('Adjusted ', '')][min_date: max_date],
                        'show': True
                    })
            for name in ['Close', 'Open', 'High', 'Low']:
                if name in price_overlay_price_list:
                    price_list.append({
                        'name': name,
                        'data': downloaded_data[tk]['ohlc'][name][min_date: max_date],
                        'show': True
                    })
            if len(price_list) > 0:
                fig_data = analyze_prices.add_price_overlays(
                    fig_data,
                    price_list,
                    target_deck = deck_number(deck_type, price_overlay_deck_name),
                    add_yaxis_title = boolean(price_overlay_add_yaxis_title),
                    yaxis_title = 'Price',
                    theme = theme,
                    color_theme = price_overlay_color_theme
                )
            added_to_plot_indicator_price_overlays_style = added_to_plot_indicator_css
            added_to_plot_indicator_prices_tab_style = added_to_plot_indicator_css

        ### Add drawdowns
        if remove_drawdowns & (fig_data is not None):
            add_drawdowns = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'drawdowns' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_drawdowns:

            dd_add_title = boolean(drawdowns_add_title)
            drawdowns_color = drawdowns_color.lower() if drawdowns_color is not None else 'red'
            drawdowns_price_color_theme = drawdowns_price_color_theme.lower() if drawdowns_price_color_theme is not None else 'base'
            df_drawdowns_price = downloaded_data[tk]['ohlc_adj'] if boolean(drawdowns_adjusted) else downloaded_data[tk]['ohlc']
            drawdowns_price = df_drawdowns_price[drawdowns_price_type][min_date: max_date]

            drawdowns_data_tk = analyze_prices.summarize_tk_drawdowns(drawdowns_price, drawdowns_top_by)
            n_drawdowns = drawdowns_data_tk['Total Drawdowns']
            top_drawdowns[tk] = n_drawdowns
            max_top_drawdowns = max([n for n in top_drawdowns.values()])
            # dd_number_value = min(n_top, n_drawdowns)
            dd_number_value = min(n_top, max_top_drawdowns)
            selected_drawdowns_data = analyze_prices.select_tk_drawdowns(drawdowns_data_tk, dd_number_value)
            # NOTE: If the date range is expanded so that n_drawdowns > n_top, it probably still makes sense to keep the number 
            # of drawdowns plotted equal to the latest chosen by the user, i.e. n_top, even if it was forced by the range narrowing
            # earlier. The so-called 'expansion' does not necessarily mean that the previous range will be contained in the new one.
            # It may happen that the range of dates shift results in n_drawdowns being lower, equal to or much higher than previously.
            # The app cannot guess how many drawdowns should be displayed after the user has changed the range of dates and n_drawdowns
            # increases as a result, it must rely on the input from the n_top dropdown.

            show_trough_to_recovery = True if 'Recovery' in drawdowns_display else False
            dd_top_by = 'length' if drawdowns_top_by == 'Total Length' else 'depth'
            
            drawdowns_price_type_full = 'Adjusted ' + drawdowns_price_type if boolean(drawdowns_adjusted) else drawdowns_price_type

            fig_data = analyze_prices.add_drawdowns(
                fig_data,
                drawdowns_price,
                tk,
                selected_drawdowns_data,
                n_top_drawdowns = n_top,
                target_deck = deck_number(deck_type, drawdowns_deck),
                add_price = not dd_add_price_disabled,
                price_type = drawdowns_price_type_full,
                top_by = dd_top_by,
                show_trough_to_recovery = show_trough_to_recovery,
                add_title = dd_add_title,
                theme = theme,
                price_color_theme = drawdowns_price_color_theme,
                drawdown_color = drawdowns_color
            )

            added_to_plot_indicator_drawdowns_style = added_to_plot_indicator_css
            added_to_plot_indicator_prices_tab_style = added_to_plot_indicator_css


        ################## VOLUME TAB

        ### Add Volume
        if remove_volume & (fig_data is not None):
            add_volume = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':
                    if tr['uid'] == 'volume':
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_volume:

            volume_color_theme = volume_color_theme.lower() if volume_color_theme is not None else 'sapphire'
            df_volume = downloaded_data[tk]['volume']

            fig_data = analyze_prices.add_hist_price(
                fig_data,
                df_volume[min_date: max_date],
                tk,
                target_deck = deck_number(deck_type, volume_deck_name),
                secondary_y = boolean(volume_secondary_y),
                plot_type = 'bar' if volume_plot_type == 'Histogram' else 'scatter',
                price_type = 'volume',
                add_title = boolean(volume_add_title),
                theme = theme,
                color_theme = volume_color_theme,
                fill_below = boolean(volume_fill_below)
            )

            added_to_plot_indicator_volume_style = added_to_plot_indicator_css
            added_to_plot_indicator_volume_tab_style = added_to_plot_indicator_css

        ### Add Dollar Volume
        if remove_dollar_volume & (fig_data is not None):
            add_dollar_volume = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':
                    if tr['uid'] == 'dollar-volume':
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_dollar_volume:

            dollar_volume_color_theme = dollar_volume_color_theme.lower() if dollar_volume_color_theme is not None else 'sapphire'
            df_dollar_volume = downloaded_data[tk]['dollar_volume_adj'] if boolean(dollar_volume_adjusted) else downloaded_data[tk]['dollar_volume']

            fig_data = analyze_prices.add_hist_price(
                fig_data,
                df_dollar_volume[min_date: max_date],
                tk,
                target_deck = deck_number(deck_type, dollar_volume_deck_name),
                secondary_y = boolean(dollar_volume_secondary_y),
                plot_type = 'bar' if dollar_volume_plot_type == 'Histogram' else 'scatter',
                price_type = 'dollar volume',
                add_title = boolean(dollar_volume_add_title),
                theme = theme,
                color_theme = dollar_volume_color_theme,
                fill_below = boolean(dollar_volume_fill_below)
            )

            added_to_plot_indicator_dollar_volume_style = added_to_plot_indicator_css
            added_to_plot_indicator_volume_tab_style = added_to_plot_indicator_css

        ### Add On-Balance Volume
        if remove_obv & (fig_data is not None):
            add_obv = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':
                    if tr['uid'] == 'obv':
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_obv:

            obv_color_theme = obv_color_theme.lower() if obv_color_theme is not None else 'sapphire'
            close_tk = downloaded_data[tk]['ohlc_adj']['Close'] if boolean(obv_adjusted) else downloaded_data[tk]['ohlc']['Close']
            volume_tk = downloaded_data[tk]['volume']

            obv_tk = analyze_prices.on_balance_volume(close_tk, volume_tk)

            fig_data = analyze_prices.add_hist_price(
                fig_data,
                obv_tk[min_date: max_date],
                tk,
                target_deck = deck_number(deck_type, obv_deck_name),
                secondary_y = boolean(obv_secondary_y),
                plot_type = 'bar' if obv_plot_type == 'Histogram' else 'scatter',
                price_type = 'obv',
                add_title = boolean(obv_add_title),
                theme = theme,
                color_theme = obv_color_theme,
                fill_below = boolean(obv_fill_below)
            )

            added_to_plot_indicator_obv_style = added_to_plot_indicator_css
            added_to_plot_indicator_volume_tab_style = added_to_plot_indicator_css


        ############ TREND INDICATORS TAB

        ### Add moving average envelopes
        if remove_ma_env & (fig_data is not None):
            add_ma_env = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'ma-envelope' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_ma_env:
            df_ma_env_price = downloaded_data[tk]['ohlc_adj'] if boolean(ma_env_adjusted) else downloaded_data[tk]['ohlc']
            ma_env_price = df_ma_env_price[ma_env_price_type]
            ma_env_list = analyze_prices.ma_envelopes(
                ma_env_price[min_date: max_date],
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
            added_to_plot_indicator_ma_env_style = added_to_plot_indicator_css
            added_to_plot_indicator_trend_tab_style = added_to_plot_indicator_css

        ### Add moving average ribbon
        if remove_ma_ribbon & (fig_data is not None):
            add_ma_ribbon = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'ma-ribbon' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_ma_ribbon:
            df_ma_ribbon_price = downloaded_data[tk]['ohlc_adj'] if boolean(ma_ribbon_adjusted) else downloaded_data[tk]['ohlc']
            ma_ribbon_price = df_ma_ribbon_price[ma_ribbon_price_type]
            ma_ribbon_list = analyze_prices.get_ma_ribbon(
                ma_type_map[ma_ribbon_ma_type],
                ma_ribbon_window,
                ma_ribbon_nbands
            )
            fig_data = analyze_prices.add_ma_overlays(
                fig_data,
                ma_ribbon_price[min_date: max_date],
                ma_ribbon_list,
                target_deck = deck_number(deck_type, ma_ribbon_deck_name),
                add_yaxis_title = boolean(ma_ribbon_add_yaxis_title),
                yaxis_title = 'Moving Average',
                theme = theme,
                color_theme = ma_ribbon_color_theme
            )
            added_to_plot_indicator_ma_ribbon_style = added_to_plot_indicator_css
            added_to_plot_indicator_trend_tab_style = added_to_plot_indicator_css

        ### Add MACD / MACD-V
        if remove_macd & (fig_data is not None):
            add_macd = 0
            # for i, tr in enumerate(fig_data['fig']['data']):
            #     if tr['legendgroup'] != 'dummy':                
            #         if 'macd' in tr['uid']:
            #             fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_macd:
            df_macd_prices = downloaded_data[tk]['ohlc_adj'] if boolean(macd_adjusted) else downloaded_data[tk]['ohlc']
            close_tk = df_macd_prices['Close'][min_date: max_date]
            #
            # MACD-V
            if boolean(macd_vol_normalized):
                high_tk = df_macd_prices['High'][min_date: max_date]
                low_tk = df_macd_prices['Low'][min_date: max_date]
                macd_data = analyze_prices.get_macd_v(
                    close_tk,
                    high_tk,
                    low_tk,
                    boolean(macd_adjusted),
                    signal_window = macd_signal_window
                )
            # MACD
            else:
                macd_data = analyze_prices.get_macd(
                    close_tk,
                    signal_window = macd_signal_window
                )
            #
            fig_data = analyze_prices.add_macd(
                fig_data,
                tk,
                macd_data,
                add_price = boolean(macd_add_price),
                volatility_normalized = boolean(macd_vol_normalized),
                histogram_type = macd_histogram_type.lower(),
                include_signal = boolean(macd_add_signal),
                plot_type = 'bar' if macd_plot_type == 'Histogram' else 'scatter',
                target_deck = deck_number(deck_type, macd_deck),
                add_title = boolean(macd_add_title),
                adjusted_prices = boolean(macd_adjusted),
                theme = theme,
                color_theme = macd_color_theme,
                signal_color_theme = macd_signal_color,
                price_color_theme = macd_price_color
            )
            added_to_plot_indicator_macd_style = added_to_plot_indicator_css
            added_to_plot_indicator_trend_tab_style = added_to_plot_indicator_css

        ### Add Impulse MACD
        if remove_impulse_macd & (fig_data is not None):
            add_impulse_macd = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'impulse' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_impulse_macd:
            df_macd_prices = downloaded_data[tk]['ohlc_adj'] if boolean(impulse_macd_adjusted) else downloaded_data[tk]['ohlc']
            close_tk = df_macd_prices['Close'][min_date: max_date]
            high_tk = df_macd_prices['High'][min_date: max_date]
            low_tk = df_macd_prices['Low'][min_date: max_date]
            impulse_macd_data = analyze_prices.get_impulse_macd(
                close_tk,
                high_tk,
                low_tk,
                smma_length = impulse_macd_smma_window,
                signal_length = impulse_macd_signal_window
            )
            #
            fig_data = analyze_prices.add_macd(
                fig_data,
                tk,
                impulse_macd_data,
                add_price = boolean(impulse_macd_add_price),
                volatility_normalized = False,
                histogram_type = impulse_macd_histogram_type.lower(),
                include_signal = boolean(impulse_macd_add_signal),
                plot_type = 'bar' if impulse_macd_plot_type == 'Histogram' else 'scatter',
                target_deck = deck_number(deck_type, impulse_macd_deck),
                add_title = boolean(impulse_macd_add_title),
                adjusted_prices = boolean(impulse_macd_adjusted),
                impulse_macd = True,
                theme = theme,
                color_theme = impulse_macd_color_theme,
                signal_color_theme = impulse_macd_signal_color,
                price_color_theme = impulse_macd_price_color
            )
            added_to_plot_indicator_impulse_macd_style = added_to_plot_indicator_css
            added_to_plot_indicator_trend_tab_style = added_to_plot_indicator_css


        ############# DIIFERENTIAL PLOTS TAB

        ### Add Differential 1
        if remove_diff_1 & (fig_data is not None):
            add_diff_1 = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'diff-1' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_diff_1:
            
            adj_prices = downloaded_data[tk]['ohlc_adj'][min_date: max_date]
            prices = downloaded_data[tk]['ohlc'][min_date: max_date]
            
            line_1_ma_type = ma_type_map[diff_1_line_1_ma_type]
            line_2_ma_type = ma_type_map[diff_1_line_2_ma_type]

            p1 = adj_prices[diff_1_line_1_price_type] if boolean(diff_1_line_1_adjusted) else prices[diff_1_line_1_price_type]
            p2 = adj_prices[diff_1_line_2_price_type] if boolean(diff_1_line_2_adjusted) else prices[diff_1_line_2_price_type]
                
            if diff_1_line_1_line_type == 'Moving Average':
                p1 = analyze_prices.moving_average(p1, line_1_ma_type, diff_1_line_1_window)
                p1_name = f'{line_1_ma_type.upper()} {diff_1_line_1_window}'
            else:
                # Price
                adj_prefix_line_1 = 'Adjusted ' if boolean(diff_1_line_1_adjusted) else ''
                p1_name = f'{adj_prefix_line_1}{diff_1_line_1_price_type}'

            if diff_1_line_2_line_type == 'Moving Average':
                p2 = analyze_prices.moving_average(p2, line_2_ma_type, diff_1_line_2_window)
                p2_name = f'{line_2_ma_type.upper()} {diff_1_line_2_window}'
            else:
                # Price
                adj_prefix_line_2 = 'Adjusted ' if boolean(diff_1_line_2_adjusted) else ''
                p2_name = f'{adj_prefix_line_2}{diff_1_line_2_price_type}'

            if not p1.equals(p2):
                fig_data = analyze_prices.add_diff(
                    fig_data,
                    tk,
                    p1,
                    p2,
                    p1_name,
                    p2_name,
                    target_deck = deck_number(deck_type, diff_1_deck),
                    plot_type = diff_1_plot_type,
                    add_signal = boolean(diff_1_add_signal), 
                    signal_ma_type = ma_type_map[diff_1_signal_ma_type],
                    signal_window = diff_1_signal_window,
                    add_price = boolean(diff_1_add_price),
                    add_title = boolean(diff_1_add_title),
                    uid_idx = 1,
                    theme = theme,
                    color_theme = diff_1_color_theme,
                    signal_color_theme = diff_1_signal_color,
                    price_color_theme = diff_1_price_color
                )

            added_to_plot_indicator_diff_1_style = added_to_plot_indicator_css
            added_to_plot_indicator_differential_tab_style = added_to_plot_indicator_css

        ### Add Differential 2
        if remove_diff_2 & (fig_data is not None):
            add_diff_2 = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'diff-2' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_diff_2:
            
            adj_prices = downloaded_data[tk]['ohlc_adj'][min_date: max_date]
            prices = downloaded_data[tk]['ohlc'][min_date: max_date]
            
            line_1_ma_type = ma_type_map[diff_2_line_1_ma_type]
            line_2_ma_type = ma_type_map[diff_2_line_2_ma_type]

            p1 = adj_prices[diff_2_line_1_price_type] if boolean(diff_2_line_1_adjusted) else prices[diff_2_line_1_price_type]
            p2 = adj_prices[diff_2_line_2_price_type] if boolean(diff_2_line_2_adjusted) else prices[diff_2_line_2_price_type]
                
            if diff_2_line_1_line_type == 'Moving Average':
                p1 = analyze_prices.moving_average(p1, line_1_ma_type, diff_2_line_1_window)
                p1_name = f'{line_1_ma_type.upper()} {diff_2_line_1_window}'
            else:
                # Price
                adj_prefix_line_1 = 'Adjusted ' if boolean(diff_2_line_1_adjusted) else ''
                p1_name = f'{adj_prefix_line_1}{diff_2_line_1_price_type}'

            if diff_2_line_2_line_type == 'Moving Average':
                p2 = analyze_prices.moving_average(p2, line_2_ma_type, diff_2_line_2_window)
                p2_name = f'{line_2_ma_type.upper()} {diff_2_line_2_window}'
            else:
                # Price
                adj_prefix_line_2 = 'Adjusted ' if boolean(diff_2_line_2_adjusted) else ''
                p2_name = f'{adj_prefix_line_2}{diff_2_line_2_price_type}'

            if not p1.equals(p2):
                fig_data = analyze_prices.add_diff(
                    fig_data,
                    tk,
                    p1,
                    p2,
                    p1_name,
                    p2_name,
                    target_deck = deck_number(deck_type, diff_2_deck),
                    plot_type = diff_2_plot_type,
                    add_signal = boolean(diff_2_add_signal), 
                    signal_ma_type = ma_type_map[diff_2_signal_ma_type],
                    signal_window = diff_2_signal_window,
                    add_price = boolean(diff_2_add_price),
                    add_title = boolean(diff_2_add_title),
                    uid_idx = 1,
                    theme = theme,
                    color_theme = diff_2_color_theme,
                    signal_color_theme = diff_2_signal_color,
                    price_color_theme = diff_2_price_color
                )

            added_to_plot_indicator_diff_2_style = added_to_plot_indicator_css
            added_to_plot_indicator_differential_tab_style = added_to_plot_indicator_css

        ### Add Differential 3
        if remove_diff_3 & (fig_data is not None):
            add_diff_3 = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'diff-3' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_diff_3:
            
            adj_prices = downloaded_data[tk]['ohlc_adj'][min_date: max_date]
            prices = downloaded_data[tk]['ohlc'][min_date: max_date]
            
            line_1_ma_type = ma_type_map[diff_3_line_1_ma_type]
            line_2_ma_type = ma_type_map[diff_3_line_2_ma_type]

            p1 = adj_prices[diff_3_line_1_price_type] if boolean(diff_3_line_1_adjusted) else prices[diff_2_line_1_price_type]
            p2 = adj_prices[diff_3_line_2_price_type] if boolean(diff_3_line_2_adjusted) else prices[diff_2_line_2_price_type]
                
            if diff_3_line_1_line_type == 'Moving Average':
                p1 = analyze_prices.moving_average(p1, line_1_ma_type, diff_3_line_1_window)
                p1_name = f'{line_1_ma_type.upper()} {diff_3_line_1_window}'
            else:
                # Price
                adj_prefix_line_1 = 'Adjusted ' if boolean(diff_3_line_1_adjusted) else ''
                p1_name = f'{adj_prefix_line_1}{diff_3_line_1_price_type}'

            if diff_3_line_2_line_type == 'Moving Average':
                p2 = analyze_prices.moving_average(p2, line_2_ma_type, diff_3_line_2_window)
                p2_name = f'{line_2_ma_type.upper()} {diff_3_line_2_window}'
            else:
                # Price
                adj_prefix_line_2 = 'Adjusted ' if boolean(diff_3_line_2_adjusted) else ''
                p2_name = f'{adj_prefix_line_2}{diff_3_line_2_price_type}'

            if not p1.equals(p2):
                fig_data = analyze_prices.add_diff(
                    fig_data,
                    tk,
                    p1,
                    p2,
                    p1_name,
                    p2_name,
                    target_deck = deck_number(deck_type, diff_3_deck),
                    plot_type = diff_3_plot_type,
                    add_signal = boolean(diff_3_add_signal), 
                    signal_ma_type = ma_type_map[diff_3_signal_ma_type],
                    signal_window = diff_3_signal_window,
                    add_price = boolean(diff_3_add_price),
                    add_title = boolean(diff_3_add_title),
                    uid_idx = 1,
                    theme = theme,
                    color_theme = diff_3_color_theme,
                    signal_color_theme = diff_3_signal_color,
                    price_color_theme = diff_3_price_color
                )

            added_to_plot_indicator_diff_3_style = added_to_plot_indicator_css
            added_to_plot_indicator_differential_tab_style = added_to_plot_indicator_css

        ### Add Diff Stochastic
        if remove_diff_stochastic & (fig_data is not None):
            add_diff_stochastic = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'diff-stochastic' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_diff_stochastic:
            stochastic_prices = downloaded_data[tk]['ohlc_adj'] if boolean(stochastic_adjusted) else downloaded_data[tk]['ohlc']
            stochastic_close_tk = stochastic_prices['Close'][min_date: max_date]
            stochastic_high_tk = stochastic_prices['High'][min_date: max_date]
            stochastic_low_tk = stochastic_prices['Low'][min_date: max_date]
            #
            stochastic_data = analyze_prices.stochastic_oscillator(
                stochastic_close_tk,
                stochastic_high_tk,
                stochastic_low_tk,
                fast_k_period = diff_stochastic_fast_k_period,
                smoothing_period = diff_stochastic_k_smoothing_period,
                sma_d_period = diff_stochastic_d_period,
                stochastic_type = diff_stochastic_type
            )
            #
            fig_data = analyze_prices.add_diff_stochastic(
                fig_data,
                stochastic_data,
                diff_stochastic_adjusted,
                tk,
                target_deck = deck_number(deck_type, diff_stochastic_deck),
                flip_sign = True if diff_stochastic_sign.startswith('%D') else False,
                plot_type = diff_stochastic_plot_type,
                add_signal = boolean(diff_stochastic_add_signal),
                signal_type = ma_type_map[diff_stochastic_signal_ma_type],
                signal_window = diff_stochastic_signal_window,
                signal_color_theme = diff_stochastic_signal_color,
                add_line = boolean(diff_stochastic_add_line),
                added_line_type = diff_stochastic_added_line_type,
                added_line_color_theme = diff_stochastic_added_line_color_theme,
                add_title = boolean(diff_stochastic_add_title),
                theme = theme,
                color_theme = diff_stochastic_color_theme
            )
            added_to_plot_indicator_diff_stochastic_style = added_to_plot_indicator_css
            added_to_plot_indicator_differential_tab_style = added_to_plot_indicator_css


        ########## VOLATILITY INDICATORS TAB

        ### Add Bollinger bands
        if remove_bollinger & (fig_data is not None):
            add_bollinger = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'bollinger-band' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_bollinger:
            df_bollinger_price = downloaded_data[tk]['ohlc_adj'] if boolean(bollinger_adjusted) else downloaded_data[tk]['ohlc']
            bollinger_price = df_bollinger_price[bollinger_price_type]
            bollinger_data = analyze_prices.bollinger_bands(
                bollinger_price[min_date: max_date],
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
            added_to_plot_indicator_bollinger_style = added_to_plot_indicator_css
            added_to_plot_indicator_volatility_tab_style = added_to_plot_indicator_css

        ### Add Bollinger Width
        if remove_boll_width & (fig_data is not None):
            add_boll_width = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'boll-width' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_boll_width:
            df_boll_width_price = downloaded_data[tk]['ohlc_adj'] if boolean(boll_width_adjusted) else downloaded_data[tk]['ohlc']
            boll_width_price = df_boll_width_price[boll_width_price_type]
            bollinger_data = analyze_prices.bollinger_bands(
                boll_width_price[min_date: max_date],
                ma_type_map[boll_width_ma_type],
                boll_width_window,
                boll_width_nstd
            )
            fig_data = analyze_prices.add_bollinger_width(
                fig_data,
                bollinger_data,
                bollinger_type = 'width' if boll_width_type == 'Bandwidth' else '%B',
                target_deck = deck_number(deck_type, boll_width_deck),
                secondary_y = boolean(boll_width_secondary_y),
                add_yaxis_title = boolean(boll_width_add_yaxis_title),
                theme = theme,
                color_theme = boll_width_color_theme
            )
            added_to_plot_indicator_boll_width_style = added_to_plot_indicator_css
            added_to_plot_indicator_volatility_tab_style = added_to_plot_indicator_css

        # Add ATR / ATRP
        if remove_atr & (fig_data is not None):
            add_atr = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':
                    if 'atr' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_atr:
            atr_color_theme = atr_color_theme.lower() if atr_color_theme is not None else 'gold'
            df_atr = downloaded_data[tk]['ohlc_adj'] if boolean(atr_adjusted) else downloaded_data[tk]['ohlc']
            atr_close_tk = df_atr['Close'][min_date: max_date]
            atr_high_tk = df_atr['High'][min_date: max_date]
            atr_low_tk = df_atr['Low'][min_date: max_date]
            atr_data = analyze_prices.average_true_rate(
                atr_close_tk,
                atr_high_tk,
                atr_low_tk,
                boolean(atr_adjusted),
                atr_periods
            )
            fig_data = analyze_prices.add_atr(
                fig_data,
                atr_data,
                atr_type = 'atr' if atr_type == 'Regular' else 'atrp',
                target_deck = deck_number(deck_type, atr_deck),
                secondary_y = boolean(atr_secondary_y),
                add_yaxis_title = boolean(atr_add_yaxis_title),
                theme = theme,
                color_theme = atr_color_theme
            )
            added_to_plot_indicator_atr_style = added_to_plot_indicator_css
            added_to_plot_indicator_volatility_tab_style = added_to_plot_indicator_css

        ### Add MVol / MStD
        if remove_mvol & (fig_data is not None):
            add_mvol = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'mvol' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_mvol:
            df_mvol_price = downloaded_data[tk]['ohlc_adj'] if boolean(mvol_adjusted) else downloaded_data[tk]['ohlc']
            mvol_price = df_mvol_price[mvol_price_type]
            mvol_data = analyze_prices.moving_volatility_stdev(
                mvol_price[min_date: max_date],
                ma_type = ma_type_map[mvol_ma_type],
                ma_window = mvol_window
            )
            fig_data = analyze_prices.add_mvol(
                fig_data,
                mvol_data,
                mvol_type = 'vol' if mvol_type == 'Volatility' else 'std',
                target_deck = deck_number(deck_type, mvol_deck),
                secondary_y = boolean(mvol_secondary_y),
                add_yaxis_title = boolean(mvol_add_yaxis_title),
                theme = theme,
                color_theme = mvol_color_theme
            )
            added_to_plot_indicator_mvol_style = added_to_plot_indicator_css
            added_to_plot_indicator_volatility_tab_style = added_to_plot_indicator_css

        ### Add Ulcer Index
        if remove_ulcer & (fig_data is not None):
            add_ulcer = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'ulcer' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_ulcer:
            df_ulcer_price = downloaded_data[tk]['ohlc_adj'] if boolean(ulcer_adjusted) else downloaded_data[tk]['ohlc']
            ulcer_price = df_ulcer_price[ulcer_price_type]
            ulcer_data = analyze_prices.get_ulcer_index(
                ulcer_price[min_date: max_date],
                window = ulcer_window
            )
            fig_data = analyze_prices.add_ulcer_index(
                fig_data,
                ulcer_data,
                window = ulcer_window,
                target_deck = deck_number(deck_type, ulcer_deck),
                secondary_y = boolean(ulcer_secondary_y),
                add_yaxis_title = boolean(ulcer_add_yaxis_title),
                theme = theme,
                color_theme = ulcer_color_theme
            )
            added_to_plot_indicator_ulcer_style = added_to_plot_indicator_css
            added_to_plot_indicator_volatility_tab_style = added_to_plot_indicator_css


        ############# MOMENTUM INDICATORS TAB

        ### Add RSI
        if remove_rsi & (fig_data is not None):
            add_rsi = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'rsi' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_rsi:
            rsi_prices = downloaded_data[tk]['ohlc_adj']['Close'] if rsi_price_type == 'Adjusted Close' else downloaded_data[tk]['ohlc']['Close']
            rsi_prices = rsi_prices[min_date: max_date]
            #
            rsi_data = analyze_prices.relative_strength(
                rsi_prices,
                period = rsi_periods
            )
            #
            fig_data = analyze_prices.add_rsi(
                fig_data,
                rsi_data,
                tk,
                price_type = rsi_price_type,
                add_price = boolean(rsi_add_price),
                target_deck = deck_number(deck_type, rsi_deck),
                oversold_threshold = rsi_oversold_level,
                overbought_threshold = rsi_overbought_level,
                add_threshold_overlays = boolean(rsi_add_overbought_oversold),
                add_title = boolean(rsi_add_title),
                theme = theme,
                rsi_color_theme = rsi_color_theme,
                price_color_theme = rsi_price_color_theme
            )
            added_to_plot_indicator_rsi_style = added_to_plot_indicator_css
            added_to_plot_indicator_momentum_tab_style = added_to_plot_indicator_css

        ### Add Stochastic
        if remove_stochastic & (fig_data is not None):
            add_stochastic = 0
            for i, tr in enumerate(fig_data['fig']['data']):
                if tr['legendgroup'] != 'dummy':                
                    if 'stochastic' in tr['uid']:
                        fig_data['fig']['data'] = fig_data['fig']['data'].remove(fig_data['fig']['data'][i])

        if add_stochastic:
            stochastic_prices = downloaded_data[tk]['ohlc_adj'] if boolean(stochastic_adjusted) else downloaded_data[tk]['ohlc']
            stochastic_close_tk = stochastic_prices['Close'][min_date: max_date]
            stochastic_high_tk = stochastic_prices['High'][min_date: max_date]
            stochastic_low_tk = stochastic_prices['Low'][min_date: max_date]
            #
            stochastic_data = analyze_prices.stochastic_oscillator(
                stochastic_close_tk,
                stochastic_high_tk,
                stochastic_low_tk,
                fast_k_period = stochastic_fast_k_period,
                smoothing_period = stochastic_k_smoothing_period,
                sma_d_period = stochastic_d_period,
                stochastic_type = stochastic_type
            )
            #
            fig_data = analyze_prices.add_stochastic(
                fig_data,
                stochastic_data,
                stochastic_adjusted,
                tk,
                add_price = boolean(stochastic_add_price),
                target_deck = deck_number(deck_type, stochastic_deck),
                oversold_threshold = stochastic_oversold_level,
                overbought_threshold = stochastic_overbought_level,
                add_threshold_overlays = boolean(stochastic_add_overbought_oversold),
                add_title = boolean(stochastic_add_title),
                theme = theme,
                k_line_color = stochastic_k_line_color,
                d_line_color = stochastic_d_line_color,
                price_color_theme = stochastic_price_color_theme
            )
            added_to_plot_indicator_stochastic_style = added_to_plot_indicator_css
            added_to_plot_indicator_momentum_tab_style = added_to_plot_indicator_css


        ######

        map_sec_y_id_to_idx = {
            'hist_price': [0],                  # hist_price_sec_y_disabled
            'volume': [1],                      # volume_sec_y_disabled
            'dollar_volume': [2],               # volume_sec_y_disabled
            'obv': [3],                         # obv_sec_y_disabled
            'atr': [4],                         # atr_sec_y_disabled
            'boll_width': [5],                  # boll_width_sec_y_disabled
            'mvol': [6],                        # mvol_sec_y_disabled
            'ulcer': [7],                       # ulcer_sec_y_disabled
            'macd': [8, 9],                     # [macd_add_price_disabled, macd_price_color_disabled]
            'impulse_macd': [10, 11],           # [impulse_macd_add_price_disabled, impulse_macd_price_color_disabled]
            'rsi': [12, 13],                    # [rsi_add_price_disabled, rsi_price_color_disabled]
            'stochastic': [14, 15],             # [stochastic_add_price_disabled, stochastic_price_color_disabled]
            'diff_1': [16, 17],                 # [diff_1_add_price_disabled, diff_1_price_color_disabled]
            'diff_2': [18, 19],                 # [diff_1_add_price_disabled, diff_1_price_color_disabled]
            'diff_3': [20, 21],                 # [diff_1_add_price_disabled, diff_1_price_color_disabled]
            'diff_stochastic': [22, 23, 24]     # [diff_stochastic_add_line_disabled, diff_stochastic_added_line_color_disabled, diff_stochastic_added_line_type_disabled]
        }

        # Must assign values to sec_y_disabled_outputs if there are no traces on secondary y
        sec_y_disabled_outputs = (
            hist_price_sec_y_disabled,
            volume_sec_y_disabled,
            dollar_volume_sec_y_disabled,
            obv_sec_y_disabled,
            atr_sec_y_disabled,
            boll_width_sec_y_disabled,
            mvol_sec_y_disabled,
            ulcer_sec_y_disabled,
            macd_add_price_disabled,
            macd_price_color_disabled,
            impulse_macd_add_price_disabled,
            impulse_macd_price_color_disabled,
            rsi_add_price_disabled,
            rsi_price_color_disabled,
            stochastic_add_price_disabled,
            stochastic_price_color_disabled,
            diff_1_add_price_disabled,
            diff_1_price_color_disabled,
            diff_2_add_price_disabled,
            diff_2_price_color_disabled,
            diff_3_add_price_disabled,
            diff_3_price_color_disabled,
            diff_stochastic_add_line_disabled,
            diff_stochastic_added_line_type_disabled,
            diff_stochastic_added_line_color_disabled
        )

        n_sec_y_disabled_outputs = len([idx for v in map_sec_y_id_to_idx.values() for idx in v])

        if len(fig_data['sec_y_source']) > 0:
            sec_y_disabled_outputs_list = [True for i in range(n_sec_y_disabled_outputs)]
            sec_y_source = fig_data['sec_y_source'][0]
            for idx in map_sec_y_id_to_idx[sec_y_source]:
                sec_y_disabled_outputs_list[idx] = False
            sec_y_disabled_outputs = tuple(sec_y_disabled_outputs_list)

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

        # NOTE: 
        # All sec_y_disabled, add_price_disabled and price_color_disabled will be in a 15-element tuple

        ######
    return (

        fig_divs,
        
        add_hist_price,  # update
        add_candlestick,
        add_volume,
        add_dollar_volume,
        add_obv,
        add_drawdowns,
        add_price_overlays,
        add_bollinger,
        add_boll_width,
        add_ma_env,
        add_ma_ribbon,
        add_macd,
        add_impulse_macd,
        add_atr,
        add_mvol,
        add_ulcer,
        add_rsi,
        add_stochastic,
        add_diff_1,
        add_diff_2,
        add_diff_3,
        add_diff_stochastic,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # Clear all remove button values

        added_to_plot_indicator_prices_tab_style,
        added_to_plot_indicator_volume_tab_style,
        added_to_plot_indicator_trend_tab_style,
        added_to_plot_indicator_differential_tab_style,
        added_to_plot_indicator_volatility_tab_style,
        added_to_plot_indicator_momentum_tab_style,

        added_to_plot_indicator_hist_price_style,
        added_to_plot_indicator_candlestick_style,
        added_to_plot_indicator_volume_style,
        added_to_plot_indicator_dollar_volume_style,
        added_to_plot_indicator_obv_style,
        added_to_plot_indicator_drawdowns_style,
        added_to_plot_indicator_price_overlays_style,
        added_to_plot_indicator_bollinger_style,
        added_to_plot_indicator_boll_width_style,
        added_to_plot_indicator_ma_env_style,
        added_to_plot_indicator_ma_ribbon_style,
        added_to_plot_indicator_macd_style,
        added_to_plot_indicator_impulse_macd_style,
        added_to_plot_indicator_atr_style,
        added_to_plot_indicator_mvol_style,
        added_to_plot_indicator_ulcer_style,
        added_to_plot_indicator_rsi_style,
        added_to_plot_indicator_stochastic_style,
        added_to_plot_indicator_diff_1_style,
        added_to_plot_indicator_diff_2_style,
        added_to_plot_indicator_diff_3_style,
        added_to_plot_indicator_diff_stochastic_style,

        macd_signal_window_disabled,
        macd_signal_color_disabled,
        impulse_macd_signal_window_disabled,
        impulse_macd_signal_color_disabled,
        rsi_overbought_level_disabled,
        rsi_oversold_level_disabled,
        stochastic_overbought_level_disabled,
        stochastic_oversold_level_disabled,

        diff_1_signal_ma_type_disabled,
        diff_1_signal_window_disabled,
        diff_1_signal_color_disabled,
        diff_1_signal_line_row_2_hidden,
        diff_1_line_1_ma_options_hidden,
        diff_1_line_2_ma_options_hidden,
        diff_2_signal_ma_type_disabled,
        diff_2_signal_window_disabled,
        diff_2_signal_color_disabled,
        diff_2_signal_line_row_2_hidden,
        diff_2_line_1_ma_options_hidden,
        diff_2_line_2_ma_options_hidden,
        diff_3_signal_ma_type_disabled,
        diff_3_signal_window_disabled,
        diff_3_signal_color_disabled,
        diff_3_signal_line_row_2_hidden,
        diff_3_line_1_ma_options_hidden,
        diff_3_line_2_ma_options_hidden,

        diff_stochastic_signal_ma_type_disabled,
        diff_stochastic_signal_window_disabled,
        diff_stochastic_signal_color_disabled,
        diff_stochastic_signal_line_row_2_hidden,

        stochastic_k_smoothing_period_disabled,
        stochastic_type,
        diff_stochastic_k_smoothing_period_disabled,
        diff_stochastic_type,

        max_top_drawdowns,
        dd_number_value,
        dd_add_price_disabled,

        start_date_value,
        end_date_value,
        min_start_date,
        max_start_date,
        min_end_date,
        max_end_date

    ) + sec_y_disabled_outputs

#######################

# Remove restriction on drawdowns to be plotted only on the upper deck.
# 
