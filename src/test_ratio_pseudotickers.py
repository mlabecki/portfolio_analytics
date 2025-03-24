import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
# import json  # Useful to check if a callback output is serializable - use json.dumps(output)

from mapping_plot_attributes import *
from mapping_portfolio_downloads import *
from mapping_tickers import *
from mapping_input_tables import *
from css_portfolio_analytics import *
from utils import *

app = Dash(__name__, external_stylesheets = [dbc.themes.YETI], suppress_callback_exceptions = True)

pseudoticker_text = """You can select a pair of tickers to construct a pseudoticker, whose value will be the ratio of prices, FX rates, or indices. This can be useful for
calculating the exchange rate between two non-USD currencies; for converting foreign currency asset prices to USD or vice versa; or for comparing the relative performance
of similar asset types (making sure they are expressed in a common currency). All plot types and features, except for volume, will be available to the pseudotickers."""

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
popover_pseudoticker_success_style = {
    'border-radius': '5px',
    'border-color': 'rgb(152, 245, 178)',
    'background-color': 'rgb(212, 250, 220)'    
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
        row_deletable = False,
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
                    'line-height': '18px',
                    'text-align': 'justify',
                    'padding': '2px'
                }
            ),
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
            children = [
                'Click the VALIDATE PSEUDOTICKER button to check if the two selected tickers can be used to create a valid pseudoticker.'
            ],
            style = {
                'width': '305px',
                'display': 'block',
                'font-family': 'Helvetica',
                'font-size': '14px',
                'vertical-align': 'top',
                'margin-top': '1px',
                'margin-left': '10px',
                'margin-bottom': '5px',
                'line-height': '18px',
                'text-align': 'justify',
                'padding': '2px'
            }
        ),
        html.Div(
            dbc.Button(
                'VALIDATE PSEUDOTICKER',
                id = 'validate-pseudoticker-button',
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
                id = 'popover-validate-pseudoticker-button-div',
                children = [],
                hidden = True,
                style = {
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
            id = 'popover-validate-pseudoticker-button',
            target = 'validate-pseudoticker-button',
            body = False,
            trigger = 'click',
            hide_arrow = True,
            is_open = False,
            style = popover_pseudoticker_danger_style
        ),

        html.Div(
            dbc.Button(
                # 'Create Pseudoticker',
                'CREATE PSEUDOTICKER',
                id = 'create-pseudoticker-button',
                n_clicks = 0,
                class_name = 'ma-1',
                color = 'light',
                size = 'sm',
                disabled = True,
                style = create_pseudoticker_button_css
            )
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

    Output('selected-pseudoticker-info', 'data'),
    Output('popover-validate-pseudoticker-button-div', 'children'),  # Popover message goes here
    Output('popover-validate-pseudoticker-button-div', 'hidden'),
    Output('popover-validate-pseudoticker-button', 'style'),
    Output('popover-validate-pseudoticker-button', 'is_open'),
    Output('create-pseudoticker-button', 'disabled'),
    Output('dash-table-pseudotickers-to-plot', 'data'),
    Output('dash-table-pseudotickers-to-plot', 'tooltip_data'),
    Output('dash-table-pseudotickers-to-plot', 'selected_rows'),
    Output('validate-pseudoticker-button', 'n_clicks'),
    Output('create-pseudoticker-button', 'n_clicks'),

    State('pseudoticker-numerator-dropdown', 'value'),
    State('pseudoticker-denominator-dropdown', 'value'),

    Input('validate-pseudoticker-button', 'n_clicks'),
    Input('create-pseudoticker-button', 'n_clicks'),
    Input('selected-pseudoticker-info', 'data'),
    Input('dash-table-pseudotickers-to-plot', 'data'),
    Input('dash-table-pseudotickers-to-plot', 'tooltip_data'),
    Input('dash-table-pseudotickers-to-plot', 'selected_rows'),
    Input('popover-validate-pseudoticker-button-div', 'children'),  # Popover message goes here
    Input('popover-validate-pseudoticker-button', 'style')    
)
def display_table_selected_pseudotickers(
    tk_num,
    tk_den,
    n_click_validate,
    n_click_create,
    selected_pseudoticker_info,
    table_pseudoticker_data,
    table_pseudoticker_tooltip_data,
    table_pseudoticker_selected_rows,
    message_popover_validate_pseudoticker,
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

    selected_pseudoticker_info = {} if selected_pseudoticker_info is None else selected_pseudoticker_info

    def add_pseudoticker_info(
        tk_num,
        tk_den,
        cur_num,
        cur_den,
        pseudo_tk_name,
        pseudo_tk_summary,
        pseudo_tk_currency,
        required_fx_tickers
    ):
        """
        cur_num:
            Currency of Numerator
        cur_den:
            Currency of Denominator
        pseudo_tk_name:
            Typically tk_num/tk_den, with '=X' possibly omitted for FX pseudotickers
        pseudo_tk_summary:
            Popover text that will appear over each row in the table of pseudotickers.
            Typically: f'Pseudoticker {pseudo_tk_name}: ...'
        pseudo_tk_currency:
            Converted tickers will have a currency, e.g. USD for 7201.T/JPYUSD=X, or JPY for USDJPY=X/USDCAD=X (=CADJPY).
            Comparative tickers (e.g. AMZN/TSLA, BMW.DE/^N225) will be dimensionless.
        required_fx_tickers:
            List of FX tickers needed in case when the selected pseudoticker requires currency conversions(s).
            For example, BMW.DE/7201.T will require EURUSD=X and JPYUSD=X for the conversion of both tk_num
            and tk_den to a common currency (USD). The historical data for these FX tickers will have to be 
            downloaded if not selected by the user (i.e., if not in selected_tickers).
        """

        # print(f'FUNCTION START\n\tselected_pseudoticker_info = {selected_pseudoticker_info}')
        pseudo_tk = tk_num + '_' + tk_den
        if pseudo_tk not in selected_pseudoticker_info.keys():
            if tk_num != tk_den:
                # Tickers must be different
                tk_num_cond = tk_num == tk_den[3:6] + tk_den.replace(tk_den[3:6], '')
                tk_den_cond = tk_den == tk_num[3:6] + tk_num.replace(tk_num[3:6], '')
                if not (tk_num.endswith('=X') & tk_den.endswith('=X') & (tk_num_cond | tk_den_cond)):
                    # Tickers must not be mutually inverse fx rates for the same currency
                    selected_pseudoticker_info[pseudo_tk] = {}  # NOTE: A nested dictionary must be declared
                    idx = len(selected_pseudoticker_info)
                    selected_pseudoticker_info[pseudo_tk]['cur_num'] = cur_num
                    selected_pseudoticker_info[pseudo_tk]['cur_den'] = cur_den
                    selected_pseudoticker_info[pseudo_tk]['name'] = pseudo_tk_name
                    selected_pseudoticker_info[pseudo_tk]['summary'] = pseudo_tk_summary
                    selected_pseudoticker_info[pseudo_tk]['currency'] = pseudo_tk_currency            
                    selected_pseudoticker_info[pseudo_tk]['required_fx_tickers'] = required_fx_tickers
                    selected_pseudoticker_info[pseudo_tk]['idx'] = idx - 1
        
                    table_pseudoticker_data.append({'Pseudoticker': pseudo_tk_name})
                    table_pseudoticker_tooltip_data.append({
                        column: {'value': pseudo_tk_summary, 'type': 'markdown' }
                        for column in ['Pseudoticker'] }
                    )
        # print(f'FUNCTION END\n\tselected_pseudoticker_info = {selected_pseudoticker_info}')

    ##############################################################################################################

    pseudo_tk_name = ''
    pseudo_tk_summary = ''
    create_pseudoticker_disabled = False if n_click_create else True
    popover_hidden = False if n_click_validate else True
    popover_is_open = True if n_click_validate else False
    
    # ctx = dash.callback_context

    ##############################################################################################################################
    """
    NOTE: If the currency exchange rate needed to convert the asset price to USD is missing from the selected ticker list,
    then it must be downloaded without user's intervention, i.e. having to go back and selecting it from the FX category list.
    """
    ##############################################################################################################################
                
    if tk_num.endswith('USD=X'):
        # The numerator is the price of another currency in USD, e.g. JPYUSD=X

        cur_num = tk_num.replace('USD=X', '')

        if tk_den.endswith('USD=X'):
            # Example: JPYUSD=X/EURUSD=X
            cur_den = tk_den.replace('USD=X', '')
            pseudo_tk_name = cur_num + cur_den + '=X'  # Keep the Yahoo Finance FX ticker format
            if n_click_validate:
                if tk_num == tk_den:
                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                    message_popover_validate_pseudoticker = f'This is invalid. The two tickers must be different.'
                    create_pseudoticker_disabled = True
                else:
                    popover_pseudoticker_style = popover_pseudoticker_success_style
                    message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}, which is the exchange rate between {cur_num} and {cur_den}.'
                    message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'
                    create_pseudoticker_disabled = False
            if n_click_create:
                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The exchange rate between {cur_num} and {cur_den}, or the price of {cur_num} in {cur_den}.'
                pseudo_tk_currency = cur_den
                required_fx_tickers = []
                add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)

        elif tk_den.startswith('USD') & tk_den.endswith('=X'):
            # Example [Incorrect]: JPYUSD=X/USDEUR=X (need to invert either Numerator or Denominator)
            cur_den = tk_den.replace('USD', '').replace('=X', '')
            if n_click_validate:
                popover_pseudoticker_style = popover_pseudoticker_danger_style
                create_pseudoticker_disabled = True
                if cur_num == cur_den:
                    message_popover_validate_pseudoticker = f'This is invalid. The Denominator ticker cannot be an inverse of the Numerator ticker.'
                else:
                    message_popover_validate_pseudoticker = f'This is invalid. Did you mean {tk_num} and {cur_den}USD=X? Or USD{cur_num}=X and {tk_den}?'
                    
        else:
            # Stock/ETF/future or index
            cur_den = selected_ticker_currencies[tk_den]
            popover_pseudoticker_style = popover_pseudoticker_danger_style
            create_pseudoticker_disabled = True
            if cur_den == 'USD':
                # Example [Incorrect]: JPYUSD=X/AMZN or JPYUSD=X/^GSPC
                if n_click_validate:
                    message_popover_validate_pseudoticker = f'This is invalid. If you want to convert {tk_den} from USD to {cur_num}, use {tk_den} as Numerator and {tk_num} as Denominator.'
            elif cur_den == cur_num:
                # Example [Incorrect]: JPYUSD=X/7201.T (Nissan) or JPYUSD=X/^N225 (Nikkei). The correct fx ticker for converting JPY to USD is USDJPY=X.
                if n_click_validate: 
                    message_popover_validate_pseudoticker = f'This is invalid. If you want to convert {tk_den} from {cur_den} to USD, use {tk_den} as Numerator and USD{cur_den}=X as Denominator.'
            else:
                # Example: JPYUSD=X/BMW.DE or JPYUSD=X/^GDAXI (currency: EUR)
                # [NEW] Suggest using BMW.DE/EURUSD=X for conversion to USD, or BMW.DE/JPYUSD=X for conversion to JPY (BMW.DE is first converted to USD, then to JPY).
                if n_click_validate:
                    message_popover_validate_pseudoticker = f'This is invalid. If you want to convert {tk_den} from {cur_den} to USD, use {tk_den} as Numerator and USD{cur_den} as Denominator.'
                    message_popover_validate_pseudoticker += f' If you want to convert {tk_den} from {cur_den} to {cur_num}, use {tk_den} as Numerator and {cur_num}USD=X as Denominator.'

    ##################################################################################################################

    elif tk_num.startswith('USD') & tk_num.endswith('=X'):
        # The numerator is the price of USD in another currency, e.g. USDJPY=X
        # In this case numerator and denominator are effectively swapped

        cur_num = tk_num.replace('USD', '').replace('=X', '')

        if tk_den.startswith('USD') & tk_den.endswith('=X'):
            # Example: USDJPY=X/USDEUR=X
            cur_den = tk_den.replace('USD', '').replace('=X', '')
            pseudo_tk_name = cur_den + cur_num + '=X'  # Keep the Yahoo Finance FX ticker format    
            if n_click_validate:
                if tk_num == tk_den:
                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                    message_popover_validate_pseudoticker = f'This is invalid. The two tickers must be different.'
                    create_pseudoticker_disabled = True
                else:
                    popover_pseudoticker_style = popover_pseudoticker_success_style
                    message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}, which is the exchange rate between {cur_den} and {cur_num}.'
                    message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'                    
                    create_pseudoticker_disabled = False
            if n_click_create:
                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The exchange rate between {cur_den} and {cur_num}, or the price of {cur_den} in {cur_num}.'
                pseudo_tk_currency = cur_num
                required_fx_tickers = []
                add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)

        elif tk_den.endswith('USD=X'):
            # # Example [Incorrect]: USDJPY=X/EURUSD=X (need to invert either Numerator or Denominator)
            cur_den = tk_den.replace('USD=X', '')
            if n_click_validate:
                popover_pseudoticker_style = popover_pseudoticker_danger_style
                create_pseudoticker_disabled = True
                if cur_num == cur_den:
                    message_popover_validate_pseudoticker = f'This is invalid. The Denominator ticker cannot be an inverse of the Numerator ticker.'                
                else:
                    message_popover_validate_pseudoticker = f'This is invalid. Did you mean {tk_num} and USD{cur_den}=X? Or {cur_num}USD=X and {tk_den}?'

        else:
            # Stock/ETF/future or index
            cur_den = selected_ticker_currencies[tk_den]
            popover_pseudoticker_style = popover_pseudoticker_danger_style
            create_pseudoticker_disabled = True
            if cur_den == 'USD':
                # Example [Incorrect}: USDJPY=X/AMZN or USDJPY/^GSPC. The correct fx ticker for converting USD to JPY is JPYUSD=X.
                if n_click_validate:
                    message_popover_validate_pseudoticker = f'This is invalid. If you want to convert {tk_den} from USD to {cur_num}, use {tk_den} as Numerator and {cur_num}USD=X as Denominator.'
            elif cur_den == cur_num:
                # Example [Incorrect]: USDJPY=X/7201.T (Nissan) or USDJPY=X/^N225 (Nikkei).The fx ticker for converting JPY to USD is correct (USDJPY=X) but the ratio should be inversed.
                if n_click_validate:
                    message_popover_validate_pseudoticker = f'This is invalid. If you want to convert {tk_den} from {cur_den} to USD, use {tk_den} as Numerator and {tk_num} as Denominator.'
            else:
                # Example: USDJPY=X/BMW.DE or USDJPU=X/^GDAXI (currency: EUR)
                # [NEW] Suggest using BMW.DE/EURUSD=X for conversion to USD, or BMW.DE/JPYUSD=X for conversion to JPY (BMW.DE is first converted to USD, then to JPY).
                if n_click_validate:
                    message_popover_validate_pseudoticker = f'This is invalid. The currency of {tk_den} is {cur_den}. If you want to convert {tk_den} from {cur_den} to USD, use {tk_den} as Numerator and USD{cur_den}=X as Denominator.'
                    message_popover_validate_pseudoticker += f' If you want to convert {tk_den} from {cur_den} to {cur_num}, use {tk_den} as Numerator and {cur_num}USD=X as Denominator.'

    ##################################################################################################################

    else:
                    
        # The numerator ticker is NOT a currency FX rate, i.e. it doesn't end with '=X'
        cur_num = selected_ticker_currencies[tk_num]
        # Use 'price' (stock/ETF/future) or 'value' () when referring to tk_num in pseudo_tk_summary and popover message
        price_or_value_num = 'value' if tk_num.startswith('^') else 'price'
        converted_to_in = 'converted to' if tk_num.startswith('^') else 'in'

        ####################

        if tk_den.endswith('USD=X'):
            cur_den = tk_den.replace('USD=X', '')
            pseudo_tk_name = tk_num + '/' + tk_den            
            if cur_num == 'USD':
                # For example, AMZN and JPYUSD=X
                if n_click_validate:
                    popover_pseudoticker_style = popover_pseudoticker_success_style                    
                    message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}, which is the {price_or_value_num} of {tk_num} {converted_to_in} {cur_den}.'
                    message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'
                    create_pseudoticker_disabled = False
                if n_click_create:
                    pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} price in USD to {tk_den} (the exchange rate between {cur_den} and USD). '
                    pseudo_tk_summary += f'This is the {price_or_value_num} of {tk_num} {converted_to_in} {cur_den}.'
                    pseudo_tk_currency = cur_den
                    required_fx_tickers = []
                    add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)
            elif cur_num == cur_den:
                if n_click_validate:
                    # For example, 7201.T (Nissan) and (incorrect) JPYUSD=X. The correct fx ticker for conversion from JPY to USD is USDJPY=X.
                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                    message_popover_validate_pseudoticker = f'This is invalid. If you want to convert {tk_num} from {cur_num} to USD, use USD{cur_num}=X.'
                    create_pseudoticker_disabled = True
            else:
                # For example, BMW.DE (currency: EUR) and JPYUSD=X. Similarly to the suggestions above, this will be the price of BMW.DE in JPY.
                if n_click_validate:
                    popover_pseudoticker_style = popover_pseudoticker_success_style                   
                    message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}, which is the {price_or_value_num} of {tk_num} {converted_to_in} {cur_den}. '
                    message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'
                    message_popover_validate_pseudoticker += f' If you want to convert {tk_num} to USD, use USD{cur_num}=X as Denominator.'
                    create_pseudoticker_disabled = False
                if n_click_create:
                    pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} price in {cur_num} to {tk_den} (the exchange rate between {cur_den} and USD), '
                    pseudo_tk_summary += f'both converted to a common currency. This is the {price_or_value_num} of {tk_num} {converted_to_in} {cur_den}.'
                    pseudo_tk_currency = cur_den
                    required_fx_tickers = [f'{cur_den}USD=X']
                    add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)

        ####################

        elif tk_den.startswith('USD') & tk_den.endswith('=X'):
            cur_den = tk_den.replace('USD', '').replace('=X', '')
            pseudo_tk_name = tk_num + '/' + tk_den
            if cur_num == 'USD':
                # For example, AMZN and (incorrect) USDJPY=X.
                if n_click_validate:
                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                    message_popover_validate_pseudoticker = f'This is invalid. If you want to convert {tk_num} from USD to {cur_den}, use {cur_den}USD=X as Denominator.'
                    create_pseudoticker_disabled = True
            elif cur_num == cur_den:
                # For example, 7201.T (Nissan) and USDJPY=X.
                if n_click_validate:
                    popover_pseudoticker_style = popover_pseudoticker_success_style
                    message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}, which is the {price_or_value_num} of {tk_num} {converted_to_in} USD.'
                    message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'
                    create_pseudoticker_disabled = False
                if n_click_create:
                    pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} price in {cur_den} to {tk_den} (the exchange rate between USD and {cur_den}).'
                    pseudo_tk_summary += f' This is the {price_or_value_num} of {tk_num} {converted_to_in} USD.'
                    pseudo_tk_currency = 'USD'
                    required_fx_tickers = []
                    add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)
            else:
                # For example, BMW.DE (currency: EUR) and USDJPY=X.
                if n_click_validate:
                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                    message_popover_validate_pseudoticker = f'This is invalid. If you want to convert {tk_num} from {cur_num} to USD, use USD{cur_num}=X as Denominator.'
                    message_popover_validate_pseudoticker += f' If you want to convert {tk_num} to {cur_den}, use {cur_den}USD=X as Denominator.'
                    create_pseudoticker_disabled = True

        ####################

        else:
            # Two stock/ETF/future prices or two indices or one stock/ETF/future price and one index

            price_or_value_den = 'value' if tk_den.startswith('^') else 'price'
            cur_den = selected_ticker_currencies[tk_den]
            pseudo_tk_name = tk_num + '/' + tk_den

            if tk_num == tk_den:
                if n_click_validate:
                    popover_pseudoticker_style = popover_pseudoticker_danger_style
                    message_popover_validate_pseudoticker = f'This is invalid. The two tickers must be different.'
                    create_pseudoticker_disabled = True
            else:
                if cur_num == cur_den:
                    # For example, ^GSPC/AMZN or BMW.DE/^GDAXI
                    if n_click_validate:
                        popover_pseudoticker_style = popover_pseudoticker_success_style
                        message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}. Both tickers are in the same currency, so no FX adjustment is necessary.'
                        message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'
                        create_pseudoticker_disabled = False
                    if n_click_create:
                        pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} {price_or_value_num}s to {tk_den} {price_or_value_den}s.'
                        pseudo_tk_currency = ''
                        required_fx_tickers = []
                        add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)
                elif cur_num == 'USD':
                    # For example, ^GSPC/BMW.DE or AAPL/^N225
                    if n_click_validate:
                        popover_pseudoticker_style = popover_pseudoticker_success_style
                        message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}. {tk_den} will first be converted from {cur_den} to USD in order to match the currency of {tk_num}.'
                        message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'
                        create_pseudoticker_disabled = False
                    if n_click_create:
                        pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} {price_or_value_num}s to {tk_den} {price_or_value_den}s, converted to a common currency (USD).'
                        pseudo_tk_currency = ''
                        required_fx_tickers = [f'{cur_den}USD=X']
                        add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)
                elif cur_den == 'USD':
                    # For example, BMW.DE/^GSPC or ^N225/AAPL
                    if n_click_validate:
                        popover_pseudoticker_style = popover_pseudoticker_success_style
                        message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}. {tk_num} will first be converted from {cur_num} to USD in order to match the currency of {tk_den}.'
                        message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'
                        create_pseudoticker_disabled = False
                    if n_click_create:
                        pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} {price_or_value_num}s to {tk_den} {price_or_value_den}s, converted to a common currency (USD).'
                        pseudo_tk_currency = ''
                        required_fx_tickers = [f'{cur_den}USD=X']
                        add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)
                else:
                    # For example, BMW.DE/^N225 or ^GDAXI/7201.T
                    if n_click_validate:
                        popover_pseudoticker_style = popover_pseudoticker_success_style
                        message_popover_validate_pseudoticker = f'This will create pseudoticker {pseudo_tk_name}. Both {tk_num} and {tk_den} will first be converted to a common currency.'
                        message_popover_validate_pseudoticker += f' You can proceed by clicking the CREATE PSEUDOTICKER button.'
                        create_pseudoticker_disabled = False
                    if n_click_create:
                        pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} {price_or_value_num}s to {tk_den} {price_or_value_den}s, converted to a common currency.'
                        pseudo_tk_currency = ''
                        required_fx_tickers = [f'{cur_num}USD=X', f'{cur_den}USD=X']
                        add_pseudoticker_info(tk_num, tk_den, cur_num, cur_den, pseudo_tk_name, pseudo_tk_summary, pseudo_tk_currency, required_fx_tickers)

    ########################

    # if (pseudo_tk_name != '') & n_click_create:
    if (pseudo_tk_name != '') & (not create_pseudoticker_disabled):
                    
        selected_pseudotickers = list(selected_pseudoticker_info.keys())  # NOTE: Each pseudoticker is a string f'{tk_num}_{tk_den}'
        print(f'selected_pseudotickers = {selected_pseudotickers}')
        selected_pseudoticker_indices = [selected_pseudoticker_info[pseudo_tk]['idx'] for pseudo_tk in selected_pseudotickers]
        table_pseudoticker_selected_rows = [int(idx) for idx in selected_pseudoticker_indices]

        print(f'pseudo_tk_name = {pseudo_tk_name}')
        print(f'table_pseudoticker_data = {table_pseudoticker_data}')
        print(f'table_pseudoticker_tooltip_data = {table_pseudoticker_tooltip_data}')
        print(f'selected_pseudoticker_indices = {selected_pseudoticker_indices}')
        print(f'table_pseudoticker_selected_rows = {table_pseudoticker_selected_rows}')
        print(f'selected_pseudoticker_info = {selected_pseudoticker_info}')
 

    # print(f'popover message:\n\t{message_popover_validate_pseudoticker}')
    # print(f'popover_hidden = {popover_hidden}')
    # print(f'n_click_create = {n_click_create}')
    # print(f'n_click_validate = {n_click_validate}')

    if n_click_validate:
        popover_hidden = False
        popover_is_open = True
        # popover_is_open = False if n_click_create else True

    if n_click_create:
        n_click_create = 0
        n_click_validate = 0
        message_popover_validate_pseudoticker = ''
        popover_hidden = True
        popover_is_open = False
        create_pseudoticker_disabled = True

    # print(f'popover_hidden = {popover_hidden}')
    # print(f'n_click_create = {n_click_create}')
    # print(f'n_click_validate = {n_click_validate}')

    ########################

    return (
        selected_pseudoticker_info,        
        message_popover_validate_pseudoticker,
        popover_hidden,
        popover_pseudoticker_style,
        popover_is_open,
        create_pseudoticker_disabled,
        table_pseudoticker_data,
        table_pseudoticker_tooltip_data,
        table_pseudoticker_selected_rows,
        n_click_validate,
        n_click_create
    )


