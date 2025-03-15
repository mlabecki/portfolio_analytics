import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from mapping_plot_attributes import *
from mapping_portfolio_downloads import *
from mapping_tickers import *
from mapping_input_tables import *
from css_portfolio_analytics import *
from utils import *

app = Dash(__name__, external_stylesheets = [dbc.themes.YETI], suppress_callback_exceptions = True)

pseudoticker_text = """You can choose a pair of tickers to create a pseudoticker, whose value will be the ratio of the two tickers' prices, FX rates, or indices.
This can be useful for calculating non-USD currency exchange rates, converting foreign currency asset prices to USD, or comparing similar asset types
after converting them to a common currency. All plot types and features, except for volume, will be available for the selected pseudotickers."""

selected_ticker_names = {
    'CADUSD=X': 'CADUSD',
    'USDCAD=X': 'USDCAD',
    'EURUSD=X': 'EURUSD',
    'USDEUR=X': 'USDEUR',
    'JPYUSD=X': 'JPYUSD',
    'USDJPY=X': 'USDJPY',
    'TSLA':     'Tesla',
    'AMZN':     'Amazon',
    '^N225':    'Nikkei 225',
    '^GSPC':    'S&P 500',
    '^GDAXI':   'DAX',
    'BMW.DE':   'BMW',
    '7201.T':   'Nissan'
}
selected_ticker_currencies = {
    'CADUSD=X': 'USD',
    'USDCAD=X': 'CAD',
    'EURUSD=X': 'USD',
    'USDEUR=X': 'EUR',
    'JPYUSD=X': 'USD',
    'USDJPY=X': 'JPY',
    'TSLA':     'USD',
    'AMZN':     'USD',
    '^N225':    'JPY',
    '^GSPC':    'USD',
    '^GDAXI':   'EUR',
    'BMW.DE':   'EUR',
    '7201.T':   'JPY'
}
selected_tickers = list(selected_ticker_names.keys())
first_tk = selected_tickers[0]
tk_den_first_legit = [tk for tk in selected_tickers[1:] if tk != (first_tk[3:6] + first_tk.replace(first_tk[3:6], ''))][0] if len(selected_tickers) > 1 else first_tk

hidden_pseudo = False if len(selected_tickers) >=2 else True

popover_pseudoticker_danger_style = {
    'border-radius': '5px',
    'border-color': 'rgb(255, 178, 185)',
    'background-color': 'rgb(255, 222, 220)'
}
popover_pseudoticker_warning_style = {
    'border-radius': '5px',
    'border-color': 'rgb(255, 208, 185)',
    'background-color': 'rgb(255, 245, 220)'    
}

def display_table_selected_tickers(
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
    
    # selected_tickers = [row['Ticker'] for row in table_data]
    selected_tickers = selected_ticker_names.keys()

    # This table appears in TICKERS tab under GENERAL SETTINGS
    dash_table_tickers_to_plot = dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in ['Ticker', 'Name']],
        data = [{'Ticker': tk, 'Name': selected_ticker_names[tk]} for tk in selected_tickers],
        editable = False,
        row_selectable = 'multi',
        selected_rows = [0],
        # selected_rows = [],
        css = [
            {   # Hide the header
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
            'rule': 'max-width: 500px; width: 500px !important; border: 1px solid rgb(211, 211, 211) !important; border-radius: 5px !important; padding: 10px; padding: 10px 12px 0px 12px; font-size: 12px; font-family: Helvetica; background-color: rgb(211, 211, 211);'
            },
            {
            'selector': '.dash-tooltip:before, .dash-tooltip:after',
            'rule': 'border-top-color: rgb(211, 211, 211) !important; border-bottom-color: rgb(211, 211, 211) !important;'
            }
        ],
        tooltip_delay = 0,
        tooltip_duration = None,
        # style_as_list_view = True,

        style_data_conditional = [
            {'if': 
                {'state': 'active'},
                'width': '305px !important',
                'backgroundColor': 'white',
                'border-top': '1px solid rgb(211, 211, 211)',
                'border-bottom': '1px solid rgb(211, 211, 211)'},
            # {'if': {'column_id': 'No.'}, 'width': 24, 'padding-left': '8px'},
            {'if': {'column_id': 'Ticker'}, 'width': 60},
            {'if': {'column_id': 'Name'}, 'width': 200},
        ],
        id = 'dash-table-tickers-to-plot',
        style_table={'overflowX': 'auto'},
        style_data = selected_pseudotickers_table_data_css
    )

    return dash_table_tickers_to_plot


##################################################################

