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

# end_date = datetime(2010, 10, 31)
# y_hist, m_hist, d_hist = 5, 0, 0
# start_date = datetime(end_date.year - y_hist, end_date.month - m_hist, end_date.day - d_hist)

hist_data = DownloadData()

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
        style_header_conditional = [
            {'if': {'column_id': 'Length*'}, 'width': 45, 'text-align': 'right', 'padding-right': '10px'},
        ],
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
            {'if': {'column_id': 'Length*'}, 'width': 45, 'text-align': 'right', 'padding-right': '15px'},
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

        # Dates selection
        html.Div(
            id = 'dates-selection-container',
            children = [

                # Start date
                html.Div(
                    id = 'start-date-select-container',
                    children = [
                        html.Div(
                            'Select Start Date',
                            style = {'font-family': 'Helvetica', 'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '3px'}
                        ),
                        html.Div(
                            id = 'start-date-year-month-day',
                            children = [
                                html.Div(
                                    id = 'start-date-year-container',
                                    children = [
                                        html.Div(
                                            'Year',
                                            style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '5px'}
                                        ),
                                        dbc.Input(
                                            id = 'start-date-year-input',
                                            type = 'number',
                                            min = 2000,
                                            max = 2025,
                                            step = 1,
                                            debounce = True,
                                            style = dates_year_input_css
                                        )
                                    ],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div(
                                    id = 'start-date-month-container',
                                    children = [
                                        html.Div(
                                            'Month',
                                            style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '5px'}
                                        ),
                                        dbc.Input(
                                            id = 'start-date-month-input',
                                            type = 'number',
                                            min = 1,
                                            max = 12,
                                            step = 1,
                                            debounce = True,
                                            style = dates_month_day_input_css
                                        )
                                    ],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div(
                                    id = 'start-date-day-container',
                                    children = [
                                        html.Div(
                                            'Day',
                                            style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '5px'}
                                        ),
                                        dbc.Input(
                                            id = 'start-date-day-input',
                                            type = 'number',
                                            min = 1,
                                            max = 31,
                                            step = 1,
                                            debounce = True,
                                            style = dates_month_day_input_css
                                        )
                                    ],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                            style = {'display': 'inline-block', 'margin-right': '50px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                        )
                    ],
                    style = {'display': 'inline-block'}
                ),

                # End date
                html.Div(
                    id = 'end-date-select-container',
                    children = [
                        html.Div(
                            'Select End Date',
                            style = {'font-family': 'Helvetica', 'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '8px'}
                        ),
                        html.Div(
                            id = 'end-date-year-month-day',
                            children = [
                                html.Div(
                                    id = 'end-date-year-container',
                                    children = [
                                        html.Div(
                                            'Year',
                                            style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '5px'}
                                        ),
                                        dbc.Input(
                                            id = 'end-date-year-input',
                                            type = 'number',
                                            min = 2000,
                                            max = 2025,
                                            step = 1,
                                            debounce = True,
                                            style = dates_year_input_css
                                        )
                                    ],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div(
                                    id = 'end-date-month-container',
                                    children = [
                                        html.Div(
                                            'Month',
                                            style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '5px'}
                                        ),
                                        dbc.Input(
                                            id = 'end-date-month-input',
                                            type = 'number',
                                            min = 1,
                                            max = 12,
                                            step = 1,
                                            debounce = True,
                                            style = dates_month_day_input_css
                                        )
                                    ],
                                    style = {'display': 'inline-block'}
                                ),
                                html.Div(
                                    id = 'end-date-day-container',
                                    children = [
                                        html.Div(
                                            'Day',
                                            style = {'font-family': 'Helvetica', 'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px', 'margin-left': '5px'}
                                        ),
                                        dbc.Input(
                                            id = 'end-date-day-input',
                                            type = 'number',
                                            min = 1,
                                            max = 31,
                                            step = 1,
                                            debounce = True,
                                            style = dates_month_day_input_css
                                        )
                                    ],
                                    style = {'display': 'inline-block'}
                                )
                            ],
                            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-left': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
                        )
                    ],
                    style = {'display': 'inline-block', 'margin-left': '5px'}
                )
            ],
            style = {'margin-left': '10px'}
        ),

        # YOUR PORTFOLIO
        html.Div(
            id = 'dates-portfolio-summary-container',
            hidden = False,
            children = [
                html.Div(
                    'PORTFOLIO SUMMARY',
                    id = 'dates-portfolio-summary-title',
                    style = dates_portfolio_summary_title_css
                ),
                html.Div(
                    id = 'dates-portfolio-summary-divs-container'
                ),
                html.Div(
                    id = 'dates-portfolio-summary'
                ),
                html.Div(
                    id = 'dates-portfolio-summary-message',
                    style = dates_portfolio_summary_message_css
                )
            ],
            style = select_ticker_container_css
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
    # Output('dates-selected-tickers', 'children'),
    # Output('dates-table-selected-tickers', 'children'),
    Output('dates-portfolio-summary', 'children'),
    Output('dates-portfolio-summary-message', 'children'),
    Output('dash-table-selected-tickers', 'data'),
    Output('dash-table-selected-tickers', 'selected_rows'),
    Output('dash-table-selected-tickers', 'tooltip_data'),

    Input('table-selected-tickers-data-stored', 'data'),
    Input('selected-ticker-summaries-stored', 'data'),
    Input('dash-table-selected-tickers', 'selected_rows'),
    Input('end-date-year-input', 'value'),
    Input('end-date-month-input', 'value'),
    Input('end-date-day-input', 'value'),
    Input('start-date-year-input', 'value'),
    Input('start-date-month-input', 'value'),
    Input('start-date-day-input', 'value')
)
def read_table_selected_tickers(
    table_selected_tickers_data,
    selected_ticker_summaries,
    selected_rows,
    end_date_year,
    end_date_month,
    end_date_day,
    start_date_year,
    start_date_month,
    start_date_day
):

    tooltip_data = [
        { column: {'value': selected_ticker_summaries[row['Ticker']], 'type': 'markdown' }
        for column in row.keys() }
        for row in table_selected_tickers_data  # e.g. {'No.': 1, 'Ticker': 'AAPL', ...} etc.
    ]

    selected_rows = [k for k in range(len(table_selected_tickers_data))] if selected_rows == [] else selected_rows
    n_tickers = len(selected_rows)
    
    selected_tickers = [row['Ticker'] for row in table_selected_tickers_data if row['No.'] - 1 in selected_rows]
    selected_start_dates = [row['Data Start'] for row in table_selected_tickers_data if row['No.'] - 1 in selected_rows]
    selected_end_dates = [row['Data End'] for row in table_selected_tickers_data if row['No.'] - 1 in selected_rows]

    portfolio_start = f'{min(selected_start_dates)}'
    portfolio_end = f'{max(selected_end_dates)}'
    tk_portfolio_start = [row['Ticker'] for row in table_selected_tickers_data if row['Data Start'] == portfolio_start][0]
    tk_portfolio_end = [row['Ticker'] for row in table_selected_tickers_data if row['Data End'] == portfolio_end][0]

    if ((start_date_year is None) | (start_date_month is None) | (start_date_day is None)):
        start_date = datetime.strptime(portfolio_start, '%Y-%m-%d')
    else:
        start_date = correct_date(start_date_year, start_date_month, start_date_day)

    if ((end_date_year is None) | (end_date_month is None) | (end_date_day is None)):
        end_date = datetime.strptime(portfolio_end, '%Y-%m-%d')
    else:
        end_date = correct_date(end_date_year, end_date_month, end_date_day)

    overlap_start = f'{max(selected_start_dates)}'
    overlap_end = f'{min(selected_end_dates)}'
    tk_overlap_start = [row['Ticker'] for row in table_selected_tickers_data if row['Data Start'] == overlap_start][0]
    tk_overlap_end = [row['Ticker'] for row in table_selected_tickers_data if row['Data End'] == overlap_end][0]

    # Use all 4 parameters above to download data just for these two tickers and two dates.
    # Then, after dropna(), count the length of the range of overlapping portfolio dates.

    # These are just the initial assignments, before the user inputs the start and end dates.
    # Once the user's start_date and end_date inputs are known, tickers_to_check should also be 
    # changed to selected_tickers.
    ### start_date = overlap_start
    ### end_date = overlap_end
    ### tickers_to_check = [tk_overlap_start, tk_overlap_end]

    tickers_to_check = selected_tickers

    portfolio_overlap_data = hist_data.check_portfolio_overlap_days(start_date, end_date, tickers_to_check)
    
    # data_overlap['length']:   overlap length in business days excluding weekends and holidays
    # data_overlap['start']:    overlap start date string, '' if no overlap
    # data_overlap['end']:      overlap end date string, '' if no overlap
    # data_overlap['excluded']:  list of tickers with no data available during the overlap period

    no_overlap_message = 'WARNING: No overlapping dates for the selected tickers'

    overlap_start = portfolio_overlap_data['overlap_start']
    overlap_end = portfolio_overlap_data['overlap_end']
    overlap_length = portfolio_overlap_data['overlap_length']
    full_start = portfolio_overlap_data['full_start']
    full_end = portfolio_overlap_data['full_end']
    full_length = portfolio_overlap_data['full_length']
    excluded_tickers = portfolio_overlap_data['excluded']

    if len(excluded_tickers) > 0:
        excluded_tickers_str = ", ".join(excluded_tickers)
        excluded_tickers_message = f'WARNING: No data available for {excluded_tickers_str} within the selected period'
    else:
        excluded_tickers_message = ' '

    portfolio_summary_keys = [
        html.B('Ticker Count'), html.Br(),
        html.B('Selected Range'), html.Br(),
        html.B('Common Range'), html.Br()
    ]

    if overlap_start <= overlap_end:

        portfolio_summary_values_from = [
            html.Span(f'{n_tickers}'), html.Br(),
            html.B('From: '), html.Span(full_start), html.Br(),
            html.B('From: '), html.Span(overlap_start), html.Br()
        ]
        portfolio_summary_values_to = [
            html.Br(),
            html.B('To: '), html.Span(full_end), html.Br(),
            html.B('To: '), html.Span(overlap_end), html.Br(),
        ]
        portfolio_summary_values_length = [
            html.Br(),
            html.B('Length*: '), html.Span(full_length), html.Br(),
            html.B('Length*: '), html.Span(overlap_length), html.Br()
        ]
    else:
        portfolio_summary_values_from = [
            html.Span(f'{n_tickers}'), html.Br(),
            html.B('From: '), html.Span(full_start), html.Br(),
            html.B(no_overlap_message), html.Br()
        ]
        portfolio_summary_values_to = [
            html.Br(),
            html.B('To: '), html.Span(full_end), html.Br(),
            html.Br()
       ]
        portfolio_summary_values_length = [
            html.Br(),
            html.B('Length*: '), html.Span(full_length), html.Br(),            
            html.Br()
        ]

    dates_portfolio_summary = html.Div(
        [
        html.Div(
            portfolio_summary_keys,
            id = 'portfolio-summary-keys',
            style = portfolio_summary_keys_css
        ),
        html.Div(
            portfolio_summary_values_from,
            id = 'portfolio-summary-values-from',
            style = portfolio_summary_values_from_css
        ),
        html.Div(
            portfolio_summary_values_to,
            id = 'portfolio-summary-values-to',
            style = portfolio_summary_values_to_css
        ),
        html.Div(
            portfolio_summary_values_length,
            id = 'portfolio-summary-values-length',
            style = portfolio_summary_values_length_css
        )
        ],
        style = {'display': 'block'}
    )


    return (
        # selected_tickers,
        # str(selected_tickers),
        # f' Portfolio Data Overlap: From {date_overlap_start} To {date_overlap_end}',
        dates_portfolio_summary,
        excluded_tickers_message,
        table_selected_tickers_data,
        selected_rows,
        tooltip_data
    )