##############################################################

if __name__ == '__main__':
    app.run(debug = True, port = 8887)


##############################################################


"""
https://money.stackexchange.com/questions/71752/does-an-index-have-a-currency


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

"""
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
                        ############################################################################################################################
                        #
                        #    Allowed pseudotickers types:
                        #
                        #    First order: Both tickers are in the original selected ticker list (including the inverted fx tickers)
                        #
                        #       I.1. Converted Pseudotickers of First Order:
                        #            NOTE: Only converted pseudotickers (1.1-1.5) can be used to construct second-order pseudotickers.
                        #
                        #       1.1.   JPYEUR=X:        Two non-USD currencies (shortened from JPYUSD=X/EURUSD=X to the yf format), currency = EUR
                        #                               NOTE: The inverse EURJPY=X can be manually created by the user, no need to add it automatically.
                        #       1.2.   BMW.DE/USDEUR=X: Stock/ETF/future price in foreign currency converted to USD, currency = USD
                        #       1.3.   AMZN/JPYUSD=X:   Stock/ETF/future price in USD converted to a foreign currency (JPY), currency = JPY
                        #       1.4.   ^N225/USDJPY=X:  Index in foreign currency adjusted to USD, currency = USD
                        #       1.5.   ^GSPC/JPYUSD=X:  Index in USD adjusted to a foreign currency (JPY), currency = JPY
                        #
                        #       II.1. Comparative Pseudotickers of First Order:
                        #             NOTE: The currencies of comparative pseudotickers are only set pro-forma.
                        #
                        #       1.6a.  AMZN/TSLA:       Two prices in the same currency, USD
                        #       1.6b.  7201.T/7202.T:   Two prices in the same currency, non-USD (Nissan/Isuzu, JPY)
                        #       1.7a.  ^GSPC/^DJI:      Two indices in the same currency, USD
                        #       1.7b.  ^GDAXI/^STOXX:   Two indices in the same currency, non-USD (EUR)
                        #       1.7c.  ^GSPC/^N225:     Two indices in different currencies, with a warning note about FX effects, currency = USD (Numerator's)
                        #       1.8.   BMW.DE/^GDAXI:   Stock/ETF/future price over index in the same currency (EUR)
                        #       1.9.   ^GDAXI/BMW.DE:   Index over stock/ETF/future price in the same currency (EUR)                        
                        #       1.10a. JPYUSD=X/^GSPC:  A non-USD currency exchange rate to USD over a USD-based index, currency = USD
                        #       1.10b. USDJPY=X/^GSPC:  USD exchange rate to a non-USD currency over a USD-based index, currency = JPY
                        #       1.11a. JPYUSD=X/^N225:  A non-USD currency exchange rate to USD over a non-USD-based index in the same currency, currency = USD
                        #       1.11b. USDJPY=X/^N225:  USD exchange rate to a non-USD currency over a non-USD-based index in the same currency, currency = JPY
                        #
                        ##########################################################################################################################
                        #
                        #    Second order: A first-order pseudoticker + a ticker from the original list (including the inverted fx tickers)
                        #       2.1-2.5. Comparison between a converted price or adjusted index pseudoticker and a price/index in the same currency
                        #       
                        #       I.2. Converted Pseudotickers of Second Order:
                        #            NOTE: Only converted pseudotickers as Denominators (2.1D) can be used to construct third-order pseudotickers.
                        #
                        #       2.1D. JPYEUR=X as Denominator, currency = EUR
                        #           2.1D.1. BMW.DE/JPYEUR=X:   Stock/ETF/future in Denominator's currency (EUR) converted to the other currency (JPY), currency = JPY
                        #           2.1D.2. ^GDAXI/JPYEUR=X:   Index based on Denominator's currency (EUR) converted to the other currency (JPY), currency = JPY
                        # 
                        #       II.2. Comparative Pseudotickers of Second Order:
                        #             NOTE: The currencies of comparative pseudotickers are only set pro-forma.                        
                        #
                        #       2.1N. JPYEUR=X as Numerator, currency = EUR
                        #           2.1N.1a. JPYEUR=X/^GDAX:   A non-USD FX pseudoticker over an index based on the pseudoticker currency (EUR), currency = EUR
                        #           2.1N.1b. JPYEUR=X/^N225:   A non-USD FX pseudoticker over an index based on the other currency (JPY), currency = EUR
                        #
                        #       2.2N. BMW.DE/USDEUR=X: as Numerator, originally a non-USD stock/ETF/future converted to USD, currency = USD
                        #           NOTE: These are inverses of 2.2D.1 and 2.2D.2.
                        #           2.2N.1. (BMW.DE/USDEUR=X)/AMZN:  Stock/ETF/future pseudoticker over stock/ETF/future in the same currency (USD)
                        #           2.2N.2. (BMW.DE/USDEUR=X)/^GSPC: Stock/ETF/future pseudoticker over index in the same currency (USD)
                        #       2.2D. BMW.DE/USDEUR=X as Denominator, originally a non-USD stock/ETF/future converted to USD, currency = USD
                        #           NOTE: These are inverses of 2.2N.1 and 2.2N.2.
                        #           2.2D.1. AMZN/(BMW.DE/USDEUR=X):  Stock/ETF/future over pseudoticker in the same currency (USD)
                        #           2.2D.2. ^GSPC/(BMW.DE/USDEUR=X): Index over pseudoticker in the same currency (USD)
                        #
                        #       2.3N. AMZN/JPYUSD=X as Numerator, originally a USD stock/ETF/future converted to foreign currency (JPY)
                        #           NOTE: These are inverses of 2.3D.1 and 2.3D.2.                        
                        #           2.3N.1. (AMZN/JPYUSD=X)/7201.T: Stock/ETF/future pseudoticker over stock/ETF/future in the same currency (JPY)
                        #           2.3N.2. (AMZN/JPYUSD=X)/^N225:  Stock/ETF/future pseudoticker over index in the same currency (JPY)
                        #       2.3D. AMZN/JPYUSD=X as Denominator, originally a USD stock/ETF/future converted to foreign currency (JPY)
                        #           NOTE: These are inverses of 2.3N.1 and 2.3N.2.                        
                        #           2.3D.1. 7201.T/(AMZN/JPYUSD=X): Stock/ETF/future over stock/ETF/future pseudoticker in the same currency (JPY)
                        #           2.3D.2. ^N225/(AMZN/JPYUSD=X):  Index over stock/ETF/future pseudoticker in the same currency (JPY)
                        #
                        #       2.4N. ^N225/USDJPY=X: as Numerator, originally a non-USD index converted to USD, currency = USD
                        #           NOTE: These are inverses of 2.4D.1 and 2.4D.2.                        
                        #           2.4N.1. (^N225/USDJPY=X)/AMZN:  Index pseudoticker over stock/ETF/future in the same currency (USD)
                        #           2.4N.2. (^N225/USDJPY=X)/^GSPC: Index pseudoticker over index in the same currency (USD)
                        #       2.4D. ^N225/USDJPY=X as Denominator, originally a non-USD index converted to USD, currency = USD
                        #           NOTE: These are inverses of 2.4N.1 and 2.4N.2.                        
                        #           2.4D.1. AMZN/(^N225/USDJPY=X):  Stock/ETF/future over stock/ETF/future pseudoticker in the same currency (USD)
                        #           2.4D.2. ^GSPC/(^N225/USDJPY=X): Index over stock/ETF/future pseudoticker in the same currency (USD)
                        #
                        #       2.5N. ^GSPC/JPYUSD=X as Numerator, originally a USD index converted to foreign currency (JPY)
                        #           NOTE: These are inverses of 2.5D.1 and 2.5D.2.                        
                        #           2.5N.1. (^GSPC/JPYUSD=X)/7201.T: Index pseudoticker over stock/ETF/future in the same currency (JPY)
                        #           2.5N.2. (^GSPC/JPYUSD=X)/^N225:  Index pseudoticker over index in the same currency (JPY)
                        #       2.5D. ^GSPC/JPYUSD=X as Denominator, originally a USD index converted to foreign currency (JPY)
                        #           NOTE: These are inverses of 2.5N.1 and 2.5N.2.                        
                        #           2.5D.1. 7201.T/(^GSPC/JPYUSD=X): Stock/ETF/future over index pseudoticker in the same currency (JPY)
                        #           2.5D.2. ^N225/(^GSPC/JPYUSD=X):  Index over index pseudoticker in the same currency (JPY)
                        #                        
                        ##########################################################################################################################
                        #
                        #    Third order: Comparison between two converted price or adjusted index pseudotickers in the same currency
                        #       NOTE: All third-order pseudotickers are comparative.       
                        #
                        #       3.1-3.2. A second-order converted pseudoticker + a ticker from the original list (including the inverted fx tickers)
                        #
                        #       3.1N. BMW.DE/JPYEUR=X as Numerator, currency = EUR
                        #           3.1N.1. (BMW.DE/JPYEUR=X)/7201.T:   Stock/ETF/future pseudoticker over stock/ETF/future in the same currency (JPY)
                        #                   NOTE: 3.1N.1 is equivalent to 4.1.1, in that both of them express the FX-adjusted ratio of BMW.DE and 7201.T prices 
                        #           3.1N.2. (BMW.DE/JPYEUR=X)/^N225:    Stock/ETF/future pseudoticker over index in the same currency (JPY)                        
                        #                   NOTE: 3.1N.2 is equivalent to 4.1.2, in that both of them express the FX-adjusted ratio of BMW.DE price to ^N225
                        #       3.2N. ^GDAXI/JPYEUR=X as Numerator, currency = EUR
                        #           3.2N.1. (^GDAXI/JPYEUR=X)/7201.T:   Index pseudoticker over stock/ETF/future in the same currency (JPY)
                        #                   NOTE: This is an inverse of 3.2D.1.
                        #           3.2N.2. (^GDAXI/JPYEUR=X)/^N225:    Index pseudoticker over index in the same currency (JPY)
                        #                   NOTE: This is an inverse of 3.2D.2.
                        #       
                        #       3.1D. BMW.DE/JPYEUR=X as Denominator, currency = EUR
                        #           3.1D.1. 7201.T/(BMW.DE/JPYEUR=X):   Stock/ETF/future over stock/ETF/future pseudoticker in the same currency (JPY)
                        #                   NOTE: This is an inverse of 3.1N.1.
                        #           3.1D.2. ^N225/(BMW.DE/JPYEUR=X):    Index over stock/ETF/future pseudoticker in the same currency (JPY)
                        #                   NOTE: This is an inverse of 3.1N.2.
                        #       3.2D. ^GDAXI/JPYEUR=X as Denominator, currency = EUR                        
                        #           3.2D.1. 7201.T/(^GDAXI/JPYEUR=X):   Stock/ETF/future over index pseudoticker in the same currency (JPY)
                        #                   NOTE: This is an inverse of 3.2N.1.
                        #           3.2D.2. ^N225/(^GDAXI/JPYEUR=X):    Index over index pseudoticker in the same currency (JPY)
                        #                   NOTE: This is an inverse of 3.2N.2.
                        #
                        #       4.1-4.2. Two first-order pseudotickers
                        #
                        #       4.1. BMW.DE/USDEUR=X as Numerator, currency = USD
                        #           NOTE: The cases of BMW.DE/USDEUR=X as Denominator are omitted below as they are simply inverses of the Numerator cases. 
                        #           4.1.1. (BMW.DE/USDEUR=X)/(7201.T/USDJPY=X): Two stock/ETF/future pseudotickers in the same currency (USD)
                        #                   NOTE: 4.1.1 is equivalent to 3.1N.1, in that both of them express the FX-adjusted ratio of BMW.DE and 7201.T prices.
                        #           4.1.2. (BMW.DE/USDEUR=X)/(^N225/USDJPY=X):  Stock/ETF/future pseudoticker over index pseudoticker in the same currency (USD)
                        #                   NOTE: 4.1.2 is equivalent to 3.1N.2, in that both of them express the FX-adjusted ratio of BMW.DE price to ^N225.
                        #       4.2. ^GDAXI/USDEUR=X as Numerator, currency = USD
                        #           NOTE: The cases of BMW.DE/USDEUR=X as Denominator are omitted below as they are simply inverses of the Numerator cases. 
                        #           4.2.1. (^GDAXI/USDEUR=X)/(7201.T/USDJPY=X): Index pseudoticker over a stock/ETF/future pseudoticker in the same currency (USD)
                        #                   NOTE: 4.2.1 is equivalent to 3.2N.1, in that both of them express the FX-adjusted ratio of ^GDAXI to 7201.T prices.
                        #           4.2.2. (^GDAXI/USDEUR=X)/(^N225/USDJPY=X):  Two index pseudotickers in the same currency (USD)
                        #                   NOTE: 4.2.2 is equivalent to 3.2N.2, in that both of them express the FX-adjusted ratio of ^GDAXI to ^N225.
                        #
                        ########################################################################################################################

                        tk_num_1 = tk_num[:3]
                        tk_num_2 = tk_num[3:6]
                        if tk_den.endswith('=X'):
                            message_popover_validate_pseudoticker = ''  #f"You can only combine {tk_num} with a ticker in  "
                            

                        cur_num = tk_num.replace('USD=X', '')

                        if tk_den.endswith('USD=X'):
                            tk_num_name = tk_num.replace('USD=X', '')
                            tk_den_name = tk_den.replace('USD=X', '')
                            pseudo_tk_name = tk_num_name + '/' + tk_den_name
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The exchange rate between {tk_num_name} and {tk_den_name}, or the price of {tk_num_name} in {tk_den_name}.'
                            # if pseudo_tk not in selected_tickers:
                            #     # Adding pseudo_tk to the Numerator and Denominator dropdown lists
                            #     selected_tickers.append(pseudo_tk)

                        elif tk_den.startswith('USD') & tk_den.endswith('=X'):
                            cur_den = tk_den.replace('USD', '').replace('=X', '')
                            message_popover_validate_pseudoticker = f"Did you mean {tk_num} and {cur_den}USD=X? Or USD{cur_num}=X and {tk_den}?"

                        else:
                            # We will only allow a ratio of currency to an index (or a currency-free asset).
                            cur_den = selected_ticker_currencies[tk_den]
                            if tk_den.startswith('^') | (cur_den == ''):
                                # An index, no currency
                                tk_num_name = tk_num.replace('=X', '')
                                pseudo_tk_name = tk_num_name + '/' + tk_den
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num_name} (the exchange rate between {cur_num} and USD) to {tk_den} values.'
                            else:
                                if cur_den == 'USD':
                                    # For example, JPYUSD=X and AMZN
                                    message_popover_validate_pseudoticker = f"The currency of {tk_den} is USD. If you want to convert it to {cur_num}, use {tk_den} as Numerator and {tk_num} as Denominator."
                                elif cur_den == cur_num:
                                    # For example, (incorrect) JPYUSD=X and 7201.T (Nissan). The correct fx ticker for converting JPY to USD is USDJPY=X.
                                    message_popover_validate_pseudoticker = f"The currency of {tk_den} is {cur_den}. If you want to convert it to USD, use {tk_den} as Numerator and USD{cur_den}=X as Denominator."
                                else:
                                    # For example, JPYUSD=X and BMW.DE (currency: EUR).
                                    # Should also allow conversion to cur_num by using tk_den (BMW.DE) as Numerator and a pseudoticker f'{cur_num}{cur_den}=X' (JPYEUR) as Denominator.
                                    message_popover_validate_pseudoticker = f"The currency of {tk_den} is {cur_den}. If you want to convert it to USD, use {tk_den} as Numerator and USD{cur_den}=X as Denominator."
                                    message_popover_validate_pseudoticker += f" If you want to convert it to {cur_num}, create a pseudoticker {cur_den}{cur_num}=X"
                                    message_popover_validate_pseudoticker += f" and then use {tk_den} as Numerator and {cur_den}{cur_num}=X as Denominator."

                    ################### END PSEUDOTICKER tk_num
