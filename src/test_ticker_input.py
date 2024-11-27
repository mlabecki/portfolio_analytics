import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table
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

hist_data = DownloadData(end_date, start_date)

tk_market = '^GSPC'
# tk_market = 'BTC-USD'

# ticker_categories = [x for x in url_settings.keys() if x != 'global']
# print(ticker_categories)
# Ticker categories:
# 'nasdaq100', 'sp500', 'dow_jones', 'biggest_companies',
# 'biggest_etfs', 'crypto_etfs', 'cryptos', 'cryptos_coin360', 'futures'

max_tickers = 5
# ticker_category = 'crypto_etfs'
# ticker_category = 'biggest_companies'
# ticker_category = 'cryptos'
# df = hist_data.download_from_url(ticker_category, max_tickers)
# 
# category_name = url_settings[ticker_category]['category_name']
# category_sort_by = url_settings[ticker_category]['sort_by']
# title_prefix = 'Top ' if not ('Biggest' in category_name) else ''
# table_title = f'{max_tickers} {title_prefix}{category_name} by {category_sort_by}'
# print(f'\n{title_prefix}{category_name} by {category_sort_by}\n')

tickers_stock_indices = list(stock_index_tickers.keys())
tickers_magnificent_seven = list(magnificent_7_tickers.keys())
tickers_precious_metal_futures = list(precious_metal_futures.keys())
tickers_bond_etfs = list(bond_etf_tickers.keys())
tickers_commodity_etfs = list(commodity_etf_tickers.keys())
tickers_crypto_benchmarks = list(crypto_benchmark_tickers.keys())
tickers_risk_free_treasury = list(risk_free_treasury_tickers.keys())
tickers_volatility_indices = list(volatility_tickers.keys())

input_table_columns = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End']

# df_ticker_info = pd.DataFrame(index = df['Symbol'], columns = input_table_columns)
df_info_tickers_bond_etfs = pd.DataFrame(index = tickers_bond_etfs, columns = input_table_columns)
df_info_tickers_stock_indices = pd.DataFrame(index = tickers_stock_indices, columns = input_table_columns)
df_info_tickers_magnificent_seven = pd.DataFrame(index = tickers_magnificent_seven, columns = input_table_columns)
df_info_tickers_commodity_etfs = pd.DataFrame(index = tickers_commodity_etfs, columns = input_table_columns)
df_info_tickers_crypto_benchmarks = pd.DataFrame(index = tickers_crypto_benchmarks, columns = input_table_columns)
df_info_tickers_precious_metal_futures = pd.DataFrame(index = tickers_precious_metal_futures, columns = input_table_columns)
df_info_tickers_risk_free_treasury = pd.DataFrame(index = tickers_risk_free_treasury, columns = input_table_columns)
df_info_tickers_volatility_indices = pd.DataFrame(index = tickers_volatility_indices, columns = input_table_columns)

# ticker_menu_info = {}
row_ticker_map_bond_etfs = {}
for i, tk in enumerate(tickers_bond_etfs):
    
    yf_tk_hist = yf.Ticker(tk).history(period = 'max')
    yf_tk_info = yf.Ticker(tk).info

    if len(yf_tk_hist.index) > 0:

        tk_start, tk_end = str(yf_tk_hist.index[0].date()), str(yf_tk_hist.index[-1].date())
        # tk_info_full = f"{i + 1}. {tk}: {df.loc[i, 'Name']}, {tk_start}, {tk_end}"

        df_info_tickers_bond_etfs.at[tk, 'No.'] = i + 1
        df_info_tickers_bond_etfs.at[tk, 'Ticker'] = tk

        if 'longName' in yf_tk_info.keys():
            tk_name = yf_tk_info['longName']
        elif 'shortName' in yf_tk_info.keys():
            tk_name = yf_tk_info['shortName']
        else:
            tk_name = bond_etf_tickers[tk]
        df_info_tickers_bond_etfs.at[tk, 'Name'] = tk_name

        df_info_tickers_bond_etfs.at[tk, 'Data Start'] = tk_start
        df_info_tickers_bond_etfs.at[tk, 'Data End'] = tk_end

        row_ticker_map_bond_etfs.update({tk: i})

        # tk_info = f"{tk}: {tk_name}"
        # ticker_menu_info.update({tk_info: tk})

    else:
        print(f'WARNING: Cannot get data for {tk} at the moment, try again later')

