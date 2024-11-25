import dash
from dash import Dash, dcc, html, Input, Output, State, callback, dash_table, ALL, MATCH
from dash.exceptions import PreventUpdate
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
from mapping_portfolio_downloads import *
from mapping_tickers import *
from css_portfolio_analytics import *
from utils import *
from download_data import DownloadData
from analyze_prices import AnalyzePrices

end_date = datetime.today()
hist_years, hist_months, hist_days = 1, 0, 0
start_date = datetime(end_date.year - hist_years, end_date.month - hist_months, end_date.day - hist_days)

deck_types = ['Single', 'Double', 'Triple']

hist_data = DownloadData(end_date, start_date)

tk_market = '^GSPC'
# tk_market = 'BTC-USD'

ticker_categories = [x for x in url_settings.keys() if x != 'global']
print(ticker_categories)
# Ticker categories:
# 'nasdaq100', 'sp500', 'dow_jones', 'biggest_companies',
# 'biggest_etfs', 'crypto_etfs', 'cryptos', 'cryptos_coin360', 'futures'

max_tickers = 5
# ticker_category = 'crypto_etfs'
ticker_category = 'biggest_companies'
# ticker_category = 'cryptos'
df = hist_data.download_from_url(ticker_category, max_tickers)

category_name = url_settings[ticker_category]['category_name']
category_sort_by = url_settings[ticker_category]['sort_by']
title_prefix = 'Top ' if not ('Biggest' in category_name) else ''
table_title = f'{max_tickers} {title_prefix}{category_name} by {category_sort_by}'
print(f'\n{title_prefix}{category_name} by {category_sort_by}\n')

df_ticker_info = pd.DataFrame(index = df['Symbol'], columns = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End'])

ticker_menu_info = {}
for i, tk in enumerate(df['Symbol']):
    
    yf_tk_hist = yf.Ticker(tk).history(period = 'max')
    yf_tk_info = yf.Ticker(tk).info

    if len(yf_tk_hist.index) > 0:

        tk_start, tk_end = str(yf_tk_hist.index[0].date()), str(yf_tk_hist.index[-1].date())
        # tk_info_full = f"{i + 1}. {tk}: {df.loc[i, 'Name']}, {tk_start}, {tk_end}"

        df_ticker_info.loc[tk, 'No.'] = i + 1
        df_ticker_info.loc[tk, 'Ticker'] = tk

        if 'longName' in yf_tk_info.keys():
            tk_name = yf_tk_info['longName']
        elif 'shortName' in yf_tk_info.keys():
            tk_name = yf_tk_info['shortName']
        else:
            tk_name = df.loc[i, 'Name']
        df_ticker_info.loc[tk, 'Name'] = tk_name

        df_ticker_info.loc[tk, 'Data Start'] = tk_start
        df_ticker_info.loc[tk, 'Data End'] = tk_end

        tk_info = f"{tk}: {tk_name}"
        ticker_menu_info.update({tk_info: tk})

    else:
        print(f'WARNING: Cannot get data for {tk} at the moment, try again later')

ticker_names = pd.Series(index = df_ticker_info.index, data = df_ticker_info['Name'])

tickers = list(df['Symbol'])
tk = tickers[0]
ticker_menu_info_list = list(ticker_menu_info.keys())

tickers_org = tickers.copy()  #
print(f'tickers_org = {tickers_org}')

# We don't want the benchmark ticker in the app menus at this point (for example, 
# the drawdown data will not generated) unless tk_market is explicitly selected.

downloaded_data = hist_data.download_yh_data(start_date, end_date, tickers, tk_market)
error_msg = downloaded_data['error_msg']

if error_msg:
    print(error_msg)

else:

    df_adj_close = downloaded_data['Adj Close']
    df_close = downloaded_data['Close']
    df_volume = downloaded_data['Volume']
    dict_ohlc = downloaded_data['OHLC']

    # Refresh the list of tickers, as some of them may have been removed
    tickers = list(df_close.columns)
    # tk = 'MSFT'
    # tk = tickers[0]

    df_ohlc = dict_ohlc[tk]
    ohlc_tk = df_ohlc.copy()
    adj_close_tk = df_adj_close[tk]
    close_tk = df_close[tk]
    open_tk = ohlc_tk['Open']
    high_tk = ohlc_tk['High']
    low_tk = ohlc_tk['Low']
    volume_tk = df_volume[tk]

    # print(df_close)

    # We don't want the benchmark ticker in the app menus at this point (for example, 
    # the drawdown data will not generated) unless tk_market is explicitly selected.

    if tk_market not in tickers_org:
        tickers = tickers[:-1]  # if added by download_data, tk_market would be in the last position

    print(tickers)

##############

def create_ticker_divs(ticker_names: pd.Series):

    ticker_divs = []
    for tk in ticker_names.index:
        name = ticker_names[tk]
        tk_id = f'select-ticker-{tk}'
        tk_icon_id = f'select-ticker-icon-{tk}'
        tk_div = html.Div(
            id = tk_id,
            hidden = True,
            children = [
                html.Div('x', id = tk_icon_id, n_clicks = 0, style = select_ticker_left_css),
                html.Div(children = [
                    html.B(tk, id = f'select-ticker-label-tk-{tk}', style = {'margin-right': '6px'}),
                    html.Span(name, id = f'select-ticker-label-name-{tk}')
                    ],
                    id = f'select-ticker-label-{tk}',
                    style = select_ticker_right_css
                )
            ],
            style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px'}
        )
        ticker_divs.append(tk_div)

    return ticker_divs


ticker_divs = create_ticker_divs(ticker_names)

table = html.Div([
    dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in df_ticker_info.columns],
        data = df_ticker_info.to_dict('records'),
        editable = False,
        row_selectable = 'multi',
        selected_rows=[],
        style_as_list_view = True,
        style_data_conditional = [
            # {'if': {'state': 'active'},'backgroundColor': 'white', 'border': '1px solid white'},
            {'if': {
                'state': 'active'},
                'backgroundColor': 'white',
                'border-top': '1px solid rgb(211, 211, 211)',
                'border-bottom': '1px solid rgb(211, 211, 211)'},
            {'if': {'column_id': ' '}, 'cursor': 'pointer'},
            # {'if': {'column_id': 'Name'}, 'textAlign': 'left', 'text-indent': '10px', 'width': 300},
        ],
        fixed_rows = {'headers': True},
        id = 'ticker-table',
        style_header = input_table_header_css,
        style_data = input_table_data_css,
    )
])