"""

"""
Q:
Can a ratio of two time series such as stock prices be considered a good measure of their correlation?

Copilot:

The ratio of two time series, such as stock prices, can reveal certain relationships or patterns, 
but it is not a direct measure of their correlation. Correlation measures the degree to which two 
variables move together, typically calculated using statistical methods like Pearson's correlation coefficient. 
This coefficient considers both the direction and strength of the linear relationship between two variables.

On the other hand, a ratio (e.g., dividing one stock price by another) gives you a relative value between the 
two series but doesn't directly reflect how consistently their movements align. For instance, the ratio might 
stay stable even if the two stocks move in opposite directions but with proportional magnitudes. Conversely, 
two highly correlated stocks could still have a fluctuating ratio if their price levels differ significantly.

If you're interested in measuring correlation, it's better to use established statistical tools. However, analyzing 
the ratio could provide complementary insights, especially if you're examining relative performance or co-movement 
over time. Would you like me to explain how to compute or interpret correlation in more detail?

Q:
Thanks, I know the standard statistical correlation tools but was just wondering about something as simple as 
the ratio of two series and its evolution over time. I'm not quite grasping at the moment your statement 
"the ratio might stay stable even if two stocks move in opposite directions but with proportional magnitudes" 
- could you give me a specific example of that? It seems to me that if one stock moves up and the other one down, 
then their ratio must change regardless of the magnitudes of the changes. Am I missing something in this interpretation?