def initialize_table_pseudotickers():

    dash_table_pseudotickers_to_plot = dash_table.DataTable(
        columns = [{'name': i, 'id': i} for i in ['Pseudoticker']],
        data = [],
        editable = False,
        row_selectable = 'multi',
        row_deletable = True,
        selected_rows = [],
        tooltip_data = [],
        css = [
            {   # Hide the header
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
            'rule': 'max-width: 500px; width: 500px !important; border: 1px solid rgb(211, 211, 211) !important; border-radius: 5px !important; padding: 10px; padding: 10px 12px 0px 12px; font-size: 12px; font-family: Helvetica; background-color: rgb(211, 211, 211);'
            },
            {
            'selector': '.dash-tooltip:before, .dash-tooltip:after',
            'rule': 'border-top-color: rgb(211, 211, 211) !important; border-bottom-color: rgb(211, 211, 211) !important;'
            }
        ],
        tooltip_delay = 0,
        tooltip_duration = None,
        # style_as_list_view = True,
        style_data_conditional = [
            {'if': 
                {'state': 'active'},
                'width': '305px !important',
                'backgroundColor': 'white',
                'border-top': '1px solid rgb(211, 211, 211)',
                'border-bottom': '1px solid rgb(211, 211, 211)'},
            {'if': {'column_id': 'Ticker'}, 'width': 150},
            {'if': {'column_id': 'Name'}, 'width': 120},
        ],
        id = 'dash-table-pseudotickers-to-plot',
        style_table={'overflowX': 'auto'},
        style_data = selected_pseudotickers_table_data_css
    )
    
    return dash_table_pseudotickers_to_plot


##########################################################################################