# print(df_info_tickers_bond_etfs)

ticker_names_org = pd.Series(index = df_info_tickers_bond_etfs.index, data = df_info_tickers_bond_etfs['Name'])

tickers = df_info_tickers_bond_etfs.index
# ticker_menu_info_list = list(ticker_menu_info.keys())

tickers_org = tickers.copy()  #
print(f'tickers_org = {tickers_org}')

# We don't want the benchmark ticker in the app menus at this point (for example, 
# the drawdown data will not generated) unless tk_market is explicitly selected.

# downloaded_data = hist_data.download_yh_data(start_date, end_date, tickers, tk_market)
# error_msg = downloaded_data['error_msg']
# 
# if error_msg:
#     print(error_msg)
# 
# else:
# 
#     df_adj_close = downloaded_data['Adj Close']
#     df_close = downloaded_data['Close']
#     df_volume = downloaded_data['Volume']
#     dict_ohlc = downloaded_data['OHLC']
# 
#     # Refresh the list of tickers, as some of them may have been removed
#     tickers = list(df_close.columns)
# 
#     # We don't want the benchmark ticker in the app menus at this point (for example, 
#     # the drawdown data will not generated) unless tk_market is explicitly selected.
# 
#     if tk_market not in tickers_org:
#         tickers = tickers[:-1]  # if added by download_data, tk_market would be in the last position
# 
#     ticker_names = ticker_names_org[tickers]
# 
#     print(tickers)
#     # print(ticker_names)

##############

ticker_div_title = html.Div(
    'YOUR PORTFOLIO:',
    style = select_ticker_title_css
)

# def create_ticker_divs(ticker_names: pd.Series, ticker_div_title):
# 
#     ticker_divs = [ticker_div_title]
# 
#     for tk in ticker_names.index:
#         name = ticker_names[tk]
#         tk_id = f'select-ticker-{tk}'
#         tk_icon_id = f'select-ticker-icon-{tk}'
#         tk_div = html.Div(
#             id = tk_id,
#             hidden = True,
#             children = [
#                 html.Div('x', id = tk_icon_id, n_clicks = 0, style = select_ticker_left_css),
#                 html.Div(children = [
#                     html.B(tk, id = f'select-ticker-label-tk-{tk}', style = {'margin-right': '6px'}),
#                     html.Span(name, id = f'select-ticker-label-name-{tk}')
#                     ],
#                     id = f'select-ticker-label-{tk}',
#                     style = select_ticker_right_css
#                 )
#             ],
#             style = {
#                 'display': 'inline-block',
#                 'margin-right': '5px',
#                 'margin-bottom': '5px',
#                 # 'margin-top': '0px',
#                 'line-height': '1',
#                 'vertical-align': 'top'
#             }
#         )
#         ticker_divs.append(tk_div)
# 
#     return ticker_divs


# ticker_divs = create_ticker_divs(ticker_names, ticker_div_title)

table_bond_etfs = html.Div([
    dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in input_table_columns],
        data = df_info_tickers_bond_etfs.to_dict('records'),
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
        id = 'table-bond-etfs',
        style_header = input_table_header_css,
        style_data = input_table_data_css,
    )
])

table_bond_etfs_title = 'Top Bond ETFs by Total Assets'

tickers_info = {}

###########################################################################################

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])