Copilot:

You're absolutely right to question that—it seems like I misspoke earlier. If one stock goes up while the other goes down, 
the ratio will indeed change. Let me clarify and adjust my explanation to avoid any confusion.

The ratio of two time series reflects their relative values. If stock A and stock B move in opposite directions, the ratio 
\( \text{A}/\text{B} \) 
must change, regardless of the magnitudes of the changes, because the numerator and denominator are moving in opposite ways.

A better example of when the ratio might remain stable would be if both stocks move **proportionally in the same direction**. 
For instance:
- Suppose stock A starts at $50, and stock B starts at $100, giving a ratio \( \text{A}/\text{B} = 0.5 \).
- If stock A increases to $75 (a 50% increase), and stock B also increases to $150 (also a 50% increase), the ratio 
    \( \text{A}/\text{B} \) remains 0.5.

This proportional movement in the same direction maintains a stable ratio. But if one stock moves up and the other down 
— even proportionally — the ratio will change. Thank you for catching that inconsistency earlier. It’s always good to
ensure we’re precise! Does this revised explanation make more sense now?

Q:
OK, thanks for the example, looks like we're more on the same page now. So, considering this, how would you revise your 
initial statements ragarding how useful the ratio can be in assessing the correlation between two price movements? 
I know it's not necessarily part of the formal statistical arsenal, I'm just trying to explore something new here that, 
as simple as it is, might be helpful in this respect. One thing I should note perhaps is that I'm not looking at a single 
number to express the correlation - a time series of the ratio is fine as long as it's meaningful enough.