app.layout = (

    dcc.Store(data = {}, id = 'selected-pseudoticker-info', storage_type = 'memory'),

    # html.Div(
    #     id = 'selected-pseudoticker-info',
    #     children = [],
    #     hidden = True
    # ),

    html.Div([
        html.Div(
            id = 'select-tickers-to-plot-title',
            children= ['Select Tickers To Plot'],
            style = {
                'width': '305px',
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
            children = [display_table_selected_tickers(selected_ticker_names)],
            style = {
                'width': '305px',
                'margin-left': '10px'
            }
        ),
        ],
        style = {
            'width': '305px',
            'display': 'block',
            'margin-right': '0px',
            'margin-left': '10px',
            'vertical-align': 'middle',
            'font-family': 'Helvetica'
        }
    ),

    html.Div(
        id = 'pseudoticker-controls-container',
        hidden = hidden_pseudo,
        children = [
            html.Div(
                id = 'select-pseudotickers-to-plot-title',
                hidden = hidden_pseudo,
                children= [pseudoticker_text],
                style = {
                    'width': '305px',
                    'display': 'block',
                    'font-family': 'Helvetica',
                    'font-size': '14px',
                    'vertical-align': 'top',
                    'margin-top': '15px',
                    'margin-bottom': '10px',
                    'line-height': '20px',
                    'text-align': 'justify',
                    'padding': '2px'
                }
            ),
            # dbc.Popover(
            #     [
            #     html.Span(
            #         """Pseudotickers will be plotted just like regular tickers (except for volume), i.e. individually on separate graphs with common plot features as selected.""",
            #         style = popover_menu_collapse_button_header_css
            #         )
            #     ], 
            #     id = 'popover-select-pseudotickers-to-plot-title',
            #     target = 'select-pseudotickers-to-plot-title',
            #     body = False,
            #     trigger = 'hover',
            #     hide_arrow = True,
            #     style = popover_menu_button_css
            # ),
            html.Div([
                html.Div('Numerator Ticker', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                dcc.Dropdown(
                    id = 'pseudoticker-numerator-dropdown',
                    className = 'plots-dropdown-button',
                    options = selected_tickers,
                    value = selected_tickers[0],
                    clearable = False,
                    style = {'width': '150px'}
                )],
                style = {'display': 'inline-block', 'margin-right': '5px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
            ),
            html.Div([
                html.Div('Denominator Ticker', style = {'font-size': '14px', 'font-weight': 'bold', 'vertical-align': 'top', 'margin-top': '0px', 'margin-left': '2px'}),
                dcc.Dropdown(
                    id = 'pseudoticker-denominator-dropdown',
                    className = 'plots-dropdown-button',
                    options = selected_tickers,
                    value = tk_den_first_legit,
                    # value = selected_tickers[1] if len(selected_tickers) >= 2 else selected_tickers[0],
                    clearable = False,
                    style = {'width': '150px'}
                )],
                style = {'display': 'inline-block', 'margin-right': '0px', 'margin-bottom': '5px', 'vertical-align': 'top', 'font-family': 'Helvetica'}
            ),
        ],
        style = {
            'width': '305px',
            'margin-left': '10px'
        }
    ),

    html.Div([
        html.Div(
            dbc.Button(
                'Create Pseudoticker From This Pair',
                id = 'create-pseudoticker-button',
                n_clicks = 0,
                class_name = 'ma-1',
                color = 'light',
                size = 'sm',
                style = create_pseudoticker_button_css
            )
        ),
        dbc.Popover(
            [
            html.Div(
                id = 'popover-create-pseudoticker-button-div',
                children = [],
                hidden = True,
                style ={
                    'width': '300px !important',
                    'padding': '2px 3px 2px 3px',
                    'vertical-align': 'middle',
                    'text-align': 'center',
                    'font-family': 'Helvetica',
                    'font-size': '13px',
                    'color': 'black'
                }
            )
            ], 
            id = 'popover-create-pseudoticker-button',
            target = 'create-pseudoticker-button',
            body = False,
            trigger = 'click',
            hide_arrow = True,
            # delay = {'show': 0, 'hide': 10000},
            style = popover_pseudoticker_danger_style
        ),

        html.Div(
            id = 'dash-table-pseudotickers-to-plot-div',
            children = [initialize_table_pseudotickers()],
            style = {
                'width': '305px',
                'margin-left': '10px'
            }
        ),
        ],
        style = {
            'display': 'block',
            'margin-right': '0px',
            'vertical-align': 'middle',
            'font-family': 'Helvetica'
        }
    ),
)


########################################################################

@callback(

    Output('popover-create-pseudoticker-button-div', 'hidden'),
    Output('popover-create-pseudoticker-button-div', 'children'),
    Output('popover-create-pseudoticker-button', 'style'),
    Output('selected-pseudoticker-info', 'data'),
    Output('dash-table-pseudotickers-to-plot', 'data'),
    Output('dash-table-pseudotickers-to-plot', 'tooltip_data'),
    Output('dash-table-pseudotickers-to-plot', 'selected_rows'),
    Output('pseudoticker-numerator-dropdown', 'options'),
    Output('pseudoticker-denominator-dropdown', 'options'),

    State('pseudoticker-numerator-dropdown', 'value'),
    State('pseudoticker-denominator-dropdown', 'value'),

    Input('create-pseudoticker-button', 'n_clicks'),
    Input('selected-pseudoticker-info', 'data'),
    Input('dash-table-pseudotickers-to-plot', 'data'),
    Input('dash-table-pseudotickers-to-plot', 'tooltip_data'),
    Input('dash-table-pseudotickers-to-plot', 'selected_rows'),
    Input('popover-create-pseudoticker-button-div', 'children'),
    Input('popover-create-pseudoticker-button', 'style'),

)
def display_table_selected_pseudotickers(
    tk_num,
    tk_den,
    n_click_pseudo,
    selected_pseudoticker_info,
    table_pseudoticker_data,
    table_pseudoticker_tooltip_data,
    table_pseudoticker_selected_rows,
    message_popover_create_pseudoticker,
    popover_pseudoticker_style

):
    """
    table_data:
        list of dictionaries in the 'records' format
    table_tooltip_data:
        a list of ticker summaries (descriptions)
    downloaded_data:
        a dictionary of historical price and volume data with selected tickers as keys
    """
    
    # selected_tickers = [row['Ticker'] for row in table_data]
    # selected_pseudoticker_info[idx] = {
    #     'tk_num': tk_num,
    #     'tk_den': tk_den,
    #     'pseudo_tk': pseudo_tk,
    #     'pseudo_tk_name': pseudo_tk_name,
    #     'pseudo_tk_summary': pseudo_tk_summary,
    # }

    # selected_tickers_augmented will contain any pseudotickers created from fx tickers, e.g. JPYEUR
    # selected_tickers_augmented = selected_tickers.copy()

    hidden_popover_create_pseudoticker = True
    # message_popover_create_pseudoticker = ''
    # popover_pseudoticker_style = popover_pseudoticker_danger_style

    print(f'start\n\tmessage_popover_create_pseudoticker = {message_popover_create_pseudoticker}')
    
    ctx = dash.callback_context

    if n_click_pseudo:
        
        hidden_popover_create_pseudoticker = False
        print(f'n_click_pseudo\n\tmessage_popover_create_pseudoticker = {message_popover_create_pseudoticker}')

        if ctx.triggered:

            # hidden_popover_create_pseudoticker = False
            # print(f'ctx_triggered\n\tmessage_popover_create_pseudoticker = {message_popover_create_pseudoticker}')

            if (tk_num != tk_den) & (tk_num != tk_den[3:6] + tk_den.replace(tk_den[3:6], '')):
                # Tickers must be different and cannot be mutually inverse fx rates for the same currency

                if tk_num.endswith('=X') & tk_den.endswith('=X'):
                    pseudo_tk = tk_num.replace('USD', '').replace('=X', '') + tk_den.replace('USD', '')
                else:
                    pseudo_tk = tk_num + '/' + tk_den

                idx = str(len(selected_pseudoticker_info))  # dcc.Store converts int to string in dictionary keys

                if int(idx) > 0:
                    selected_pseudoticker_indices = list(selected_pseudoticker_info.keys())
                    selected_pseudotickers = [selected_pseudoticker_info[i]['pseudo_tk'] for i in selected_pseudoticker_indices]
                    new_pseudo_tk = False if pseudo_tk in selected_pseudotickers else True
                else:
                    selected_pseudoticker_indices = []
                    selected_pseudotickers = []
                    new_pseudo_tk = True

                if new_pseudo_tk:

                    selected_pseudoticker_info[idx] = {}              

                    selected_pseudoticker_info[idx]['tk_num'] = tk_num
                    selected_pseudoticker_info[idx]['tk_den'] = tk_den
                    selected_pseudoticker_info[idx]['pseudo_tk'] = pseudo_tk

                    selected_pseudoticker_indices.append(idx)
                    selected_pseudotickers.append(pseudo_tk)

                    selected_pseudoticker_index_map = dict(zip(selected_pseudotickers, selected_pseudoticker_indices))

                    pseudo_tk_name = ''
                    pseudo_tk_summary = ''
                    pseudo_tk_currency = 'USD'  # This will be adjusted below, if necessary

                    ################### 

                    if tk_num.endswith('USD=X'):
                        # The numerator is the price of another currency in USD, e.g. JPYUSD=X

                        cur_num = tk_num.replace('USD=X', '')

                        if tk_den.endswith('USD=X'):
                            # Example: JPYUSD=X/EURUSD=X
                            tk_num_name = tk_num.replace('USD=X', '')
                            tk_den_name = tk_den.replace('USD=X', '')
                            pseudo_tk_name = tk_num_name + '/' + tk_den_name
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The exchange rate between {tk_num_name} and {tk_den_name}, or the price of {tk_num_name} in {tk_den_name}.'
                            if pseudo_tk not in selected_tickers:
                                selected_tickers.append(pseudo_tk)
                            pseudo_tk_currency = tk_den_name

                        elif tk_den.startswith('USD') & tk_den.endswith('=X'):
                            # Example [Incorrect]: JPYUSD=X/USDEUR=X (need to invert either Numerator or Denominator)
                            cur_den = tk_den.replace('USD', '').replace('=X', '')
                            hidden_popover_create_pseudoticker = False
                            message_popover_create_pseudoticker = f"Did you mean {tk_num} and {cur_den}USD=X? Or USD{cur_num}=X and {tk_den}?"

                        else:
                            # We will only allow a ratio of currency to an index
                            # For a ratio of a currency to priced asset we will suggest an inverse, i.e. the asset converted to the appropriate currency
                            cur_den = selected_ticker_currencies[tk_den]
                            
                            if tk_den.startswith('^'):
                                if (cur_num == cur_den) | (cur_den == 'USD'):
                                    # Example: JPYUSD=X/^N225 or JPYUSD=X/^GSPC
                                    hidden_popover_create_pseudoticker = True
                                    tk_num_name = tk_num.replace('=X', '')
                                    pseudo_tk_name = tk_num_name + '/' + tk_den
                                    pseudo_tk_currency = cur_den
                                    pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num_name} (the exchange rate between {cur_num} and USD) to {tk_den} values. Its currency is set to {cur_den}.'
                                else:
                                    # Example [Incorrect]: JPYUSD=X/^GDAXI
                                    hidden_popover_create_pseudoticker = False
                                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                                    message_popover_create_pseudoticker = f'NOTE: {tk_den} is based on prices in {cur_den}. Did you mean to use {cur_num}USD=X as Numerator?'
                            else:
                                hidden_popover_create_pseudoticker = False
                                if cur_den == 'USD':
                                    # Example [Incorrect]: JPYUSD=X/AMZN
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is USD. If you want to convert it to {cur_num}, use {tk_den} as Numerator and {tk_num} as Denominator."
                                elif cur_den == cur_num:
                                    # Example [Incorrect]: JPYUSD=X/7201.T (Nissan). The correct fx ticker for converting JPY to USD is USDJPY=X.
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is {cur_den}. If you want to convert it to USD, use {tk_den} as Numerator and USD{cur_den}=X as Denominator."
                                else:
                                    # Example: JPYUSD=X/BMW.DE (currency: EUR)
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is {cur_den}. If you want to convert it to USD, use {tk_den} as Numerator and USD{cur_den}=X as Denominator."
                                    message_popover_create_pseudoticker += f" If you want to convert it to {cur_num}, create a pseudoticker {cur_den}{cur_num}=X"
                                    message_popover_create_pseudoticker += f" and then use {tk_den} as Numerator and {cur_den}{cur_num}=X as Denominator."

                    ###################

                    elif tk_num.startswith('USD') & tk_num.endswith('=X'):
                        # The numerator is the price of USD in another currency, e.g. USDJPY=X

                        # In this case numerator and denominator are effectively swapped
                        cur_num = tk_num.replace('USD', '').replace('=X', '')

                        if tk_den.startswith('USD') & tk_den.endswith('=X'):
                            # Example: USDJPY=X/USDEUR=X
                            tk_num_name = tk_num.replace('USD', '').replace('=X', '')
                            tk_den_name = tk_den.replace('USD', '').replace('=X', '')
                            pseudo_tk_name = tk_den_name + '/' + tk_num_name
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The exchange rate between {tk_den_name} and {tk_num_name}, or the price of {tk_den_name} in {tk_num_name}.'
                            if pseudo_tk not in selected_tickers:
                                # Adding pseudo_tk to the Numerator and Denominator dropdown lists
                                selected_tickers.append(pseudo_tk)
                            pseudo_tk_currency = cur_num

                        elif tk_den.endswith('USD=X'):
                            # # Example [Incorrect]: USDJPY=X/EURUSD=X (need to invert either Numerator or Denominator)
                            cur_den = tk_den.replace('USD=X', '')
                            hidden_popover_create_pseudoticker = False
                            message_popover_create_pseudoticker = f"Did you mean {tk_num} and USD{cur_den}=X? Or {cur_num}USD=X and {tk_den}?"

                        else:
                            # We will only allow a ratio of currency to an index
                            # NOTE: A ratio of currency to price is not allowed but an inverse of price to currency may be

                            cur_den = selected_ticker_currencies[tk_den]
                            if tk_den.startswith('^'):
                                if (cur_num == cur_den) | (cur_den == 'USD'):
                                    # Example: USDJPY=X/^N225 or USDJPY=X/^GSPC
                                    hidden_popover_create_pseudoticker = True
                                    tk_num_name = tk_num.replace('=X', '')
                                    pseudo_tk_name = tk_num_name + '/' + tk_den
                                    pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num_name} (the exchange rate between {cur_num} and USD) to {tk_den} values.'
                                    pseudo_tk_currency = cur_den
                                else:
                                    # Example [Incorrect]: USDJPY=X/^GDAXI
                                    hidden_popover_create_pseudoticker = False
                                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                                    message_popover_create_pseudoticker = f'NOTE: {tk_den} is based on prices in {cur_den}. Did you mean to use USD{cur_num}=X as Numerator?'

                            else:
                                hidden_popover_create_pseudoticker = False
                                if cur_den == 'USD':
                                    # Example [Incorrect}: USDJPY=X/AMZN. The correct fx ticker for converting USD to JPY is JPYUSD=X.
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is USD. If you want to convert it to {cur_num}, use {tk_den} as Numerator and {cur_num}USD=X as Denominator."
                                elif cur_den == cur_num:
                                    # Example [Incorrect]: USDJPY=X/7201.T (Nissan)
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is {cur_den}. If you want to convert it to USD, use {tk_den} as Numerator and {tk_num} as Denominator."
                                else:
                                    # Example: USDJPY=X/BMW.DE (currency: EUR)
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is {cur_den}. If you want to convert it to USD, use {tk_den} as Numerator and {cur_den}USD=X as Denominator."
                                    message_popover_create_pseudoticker += f" If you want to convert it to {cur_num}, create a pseudoticker {cur_den}{cur_num}=X"
                                    message_popover_create_pseudoticker += f" and then use {tk_den} as Numerator and {cur_den}{cur_num}=X as Denominator."


                    ################### BEGIN PSEUDOTICKER tk_num

                    if tk_num.endswith('=X'):
                        # A pseudoticker composed of two non-USD currencies, e.g. JPYEUR=X
                        # Restrict its use to combination with a ticker that is in one of the currencies, e.g. BMW.DE or 7201.T
                        #
                        # NOTE: Pseudotickers created by converting prices or indices to another currency for the purpose
                        #       of comparison with another asset of the same type should be allowed.
                        #       For example:
                        #    1. Convert 7201.T to EUR (pseudoticker 7201.T/JPYEUR=X) for direct comparison with BMW.DE through the pseudoticker
                        #       (7201.T/JPYEUR=X)/BMW.DE. Creation of a pseudoticker from two non-currency tickers priced in different currencies
                        #       should not be allowed.
                        #    2. Convert ^N225 to USD for a more meaningful comparison with ^GSPC. Indices are not expressed in currencies but
                        #       are derived from prices in the exchange's currency, thus reflecting market conditions in that local currency.
                        #       A direct comparison of indices composed of assets in different currencies should be allowed with a note that 
                        #       bringing the indices to a common currency would be more meaningful.
                        #
                        # Allowed pseudotickers types:
                        #    First order (both tickers are in the original selected ticker list, including the invertd fx tickers):
                        #       1. JPYEUR=X:           Two non-USD currencies (shortened from JPYUSD=X/EURUSD=X to the yf format)
                        #       2. AMZN/JPYUSD=X:      Stock/ETF/Future price in USD converted to a foreign currency
                        #       3. BMW.DE/USDEUR=X:    Stock/ETF/Future price in foreign currency converted to USD
                        #



                        tk_num_1 = tk_num[:3]
                        tk_num_2 = tk_num[3:6]
                        if tk_den.endswith('=X'):
                            hidden_popover_create_pseudoticker = False
                            message_popover_create_pseudoticker = ''  #f"You can only combine {tk_num} with a ticker in  "
                            

                        cur_num = tk_num.replace('USD=X', '')

                        if tk_den.endswith('USD=X'):
                            tk_num_name = tk_num.replace('USD=X', '')
                            tk_den_name = tk_den.replace('USD=X', '')
                            pseudo_tk_name = tk_num_name + '/' + tk_den_name
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The exchange rate between {tk_num_name} and {tk_den_name}, or the price of {tk_num_name} in {tk_den_name}.'
                            if pseudo_tk not in selected_tickers:
                                selected_tickers.append(pseudo_tk)

                        elif tk_den.startswith('USD') & tk_den.endswith('=X'):
                            cur_den = tk_den.replace('USD', '').replace('=X', '')
                            hidden_popover_create_pseudoticker = False
                            message_popover_create_pseudoticker = f"Did you mean {tk_num} and {cur_den}USD=X? Or USD{cur_num}=X and {tk_den}?"

                        else:
                            # We will only allow a ratio of currency to an index (or a currency-free asset).
                            cur_den = selected_ticker_currencies[tk_den]
                            if tk_den.startswith('^') | (cur_den == ''):
                                # An index, no currency
                                tk_num_name = tk_num.replace('=X', '')
                                pseudo_tk_name = tk_num_name + '/' + tk_den
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num_name} (the exchange rate between {cur_num} and USD) to {tk_den} values.'
                            else:
                                hidden_popover_create_pseudoticker = False
                                if cur_den == 'USD':
                                    # For example, JPYUSD=X and AMZN
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is USD. If you want to convert it to {cur_num}, use {tk_den} as Numerator and {tk_num} as Denominator."
                                elif cur_den == cur_num:
                                    # For example, (incorrect) JPYUSD=X and 7201.T (Nissan). The correct fx ticker for converting JPY to USD is USDJPY=X.
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is {cur_den}. If you want to convert it to USD, use {tk_den} as Numerator and USD{cur_den}=X as Denominator."
                                else:
                                    # For example, JPYUSD=X and BMW.DE (currency: EUR).
                                    # Should also allow conversion to cur_num by using tk_den (BMW.DE) as Numerator and a pseudoticker f'{cur_num}{cur_den}=X' (JPYEUR) as Denominator.
                                    message_popover_create_pseudoticker = f"The currency of {tk_den} is {cur_den}. If you want to convert it to USD, use {tk_den} as Numerator and USD{cur_den}=X as Denominator."
                                    message_popover_create_pseudoticker += f" If you want to convert it to {cur_num}, create a pseudoticker {cur_den}{cur_num}=X"
                                    message_popover_create_pseudoticker += f" and then use {tk_den} as Numerator and {cur_den}{cur_num}=X as Denominator."

                    ################### END PSEUDOTICKER tk_num

                    else:
                        # The numerator ticker is NOT a currency FX rate, i.e. it doesn't end with '=X'

                        pseudo_tk_idx = selected_pseudoticker_index_map[tk_num]
                        cur_num = selected_pseudoticker_info[pseudo_tk_idx][tk_num]

                        if tk_den.endswith('USD=X'):
                            cur_den = tk_den.replace('USD=X', '')
                            tk_den_name = tk_den.replace('=X', '')
                            if cur_num == 'USD':
                                # For example, AMZN and JPYUSD=X.
                                pseudo_tk_name = tk_num + '/' + tk_den_name
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} price in USD to {tk_den_name} (the exchange rate between {cur_den} and USD). '
                                pseudo_tk_summary += f'This is the price of {tk_num} in {cur_den}.'
                                pseudo_tk_currency = cur_den
                            elif cur_num == cur_den:
                                # For example, 7201.T (Nissan) and (incorrect) JPYUSD=X. The correct fx ticker for conversion from JPY to USD is USDJPY=X.
                                hidden_popover_create_pseudoticker = False
                                message_popover_create_pseudoticker = f"The currency of {tk_num} is {cur_den}. If you want to convert it to USD, use USD{cur_den }=X."
                            elif cur_num != '':
                                # For example, BMW.DE (currency: EUR) and JPYUSD=X.
                                # Should also allow conversion to cur_den (JPY) by using a pseudoticker f'{cur_den}{cur_num}=X' (EURJPY) as Denominator.
                                hidden_popover_create_pseudoticker = False
                                message_popover_create_pseudoticker = f"The currency of {tk_num} is {cur_num}. If you want to convert it to USD, use USD{cur_num}=X."
                                message_popover_create_pseudoticker += f" If you want to convert it to {cur_den}, create a pseudoticker {cur_den}{cur_num}=X and use it as Denominator."
                            else:
                                # No currency, e.g. an index, and CADUSD=X. Doesn't make much sense but it's not incorrect.
                                pseudo_tk_name = tk_num + '/' + tk_den_name
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den_name} (the exchange rate between {cur_den} and USD).'

                        elif tk_den.startswith('USD') & tk_den.endswith('=X'):
                            
                            cur_den = tk_den.replace('USD', '').replace('=X', '')
                            tk_den_name = tk_den.replace('=X', '')
                            if cur_num == 'USD':
                                # For example, AMZN and (incorrect) USDJPY=X.
                                hidden_popover_create_pseudoticker = False
                                message_popover_create_pseudoticker = f"The currency of {tk_num} is USD. If you want to convert it to {cur_den}, use {cur_den}USD=X."
                            elif cur_num == cur_den:
                                # For example, 7201.T (Nissan) and USDJPY=X.
                                pseudo_tk_name = tk_num + '/' + tk_den_name
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} price in {cur_den} to {tk_den_name} (the exchange rate between USD and {cur_den}). '
                                pseudo_tk_summary += f'This is the price of {tk_num} in USD.'
                                pseudo_tk_currency = cur_den
                            else:
                                # For example, BMW.DE (currency: EUR) and USDJPY=X.
                                # Should also allow conversion to cur_den (JPY) by using a pseudoticker f'{cur_den}{cur_num}=X' (EURJPY) as Denominator.
                                hidden_popover_create_pseudoticker = False
                                message_popover_create_pseudoticker = f"The currency of {tk_num} is {cur_num}. If you want to convert it to USD, use USD{cur_num}=X."
                                message_popover_create_pseudoticker += f" If you want to convert it to {cur_den}, create a pseudoticker {cur_den}{cur_num}=X and use it as Denominator."

                        else:
                            
                            # Only allow if tk_num and tk_den are both indices, or they're both in the same currency
                            
                            cur_den = selected_ticker_currencies[tk_den]

                            if tk_num.startswith('^') & tk_den.startswith('^'):
                                # Two indices
                                # Check currencies - if they're different, allow with a note that conversion common currency would be more meaningful. 
                                # If they're different and neither is USD, advise to create a non-USD fx pseudoticker first, before converting.
                                pseudo_tk_name = tk_num + '/' + tk_den
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den} values.'
                                pseudo_tk_currency = cur_num  # This is only pro-forma
                                if cur_num != cur_den:
                                    popover_pseudoticker_style = popover_pseudoticker_warning_style
                                    hidden_popover_create_pseudoticker = False
                                    message_popover_create_pseudoticker = f'NOTE: This is a raw ratio of the two indices, where {tk_num} is based on {cur_num} prices and {tk_den} on {cur_den} prices.'
                                    message_popover_create_pseudoticker += f' In order to account for FX effects, you may want to adjust them to a common currency.'
                                    if cur_num == 'USD':
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_den} to USD by first creating a pseudoticker {tk_den}/USD{cur_den}=X, and then {tk_num}/({tk_den}/USD{cur_den}=X) for an FX-adjusted comparison between the two indices.'
                                    elif cur_den == 'USD':
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_num} to USD by first creating a pseudoticker {tk_num}/USD{cur_num}=X, and then ({tk_num}/USD{cur_num}=X)/{tk_den} for an FX-adjusted comparison between the two indices.'
                                    else:
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_den} to {cur_num} by first creating a pseudoticker {cur_num}{cur_den}=X from {cur_num}USD=X and {cur_den}USD=X,'
                                        message_popover_create_pseudoticker += f' then a pseudoticker {tk_den}/{cur_num}{cur_den}=X, and finally {tk_num}/({tk_den}/{cur_num}{cur_den}=X) for an FX-adjusted comparison between the two indices.'

                            elif (not tk_num.startswith('^')) & (not tk_den.startswith('^')):
                                # Two prices
                                # !!! Check currencies - if they're different, do not allow to create pseudoticker. Advise to convert to a common currency first. 
                                # If neither currency is USD - advise to create a non-USD fx pseudoticker first, before converting.
                                if cur_num != cur_den:
                                    hidden_popover_create_pseudoticker = False
                                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                                    message_popover_create_pseudoticker = f"{tk_num} is priced in {cur_num} and {tk_den} in {cur_den}. They must be in a common currency in order to create a pseudoticker."
                                    if cur_num == 'USD':
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_den} to USD by first creating a pseudoticker {tk_den}/USD{cur_den}=X, and then {tk_num}/({tk_den}/USD{cur_den}=X) for an FX-adjusted comparison between the two indices.'
                                    elif cur_den == 'USD':
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_num} to USD by first creating a pseudoticker {tk_num}/USD{cur_num}=X, and then ({tk_num}/USD{cur_num}=X)/{tk_den} for an FX-adjusted comparison between the two indices.'
                                    else:
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_den} to {cur_num} by first creating a pseudoticker {cur_num}{cur_den}=X from {cur_num}USD=X and {cur_den}USD=X,'
                                        message_popover_create_pseudoticker += f' then a pseudoticker {tk_den}/{cur_num}{cur_den}=X, and finally {tk_num}/({tk_den}/{cur_num}{cur_den}=X) for an FX-adjusted comparison between the two indices.'
                                else:
                                    hidden_popover_create_pseudoticker = True
                                    pseudo_tk_name = tk_num + '/' + tk_den
                                    pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den} prices.'
                                    pseudo_tk_currency = cur_num

                            else:
                                # One index and one price
                                # Check currencies - if they're different, do not allow to create pseudoticker. Advise to convert to a common currency first. 
                                # If neither currency is USD - advise to create a non-USD fx pseudoticker first, before converting.
                                if cur_num != cur_den:
                                    hidden_popover_create_pseudoticker = False
                                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                                    message_popover_create_pseudoticker = f"{tk_num} is priced in {cur_num} and {tk_den} in {cur_den}. They must be in a common currency in order to create a pseudoticker."
                                    if cur_num == 'USD':
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_den} to USD by first creating a pseudoticker {tk_den}/USD{cur_den}=X, and then {tk_num}/({tk_den}/USD{cur_den}=X) for an FX-adjusted comparison between the two indices.'
                                    elif cur_den == 'USD':
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_num} to USD by first creating a pseudoticker {tk_num}/USD{cur_num}=X, and then ({tk_num}/USD{cur_num}=X)/{tk_den} for an FX-adjusted comparison between the two indices.'
                                    else:
                                        message_popover_create_pseudoticker += f' For example, you could adjust {tk_den} to {cur_num} by first creating a pseudoticker {cur_num}{cur_den}=X from {cur_num}USD=X and {cur_den}USD=X,'
                                        message_popover_create_pseudoticker += f' then a pseudoticker {tk_den}/{cur_num}{cur_den}=X, and finally {tk_num}/({tk_den}/{cur_num}{cur_den}=X) for an FX-adjusted comparison between the two indices.'
                                else:
                                    hidden_popover_create_pseudoticker = True
                                    pseudo_tk_name = tk_num + '/' + tk_den
                                    pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den} prices and values.'
                                    pseudo_tk_currency = cur_num
                                

                    ########################

                    if pseudo_tk_name != '':
                        
                        selected_pseudoticker_info[idx]['pseudo_tk_name'] = pseudo_tk_name
                        selected_pseudoticker_info[idx]['pseudo_tk_summary'] = pseudo_tk_summary
                        selected_pseudoticker_info[idx]['currency'] = pseudo_tk_currency

                        table_pseudoticker_data.append({
                            'Pseudoticker': pseudo_tk
                            # 'Name': pseudo_tk_name
                        })    

                        table_pseudoticker_selected_rows = [int(idx) for idx in selected_pseudoticker_indices]
                        table_pseudoticker_tooltip_data.append({
                            column: {'value': pseudo_tk_summary, 'type': 'markdown' }
                            # for column in ['Pseudoticker', 'Name'] }
                            for column in ['Pseudoticker'] }
                        )
            else:
                
                # Cancel popover message if tk_num or tk_den have changed
                hidden_popover_create_pseudoticker = True
                message_popover_create_pseudoticker = ''
                # print(f'n_click_pseudo\n\tmessage_popover_create_pseudoticker = {message_popover_create_pseudoticker}')

    # print(f'(END)\n{selected_pseudoticker_info}')

    return (
        hidden_popover_create_pseudoticker,
        message_popover_create_pseudoticker,
        popover_pseudoticker_style,
        selected_pseudoticker_info,
        table_pseudoticker_data,
        table_pseudoticker_tooltip_data,
        table_pseudoticker_selected_rows,
        selected_tickers,
        selected_tickers
    )