ticker_div_title = html.Div(
    'YOUR PORTFOLIO:',
    style = select_ticker_title_css
)

###########################################################################################

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])

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

app.layout = html.Div([

    html.Div(id = 'ticker-output', hidden = True, style = {'font-size' : '14px'}),

    html.B('remove-ticker-list'),
    html.Div(id = 'remove-ticker-list', hidden = False),

    html.B('select-ticker-list'),
    html.Div(id = 'select-ticker-list', hidden = False),

    html.B('updated-ticker-list'),
    html.Div(id = 'updated-ticker-list', hidden = False),

    # html.Div(id = 'select-ticker-dummy', n_clicks = 0, hidden = True),

    html.Div(
        # ticker_divs,
        id = 'select-ticker-container',
        hidden = False,
        style = select_ticker_container_css
    ),

    html.Div([
        html.Div(
            children = table_title,
            id = 'table-title',
            style = {
                'font-family': 'Helvetica',
                'font-size': '18px',
                'font-weight': 'bold',
                'padding': '5px'
            }
        ),
        table
    ],
        id = 'data-table-container',
        style = input_table_data_css
    ),
    
    html.Br(),

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
                    'width': '300px'
                }
            )
        ),

        dbc.Collapse(

            html.Div(

                id = 'ticker-selection',
                children = [

                    html.Div([
                        html.Div('Ticker',
                            style = {
                                # 'font-family': 'Helvetica',
                                'font-size': '15px',
                                'font-weight': 'bold',
                                'vertical-align': 'top',
                                'margin-bottom': '0px'
                            }
                        ),
                        dcc.Dropdown(
                            id='tickers-dropdown',
                            # options = tickers,
                            value = '',
                            options = ticker_menu_info_list,
                            # value = ticker_menu_info_list[0],
                            # clearable = False,
                            clearable = True,
                            multi = True,
                            style = {
                                'width': '450px',
                                'height': '32px',
                                # 'display': 'inline-block',
                                'margin-top': '0px',
                                'margin-bottom': '0px',
                                # 'margin-right': '5px',
                                'vertical-align': 'top',
                                # 'font-family': 'Helvetica',
                                'font-size': '14px'
                            }                            
                            # style = {'width': '180px'}
                            # style = {'width': '450px', 'height': '24px', 'font-size': '14px'}
                        )],
                        style = {
                            'width': '450px',
                            # 'height': '32px',
                            'display': 'inline-block',
                            # 'margin-top': '0px',
                            # 'margin-bottom': '0px',
                            'margin-right': '5px',
                            # 'vertical-align': 'top',
                            'font-family': 'Helvetica',
                            # 'font-size': '14px'
                        }
                    ),

                ]  # 'ticker_selection' children
            ),  # html.Div id 'ticker_selection'
                    
            id = 'collapse-tickers',
            is_open = False

        )  # dbc.Collapse
    ]),  # html.Div with dbc.Button and dbc.Collapse


])  # app.layout

####################################################################