Copilot:

Thanks for clarifying your approach—it definitely opens up some creative avenues for exploring relationships between two 
price movements. Let's refine the original idea, keeping in mind the unique perspective you're aiming for.

A time series of the ratio can indeed offer meaningful insights, especially if you're not seeking a single-number summary 
like a correlation coefficient. Here’s how the ratio could be useful in assessing relationships between two price movements:

1. **Relative Performance**: 
    A stable or smoothly evolving ratio indicates that the two stocks are maintaining a consistent relationship in relative 
    performance. Sudden shifts in the ratio could signal a divergence, which might be worth investigating further — such as 
    a specific market event or a shift in investor sentiment affecting only one of the two.

2. **Volatility Comparison**: 
    If one stock is consistently more volatile than the other, it might create fluctuations in the ratio without necessarily 
    indicating a lack of correlation. By analyzing the ratio's time series, you can capture these nuances, especially if you 
    layer this with additional measures like standard deviation.

3. **Detecting Asymmetrical Movements**: 
    Monitoring the ratio can help spot periods where the two stocks move disproportionately, even if they exhibit overall 
    correlation. For example, if the ratio spikes or drops sharply, you might examine what caused one stock to outpace or lag 
    behind its counterpart during that window.

4. **Trend Dynamics**: 
    The time series of the ratio itself might reveal trends that aren’t obvious when viewing the two price series separately. 
    For instance, a steadily increasing ratio could suggest that one stock is consistently outperforming the other over time, 
    even if their day-to-day movements align.

