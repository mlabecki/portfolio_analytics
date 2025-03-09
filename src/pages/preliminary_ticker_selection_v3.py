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
from css_portfolio_analytics import *
from utils import *
from download_info import DownloadInfo


register_page(
    __name__,
    path = '/preliminary_ticker_selection_v3'
    # page_components = [html.Div('')]
)

hist_info = DownloadInfo()

max_tickers = {
    'biggest_companies': 100,
    'sp500': 100,
    'nasdaq100': 120,
    'dow_jones': 35,
    'car_companies': 75,
    # 'car_companies': 10,
    'rare_metals_companies': 20,
    'quantum_companies': 50,
    'biggest_etfs': 100,
    'fixed_income_etfs': 100,
    'ai_etfs': 50,
    'precious_metals': 20, # ETFs
    'commodity_etfs': 50,
    'currency_etfs': 10,
    'cryptos': 100, 
    'crypto_etfs': 100,
    'futures': 100,
    'fx': 152,
    'stock_indices': 20,
    'volatility_indices': 10,
    'benchmarks': 30
}
etf_categories = [
    'biggest_etfs',
    'fixed_income_etfs',
    'ai_etfs',
    'precious_metals',
    'commodity_etfs',
    'currency_etfs',
    'crypto_etfs'
]
pre_table_columns = ['No.', 'Ticker', 'Name']
pre_table_columns_fx = ['No.', 'Ticker', 'Name', 'Currency Name', 'Currency Region', 'Currency Group']
# Ticker: 'CAD=X', 'AUD=X', 'KWD=X' ...
# Name: 'CAD/USD', 'AUD/USD', 'KWD/USD' ...
# Currency Name: 'Canadian Dollar', 'Australian Dollar', 'Kuwaiti Dinar' ...
# Currency Region: 'North America', 'Oceania', 'Middle East' ...
# Currency Group: 'Major', 'Major', 'Minor' ...

n_currencies_major = len(currencies_major)
n_currencies_minor = len(currencies_minor)
n_currencies_all = len(currencies_all)
indices_currencies_major = list(range(n_currencies_major))
indices_currencies_minor = list(range(n_currencies_major, n_currencies_all))
indices_currencies_all = list(range(n_currencies_all))

indices_currencies_europe = [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'Europe']
indices_currencies_africa = [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'Africa']
indices_currencies_middle_east= [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'Middle East']
indices_currencies_east_asia = [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'East Asia']
indices_currencies_central_asia = [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'Central Asia']
indices_currencies_south_asia = [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'South Asia']
indices_currencies_south_america = [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'South America']
indices_currencies_north_america = [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'North America']
indices_currencies_oceania = [idx for idx, currency in enumerate(currencies_combined_regions.keys()) if currencies_combined_regions[currency] == 'Oceania']

###########################################################################################
### LAYOUT
###

layout = html.Div([

    # LOADING WRAPPER
    dcc.Loading([

    html.Div(id = 'ticker-output', hidden = True, style = {'font-size' : '14px'}),

    # MAIN TITLE
    html.Div(
        'Pre-select ticker categories or individual tickers to extract more details about',
        id = 'ticker-main-title',
        style = ticker_main_title_css
    ),

    html.Div(id = 'pre-select-ticker-list', hidden = True),
    html.Div(id = 'pre-select-ticker-list-check', hidden = False),

    # html.Div(children = [], id = 'prev-table-selected-rows', hidden = True),
    # dcc.Store(data = {}, id = 'pre-prev-table-selected-rows', storage_type = 'session'),
    # dcc.Store(data = {}, id = 'tk-selected-category-map', storage_type = 'session'),
    # dcc.Store(data = [], id = 'preselected-categories', storage_type = 'session'),

    dcc.Store(data = {}, id = 'ticker-category-info-map', storage_type = 'session'),
    dcc.Store(data = {}, id = 'ticker-names', storage_type = 'session'),

    dcc.Store(data = {}, id = 'pre-prev-table-selected-rows', storage_type = 'memory'),
    dcc.Store(data = {}, id = 'tk-selected-category-map', storage_type = 'memory'),
    dcc.Store(data = [], id = 'preselected-categories', storage_type = 'memory'),

    # YOUR PORTFOLIO
    html.Div(
        id = 'pre-select-ticker-container',
        hidden = True,
        style = select_ticker_container_css
    ),

    ################
    html.Div([
        html.Div(
            'Total distinct tickers pre-selected:',
            style = {
                'display': 'inline-block',
                'font-family': 'Helvetica',
                'font-size': '16px',
                'font-weight': 'bold',
                'text-align': 'left',
                'vertical-align': 'middle',
                # 'margin-top': '5px',
                'margin-bottom': '5px',
                'margin-left': '5px'
            }
        ),
        html.Div(
            id = 'pre-selected-tickers-total',
            # hidden = True,
            style = {
                'display': 'inline-block',
                'font-family': 'Helvetica',
                'font-size': '16px',
                'font-weight': 'bold',
                'text-align': 'left',
                'color': 'darkgreen',
                'vertical-align': 'middle',
                # 'margin-top': '5px',
                'margin-bottom': '5px',
                'margin-left': '5px'
            }
        ),
    ]),

    ################

    html.Div(
        id = 'pre-all-tables-container',
        # children = pre_tables
    ),
],
    
    id = 'ticker-input-loading-wrapper',
    custom_spinner = html.Div([
        html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),
        html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),
        'Loading Ticker Categories',
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
            dcc.Link('Start Over Category Selection', href='/'),
            html.Br(),
            dcc.Link('Continue to Ticker Info & Portfolio Selection', href='/test_ticker_input_v3')
        ],
        style = link_container_css
    )

])  # app.layout

#######################################

for category in category_titles_ids.keys():
    init_ticker_category_info_map[category]['df'] = {}
    init_ticker_category_info_map[category]['row'] = {}
    init_ticker_category_info_map[category]['dict'] = {}

#######################################