##############################################################

if __name__ == '__main__':
    app.run(debug = True, port = 8887)


##############################################################


"""
Q:
What is the unit of a market exchange index such as S&P 500 or Nikkei 225? Is it the currency, such as USD or JPY, or is it just a number?
What I need to know is whether we can compare the values of different market indices directly or do we need to bring them to a common currency first?

--------
Copilot:
Market exchange indices, like the S&P 500 or Nikkei 225, don't have a direct "unit" like a currency. Instead, their values are expressed as numbers. 
These numbers represent the weighted average of the prices of a group of stocks in the index, adjusted by factors such as market capitalization 
or other proprietary calculations.

Because these indices are just numbers and not tied to a specific currency, their values can't be compared directly across markets. 
For example, the value of the S&P 500 and the Nikkei 225 are calculated using different methodologies, and they reflect the performance of companies 
within their respective regions (U.S. and Japan). Additionally, the S&P 500 is influenced by USD-based stock prices, while the Nikkei 225 uses JPY-based prices.

To meaningfully compare indices across markets, you'd need to consider several factors:
1. **Currency exchange rates**: Convert the values into a common currency to reflect purchasing power or investment comparisons.
2. **Index composition and methodology**: Understand what each index measures and how its value is calculated.
3. **Historical and contextual differences**: Regional economic conditions, industry representation, and market dynamics also play a significant role.

Would you like to dive deeper into how these indices are calculated or how currency exchange impacts investments? I’d be happy to explain further!

--------
Q:
I'm just trying to clarify at the high level whether - analytically speaking - I need to apply currency conversion when comparing the values of those 
two indices, as I would need to in the case of stock prices in differet currencies. I don't need to dive into index composition or economic 
considerations at this point, just want to make sure that I use the numbers right. If I think of S&P 500 as a strength indicator of the US market and Nikkei 
as a strength indicator of the Japanese market, couldn't I just look at their ratio directly for a ballpark comparison? And then if I wanted to refine 
that comparison by bringing the two indices to a common currency (although they're not expressed in any currency like stock or ETF prices) - 
e.g. divide the Nikkei index by the price of USD in JPY - would that make that comparison much more meaningful?

--------
Copilot:
Great question! At a high level, you’re correct that indices like the S&P 500 and Nikkei 225 can be seen as relative "strength indicators" 
for their respective markets. For a quick ballpark comparison, you could indeed look at their ratio directly, treating each index as a standalone 
number without worrying about currency conversion. This would give you a rough sense of their relative magnitudes.

However, to refine this comparison and make it more meaningful, incorporating currency conversion is a smart approach. Since these indices indirectly reflect
market conditions in USD (for the S&P 500) and JPY (for the Nikkei 225), converting them to a common currency can provide a more apples-to-apples comparison. 
Dividing the Nikkei 225 by the USD/JPY exchange rate effectively adjusts the Nikkei's value to a dollar-equivalent term, allowing a more aligned perspective.

In short:
Quick comparison: Looking at the raw ratio is fine for a rough idea.
Refined comparison: Adjusting for currency adds depth and reduces distortion, especially if you’re making analytical or investment-related decisions.

"""