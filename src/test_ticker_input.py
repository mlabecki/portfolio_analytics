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

ticker_names_org = pd.Series(index = df_ticker_info.index, data = df_ticker_info['Name'])

tickers = list(df['Symbol'])
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
    
    # tk = tickers[0]
    # tk = 'MSFT'
    # tk = tickers[0]

    # df_ohlc = dict_ohlc[tk]
    # ohlc_tk = df_ohlc.copy()
    # adj_close_tk = df_adj_close[tk]
    # close_tk = df_close[tk]
    # open_tk = ohlc_tk['Open']
    # high_tk = ohlc_tk['High']
    # low_tk = ohlc_tk['Low']
    # volume_tk = df_volume[tk]

    # print(df_close)

    # We don't want the benchmark ticker in the app menus at this point (for example, 
    # the drawdown data will not generated) unless tk_market is explicitly selected.

    if tk_market not in tickers_org:
        tickers = tickers[:-1]  # if added by download_data, tk_market would be in the last position

    ticker_names = ticker_names_org[tickers]

    print(tickers)
    # print(ticker_names)

##############

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
    'font-weight': 'bold',
    'line-height': '1.5',
    'padding-left': '5px',
    'padding-right': '5px',
    'margin-top': '0px',
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
    'margin-top': '0px',
    'vertical-align': 'center'
}

ticker_div_title = html.Div(
    'YOUR PORTFOLIO:',
    style = {
        'font-family': 'Helvetica',
        'font-size': '14px',
        'font-weight': 'bold',
        'color': 'rgb(0, 126, 255)',
        'margin-top': '5px',
        'margin-bottom': '3px',
        'margin-left': '3px',
        'margin-right': '8px'
    }
)

def create_ticker_divs(ticker_names: pd.Series, ticker_div_title):

    ticker_divs = [ticker_div_title]

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
            style = {
                'display': 'inline-block',
                'margin-right': '5px',
                'margin-bottom': '5px',
                # 'margin-top': '0px',
                'line-height': '1',
                'vertical-align': 'top'
            }
        )
        ticker_divs.append(tk_div)

    return ticker_divs


ticker_divs = create_ticker_divs(ticker_names, ticker_div_title)

tickers_info = {}

###########################################################################################

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.YETI])

app.layout = html.Div([

    html.Div(id = 'ticker-output', hidden = True, style = {'font-size' : '14px'}),

    # html.Div(id = 'remove-ticker-list', hidden = False),

    # html.B('select-ticker-list'),
    html.Div(id = 'select-ticker-list', hidden = True),

    html.Div(
        # children = [], # ticker_divs,
        id = 'select-ticker-container',
        hidden = True,
        style = select_ticker_container_css
    ),

    html.Div([
        html.Div('Type In Ticker', style = {'font-size': '15px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-bottom': '0px'}),
        dbc.Input(
            id = 'custom-ticker-input',
            type = 'text',
            value = '',
            debounce = True,
            placeholder = '',
            style = {'width': '120px', 'height': '36px', 'border-color': 'rgb(204, 204, 204)', 'border-radius': '5px', 'font-size': '15px'}
        ),
        html.Div(
            id = 'ticker-input-message',
            hidden = True,
            style = {
                'font-size': '14px',
                'font-weight': 'bold',
                'vertical-align': 'top',
                'margin-top': '5px',
                'margin-bottom': '5px',
            }
        )],
        style = {
            'display': 'block',
            'margin-right': '5px',
            'margin-left': '5px',
            'vertical-align': 'top',
            'font-family': 'Helvetica'
        }
    ),

    html.Br()

])  # app.layout

####################################################################

@app.callback(
    Output('select-ticker-container', 'children'),
    Output('select-ticker-container', 'hidden'),
    Output('select-ticker-list', 'children'),
    Output('custom-ticker-input', 'value'),
    Output('ticker-input-message', 'hidden'),
    Output('ticker-input-message', 'children'),
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
    selected_tickers,
    ticker_divs,
    tk_input,
    n_clicks):

    ctx = dash.callback_context
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
        hide_tk_input_message = True
        for tk in selected_tickers:
            if tk == remove_tk:
                updated_tickers.remove(tk)

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
        tk_input_message
    )


if __name__ == '__main__':
    app.run_server(debug = True, port = 8055)