@callback(
    Output('pre-all-tables-container', 'children'),
    Output('ticker-category-info-map', 'data'),
    Output('ticker-names', 'data'),
    Input('selected-categories-stored', 'data')
)
def generate_preselected_tables(
    selected_categories_stored
):

    for category in init_ticker_category_info_map.keys():
        
        if category in selected_categories_stored:
            
            if category in url_settings.keys():
                # Get tickers (index) and sort them
                df_cat = hist_info.download_from_url(category, max_tickers[category])
                dict_cat = df_cat[['Symbol', 'Name']].set_index('Symbol')['Name'].to_dict()
            else:
                dict_cat = tickers_non_url[category]  # in mapping_tickers

            # tickers_cat = list(dict_cat.keys())
            # init_ticker_category_info_map[category]['df'].index = tickers_cat
            init_ticker_category_info_map[category]['dict'] = dict_cat
            # init_ticker_category_info_map[category]['df'].columns = pre_table_columns

    ############

    ticker_names = {}  # To help user decide on tickers based on the name

    def create_pre_table(
        category,
        tk_cat_info_map
    ):

        # df_pre_tickers = tk_cat_info_map[category]['df']  # A dataframe
        row_ticker_map = tk_cat_info_map[category]['row']
        dict_info_tickers = tk_cat_info_map[category]['dict']
        tk_sort_by = tk_cat_info_map[category]['sort_by']

        # For fx, the dictionary keys are 3-letter currency ISO codes, not YF tickers
        fx_suffix_tk = 'USD=X' if category == 'fx' else ''
        fx_suffix_name = '/USD' if category == 'fx' else ''
        category_tickers = [tk + fx_suffix_tk for tk in dict_info_tickers.keys()]
        
        n_tickers = min(len(category_tickers), max_tickers[category])
        category_tickers = category_tickers[: n_tickers]
        max_tickers[category] = n_tickers

        category_tickers_sorted = category_tickers

        df_pre_tickers = pd.DataFrame(index = category_tickers)

        # Sort ticker list by marketCap (equities), totalAssets (ETFs) or openInterest (futures)

        if tk_sort_by != '':
            # This means that the tickers are NOT from a URL and are NOT fx (currencies)
        
            dict_tickers_values = {}
            dict_currency_fx_rates = {}
            for tk in category_tickers:
                tk_info = yf.Ticker(tk).info
                currency = tk_info['currency']
                if currency != 'USD':
                    if currency in dict_currency_fx_rates.keys():
                        dict_tickers_values.update({currency: dict_currency_fx_rates[currency]})
                    else:
                        fx_rate = hist_info.get_usd_fx_rate(currency)
                        fx_rate = 1 if fx_rate == 0 else fx_rate
                        dict_tickers_values.update({tk: tk_info[tk_sort_by] / fx_rate})
                        dict_currency_fx_rates.update({tk: fx_rate})
                else:
                    dict_tickers_values.update({tk: tk_info[tk_sort_by]})

            category_tickers_sorted = [i[0] for i in sorted(dict_tickers_values.items(), key=itemgetter(1), reverse=True)]
            df_pre_tickers.index = category_tickers_sorted  

        for i, tk in enumerate(category_tickers_sorted):

            if tk not in ticker_names.keys():

                df_pre_tickers.at[tk, 'No.'] = i + 1
                df_pre_tickers.at[tk, 'Ticker'] = tk
                if category == 'fx':
                    currency = tk.replace(fx_suffix_tk, '')
                    tk_name = currency + fx_suffix_name
                else:
                    tk_name = dict_info_tickers[tk]
                df_pre_tickers.at[tk, 'Name'] = tk_name
                ticker_names.update({tk: tk_name})
                if category == 'fx':
                    df_pre_tickers.at[tk, 'Currency Name'] = currencies_combined[currency]
                    df_pre_tickers.at[tk, 'Currency Region'] = currencies_combined_regions[currency]
                    df_pre_tickers.at[tk, 'Currency Group'] = 'Major' if currency in currencies_major.keys() else 'Minor'

            else:
                # In case the ticker is in multiple categories
                # NOTE: Non-crypto currencies will only be in the fx category

                df_pre_tickers.at[tk, 'No.'] = i + 1
                df_pre_tickers.at[tk, 'Ticker'] = tk
                if tk in bond_etfs.keys():
                    # To avoid corrupt names at https://8marketcap.com/etfs/
                    df_pre_tickers.at[tk, 'Name'] = bond_etfs[tk]
                else:
                    df_pre_tickers.at[tk, 'Name'] = ticker_names[tk]

            row_ticker_map.update({tk: i})  # {'AED=X'}: 0 for fx!

        pre_table_data = {
            'df': df_pre_tickers,
            'row': row_ticker_map,
            'maxn': n_tickers
        }

        return pre_table_data

    ##############

    df_ticker_category_info_map = {}  # Dictionary of dataframes
    for category in init_ticker_category_info_map.keys():
        df_ticker_category_info_map[category] = pd.DataFrame()
    
    for category in selected_categories_stored:
        print(f'\nProcessing {category} ...')
        pre_table_data = create_pre_table(category, init_ticker_category_info_map)
        df_ticker_category_info_map[category] = pre_table_data['df']
        init_ticker_category_info_map[category]['row'] = pre_table_data['row']
        max_tickers.update({category: pre_table_data['maxn']})
        # print(init_ticker_category_info_map[category]['df'])
        # print(init_ticker_category_info_map[category]['row'])

    pre_table_titles = {
        'biggest_companies': f'{max_tickers["biggest_companies"]} BIGGEST COMPANIES by Market Capitalization',
        'sp500': f'{max_tickers["sp500"]} S&P 500 COMPANIES by Market Capitalization',
        'nasdaq100': f'{max_tickers["nasdaq100"]} NASDAQ 100 COMPANIES by Market Capitalization',
        'dow_jones': f'{max_tickers["dow_jones"]} DOW JONES INDUSTRIAL AVERAGE COMPANIES by Market Capitalization',
        'car_companies': f'{max_tickers["car_companies"]} CAR COMPANIES by Market Capitalization',
        'rare_metals_companies': f'{max_tickers["rare_metals_companies"]} RARE METAL COMPANIES by Market Capitalization',
        'quantum_companies': f'{max_tickers["quantum_companies"]} QUANTUM COMPUTING COMPANIES by Market Capitalization',
        'biggest_etfs': f'{max_tickers["biggest_etfs"]} BIGGEST ETFs by Total Assets Under Management',
        'fixed_income_etfs': f'{max_tickers["fixed_income_etfs"]} FIXED INCOME ETFs by Total Assets Under Management',
        'ai_etfs': f'{max_tickers["ai_etfs"]} ARTIFICIAL INTELLIGENCE ETFs by Total Assets Under Management',
        'precious_metals': f'{max_tickers["precious_metals"]} PRECIOUS METAL ETFs sorted by Total Assets Under Management',
        'commodity_etfs': f'{max_tickers["commodity_etfs"]} COMMODITY ETFs sorted by Total Assets Under Management',
        'currency_etfs': f'{max_tickers["currency_etfs"]} CURRENCY ETFs sorted by Total Assets Under Management',
        'cryptos': f'{max_tickers["cryptos"]} CRYPTOCURRENCIES by Market Capitalization',
        'crypto_etfs': f'{max_tickers["crypto_etfs"]} CRYPTOCURRENCY ETFs by Total Assets Under Management',
        'futures': f'{max_tickers["futures"]} COMMODITY FUTURES by Open Interest',
        'fx': f'{n_currencies_major} MAJOR & {n_currencies_minor} OTHER CURRENCY EXCHANGE RATES to USD',
        'stock_indices': f'{max_tickers["stock_indices"]} STOCK INDICES',
        'volatility_indices': f'{max_tickers["volatility_indices"]} VOLATILITY INDICES',
        'benchmarks': f'{max_tickers["benchmarks"]} BENCHMARKS'
    }

    print(f'\nTotal tickers: {len(ticker_names)}')

    ##############

    pre_selection_table = {}  # A dictionary mapping ticker category to the corresponding pre-selection table
    pre_selection_table_collapse_div = {}
    pre_tables = []

    for category in init_ticker_category_info_map.keys():
        # There could be issues with non-existent callback IDs later if the loop is over selected_categories_stored only
        # ??...

        id_string = init_ticker_category_info_map[category]['id_string']

        if category in selected_categories_stored:
            table_columns = [{'name': i, 'id': i} for i in df_ticker_category_info_map[category].columns]
            table_data = df_ticker_category_info_map[category].to_dict('records')
        else:
            table_columns = []
            table_data = []

        if category == 'fx':
            conditional_css = [
                {'if': {'state': 'active'},
                    'background': 'grey',
                    'border-top': '1px solid rgb(211, 211, 211)',
                    'border-bottom': '1px solid rgb(211, 211, 211)'},
                {'if': {'column_id': 'No.'}, 'width': 24},
                {'if': {'column_id': 'Ticker'}, 'width': 95},
                {'if': {'column_id': 'Name'}, 'width': 85},
                # {'if': {'column_id': 'Currency Region'}, 'width': 95},
                # {'if': {'row_index': [idx for idx in range(indices_currencies_major[-1] + 1, indices_currencies_all[-1] + 1)]},
                {'if': {
                    'filter_query': '{Currency Group} = Minor',
                    # 'column_id': 'Currency Group'
                    },
                    'background': 'rgb(225, 225, 225)',
                    'border-bottom': '1px solid rgb(185, 185, 185)'},
                {'if': {'row_index': indices_currencies_major[-1]}, 'border-bottom': '2px solid rgb(55, 55, 55)'}                    
            ]
        else:
            conditional_css = [
                {'if': {'state': 'active'},
                    'background-color': 'white',
                    'border-top': '1px solid rgb(211, 211, 211)',
                    'border-bottom': '1px solid rgb(211, 211, 211)'},
                {'if': {'column_id': 'No.'}, 'width': 24},
                {'if': {'column_id': 'Ticker'}, 'width': 95},
            ]
    
        pre_selection_table[category] = html.Div([
            dash_table.DataTable(
                columns = table_columns,
                data = table_data,
                editable = False,
                row_selectable = 'multi',
                selected_rows = [],
                style_as_list_view = True,
                id = f'pre-dash-table-{id_string}',
                style_header = input_table_header_css,
                style_data = input_table_data_css,
                style_data_conditional = conditional_css                
            )
        ])

        hidden_cat = False if category in selected_categories_stored else True
        hidden_major = False if category == 'fx' else True

        pre_selection_table_collapse_div[category] = html.Div(
            hidden = hidden_cat,
            children =
            [
                html.Div(
                    init_ticker_category_info_map[category]['collapse_title'],
                    id = f'pre-collapse-button-title-{id_string}',
                    hidden = True
                ),

                html.Div([
                    dbc.Button(
                        id = f'pre-collapse-button-table-{id_string}',
                        class_name = 'ma-1',
                        color = 'primary',
                        size = 'sm',
                        n_clicks = 0,
                        style = collapse_button_pre_table_css
                    ),
                    html.Div(
                        id = f'n-preselected-{id_string}-container',
                        children = [
                            html.Div(
                                id = f'n-preselected-{id_string}',
                                hidden = False,
                                style = n_selected_category_css
                            ),
                            html.Div(
                                f'/ {max_tickers[category]}',
                                hidden = False,
                                style = n_tickers_category_css
                            ),
                            html.Div(
                                'pre-selected',
                                hidden = False,
                                style = selected_string_css
                            )
                        ],
                        style = {'display': 'inline-block'}
                    )
                ]),

                dbc.Collapse(
                    html.Div(
                        html.Div(
                            id = f'pre-category-{id_string}-container',
                            children = [

                                html.Div(
                                    id = f'pre-menu-{id_string}-container',
                                    children = [

                                        ### Select buttons
                                        html.Div(
                                            id = f'pre-menu-{id_string}-select-buttons-container',
                                            style = {'margin-bottom': '10px', 'margin-left': '10px'},
                                            children = [
                                                dbc.Button(
                                                    'Select All',
                                                    id = f'pre-menu-{id_string}-select-all-button',
                                                    n_clicks = 0,
                                                    class_name = 'ma-1',
                                                    color = 'success',
                                                    size = 'sm',
                                                    style = pre_menu_select_all_button_css
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Select Major',
                                                        id = f'pre-menu-{id_string}-select-major-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Select Minor',
                                                        id = f'pre-menu-{id_string}-select-minor-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Select Africa',
                                                        id = f'pre-menu-{id_string}-select-africa-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Select Central Asia',
                                                        id = f'pre-menu-{id_string}-select-central-asia-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),                                                
                                                html.Div([
                                                    dbc.Button(
                                                        'Select East Asia',
                                                        id = f'pre-menu-{id_string}-select-east-asia-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),                                                
                                                html.Div([
                                                    dbc.Button(
                                                        'Select Europe',
                                                        id = f'pre-menu-{id_string}-select-europe-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),                    
                                                html.Div([
                                                    dbc.Button(
                                                        'Select Middle East',
                                                        id = f'pre-menu-{id_string}-select-middle-east-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Select North America',
                                                        id = f'pre-menu-{id_string}-select-north-america-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Select Oceania',
                                                        id = f'pre-menu-{id_string}-select-oceania-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Select South America',
                                                        id = f'pre-menu-{id_string}-select-south-america-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Select South Asia',
                                                        id = f'pre-menu-{id_string}-select-south-asia-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'success',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),

                                                html.Div(
                                                    id = 'pre-menu-{id_string}-select-first-last-tickers-container',
                                                    hidden = not hidden_major,
                                                    children = [
                                                        html.Div('Select Ticker Range', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '5px', 'margin-left': '2px'}),
                                                        html.Div([
                                                            html.Div(
                                                                'First No.',
                                                                style = {
                                                                    'font-size': '14px',
                                                                    'vertical-align': 'top',
                                                                    'margin-bottom': '0px',
                                                                    'margin-left': '2px',
                                                                    'margin-right': '0px'
                                                                }
                                                            ),
                                                            dbc.Input(
                                                                id = f'pre-menu-{id_string}-select-first-ticker-input',
                                                                type = 'number',
                                                                min = 1,
                                                                max = max_tickers[category],
                                                                step = 1,
                                                                debounce = True,
                                                                style = pre_menu_input_css
                                                            )],
                                                            style = pre_menu_item_css
                                                        ),
                                                        html.Div([
                                                            html.Div(
                                                                'Last No.',
                                                                style = {
                                                                    'font-size': '14px',
                                                                    'vertical-align': 'top',
                                                                    'margin-bottom': '0px',
                                                                    'margin-left': '2px',
                                                                    'margin-right': '4px'
                                                                }
                                                            ),
                                                            dbc.Input(
                                                                id = f'pre-menu-{id_string}-select-last-ticker-input',
                                                                type = 'number',
                                                                min = 1,
                                                                max = max_tickers[category],
                                                                step = 1,
                                                                debounce = True,
                                                                style = pre_menu_input_css
                                                            )],
                                                            style = pre_menu_item_css
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),

                                        ### Unselect buttons
                                        html.Div(
                                            id = f'pre-menu-{id_string}-unselect-buttons-container',
                                            style = {'margin': '10px 0px 10px 10px'},
                                            children = [
                                                dbc.Button(
                                                    'Unselect All',
                                                    id = f'pre-menu-{id_string}-unselect-all-button',
                                                    n_clicks = 0,
                                                    class_name = 'ma-1',
                                                    color = 'danger',
                                                    size = 'sm',
                                                    style = pre_menu_select_all_button_css
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect Major',
                                                        id = f'pre-menu-{id_string}-unselect-major-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect Minor',
                                                        id = f'pre-menu-{id_string}-unselect-minor-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect Africa',
                                                        id = f'pre-menu-{id_string}-unselect-africa-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect Central Asia',
                                                        id = f'pre-menu-{id_string}-unselect-central-asia-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),                                                
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect East Asia',
                                                        id = f'pre-menu-{id_string}-unselect-east-asia-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),                                                
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect Europe',
                                                        id = f'pre-menu-{id_string}-unselect-europe-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),                    
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect Middle East',
                                                        id = f'pre-menu-{id_string}-unselect-middle-east-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect North America',
                                                        id = f'pre-menu-{id_string}-unselect-north-america-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect Oceania',
                                                        id = f'pre-menu-{id_string}-unselect-oceania-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect South America',
                                                        id = f'pre-menu-{id_string}-unselect-south-america-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),
                                                html.Div([
                                                    dbc.Button(
                                                        'Unselect South Asia',
                                                        id = f'pre-menu-{id_string}-unselect-south-asia-button',
                                                        n_clicks = 0,
                                                        class_name = 'ma-1',
                                                        color = 'danger',
                                                        size = 'sm',
                                                        style = pre_menu_select_major_button_css
                                                    )],
                                                    hidden = hidden_major
                                                ),

                                                html.Div(
                                                    id = 'pre-menu-{id_string}-unselect-first-last-tickers-container',
                                                    hidden = not hidden_major,                                                    
                                                    children = [
                                                        html.Div('Unselect Ticker Range', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '5px', 'margin-left': '2px'}),
                                                        html.Div([
                                                            html.Div(
                                                                'First No.',
                                                                style = {
                                                                    'font-size': '14px',
                                                                    'vertical-align': 'top',
                                                                    'margin-bottom': '0px',
                                                                    'margin-left': '2px',
                                                                    'margin-right': '0px'
                                                                }
                                                            ),
                                                            dbc.Input(
                                                                id = f'pre-menu-{id_string}-unselect-first-ticker-input',
                                                                type = 'number',
                                                                min = 1,
                                                                max = max_tickers[category],
                                                                step = 1,
                                                                debounce = True,
                                                                style = pre_menu_input_css
                                                            )],
                                                            style = pre_menu_item_css
                                                        ),
                                                        html.Div([
                                                            html.Div(
                                                                'Last No.',
                                                                style = {
                                                                    'font-size': '14px',
                                                                    'vertical-align': 'top',
                                                                    'margin-bottom': '0px',
                                                                    'margin-left': '2px',
                                                                    'margin-right': '4px'
                                                                }
                                                            ),
                                                            dbc.Input(
                                                                id = f'pre-menu-{id_string}-unselect-last-ticker-input',
                                                                type = 'number',
                                                                min = 1,
                                                                max = max_tickers[category],
                                                                step = 1,
                                                                debounce = True,
                                                                style = pre_menu_input_css
                                                            )],
                                                            style = pre_menu_item_css
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    style = pre_menu_container_css
                                ),

                                html.Div(
                                    id = f'pre-table-{id_string}-container',
                                    children = [
                                    html.Div(
                                        children = pre_table_titles[category],
                                        id = f'pre-table-{id_string}-title',
                                        style = input_table_title_css
                                    ),
                                    pre_selection_table[category]
                                    ],
                                    style = pre_table_container_css
                                )
                            ],
                            # style = {'display': 'inline-block'}
                        ),
                    ),
                    id = f'pre-collapse-table-{id_string}',
                    is_open = False
                ),  # dbc.Collapse
            ]
        )  # html.Div with dbc.Button and dbc.Collapse

        pre_tables.append(pre_selection_table_collapse_div[category])

        init_ticker_category_info_map[category]['df'] = df_ticker_category_info_map[category].to_dict()

    return (
        pre_tables,
        init_ticker_category_info_map,
        ticker_names
    )

####################################################################

# @app.callback(
@callback(        
    Output('pre-select-ticker-container', 'children'),
    Output('pre-select-ticker-container', 'hidden'),
    Output('pre-select-ticker-list', 'children'),
    Output('pre-prev-table-selected-rows', 'data'),

    Output('pre-menu-biggest-companies-select-all-button', 'n_clicks'),
    Output('pre-menu-sp500-select-all-button', 'n_clicks'),
    Output('pre-menu-nasdaq100-select-all-button', 'n_clicks'),
    Output('pre-menu-dow-jones-select-all-button', 'n_clicks'),
    Output('pre-menu-car-companies-select-all-button', 'n_clicks'),
    Output('pre-menu-rare-metals-companies-select-all-button', 'n_clicks'),
    Output('pre-menu-quantum-companies-select-all-button', 'n_clicks'),
    Output('pre-menu-biggest-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-fixed-income-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-ai-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-commodity-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-currency-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-cryptos-select-all-button', 'n_clicks'),
    Output('pre-menu-crypto-etfs-select-all-button', 'n_clicks'),
    Output('pre-menu-futures-select-all-button', 'n_clicks'),
    Output('pre-menu-fx-select-all-button', 'n_clicks'),
    Output('pre-menu-precious-metals-select-all-button', 'n_clicks'),
    Output('pre-menu-stock-indices-select-all-button', 'n_clicks'),
    Output('pre-menu-volatility-indices-select-all-button', 'n_clicks'),
    Output('pre-menu-benchmarks-select-all-button', 'n_clicks'),

    Output('pre-menu-fx-select-major-button', 'n_clicks'),
    Output('pre-menu-fx-select-minor-button', 'n_clicks'),
    Output('pre-menu-fx-select-africa-button', 'n_clicks'),
    Output('pre-menu-fx-select-europe-button', 'n_clicks'),
    Output('pre-menu-fx-select-middle-east-button', 'n_clicks'),
    Output('pre-menu-fx-select-east-asia-button', 'n_clicks'),
    Output('pre-menu-fx-select-central-asia-button', 'n_clicks'),
    Output('pre-menu-fx-select-south-asia-button', 'n_clicks'),
    Output('pre-menu-fx-select-south-america-button', 'n_clicks'),
    Output('pre-menu-fx-select-north-america-button', 'n_clicks'),
    Output('pre-menu-fx-select-oceania-button', 'n_clicks'),

    Output('pre-menu-biggest-companies-unselect-all-button', 'n_clicks'),
    Output('pre-menu-sp500-unselect-all-button', 'n_clicks'),
    Output('pre-menu-nasdaq100-unselect-all-button', 'n_clicks'),
    Output('pre-menu-dow-jones-unselect-all-button', 'n_clicks'),
    Output('pre-menu-car-companies-unselect-all-button', 'n_clicks'),
    Output('pre-menu-quantum-companies-unselect-all-button', 'n_clicks'),
    Output('pre-menu-rare-metals-companies-unselect-all-button', 'n_clicks'),
    Output('pre-menu-biggest-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-fixed-income-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-ai-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-commodity-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-currency-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-cryptos-unselect-all-button', 'n_clicks'),
    Output('pre-menu-crypto-etfs-unselect-all-button', 'n_clicks'),
    Output('pre-menu-futures-unselect-all-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-all-button', 'n_clicks'),
    Output('pre-menu-precious-metals-unselect-all-button', 'n_clicks'),
    Output('pre-menu-stock-indices-unselect-all-button', 'n_clicks'),
    Output('pre-menu-volatility-indices-unselect-all-button', 'n_clicks'),
    Output('pre-menu-benchmarks-unselect-all-button', 'n_clicks'),

    Output('pre-menu-fx-unselect-major-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-minor-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-africa-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-europe-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-middle-east-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-east-asia-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-central-asia-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-south-asia-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-south-america-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-north-america-button', 'n_clicks'),
    Output('pre-menu-fx-unselect-oceania-button', 'n_clicks'),

    Output('pre-menu-biggest-companies-select-first-ticker-input', 'value'),
    Output('pre-menu-sp500-select-first-ticker-input', 'value'),
    Output('pre-menu-nasdaq100-select-first-ticker-input', 'value'),
    Output('pre-menu-dow-jones-select-first-ticker-input', 'value'),
    Output('pre-menu-car-companies-select-first-ticker-input', 'value'),
    Output('pre-menu-rare-metals-companies-select-first-ticker-input', 'value'),
    Output('pre-menu-quantum-companies-select-first-ticker-input', 'value'),
    Output('pre-menu-biggest-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-fixed-income-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-ai-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-commodity-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-currency-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-cryptos-select-first-ticker-input', 'value'),
    Output('pre-menu-crypto-etfs-select-first-ticker-input', 'value'),
    Output('pre-menu-futures-select-first-ticker-input', 'value'),
    Output('pre-menu-fx-select-first-ticker-input', 'value'),
    Output('pre-menu-precious-metals-select-first-ticker-input', 'value'),
    Output('pre-menu-stock-indices-select-first-ticker-input', 'value'),
    Output('pre-menu-volatility-indices-select-first-ticker-input', 'value'),
    Output('pre-menu-benchmarks-select-first-ticker-input', 'value'),

    Output('pre-menu-biggest-companies-select-last-ticker-input', 'value'),
    Output('pre-menu-sp500-select-last-ticker-input', 'value'),
    Output('pre-menu-nasdaq100-select-last-ticker-input', 'value'),
    Output('pre-menu-dow-jones-select-last-ticker-input', 'value'),
    Output('pre-menu-car-companies-select-last-ticker-input', 'value'),
    Output('pre-menu-rare-metals-companies-select-last-ticker-input', 'value'),
    Output('pre-menu-quantum-companies-select-last-ticker-input', 'value'),
    Output('pre-menu-biggest-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-fixed-income-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-ai-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-commodity-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-currency-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-cryptos-select-last-ticker-input', 'value'),
    Output('pre-menu-crypto-etfs-select-last-ticker-input', 'value'),
    Output('pre-menu-futures-select-last-ticker-input', 'value'),
    Output('pre-menu-fx-select-last-ticker-input', 'value'),
    Output('pre-menu-precious-metals-select-last-ticker-input', 'value'),
    Output('pre-menu-stock-indices-select-last-ticker-input', 'value'),
    Output('pre-menu-volatility-indices-select-last-ticker-input', 'value'),
    Output('pre-menu-benchmarks-select-last-ticker-input', 'value'),

    Output('pre-menu-biggest-companies-unselect-first-ticker-input', 'value'),
    Output('pre-menu-sp500-unselect-first-ticker-input', 'value'),
    Output('pre-menu-nasdaq100-unselect-first-ticker-input', 'value'),
    Output('pre-menu-dow-jones-unselect-first-ticker-input', 'value'),
    Output('pre-menu-car-companies-unselect-first-ticker-input', 'value'),
    Output('pre-menu-rare-metals-companies-unselect-first-ticker-input', 'value'),
    Output('pre-menu-quantum-companies-unselect-first-ticker-input', 'value'),
    Output('pre-menu-biggest-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-fixed-income-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-ai-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-commodity-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-currency-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-cryptos-unselect-first-ticker-input', 'value'),
    Output('pre-menu-crypto-etfs-unselect-first-ticker-input', 'value'),
    Output('pre-menu-futures-unselect-first-ticker-input', 'value'),
    Output('pre-menu-fx-unselect-first-ticker-input', 'value'),
    Output('pre-menu-precious-metals-unselect-first-ticker-input', 'value'),
    Output('pre-menu-stock-indices-unselect-first-ticker-input', 'value'),
    Output('pre-menu-volatility-indices-unselect-first-ticker-input', 'value'),
    Output('pre-menu-benchmarks-unselect-first-ticker-input', 'value'),

    Output('pre-menu-biggest-companies-unselect-last-ticker-input', 'value'),
    Output('pre-menu-sp500-unselect-last-ticker-input', 'value'),
    Output('pre-menu-nasdaq100-unselect-last-ticker-input', 'value'),
    Output('pre-menu-dow-jones-unselect-last-ticker-input', 'value'),
    Output('pre-menu-car-companies-unselect-last-ticker-input', 'value'),
    Output('pre-menu-rare-metals-companies-unselect-last-ticker-input', 'value'),
    Output('pre-menu-quantum-companies-unselect-last-ticker-input', 'value'),
    Output('pre-menu-biggest-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-fixed-income-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-ai-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-commodity-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-currency-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-cryptos-unselect-last-ticker-input', 'value'),
    Output('pre-menu-crypto-etfs-unselect-last-ticker-input', 'value'),
    Output('pre-menu-futures-unselect-last-ticker-input', 'value'),
    Output('pre-menu-fx-unselect-last-ticker-input', 'value'),    
    Output('pre-menu-precious-metals-unselect-last-ticker-input', 'value'),
    Output('pre-menu-stock-indices-unselect-last-ticker-input', 'value'),
    Output('pre-menu-volatility-indices-unselect-last-ticker-input', 'value'),
    Output('pre-menu-benchmarks-unselect-last-ticker-input', 'value'),

    Output('pre-dash-table-biggest-companies', 'selected_rows'),
    Output('pre-dash-table-sp500', 'selected_rows'),
    Output('pre-dash-table-nasdaq100', 'selected_rows'),
    Output('pre-dash-table-dow-jones', 'selected_rows'),
    Output('pre-dash-table-car-companies', 'selected_rows'),
    Output('pre-dash-table-rare-metals-companies', 'selected_rows'),
    Output('pre-dash-table-quantum-companies', 'selected_rows'),
    Output('pre-dash-table-biggest-etfs', 'selected_rows'),
    Output('pre-dash-table-fixed-income-etfs', 'selected_rows'),
    Output('pre-dash-table-ai-etfs', 'selected_rows'),
    Output('pre-dash-table-commodity-etfs', 'selected_rows'),
    Output('pre-dash-table-currency-etfs', 'selected_rows'),
    Output('pre-dash-table-cryptos', 'selected_rows'),
    Output('pre-dash-table-crypto-etfs', 'selected_rows'),
    Output('pre-dash-table-futures', 'selected_rows'),
    Output('pre-dash-table-fx', 'selected_rows'),
    Output('pre-dash-table-precious-metals', 'selected_rows'),
    Output('pre-dash-table-stock-indices', 'selected_rows'),
    Output('pre-dash-table-volatility-indices', 'selected_rows'),
    Output('pre-dash-table-benchmarks', 'selected_rows'),

    Output('n-preselected-biggest-companies', 'children'),
    Output('n-preselected-sp500', 'children'),
    Output('n-preselected-nasdaq100', 'children'),
    Output('n-preselected-dow-jones', 'children'),
    Output('n-preselected-car-companies', 'children'),
    Output('n-preselected-rare-metals-companies', 'children'),
    Output('n-preselected-quantum-companies', 'children'),
    Output('n-preselected-biggest-etfs', 'children'),
    Output('n-preselected-fixed-income-etfs', 'children'),
    Output('n-preselected-ai-etfs', 'children'),
    Output('n-preselected-commodity-etfs', 'children'),
    Output('n-preselected-currency-etfs', 'children'),
    Output('n-preselected-cryptos', 'children'),
    Output('n-preselected-crypto-etfs', 'children'),
    Output('n-preselected-futures', 'children'),
    Output('n-preselected-fx', 'children'),
    Output('n-preselected-precious-metals', 'children'),
    Output('n-preselected-stock-indices', 'children'),
    Output('n-preselected-volatility-indices', 'children'),
    Output('n-preselected-benchmarks', 'children'),

    Output('pre-selected-tickers-total', 'children'),
    Output('tk-selected-category-map', 'data'),
    Output('preselected-categories', 'data'),

    Input('pre-menu-biggest-companies-select-all-button', 'n_clicks'),
    Input('pre-menu-sp500-select-all-button', 'n_clicks'),
    Input('pre-menu-nasdaq100-select-all-button', 'n_clicks'),
    Input('pre-menu-dow-jones-select-all-button', 'n_clicks'),
    Input('pre-menu-car-companies-select-all-button', 'n_clicks'),
    Input('pre-menu-rare-metals-companies-select-all-button', 'n_clicks'),
    Input('pre-menu-quantum-companies-select-all-button', 'n_clicks'),
    Input('pre-menu-biggest-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-fixed-income-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-ai-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-commodity-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-currency-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-cryptos-select-all-button', 'n_clicks'),
    Input('pre-menu-crypto-etfs-select-all-button', 'n_clicks'),
    Input('pre-menu-futures-select-all-button', 'n_clicks'),
    Input('pre-menu-fx-select-all-button', 'n_clicks'),
    Input('pre-menu-precious-metals-select-all-button', 'n_clicks'),
    Input('pre-menu-stock-indices-select-all-button', 'n_clicks'),
    Input('pre-menu-volatility-indices-select-all-button', 'n_clicks'),
    Input('pre-menu-benchmarks-select-all-button', 'n_clicks'),

    Input('pre-menu-fx-select-major-button', 'n_clicks'),
    Input('pre-menu-fx-select-minor-button', 'n_clicks'),
    Input('pre-menu-fx-select-africa-button', 'n_clicks'),
    Input('pre-menu-fx-select-europe-button', 'n_clicks'),
    Input('pre-menu-fx-select-middle-east-button', 'n_clicks'),
    Input('pre-menu-fx-select-east-asia-button', 'n_clicks'),
    Input('pre-menu-fx-select-central-asia-button', 'n_clicks'),
    Input('pre-menu-fx-select-south-asia-button', 'n_clicks'),
    Input('pre-menu-fx-select-south-america-button', 'n_clicks'),
    Input('pre-menu-fx-select-north-america-button', 'n_clicks'),
    Input('pre-menu-fx-select-oceania-button', 'n_clicks'),

    Input('pre-menu-biggest-companies-unselect-all-button', 'n_clicks'),
    Input('pre-menu-sp500-unselect-all-button', 'n_clicks'),
    Input('pre-menu-nasdaq100-unselect-all-button', 'n_clicks'),
    Input('pre-menu-dow-jones-unselect-all-button', 'n_clicks'),
    Input('pre-menu-car-companies-unselect-all-button', 'n_clicks'),
    Input('pre-menu-rare-metals-companies-unselect-all-button', 'n_clicks'),
    Input('pre-menu-quantum-companies-unselect-all-button', 'n_clicks'),
    Input('pre-menu-biggest-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-fixed-income-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-ai-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-commodity-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-currency-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-cryptos-unselect-all-button', 'n_clicks'),
    Input('pre-menu-crypto-etfs-unselect-all-button', 'n_clicks'),
    Input('pre-menu-futures-unselect-all-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-all-button', 'n_clicks'),
    Input('pre-menu-precious-metals-unselect-all-button', 'n_clicks'),
    Input('pre-menu-stock-indices-unselect-all-button', 'n_clicks'),
    Input('pre-menu-volatility-indices-unselect-all-button', 'n_clicks'),
    Input('pre-menu-benchmarks-unselect-all-button', 'n_clicks'),

    Input('pre-menu-fx-unselect-major-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-minor-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-africa-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-europe-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-middle-east-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-east-asia-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-central-asia-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-south-asia-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-south-america-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-north-america-button', 'n_clicks'),
    Input('pre-menu-fx-unselect-oceania-button', 'n_clicks'),

    State('pre-menu-biggest-companies-select-first-ticker-input', 'value'),
    State('pre-menu-sp500-select-first-ticker-input', 'value'),
    State('pre-menu-nasdaq100-select-first-ticker-input', 'value'),
    State('pre-menu-dow-jones-select-first-ticker-input', 'value'),
    State('pre-menu-car-companies-select-first-ticker-input', 'value'),
    State('pre-menu-rare-metals-companies-select-first-ticker-input', 'value'),
    State('pre-menu-quantum-companies-select-first-ticker-input', 'value'),
    State('pre-menu-biggest-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-fixed-income-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-ai-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-commodity-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-currency-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-cryptos-select-first-ticker-input', 'value'),
    State('pre-menu-crypto-etfs-select-first-ticker-input', 'value'),
    State('pre-menu-futures-select-first-ticker-input', 'value'),
    State('pre-menu-fx-select-first-ticker-input', 'value'),
    State('pre-menu-precious-metals-select-first-ticker-input', 'value'),
    State('pre-menu-stock-indices-select-first-ticker-input', 'value'),
    State('pre-menu-volatility-indices-select-first-ticker-input', 'value'),
    State('pre-menu-benchmarks-select-first-ticker-input', 'value'),

    Input('pre-menu-biggest-companies-select-last-ticker-input', 'value'),
    Input('pre-menu-sp500-select-last-ticker-input', 'value'),
    Input('pre-menu-nasdaq100-select-last-ticker-input', 'value'),
    Input('pre-menu-dow-jones-select-last-ticker-input', 'value'),
    Input('pre-menu-car-companies-select-last-ticker-input', 'value'),
    Input('pre-menu-rare-metals-companies-select-last-ticker-input', 'value'),
    Input('pre-menu-quantum-companies-select-last-ticker-input', 'value'),
    Input('pre-menu-biggest-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-fixed-income-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-ai-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-commodity-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-currency-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-cryptos-select-last-ticker-input', 'value'),
    Input('pre-menu-crypto-etfs-select-last-ticker-input', 'value'),
    Input('pre-menu-futures-select-last-ticker-input', 'value'),
    Input('pre-menu-fx-select-last-ticker-input', 'value'),
    Input('pre-menu-precious-metals-select-last-ticker-input', 'value'),
    Input('pre-menu-stock-indices-select-last-ticker-input', 'value'),
    Input('pre-menu-volatility-indices-select-last-ticker-input', 'value'),
    Input('pre-menu-benchmarks-select-last-ticker-input', 'value'),

    State('pre-menu-biggest-companies-unselect-first-ticker-input', 'value'),
    State('pre-menu-sp500-unselect-first-ticker-input', 'value'),
    State('pre-menu-nasdaq100-unselect-first-ticker-input', 'value'),
    State('pre-menu-dow-jones-unselect-first-ticker-input', 'value'),
    State('pre-menu-car-companies-unselect-first-ticker-input', 'value'),
    State('pre-menu-rare-metals-companies-unselect-first-ticker-input', 'value'),
    State('pre-menu-quantum-companies-unselect-first-ticker-input', 'value'),
    State('pre-menu-biggest-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-fixed-income-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-ai-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-commodity-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-currency-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-cryptos-unselect-first-ticker-input', 'value'),
    State('pre-menu-crypto-etfs-unselect-first-ticker-input', 'value'),
    State('pre-menu-futures-unselect-first-ticker-input', 'value'),
    State('pre-menu-fx-unselect-first-ticker-input', 'value'),
    State('pre-menu-precious-metals-unselect-first-ticker-input', 'value'),
    State('pre-menu-stock-indices-unselect-first-ticker-input', 'value'),
    State('pre-menu-volatility-indices-unselect-first-ticker-input', 'value'),
    State('pre-menu-benchmarks-unselect-first-ticker-input', 'value'),

    Input('pre-menu-biggest-companies-unselect-last-ticker-input', 'value'),
    Input('pre-menu-sp500-unselect-last-ticker-input', 'value'),
    Input('pre-menu-nasdaq100-unselect-last-ticker-input', 'value'),
    Input('pre-menu-dow-jones-unselect-last-ticker-input', 'value'),
    Input('pre-menu-car-companies-unselect-last-ticker-input', 'value'),
    Input('pre-menu-rare-metals-companies-unselect-last-ticker-input', 'value'),
    Input('pre-menu-quantum-companies-unselect-last-ticker-input', 'value'),
    Input('pre-menu-biggest-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-fixed-income-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-ai-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-commodity-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-currency-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-cryptos-unselect-last-ticker-input', 'value'),
    Input('pre-menu-crypto-etfs-unselect-last-ticker-input', 'value'),
    Input('pre-menu-futures-unselect-last-ticker-input', 'value'),
    Input('pre-menu-fx-unselect-last-ticker-input', 'value'),
    Input('pre-menu-precious-metals-unselect-last-ticker-input', 'value'),
    Input('pre-menu-stock-indices-unselect-last-ticker-input', 'value'),
    Input('pre-menu-volatility-indices-unselect-last-ticker-input', 'value'),
    Input('pre-menu-benchmarks-unselect-last-ticker-input', 'value'),

    Input('pre-dash-table-biggest-companies', 'data'),
    Input('pre-dash-table-sp500', 'data'),
    Input('pre-dash-table-nasdaq100', 'data'),
    Input('pre-dash-table-dow-jones', 'data'),
    Input('pre-dash-table-car-companies', 'data'),
    Input('pre-dash-table-rare-metals-companies', 'data'),
    Input('pre-dash-table-quantum-companies', 'data'),
    Input('pre-dash-table-biggest-etfs', 'data'),
    Input('pre-dash-table-fixed-income-etfs', 'data'),
    Input('pre-dash-table-ai-etfs', 'data'),    
    Input('pre-dash-table-commodity-etfs', 'data'),
    Input('pre-dash-table-currency-etfs', 'data'),
    Input('pre-dash-table-cryptos', 'data'),
    Input('pre-dash-table-crypto-etfs', 'data'),    
    Input('pre-dash-table-futures', 'data'),
    Input('pre-dash-table-fx', 'data'),
    Input('pre-dash-table-precious-metals', 'data'),
    Input('pre-dash-table-stock-indices', 'data'),
    Input('pre-dash-table-volatility-indices', 'data'),
    Input('pre-dash-table-benchmarks', 'data'),

    Input('pre-dash-table-biggest-companies', 'selected_rows'),
    Input('pre-dash-table-sp500', 'selected_rows'),
    Input('pre-dash-table-nasdaq100', 'selected_rows'),
    Input('pre-dash-table-dow-jones', 'selected_rows'),
    Input('pre-dash-table-car-companies', 'selected_rows'),
    Input('pre-dash-table-rare-metals-companies', 'selected_rows'),
    Input('pre-dash-table-quantum-companies', 'selected_rows'),
    Input('pre-dash-table-biggest-etfs', 'selected_rows'),
    Input('pre-dash-table-fixed-income-etfs', 'selected_rows'),
    Input('pre-dash-table-ai-etfs', 'selected_rows'),
    Input('pre-dash-table-commodity-etfs', 'selected_rows'),
    Input('pre-dash-table-currency-etfs', 'selected_rows'),
    Input('pre-dash-table-cryptos', 'selected_rows'),
    Input('pre-dash-table-crypto-etfs', 'selected_rows'),
    Input('pre-dash-table-futures', 'selected_rows'),
    Input('pre-dash-table-fx', 'selected_rows'),
    Input('pre-dash-table-precious-metals', 'selected_rows'),
    Input('pre-dash-table-stock-indices', 'selected_rows'),
    Input('pre-dash-table-volatility-indices', 'selected_rows'),
    Input('pre-dash-table-benchmarks', 'selected_rows'),

    Input('pre-select-ticker-list', 'children'),
    Input('pre-prev-table-selected-rows', 'data'),
    Input('pre-select-ticker-container', 'children'),
    Input({'index': ALL, 'type': 'ticker_icon'}, 'n_clicks'),

    Input('selected-categories-stored', 'data'),
    Input('ticker-category-info-map', 'data'),
    Input('ticker-names', 'data'),

    State('tk-selected-category-map', 'data'),
    # Input('tk-selected-category-map', 'data'),

    suppress_callback_exceptions = True
)
def output_custom_tickers(

    select_all_biggest_companies,
    select_all_sp500,
    select_all_nasdaq100,
    select_all_dow_jones,
    select_all_car_companies,
    select_all_rare_metals_companies,
    select_all_quantum_companies,
    select_all_biggest_etfs,
    select_all_fixed_income_etfs,
    select_all_ai_etfs,
    select_all_commodity_etfs,
    select_all_currency_etfs,
    select_all_cryptos,
    select_all_crypto_etfs,
    select_all_futures,
    select_all_fx,
    select_all_precious_metals,
    select_all_stock_indices,
    select_all_volatility_indices,
    select_all_benchmarks,

    select_major_fx,
    select_minor_fx,
    select_africa_fx,
    select_europe_fx,
    select_middle_east_fx,
    select_east_asia_fx,
    select_central_asia_fx,
    select_south_asia_fx,
    select_south_america_fx,
    select_north_america_fx,
    select_oceania_fx,

    unselect_all_biggest_companies,
    unselect_all_sp500,
    unselect_all_nasdaq100,
    unselect_all_dow_jones,
    unselect_all_car_companies,
    unselect_all_rare_metals_companies,
    unselect_all_quantum_companies,
    unselect_all_biggest_etfs,
    unselect_all_fixed_income_etfs,
    unselect_all_ai_etfs,
    unselect_all_commodity_etfs,
    unselect_all_currency_etfs,
    unselect_all_cryptos,
    unselect_all_crypto_etfs,
    unselect_all_futures,
    unselect_all_fx,
    unselect_all_precious_metals,
    unselect_all_stock_indices,
    unselect_all_volatility_indices,
    unselect_all_benchmarks,

    unselect_major_fx,
    unselect_minor_fx,
    unselect_africa_fx,
    unselect_europe_fx,
    unselect_middle_east_fx,
    unselect_east_asia_fx,
    unselect_central_asia_fx,
    unselect_south_asia_fx,
    unselect_south_america_fx,
    unselect_north_america_fx,
    unselect_oceania_fx,

    select_first_ticker_biggest_companies,
    select_first_ticker_sp500,
    select_first_ticker_nasdaq100,
    select_first_ticker_dow_jones,
    select_first_ticker_car_companies,
    select_first_ticker_rare_metals_companies,
    select_first_ticker_quantum_companies,
    select_first_ticker_biggest_etfs,
    select_first_ticker_fixed_income_etfs,
    select_first_ticker_ai_etfs,
    select_first_ticker_commodity_etfs,
    select_first_ticker_currency_etfs,
    select_first_ticker_cryptos,
    select_first_ticker_crypto_etfs,
    select_first_ticker_futures,
    select_first_ticker_fx,
    select_first_ticker_precious_metals,
    select_first_ticker_stock_indices,
    select_first_ticker_volatility_indices,
    select_first_ticker_benchmarks,

    select_last_ticker_biggest_companies,
    select_last_ticker_sp500,
    select_last_ticker_nasdaq100,
    select_last_ticker_dow_jones,
    select_last_ticker_car_companies,
    select_last_ticker_rare_metals_companies,
    select_last_ticker_quantum_companies,
    select_last_ticker_biggest_etfs,
    select_last_ticker_fixed_income_etfs,
    select_last_ticker_ai_etfs,
    select_last_ticker_commodity_etfs,
    select_last_ticker_currency_etfs,
    select_last_ticker_cryptos,
    select_last_ticker_crypto_etfs,
    select_last_ticker_futures,
    select_last_ticker_fx,
    select_last_ticker_precious_metals,
    select_last_ticker_stock_indices,
    select_last_ticker_volatility_indices,
    select_last_ticker_benchmarks,

    unselect_first_ticker_biggest_companies,
    unselect_first_ticker_sp500,
    unselect_first_ticker_nasdaq100,
    unselect_first_ticker_dow_jones,
    unselect_first_ticker_car_companies,
    unselect_first_ticker_rare_metals_companies,
    unselect_first_ticker_quantum_companies,
    unselect_first_ticker_biggest_etfs,
    unselect_first_ticker_fixed_income_etfs,
    unselect_first_ticker_ai_etfs,
    unselect_first_ticker_commodity_etfs,
    unselect_first_ticker_currency_etfs,
    unselect_first_ticker_cryptos,
    unselect_first_ticker_crypto_etfs,
    unselect_first_ticker_futures,
    unselect_first_ticker_fx,
    unselect_first_ticker_precious_metals,
    unselect_first_ticker_stock_indices,
    unselect_first_ticker_volatility_indices,
    unselect_first_ticker_benchmarks,

    unselect_last_ticker_biggest_companies,
    unselect_last_ticker_sp500,
    unselect_last_ticker_nasdaq100,
    unselect_last_ticker_dow_jones,
    unselect_last_ticker_car_companies,
    unselect_last_ticker_rare_metals_companies,
    unselect_last_ticker_quantum_companies,
    unselect_last_ticker_biggest_etfs,
    unselect_last_ticker_fixed_income_etfs,
    unselect_last_ticker_ai_etfs,
    unselect_last_ticker_commodity_etfs,
    unselect_last_ticker_currency_etfs,
    unselect_last_ticker_cryptos,
    unselect_last_ticker_crypto_etfs,
    unselect_last_ticker_futures,
    unselect_last_ticker_fx,
    unselect_last_ticker_precious_metals,
    unselect_last_ticker_stock_indices,
    unselect_last_ticker_volatility_indices,
    unselect_last_ticker_benchmarks,

    table_biggest_companies_data,
    table_sp500_data,
    table_nasdaq100_data,
    table_dow_jones_data,
    table_car_companies_data,
    table_rare_metals_companies_data,
    table_quantum_companies_data,
    table_biggest_etfs_data,
    table_fixed_income_etfs_data,
    table_ai_etfs_data,
    table_commodity_etfs_data,
    table_currency_etfs_data,
    table_cryptos_data,
    table_crypto_etfs_data,
    table_futures_data,
    table_fx_data,
    table_precious_metals_data,
    table_stock_indices_data,
    table_volatility_indices_data,
    table_benchmarks_data,

    table_biggest_companies_selected_rows,
    table_sp500_selected_rows,
    table_nasdaq100_selected_rows,
    table_dow_jones_selected_rows,
    table_car_companies_selected_rows,
    table_rare_metals_companies_selected_rows,
    table_quantum_companies_selected_rows,
    table_biggest_etfs_selected_rows,
    table_fixed_income_etfs_selected_rows,
    table_ai_etfs_selected_rows,
    table_commodity_etfs_selected_rows,
    table_currency_etfs_selected_rows,
    table_cryptos_selected_rows,
    table_crypto_etfs_selected_rows,
    table_futures_selected_rows,
    table_fx_selected_rows,
    table_precious_metals_selected_rows,
    table_stock_indices_selected_rows,
    table_volatility_indices_selected_rows,
    table_benchmarks_selected_rows,

    selected_tickers,
    prev_table_selected_rows,
    ticker_divs,
    n_clicks,

    selected_categories_stored,
    ticker_category_info_map,
    ticker_names,

    tk_selected_category_map
):

    table_selected_rows = {
        'biggest_companies': table_biggest_companies_selected_rows,
        'sp500': table_sp500_selected_rows,
        'nasdaq100': table_nasdaq100_selected_rows,
        'dow_jones': table_dow_jones_selected_rows,
        'car_companies': table_car_companies_selected_rows,
        'rare_metals_companies': table_rare_metals_companies_selected_rows,
        'quantum_companies': table_quantum_companies_selected_rows,
        'biggest_etfs': table_biggest_etfs_selected_rows,
        'fixed_income_etfs': table_fixed_income_etfs_selected_rows,
        'ai_etfs': table_ai_etfs_selected_rows,
        'precious_metals': table_precious_metals_selected_rows,
        'commodity_etfs': table_commodity_etfs_selected_rows,
        'currency_etfs': table_currency_etfs_selected_rows,
        'cryptos': table_cryptos_selected_rows,
        'crypto_etfs': table_crypto_etfs_selected_rows,
        'futures': table_futures_selected_rows,
        'fx': table_fx_selected_rows,
        'stock_indices': table_stock_indices_selected_rows,
        'volatility_indices': table_volatility_indices_selected_rows,
        'benchmarks': table_benchmarks_selected_rows
    }
    table_data = {
        'biggest_companies': table_biggest_companies_data,
        'sp500': table_sp500_data,
        'nasdaq100': table_nasdaq100_data,
        'dow_jones': table_dow_jones_data,
        'car_companies': table_car_companies_data,
        'rare_metals_companies': table_rare_metals_companies_data,
        'quantum_companies': table_quantum_companies_data,
        'biggest_etfs': table_biggest_etfs_data,
        'fixed_income_etfs': table_fixed_income_etfs_data,
        'ai_etfs': table_ai_etfs_data,
        'precious_metals': table_precious_metals_data,
        'commodity_etfs': table_commodity_etfs_data,
        'currency_etfs': table_currency_etfs_data,
        'cryptos': table_cryptos_data,
        'crypto_etfs': table_crypto_etfs_data,
        'futures': table_futures_data,
        'fx': table_fx_data,
        'stock_indices': table_stock_indices_data,
        'volatility_indices': table_volatility_indices_data,
        'benchmarks': table_benchmarks_data
    }
    select_all_button_nclicks = {
        'biggest_companies': select_all_biggest_companies,
        'sp500': select_all_sp500,
        'nasdaq100': select_all_nasdaq100,
        'dow_jones': select_all_dow_jones,
        'car_companies': select_all_car_companies,
        'rare_metals_companies': select_all_rare_metals_companies,
        'quantum_companies': select_all_quantum_companies,
        'biggest_etfs': select_all_biggest_etfs,
        'fixed_income_etfs': select_all_fixed_income_etfs,
        'ai_etfs': select_all_ai_etfs,
        'precious_metals': select_all_precious_metals,
        'commodity_etfs': select_all_commodity_etfs,
        'currency_etfs': select_all_currency_etfs,
        'cryptos': select_all_cryptos,
        'crypto_etfs': select_all_crypto_etfs,
        'futures': select_all_futures,
        'fx': select_all_fx,
        'stock_indices': select_all_stock_indices,
        'volatility_indices': select_all_volatility_indices,
        'benchmarks': select_all_benchmarks
    }
    unselect_all_button_nclicks = {
        'biggest_companies': unselect_all_biggest_companies,
        'sp500': unselect_all_sp500,
        'nasdaq100': unselect_all_nasdaq100,
        'dow_jones': unselect_all_dow_jones,
        'car_companies': unselect_all_car_companies,
        'rare_metals_companies': unselect_all_rare_metals_companies,
        'quantum_companies': unselect_all_quantum_companies,
        'biggest_etfs': unselect_all_biggest_etfs,
        'fixed_income_etfs': unselect_all_fixed_income_etfs,
        'ai_etfs': unselect_all_ai_etfs,
        'precious_metals': unselect_all_precious_metals,
        'commodity_etfs': unselect_all_commodity_etfs,
        'currency_etfs': unselect_all_currency_etfs,
        'cryptos': unselect_all_cryptos,
        'crypto_etfs': unselect_all_crypto_etfs,
        'futures': unselect_all_futures,
        'fx': unselect_all_fx,
        'stock_indices': unselect_all_stock_indices,
        'volatility_indices': unselect_all_volatility_indices,
        'benchmarks': unselect_all_benchmarks
    }
    select_first_ticker = {
        'biggest_companies': select_first_ticker_biggest_companies,
        'sp500': select_first_ticker_sp500,
        'nasdaq100': select_first_ticker_nasdaq100,
        'dow_jones': select_first_ticker_dow_jones,
        'car_companies': select_first_ticker_car_companies,
        'rare_metals_companies': select_first_ticker_rare_metals_companies,
        'quantum_companies': select_first_ticker_quantum_companies,
        'biggest_etfs': select_first_ticker_biggest_etfs,
        'fixed_income_etfs': select_first_ticker_fixed_income_etfs,
        'ai_etfs': select_first_ticker_ai_etfs,
        'precious_metals': select_first_ticker_precious_metals,
        'commodity_etfs': select_first_ticker_commodity_etfs,
        'currency_etfs': select_first_ticker_currency_etfs,
        'cryptos': select_first_ticker_cryptos,
        'crypto_etfs': select_first_ticker_crypto_etfs,
        'futures': select_first_ticker_futures,
        'fx': select_first_ticker_fx,
        'stock_indices': select_first_ticker_stock_indices,
        'volatility_indices': select_first_ticker_volatility_indices,
        'benchmarks': select_first_ticker_benchmarks
    }
    select_last_ticker = {
        'biggest_companies': select_last_ticker_biggest_companies,
        'sp500': select_last_ticker_sp500,
        'nasdaq100': select_last_ticker_nasdaq100,
        'dow_jones': select_last_ticker_dow_jones,
        'car_companies': select_last_ticker_car_companies,
        'rare_metals_companies': select_last_ticker_rare_metals_companies,
        'quantum_companies': select_last_ticker_quantum_companies,
        'biggest_etfs': select_last_ticker_biggest_etfs,
        'fixed_income_etfs': select_last_ticker_fixed_income_etfs,
        'ai_etfs': select_last_ticker_ai_etfs,
        'precious_metals': select_last_ticker_precious_metals,
        'commodity_etfs': select_last_ticker_commodity_etfs,
        'currency_etfs': select_last_ticker_currency_etfs,
        'cryptos': select_last_ticker_cryptos,
        'crypto_etfs': select_last_ticker_crypto_etfs,
        'futures': select_last_ticker_futures,
        'fx': select_last_ticker_fx,
        'stock_indices': select_last_ticker_stock_indices,
        'volatility_indices': select_last_ticker_volatility_indices,
        'benchmarks': select_last_ticker_benchmarks
    }
    unselect_first_ticker = {
        'biggest_companies': unselect_first_ticker_biggest_companies,
        'sp500': unselect_first_ticker_sp500,
        'nasdaq100': unselect_first_ticker_nasdaq100,
        'dow_jones': unselect_first_ticker_dow_jones,
        'car_companies': unselect_first_ticker_car_companies,
        'rare_metals_companies': unselect_first_ticker_rare_metals_companies,
        'quantum_companies': unselect_first_ticker_quantum_companies,
        'biggest_etfs': unselect_first_ticker_biggest_etfs,
        'fixed_income_etfs': unselect_first_ticker_fixed_income_etfs,
        'ai_etfs': unselect_first_ticker_ai_etfs,
        'precious_metals': unselect_first_ticker_precious_metals,
        'commodity_etfs': unselect_first_ticker_commodity_etfs,
        'currency_etfs': unselect_first_ticker_currency_etfs,
        'cryptos': unselect_first_ticker_cryptos,
        'crypto_etfs': unselect_first_ticker_crypto_etfs,
        'futures': unselect_first_ticker_futures,
        'fx': unselect_first_ticker_fx,
        'stock_indices': unselect_first_ticker_stock_indices,
        'volatility_indices': unselect_first_ticker_volatility_indices,
        'benchmarks': unselect_first_ticker_benchmarks
    }
    unselect_last_ticker = {
        'biggest_companies': unselect_last_ticker_biggest_companies,
        'sp500': unselect_last_ticker_sp500,
        'nasdaq100': unselect_last_ticker_nasdaq100,
        'dow_jones': unselect_last_ticker_dow_jones,
        'car_companies': unselect_last_ticker_car_companies,
        'rare_metals_companies': unselect_last_ticker_rare_metals_companies,
        'quantum_companies': unselect_last_ticker_quantum_companies,
        'biggest_etfs': unselect_last_ticker_biggest_etfs,
        'fixed_income_etfs': unselect_last_ticker_fixed_income_etfs,
        'ai_etfs': unselect_last_ticker_ai_etfs,
        'precious_metals': unselect_last_ticker_precious_metals,
        'commodity_etfs': unselect_last_ticker_commodity_etfs,
        'currency_etfs': unselect_last_ticker_currency_etfs,
        'cryptos': unselect_last_ticker_cryptos,
        'crypto_etfs': unselect_last_ticker_crypto_etfs,
        'futures': unselect_last_ticker_futures,
        'fx': unselect_last_ticker_fx,
        'stock_indices': unselect_last_ticker_stock_indices,
        'volatility_indices': unselect_last_ticker_volatility_indices,
        'benchmarks': unselect_last_ticker_benchmarks
    }

    n_preselected = {}

    if selected_tickers is None:
        selected_tickers = []

    updated_tickers = selected_tickers

    if prev_table_selected_rows == {}:
        for category in ticker_category_info_map.keys():
            prev_table_selected_rows[category] = []

    dict_cat_tickers = {}

    for category in ticker_category_info_map.keys():

        n_category_tickers = len(table_data[category])

        if select_all_button_nclicks[category]:
            table_selected_rows[category] = list(range(n_category_tickers))

            # print(f'category: {category}')
            # print(f'selected rows: {table_selected_rows[category]}\n')

        elif unselect_all_button_nclicks[category]:
            table_selected_rows[category] = []
            select_first_ticker[category] = None
            select_last_ticker[category] = None

        elif (select_first_ticker[category] is not None):
            if (select_last_ticker[category] is not None):
                select_first_row = select_first_ticker[category] - 1
                if select_last_ticker[category] < select_first_ticker[category]:
                    select_last_row = select_first_ticker[category]
                else:
                    select_last_row = select_last_ticker[category]
                select_rows_range = [k for k in range(select_first_row, select_last_row)]
                for row in select_rows_range:
                    if row not in table_selected_rows[category]:
                        table_selected_rows[category].append(row)
                select_last_ticker[category] = None 
        
        elif (unselect_first_ticker[category] is not None):
            if (unselect_last_ticker[category] is not None):
                unselect_first_row = unselect_first_ticker[category] - 1
                if unselect_last_ticker[category] < unselect_first_ticker[category]:
                    unselect_last_row = unselect_first_ticker[category]
                else:
                    unselect_last_row = unselect_last_ticker[category]
                unselect_rows_range = [k for k in range(unselect_first_row, unselect_last_row)]
                for row in unselect_rows_range:
                    if row in table_selected_rows[category]:
                        table_selected_rows[category].remove(row)
                unselect_last_ticker[category] = None

        else:
            select_last_ticker[category] = None
            unselect_last_ticker[category] = None

    ### FX major, minor and regions

    if select_major_fx:
        for idx in indices_currencies_major:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_major_fx:
        for idx in indices_currencies_major:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_minor_fx:
        for idx in indices_currencies_minor:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_minor_fx:
        for idx in indices_currencies_minor:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_europe_fx:
        for idx in indices_currencies_europe:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_europe_fx:
        for idx in indices_currencies_europe:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_africa_fx:
        for idx in indices_currencies_africa:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_africa_fx:
        for idx in indices_currencies_africa:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_middle_east_fx:
        for idx in indices_currencies_middle_east:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_middle_east_fx:
        for idx in indices_currencies_middle_east:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_east_asia_fx:
        for idx in indices_currencies_east_asia:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_east_asia_fx:
        for idx in indices_currencies_east_asia:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_central_asia_fx:
        for idx in indices_currencies_central_asia:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_central_asia_fx:
        for idx in indices_currencies_central_asia:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_south_asia_fx:
        for idx in indices_currencies_south_asia:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_south_asia_fx:
        for idx in indices_currencies_south_asia:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_south_america_fx:
        for idx in indices_currencies_south_america:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_south_america_fx:
        for idx in indices_currencies_south_america:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_north_america_fx:
        for idx in indices_currencies_north_america:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_north_america_fx:
        for idx in indices_currencies_north_america:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    if select_oceania_fx:
        for idx in indices_currencies_oceania:
            if idx not in table_selected_rows['fx']:
                table_selected_rows['fx'].append(idx)
    elif unselect_oceania_fx:
        for idx in indices_currencies_oceania:
            if idx in table_selected_rows['fx']:
                table_selected_rows['fx'].remove(idx)

    #########

    # table_selected_tickers = {}
    # table_nonselected_tickers = {}
    # for category in ticker_category_info_map.keys():
    #     row_map = ticker_category_info_map[category]['row']
    #     table_selected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]
    #     table_nonselected_tickers[category] = [tk for tk in row_map.keys() if row_map[tk] not in table_selected_rows[category]]

    ctx = dash.callback_context

    # Should change to added tickers in this format
    added_tickers = []
    removed_tickers = []
    if 1 in n_clicks:
        if ctx.triggered:
            trig_id_str_list = [ctx.triggered[k]['prop_id'].split('.n_clicks')[0] for k in range(len(ctx.triggered)) if ctx.triggered[k]['value']]
            if len(trig_id_str_list) > 0:
                trig_id_str = trig_id_str_list[0]  # this is a stringified dictionary with whitespaces removed
                removed_ticker = trig_id_str.split('{"index":"')[1].split('","type"')[0].replace('select-ticker-icon-', '')  # {tk}
                removed_tickers.append(removed_ticker)

    for removed_ticker in removed_tickers:
        if removed_ticker in updated_tickers:
            updated_tickers.remove(removed_ticker)

    ticker_div_title = html.Div(
        'YOUR PORTFOLIO:',
        style = select_ticker_title_css
    )
    ticker_divs = [ticker_div_title]  # 'YOUR PORTFOLIO'

    hide_ticker_container = False if len(updated_tickers) > 0 else True

    ##### INPUT TABLES
    # Check whether a ticker was added to or removed from any table

    # Construct the final list of categories from which the user has selected tickers
    # This is to prevent passing to next page other categories containing the same tickers

    # tk_selected_cat_map = {}

    for category in ticker_category_info_map.keys():
        row_map = ticker_category_info_map[category]['row']
        df_pre = ticker_category_info_map[category]['df']  # Dictionary
        selected_rows = [k for k in table_selected_rows[category] if k not in prev_table_selected_rows[category]]
        if len(selected_rows) > 0:
            # preselected_categories.append(category)
            for row in selected_rows:
                # added_ticker = df_pre.index[df_pre['No.'] == row + 1][0]
                added_ticker = [tk for tk in row_map.keys() if row_map[tk] == row][0]
                if added_ticker not in added_tickers:
                    added_tickers.append(added_ticker)
                if added_ticker not in updated_tickers:
                    updated_tickers.append(added_ticker)
                    if added_ticker not in tk_selected_category_map.keys():
                        tk_selected_category_map[added_ticker] = category
            break
        else:
            unselected_rows = [k for k in prev_table_selected_rows[category] if k not in table_selected_rows[category]]
            if len(unselected_rows) > 0:
                for row in unselected_rows:
                    # removed_ticker = df_pre.index[df_pre['No.'] == row + 1][0]
                    removed_ticker = [tk for tk in row_map.keys() if row_map[tk] == row][0]
                    if removed_ticker not in removed_tickers:
                        removed_tickers.append(removed_ticker)
                    if removed_ticker in updated_tickers:
                        updated_tickers.remove(removed_ticker)
                        if removed_ticker in tk_selected_category_map.keys():
                            del tk_selected_category_map[removed_ticker]
                break
        # Check if category is empty and remove it from preselected_categories if it is
        # if (len(table_selected_rows[category]) == 0) & (category in preselected_categories):
        #     preselected_categories.remove(category)

    preselected_categories = list(set(tk_selected_category_map.values()))  # Set removes duplicates

    # Make sure added_ticker is selected in all tables and removed_ticker is removed from all tables
    if added_tickers != []:
        # for category in ticker_category_info_map.keys():
        for category in selected_categories_stored:
            df_pre = ticker_category_info_map[category]['df']  # This is a dictionary!
            # print(f'Tickers added\n{df_pre}\n')
            for added_ticker in added_tickers:
                if added_ticker in list(df_pre['Ticker'].values()):
                    row_map = ticker_category_info_map[category]['row']
                    if row_map[added_ticker] not in table_selected_rows[category]:
                        table_selected_rows[category].append(row_map[added_ticker])

    if removed_tickers != []:
        # for category in ticker_category_info_map.keys():
        for category in selected_categories_stored:
            df_pre = ticker_category_info_map[category]['df']  # This is a dictionary!
            # print(f'Tickers removed\n{df_pre}\n')
            for removed_ticker in removed_tickers:
                if removed_ticker in list(df_pre['Ticker'].values()):
                    row_map = ticker_category_info_map[category]['row']
                    if row_map[removed_ticker] in table_selected_rows[category]:
                        table_selected_rows[category].remove(row_map[removed_ticker])

    # df.to_dict() = {
    #   'Ticker':   {0: 'AAPL', 1: 'AMZN', 2: 'TM'},
    #   'Name':     {0: 'Apple', 1: 'Amazon', 2: 'Toyota'}
    # }
    # df.to_dict('records') = [
    #   {'Ticker': 'AAPL', 'Name': 'Apple'},
    #   {'Ticker': 'AMZN', 'Name': 'Amazon'},
    #   {'Ticker': 'TM', 'Name': 'Toyota'} 
    # ]

    ##### SELECTED TICKERS
    # Set up selected tickers divs

    for tk in updated_tickers:
        
        tk_id = f'select-ticker-{tk}'
        tk_icon_id = f'select-ticker-icon-{tk}'
        name = ticker_names[tk] if tk in ticker_names.keys() is not None else tk

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
                ),
            ],
            style = select_ticker_div_css
        )
        ticker_divs.append(tk_div)

    for category in table_selected_rows.keys():
        n_preselected[category] = len(table_selected_rows[category])

    n_preselected_total = len(updated_tickers)

    # hide_ticker_container = True if len(updated_tickers) == 0 else False
    hide_ticker_container = True

    return (
        ticker_divs,
        hide_ticker_container,
        updated_tickers,
        table_selected_rows,

        # select_all_button_nclicks
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # FX select_major, minor and regions
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # unselect_all_button_nclicks
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # FX unselect_major, minor and regions
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        # select_first_ticker
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        # select_last_ticker
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        # unselect_first_ticker
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
        # unselect_last_ticker
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,

        table_selected_rows['biggest_companies'],
        table_selected_rows['sp500'],
        table_selected_rows['nasdaq100'],
        table_selected_rows['dow_jones'],
        table_selected_rows['car_companies'],
        table_selected_rows['rare_metals_companies'],
        table_selected_rows['quantum_companies'],
        table_selected_rows['biggest_etfs'],
        table_selected_rows['fixed_income_etfs'],
        table_selected_rows['ai_etfs'],
        table_selected_rows['commodity_etfs'],
        table_selected_rows['currency_etfs'],
        table_selected_rows['cryptos'],
        table_selected_rows['crypto_etfs'],
        table_selected_rows['futures'],
        table_selected_rows['fx'],
        table_selected_rows['precious_metals'],
        table_selected_rows['stock_indices'],
        table_selected_rows['volatility_indices'],
        table_selected_rows['benchmarks'],

        n_preselected['biggest_companies'],
        n_preselected['sp500'],
        n_preselected['nasdaq100'],
        n_preselected['dow_jones'],
        n_preselected['car_companies'],
        n_preselected['rare_metals_companies'],
        n_preselected['quantum_companies'],
        n_preselected['biggest_etfs'],
        n_preselected['fixed_income_etfs'],
        n_preselected['ai_etfs'],
        n_preselected['commodity_etfs'],
        n_preselected['currency_etfs'],
        n_preselected['cryptos'],
        n_preselected['crypto_etfs'],
        n_preselected['futures'],
        n_preselected['fx'],
        n_preselected['precious_metals'],
        n_preselected['stock_indices'],
        n_preselected['volatility_indices'],
        n_preselected['benchmarks'],

        n_preselected_total,
        tk_selected_category_map,
        preselected_categories
    )


def toggle_collapse_tickers(title, n, is_open):
    # Cool arrows from https://www.alt-codes.net/arrow_alt_codes.php
    label = f'► {title}' if is_open else f'▼ {title}'
    if n:
        return label, not is_open
    else:
        return f'► {title}', is_open


for category in category_titles_ids.keys():
    id_string = category_titles_ids[category]['id_string']
    callback(
    # app.callback(        
        Output(f'pre-collapse-button-table-{id_string}', 'children'),
        Output(f'pre-collapse-table-{id_string}', 'is_open'),
        Input(f'pre-collapse-button-title-{id_string}', 'children'),
        Input(f'pre-collapse-button-table-{id_string}', 'n_clicks'),
        State(f'pre-collapse-table-{id_string}', 'is_open')
    )(toggle_collapse_tickers)

########## MULTIPAGE APP CALLBACKS

# @callback(
# Output('pre-select-ticker-list-check', 'children'),
# Input('preselected-updated-tickers', 'data'),
# # State('pre-select-ticker-list', 'children'),
# suppress_callback_exceptions = True
# )
# # def store_preselected_updated_tickers(pathname, updated_tickers):  # , stored_updated_tickers):
# def retrieve_preselected_updated_tickers(stored_updated_tickers): # , updated_tickers):
#     # if (stored_updated_tickers != []) & (updated_tickers == []):
#     # if stored_updated_tickers != []:
#     # if pathname == '/test_multipage_app':
#     return stored_updated_tickers

@callback(
Output('n-preselected-stored', 'data'),
Output('preselected-ticker-tables-stored', 'data'),

Input('pre-dash-table-biggest-companies', 'selected_rows'),
Input('pre-dash-table-sp500', 'selected_rows'),
Input('pre-dash-table-nasdaq100', 'selected_rows'),
Input('pre-dash-table-dow-jones', 'selected_rows'),
Input('pre-dash-table-car-companies', 'selected_rows'),
Input('pre-dash-table-rare-metals-companies', 'selected_rows'),
Input('pre-dash-table-quantum-companies', 'selected_rows'),
Input('pre-dash-table-biggest-etfs', 'selected_rows'),
Input('pre-dash-table-fixed-income-etfs', 'selected_rows'),
Input('pre-dash-table-ai-etfs', 'selected_rows'),
Input('pre-dash-table-commodity-etfs', 'selected_rows'),
Input('pre-dash-table-currency-etfs', 'selected_rows'),
Input('pre-dash-table-cryptos', 'selected_rows'),
Input('pre-dash-table-crypto-etfs', 'selected_rows'),
Input('pre-dash-table-futures', 'selected_rows'),
Input('pre-dash-table-fx', 'selected_rows'),
Input('pre-dash-table-precious-metals', 'selected_rows'),
Input('pre-dash-table-stock-indices', 'selected_rows'),
Input('pre-dash-table-volatility-indices', 'selected_rows'),
Input('pre-dash-table-benchmarks', 'selected_rows'),

Input('preselected-categories', 'data'),
Input('ticker-category-info-map', 'data'),
Input('ticker-names', 'data')
)
def store_preselected_tickers(
    table_biggest_companies_selected_rows,
    table_sp500_selected_rows,
    table_nasdaq100_selected_rows,
    table_dow_jones_selected_rows,
    table_car_companies_selected_rows,
    table_rare_metals_companies_selected_rows,
    table_quantum_companies_selected_rows,
    table_biggest_etfs_selected_rows,
    table_fixed_income_etfs_selected_rows,
    table_ai_etfs_selected_rows,
    table_commodity_etfs_selected_rows,
    table_currency_etfs_selected_rows,
    table_cryptos_selected_rows,
    table_crypto_etfs_selected_rows,
    table_futures_selected_rows,
    table_fx_selected_rows,
    table_precious_metals_selected_rows,
    table_stock_indices_selected_rows,
    table_volatility_indices_selected_rows,
    table_benchmarks_selected_rows,

    preselected_categories,
    ticker_category_info_map,
    ticker_names
):
    table_selected_rows = {
        'biggest_companies': table_biggest_companies_selected_rows,
        'sp500': table_sp500_selected_rows,
        'nasdaq100': table_nasdaq100_selected_rows,
        'dow_jones': table_dow_jones_selected_rows,
        'car_companies': table_car_companies_selected_rows,
        'rare_metals_companies': table_rare_metals_companies_selected_rows,
        'quantum_companies': table_quantum_companies_selected_rows,
        'biggest_etfs': table_biggest_etfs_selected_rows,
        'fixed_income_etfs': table_fixed_income_etfs_selected_rows,
        'ai_etfs': table_ai_etfs_selected_rows,
        'precious_metals': table_precious_metals_selected_rows,
        'commodity_etfs': table_commodity_etfs_selected_rows,
        'currency_etfs': table_currency_etfs_selected_rows,
        'cryptos': table_cryptos_selected_rows,
        'crypto_etfs': table_crypto_etfs_selected_rows,
        'futures': table_futures_selected_rows,
        'fx': table_fx_selected_rows,
        'stock_indices': table_stock_indices_selected_rows,
        'volatility_indices': table_volatility_indices_selected_rows,
        'benchmarks': table_benchmarks_selected_rows
    }

    # n_preselected will only be non-zero if the user has selected from that particular category
    n_preselected = {}
    preselected_ticker_tables = {}

    for category in ticker_category_info_map.keys():
        
        if category in preselected_categories:
            n_preselected[category] = len(table_selected_rows[category])
        else:
            n_preselected[category] = 0

        row_map = ticker_category_info_map[category]['row']
        # preselected_ticker_tables[category] = [tk for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]]
        preselected_ticker_tables[category] = [{tk: ticker_names[tk] for tk in row_map.keys() if row_map[tk] in table_selected_rows[category]}]

    return (
        n_preselected,
        preselected_ticker_tables
    )
    
##########################################################################