5. **Complementary Analysis**: 
    While the ratio can't replace formal correlation measures, it can work alongside them. For example, you might calculate 
    rolling windows of correlation coefficients between the two stocks while also tracking the ratio, to see 
    whether shifts in one align with changes in the other.

By focusing on the time series of the ratio, you’re effectively adding an exploratory layer to the analysis. It may not meet the 
rigorous demands of traditional statistical methods, but it could still uncover valuable patterns or relationships that numbers 
like correlation coefficients might miss.

Does this revised perspective resonate with your goals? I’d love to hear if you think this approach offers potential!

Copilot (revising):

Thanks for your patience—let’s take another look at this. Based on your clarification and the focus on a time series of the ratio 
rather than a single statistic, I'd revise my initial statements to reflect this exploratory lens.

The ratio time series can be a creative and practical way to observe relationships between two price movements. While it doesn't 
measure correlation in a strict, statistical sense, it can still provide meaningful insights in these ways:

1. **Dynamic Relationships**: 
    Unlike a static correlation coefficient, the ratio evolves over time, capturing changes in the relative relationship between the
    two series. This can highlight periods of divergence, convergence, or stability that a correlation coefficient might not reveal.

2. **Shift in Market Conditions**: 
    Spikes or dips in the ratio might serve as red flags for major events affecting one stock more than the other, such as earnings 
    announcements or sector-specific news. It’s a straightforward way to track imbalances.