app.layout = html.Div([

    html.Div(id = 'ticker-output', hidden = True, style = {'font-size' : '14px'}),

    # html.Div(id = 'remove-ticker-list', hidden = False),

    # html.B('select-ticker-list'),
    html.Div(id = 'select-ticker-list', hidden = True),

    html.Div(
        id = 'select-ticker-container',
        hidden = True,
        style = select_ticker_container_css
    ),

    html.Div(
        id = 'custom-ticker-input-container',
        children = [
        html.Div(
            'Type In Ticker',
            id = 'custom-ticker-input-title',
            style = custom_ticker_input_title_css
        ),
        dbc.Input(
            id = 'custom-ticker-input',
            type = 'text',
            value = '',
            debounce = True,
            placeholder = '',
            style = custom_ticker_input_css
        ),
        html.Div(
            id = 'custom-ticker-input-message',
            hidden = True,
            style = custom_ticker_input_message_css
        )],
        style = custom_ticker_input_container
    ),

html.Div([
        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        html.Div(
            dbc.Button(
                id = 'collapse-button-table-bond-etfs',
                class_name = 'ma-1',
                color = 'primary',
                size = 'sm',
                n_clicks = 0,
                style = collapse_button_table_css
            )
        ),
        dbc.Collapse(
            html.Div(
                html.Div(
                    id = 'table-bond-etfs-container',
                    children = [
                    html.Div(
                        children = table_bond_etfs_title,
                        id = 'table-bond-etfs-title',
                        style = input_table_title_css
                    ),
                    table_bond_etfs
                    ],
                    style = input_table_container_css
                ),
            ),
            id = 'collapse-table-bond-etfs',
            is_open = False
        )  # dbc.Collapse
    ]),  # html.Div with dbc.Button and dbc.Collapse

    html.Br()

])  # app.layout

####################################################################