@app.callback(
    Output('select-ticker-container', 'children'),
    Output('select-ticker-container', 'hidden'),
    Output('ticker-table', 'selected_rows'),
    # Output('remove-ticker-list', 'children', allow_duplicate = True),
    # Output('ticker-output', 'children'),
    Input('ticker-table', 'data'),
    Input('ticker-table', 'selected_rows'),
    Input({'index': ALL, 'type': 'ticker_div'}, 'hidden'),
    # Input('select-ticker-list', 'children'),
    # Input('remove-ticker-list', 'children'),  # This might create a circular reference
    # prevent_initial_call = True
    # Input('select-ticker-container', 'children')
    # suppress_callback_exceptions = True
)
def output_ticker_rows(data, rows, removed_tk):

    # ctx = dash.callback_context

    ticker_divs = [ticker_div_title] # if ticker_divs == [] else ticker_divs
    ticker_divs_visible = [ticker_div_title]
  
    # selected_tickers = []

    hide_ticker_container = False

    if rows == []:
        hide_ticker_container = True

    else:
        # for row_id in rows:
        for row_id in range(len(data)):  # All rows

            tk = data[row_id]['Ticker']
            tk_id = f'select-ticker-{tk}'
            tk_icon_id = f'select-ticker-icon-{tk}'

            if tk_icon_id in removed_tk:
                is_hidden = True
                if row_id in rows:
                    rows.remove(row_id)
            else:
                if row_id in rows:
                    is_hidden = False
                else:
                    is_hidden = True

            # if not is_hidden:
            #     selected_tickers.append(tk)

            name = data[row_id]['Name']
            tk_div = html.Div(
                id = {'index': tk_id, 'type': 'ticker_div'},
                # id = {'index': 'n_clicks', 'type': 'ticker_div'},
                hidden = is_hidden,
                children = [
                    html.Div(
                        'x',
                        id = {'index': tk_id, 'type': 'ticker_icon'},
                        # id = {'index': tk_icon_id, 'type': 'ticker_icon'},
                        # id = {'index': 'n_clicks', 'type': 'ticker_icon'},
                        n_clicks = 0,
                        style = select_ticker_left_css
                    ),
                    html.Div(children = [
                        html.B(tk, id = f'select-ticker-label-tk-{tk}', style = {'margin-right': '6px'}),
                        html.Span(name, id = f'select-ticker-label-name-{tk}')
                        ],
                        id = f'select-ticker-label-{tk}',
                        style = select_ticker_right_css
                    )
                ],
                style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px'}
            )
            ticker_divs.append(tk_div)
            if row_id in rows:
                ticker_divs_visible.append(tk_div)

        hide_ticker_container = True if len(ticker_divs_visible) == 1 else False

    return ticker_divs, hide_ticker_container, rows  #, []  # , selected_tickers


# @app.callback(
#     Output('select-ticker-list', 'children'),
#     Input('updated-ticker-list', 'children')
# )
# def update_selected_tickers(*args):
#     return args


# selected_tickers = update_selected_tickers()


@app.callback(
    Output({'index': MATCH, 'type': 'ticker_div'}, 'hidden'),  #  must match id based on what got triggered
    # Output('remove-ticker-list', 'children'),
    # Input({'index': ALL, 'type': 'ticker_icon'}, 'n_clicks'),
    Input({'index': MATCH, 'type': 'ticker_icon'}, 'n_clicks'),
    # State({'index': MATCH, 'type': 'ticker_icon'}, 'id')
    # prevent_initial_call = 'initial_duplicate'
    # Input('select-ticker-dummy', 'n_clicks')
)
# def remove_selected_ticker(n_clicks, tk_icon_id):
def remove_selected_ticker(n_clicks):
    # if args:
    # if 1 in n_clicks:  # args = ([0, 0, 0, 0, 0],)
    if n_clicks:
        return True
        # ctx = dash.callback_context
        # if ctx.triggered:
        #     # trig_id = ctx.triggered_id  # This is incorrectly set to ctx.triggered[0]['prop_id'].split('.')[0]
        #     trig_value_list = [ctx.triggered[k] for k in range(len(ctx.triggered))]
        #     trig_id_str_list = [ctx.triggered[k]['prop_id'].split('.')[0] for k in range(len(ctx.triggered)) if ctx.triggered[k]['value']]
        #     if len(trig_id_str_list) > 0:
        #         trig_id_str = trig_id_str_list[0]  # this is a stringified dictionary with whitespaces removed
        #         trig_id_list = [trig_id_str.split('{"index":"')[1].split('","type"')[0]]  # select-ticker-icon-{tk}
        #         # trig_id_list = [trig_id_str.split('{"index":"')[1].split('","type"')[0].remove('-icon')]  # select-ticker-{tk}
        #         return trig_id_list  # or the value of 'hidden' if select-ticker-{tk} is used 
        #     else:
        #         # return []
        #         return False
        # else:
        #     # return []
        #     return False
    else: 
        # return []
        return False


# @app.callback(
#     Output('select-ticker-list', 'children'),
#     Input('select-ticker-container', 'children')
#     # Input('select-ticker-icon', 'n_clicks')
# )
# def get_selected_tickers(ticker_divs):
#     ctx = dash.callback_context
#     n_tk_div = len(ticker_divs) - 1
#     tk_div_list = []
#     for k in range(1, n_tk_div):
#         tk_div_list.append(ctx.inputs_list[k]['value'][-1]['props']['children'][0]['props']['id'])
#     return tk_div_list

# @app.callback(
#     # Output('select-ticker_label', 'children'),
#     Output('select-ticker', 'hidden'),
#     # Input('tickers-dropdown', 'value'),
#     Input('select-ticker-icon', 'n_clicks')
# )
# def remove_ticker_select(n):
#     if n:
#         return True
#     else:
#         return False


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
    

if __name__ == '__main__':
    app.run_server(debug=True, port=8053)