3. **Behavioral Context**: 
    By pairing the ratio's time series with visual observations of the raw price movements, you can identify whether ratio changes 
    correspond to certain patterns—such as both stocks rising or falling together but at differing rates.

4. **Complement to Rolling Correlation**: 
    While traditional rolling correlation measures can show how linear relationships between the stocks change over time, the ratio 
    can offer an intuitive, complementary view of how one stock's performance evolves relative to the other.

5. **Simplicity with Depth**: 
    Sometimes, simplicity fosters insight. A time series of the ratio is easy to interpret and doesn't rely on complex statistical 
    tools—making it useful for initial exploration or quick diagnostics.

In essence, while the ratio isn't a direct measure of correlation, it’s a versatile tool that adds depth to your analysis by emphasizing 
relative dynamics. If you're comfortable experimenting, layering it with other methods, like rolling correlations or volatility measures, 
could yield an even richer understanding.

How does this revised take align with your thoughts? If you'd like, we could brainstorm specific ways to integrate the ratio into your 
workflow or further refine its interpretation.

Q:
I'm building a technical analysis app, in which I offer the user - for most Yahoo Finance tickers - a variety of customizable plot options 
like historical prices, candlestick, the whole spectrum of moving averages, momentum indicators, volatility indicators and more. I'm giving 
the user an options of defining a so-called pseudoticker, which is the ratios of two regular ticker prices. Then, this user-selected pseudoticker 
would be treated in the same way as any other ticker, in that all plotting options (price/moving average/momentum indicators, etc.) would be 
available to those ratio "pseudotickers", as well. My question is: To what extent would the options I offer to the user in my app for plotting 
the historical pseudoticker values be aligned with some of your suggested, so to speak "categories of usefuleness in the context of correlation" 
- kindly provided above?