@app.callback(
    Output('select-ticker-container', 'children'),
    Output('select-ticker-container', 'hidden'),
    Output('select-ticker-list', 'children'),
    Output('custom-ticker-input', 'value'),
    Output('custom-ticker-input-message', 'hidden'),
    Output('custom-ticker-input-message', 'children'),
    Output('table-bond-etfs', 'selected_rows'),

    Input('table-bond-etfs', 'data'),
    Input('table-bond-etfs', 'selected_rows'),

    # Output('ticker-table', 'selected_rows'),
    # Output('ticker-output', 'children'),
    # Input('ticker-table', 'data'),
    # Input('ticker-table', 'selected_rows'),

    Input('select-ticker-list', 'children'),
    Input('select-ticker-container', 'children'),
    Input('custom-ticker-input', 'value'),
    Input({'index': ALL, 'type': 'ticker_icon'}, 'n_clicks')
    # Input('remove-ticker-list', 'children')  # This might create a circular reference
    # Input('select-ticker-container', 'children')
    # suppress_callback_exceptions = True
)
def output_custom_tickers(
    table_bond_etfs_data,
    table_bond_etfs_selected_rows,
    selected_tickers,
    ticker_divs,
    tk_input,
    n_clicks):

    ctx = dash.callback_context
    # if tk_input is None:
    #     tk_input = ''
    remove_tk = ''

    if 1 in n_clicks:
        if ctx.triggered:
            # trig_value_list = [ctx.triggered[k] for k in range(len(ctx.triggered))]
            trig_id_str_list = [ctx.triggered[k]['prop_id'].split('.')[0] for k in range(len(ctx.triggered)) if ctx.triggered[k]['value']]
            if len(trig_id_str_list) > 0:
                trig_id_str = trig_id_str_list[0]  # this is a stringified dictionary with whitespaces removed
                remove_tk = trig_id_str.split('{"index":"')[1].split('","type"')[0].replace('select-ticker-icon-', '')  # {tk}

    ticker_divs = [ticker_div_title]

    if selected_tickers is None:
        selected_tickers = []

    updated_tickers = selected_tickers

    hide_ticker_container = False if len(updated_tickers) > 0 else True

    #####
    # Read in ticker from input button

    hide_tk_input_message = True
    tk_input_message = ''
    tk_input = tk_input.upper()

    if (tk_input != '') & (tk_input not in selected_tickers):
        
        _ = yf.download(tk_input, progress = False)  
        # Unfortunately a failure of yf.Ticker(tk).info query does not add tk to yf.shared._ERRORS
        if tk_input in yf.shared._ERRORS.keys():
            tk_input_message = f"ERROR: Invalid ticker '{tk_input}'"
            hide_tk_input_message = False
        else:
            updated_tickers.append(tk_input)
            tk_info = yf.Ticker(tk_input).info
            if 'shortName' in tk_info.keys():
                tk_name = tk_info['shortName']
            elif 'longName' in tk_info.keys():
                tk_name = tk_info['longName']
            else:
                tk_name = tk_input
            if tk_input not in tickers_info.keys():
                tickers_info.update({tk_input: tk_name})

    elif (tk_input == '') & (remove_tk != ''):
    # if (tk_input == '') & (remove_tk != ''):
        hide_tk_input_message = True
        for tk in selected_tickers:
            if tk == remove_tk:
                updated_tickers.remove(tk)

    # Map tk_input to the corresponding row_id and add the latter to selected_rows in all relevant tables

    table_bond_etfs_selected_tickers = [tk for tk in row_ticker_map_bond_etfs.keys() if row_ticker_map_bond_etfs[tk] in table_bond_etfs_selected_rows]
    if (tk_input != '') & (tk_input in row_ticker_map_bond_etfs.keys()) & (tk_input not in table_bond_etfs_selected_tickers):
        table_bond_etfs_selected_rows.append(row_ticker_map_bond_etfs[tk_input])

    # Remove tickers that are not selected in the table
    
    table_bond_etfs_nonselected_tickers = [tk for tk in row_ticker_map_bond_etfs.keys() if row_ticker_map_bond_etfs[tk] not in table_bond_etfs_selected_rows]
    table_tickers_remove = []  # This should suffice for all tables
    for tk in updated_tickers:
        if tk in table_bond_etfs_nonselected_tickers:
            if tk not in table_tickers_remove:
                table_tickers_remove.append(tk)
    
    for tk in table_tickers_remove:
        # if tk in updated_tickers:  # -- this shouldn't be necessary
        updated_tickers.remove(tk)

    # Read in tickers from table_bond_etfs

    for row_id in range(len(table_bond_etfs_data)):  # All rows
        
        tk = table_bond_etfs_data[row_id]['Ticker']
        tk_name = table_bond_etfs_data[row_id]['Name']
        
        if row_id in table_bond_etfs_selected_rows:
            
            if tk == remove_tk:
                table_bond_etfs_selected_rows.remove(row_id)
                if tk in updated_tickers:
                    updated_tickers.remove(tk)

            elif tk not in updated_tickers:
                updated_tickers.append(tk)
                if tk not in tickers_info.keys():
                    tickers_info.update({tk: tk_name})

    #######

    for tk in updated_tickers:
        
        tk_id = f'select-ticker-{tk}'
        tk_icon_id = f'select-ticker-icon-{tk}'
        name = tickers_info[tk] if tk in tickers_info.keys() is not None else tk
        # name = tickers_info[tk]
        tk_div = html.Div(
            id = tk_id,
            children = [
                html.Div(
                    'x',
                    id = {'index': tk_icon_id, 'type': 'ticker_icon'},
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
            style = select_ticker_div_css
        )
        ticker_divs.append(tk_div)

    hide_ticker_container = True if len(updated_tickers) == 0 else False

    return (
        ticker_divs,
        hide_ticker_container,
        updated_tickers,
        '',
        hide_tk_input_message,
        tk_input_message,
        table_bond_etfs_selected_rows
    )


@app.callback(
    Output('collapse-button-table-bond-etfs', 'children'),
    Output('collapse-table-bond-etfs', 'is_open'),
    Input('collapse-button-table-bond-etfs', 'n_clicks'),
    State('collapse-table-bond-etfs', 'is_open')
)
def toggle_collapse_tickers(n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    title = 'TOP BOND ETFs'
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open

#######################################################################

if __name__ == '__main__':
    app.run_server(debug = True, port = 8055)