Copilot:

Thanks for sharing the broader context—it’s a very intriguing application you’re building! I can see how your pseudoticker concept opens up a powerful way
for users to gain fresh insights. Let’s map your customizable plotting options to the earlier-mentioned categories of usefulness in the context of correlation:

1. **Dynamic Relationships**: 
    Your historical pseudoticker plots naturally align here. By offering tools like moving averages and historical charts for pseudotickers, you're helping 
    users identify evolving dynamics between two assets over time. This could highlight divergence, convergence, or periods of relative stability, making 
    the relationship between the assets more intuitive to spot.

2. **Shift in Market Conditions**: 
    Volatility indicators and momentum tools for pseudotickers would tie in well with this category. A sudden spike or dip in the pseudoticker value could signal
    market events or news impacting one stock disproportionately. Users could plot these metrics to investigate the causes and monitor when conditions normalize.

3. **Behavioral Context**: 
    Candlestick charts or moving averages applied to pseudotickers provide a great way to visualize context. These tools enable users to see whether ratio changes 
    align with certain patterns — for example, steady trends or abrupt breaks — and connect these patterns to broader price movements of the individual tickers.

4. **Complement to Rolling Correlation**: 
    While you’re focusing on pseudotickers instead of formal correlation metrics, allowing users to plot technical indicators like moving averages or Bollinger Bands 
    for pseudotickers acts as a complementary measure. It helps users explore the behavior of the ratio over time, potentially spotting when one asset might temporarily 
    dominate or lag behind the other.

5. **Simplicity with Depth**: 
    The broad range of plotting options (e.g., overlays of momentum or volatility indicators) ensures that users can access both high-level trends and granular details. 
    By treating the pseudotickers like regular tickers, you simplify their exploration while adding analytical depth.

Your app already seems to align well with these categories, but there’s room to build on this further:
- **User-Defined Alerts**: 
    Allowing users to set alerts on pseudoticker thresholds or specific patterns (e.g., crossing a moving average) could make the analysis even more actionable.
- **Trend Comparisons**: 
    Enable users to overlay individual ticker data on the same plot as the pseudoticker. This could clarify how movements in one asset influence the ratio.
- **Custom Time Frames**: 
    If not already planned, giving users the ability to define rolling windows for indicators or moving averages on pseudoticker plots could add another layer of flexibility.

It sounds like you’re creating something highly versatile and user-friendly. How does this alignment resonate with your vision for the app? I’d be happy to explore specific 
features or user cases further with you!

Q:
Very helpful indeed! Let me catch a breath and chew on it for a while, as there is a lot of substances and ideas in what you've come up with in your response. 
I should have had this great conversation earlier - many thanks!

Copilot:
You're more than welcome — I’m thrilled this discussion has sparked some useful ideas for your project! It’s clear you’re building something innovative,
and it’s exciting to be part of your creative process. Take all the time you need to digest everything, and know that I’m here whenever you’re ready 
to dive back in or bounce around more ideas. Wishing you all the best as you move forward—it’s going to be great! 🚀

"""