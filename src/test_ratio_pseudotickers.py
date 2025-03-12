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

pseudoticker_text = """You can choose a pair of tickers to create a Ratio Pseudoticker, whose value will be the ratio of the two tickers' prices, FX rates, or indices.
This can be useful for calculating non-USD currency exchange rates, converting foreign currency asset prices to USD, comparing similar asset types, etc.
All plot types and features, except for volume, will be available for the Pseudotickers."""

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
    'BMW.DE':   'BMW',
    '7201.T':   'Nissan'
}
selected_tickers = list(selected_ticker_names.keys())
first_tk = selected_tickers[0]
tk_den_first_legit = [tk for tk in selected_tickers[1:] if tk != (first_tk[3:6] + first_tk.replace(first_tk[3:6], ''))][0] if len(selected_tickers) > 1 else first_tk

hidden_pseudo = False if len(selected_tickers) >=2 else True


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
        columns = [{'name': i, 'id': i} for i in ['Pseudoticker', 'Name']],
        data = [],
        editable = False,
        row_selectable = 'multi',
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
        dbc.Button(
            'Create A Ratio Pseudoticker',
            id = 'create-pseudoticker-button',
            n_clicks = 0,
            class_name = 'ma-1',
            color = 'light',
            size = 'sm',
            style = create_pseudoticker_button_css
        ),
        dbc.Popover(
        # dmc.Popover(
            [
            html.Div(
                id = 'popover-create-pseudoticker-button-div',
                children = [],
                hidden = True,
                style ={
                    'width': '300px !important',
                    # 'height': '32px',
                    # 'margin': '3px 0px 7px 0px',
                    # 'padding-left': '0px',
                    # 'padding-right': '0px',
                    # 'padding-bottom': '2px',
                    'vertical-align': 'middle',
                    'text-align': 'center',
                    'font-family': 'Helvetica',
                    'font-size': '13px',
                    # 'font-weight': 'bold',
                    'color': 'black'
                }

                )
            ], 
            id = 'popover-create-pseudoticker-button',
            target = 'create-pseudoticker-button',
            body = False,
            trigger = 'click',
            hide_arrow = True,
            delay = {'show': 0, 'hide': 8000},
            style ={
                'width': '300px !important',
                # 'height': '32px',
                'margin': '3px 0px 7px 0px',
                'padding-left': '0px',
                'padding-right': '0px',
                'padding-bottom': '2px',
                # 'vertical-align': 'middle',
                # 'text-align': 'center',
                # 'font-family': 'Helvetica',
                # 'font-size': '14px',
                # 'font-weight': 'bold',
                'border-radius': '5px',
                'border-color': 'rgb(255, 178, 185)',
                'background-color': 'rgb(255, 222, 220)',
                # 'color': 'black'
            }
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
    Output('selected-pseudoticker-info', 'data'),
    Output('dash-table-pseudotickers-to-plot', 'data'),
    Output('dash-table-pseudotickers-to-plot', 'tooltip_data'),
    Output('dash-table-pseudotickers-to-plot', 'selected_rows'),

    State('pseudoticker-numerator-dropdown', 'value'),
    State('pseudoticker-denominator-dropdown', 'value'),

    Input('create-pseudoticker-button', 'n_clicks'),
    Input('selected-pseudoticker-info', 'data'),
    Input('dash-table-pseudotickers-to-plot', 'data'),
    Input('dash-table-pseudotickers-to-plot', 'tooltip_data'),
    Input('dash-table-pseudotickers-to-plot', 'selected_rows')

)
def display_table_selected_pseudotickers(
    tk_num,
    tk_den,
    n_click_pseudo,
    selected_pseudoticker_info,
    table_pseudoticker_data,
    table_pseudoticker_tooltip_data,
    table_pseudoticker_selected_rows
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

    hidden_popover_create_pseudoticker = True
    message_popover_create_pseudoticker = ''

    ctx = dash.callback_context

    if n_click_pseudo:
        
        if ctx.triggered:
            
            if (tk_num != tk_den) & (tk_num != tk_den[3:6] + tk_den.replace(tk_den[3:6], '')):
                # Tickers must be different and cannot be mutually inverse fx rates for the same currency

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

                    pseudo_tk_name = ''
                    pseudo_tk_summary = ''

                    if tk_num.endswith('USD=X'):
                        cur_num = tk_num.replace('USD=X', '')
                        if tk_den.endswith('USD=X'):
                            tk_num_name = tk_num.replace('USD=X', '')
                            tk_den_name = tk_den.replace('USD=X', '')
                            pseudo_tk_name = tk_num_name + '/' + tk_den_name
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The exchange rate between {tk_num_name} and {tk_den_name}, or the price of {tk_num_name} in {tk_den_name}.'
                        elif tk_den.startswith('USD') & tk_den.endswith('=X'):
                            cur_den = tk_den.replace('USD', '').replace('=X', '')
                            hidden_popover_create_pseudoticker = False
                            # message_popover_create_pseudoticker = 'You cannot create a pseudoticker in this manner. '
                            message_popover_create_pseudoticker = f"Did you mean {tk_num} and {cur_den + 'USD=X'}? Or {'USD' + cur_num + '=X'} and {tk_den}?"
                        else:
                            tk_num_name = tk_num.replace('=X', '')
                            pseudo_tk_name = tk_num_name + '/' + tk_den
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num_name} (the exchange rate between {cur_num} and USD) to {tk_den} prices or index values.'

                    elif tk_num.startswith('USD') & tk_num.endswith('=X'):
                        # In this case numerator and denominator are effectively swapped
                        cur_num = tk_num.replace('USD', '').replace('=X', '')
                        if tk_den.startswith('USD') & tk_den.endswith('=X'):
                            tk_num_name = tk_num.replace('USD', '').replace('=X', '')
                            tk_den_name = tk_den.replace('USD', '').replace('=X', '')
                            pseudo_tk_name = tk_den_name + '/' + tk_num_name
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The exchange rate between {tk_den_name} and {tk_num_name}, or the price of {tk_den_name} in {tk_num_name}.'
                        elif tk_den.endswith('USD=X'):
                            cur_den = tk_den.replace('USD=X', '')
                            hidden_popover_create_pseudoticker = False
                            # message_popover_create_pseudoticker = 'You cannot create a pseudoticker in this manner. '
                            message_popover_create_pseudoticker = f"Did you mean {tk_num} and {'USD' + cur_den + '=X'}? Or {cur_num + 'USD=X'} and {tk_den}?"
                        else:
                            tk_num_name = tk_num.replace('=X', '')
                            pseudo_tk_name = tk_num_name + '/' + tk_den
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num_name} (the exchange rate between {cur_num} and USD) to {tk_den} prices or index values.'

                    else:
                        if tk_den.endswith('USD=X'):
                            cur_den = tk_den.replace('USD=X', '')
                            tk_den_name = tk_den.replace('=X', '')
                            pseudo_tk_name = tk_num + '/' + tk_den_name
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den_name} (the exchange rate between {cur_den} and USD). '
                            pseudo_tk_summary += f'If the currency of {tk_num} is USD, then this is the price of {tk_num} in {cur_den}.'
                        elif tk_den.startswith('USD') & tk_den.endswith('=X'):                            
                            cur_den = tk_den.replace('USD', '').replace('=X', '')
                            tk_den_name = tk_den.replace('=X', '')
                            pseudo_tk_name = tk_num + '/' + tk_den_name
                            pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den_name} (the exchange rate between USD and {cur_den}). '
                            pseudo_tk_summary += f'If the currency of {tk_num} is {cur_den}, then this is the price of {tk_num} in USD.'
                        else:
                            pseudo_tk_name = tk_num + '/' + tk_den
                            if tk_num.startswith('^') & tk_den.startswith('^'):
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den} index values.'
                            elif (not tk_num.startswith('^')) & (not tk_den.startswith('^')):
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den} prices.'
                            else:
                                pseudo_tk_summary = f'Pseudoticker {pseudo_tk_name}: The ratio of {tk_num} to {tk_den} prices and index values.'

                    ########################

                    if pseudo_tk_name != '':
                        
                        selected_pseudoticker_info[idx]['pseudo_tk_name'] = pseudo_tk_name
                        selected_pseudoticker_info[idx]['pseudo_tk_summary'] = pseudo_tk_summary

                        table_pseudoticker_data.append({
                            'Pseudoticker': pseudo_tk,
                            'Name': pseudo_tk_name
                        })    

                        table_pseudoticker_selected_rows = [int(idx) for idx in selected_pseudoticker_indices]
                        table_pseudoticker_tooltip_data.append({
                            column: {'value': pseudo_tk_summary, 'type': 'markdown' }
                            for column in ['Pseudoticker', 'Name'] }
                        )

    # print(f'(END)\n{selected_pseudoticker_info}')

    return (
        hidden_popover_create_pseudoticker,
        message_popover_create_pseudoticker,
        selected_pseudoticker_info,
        table_pseudoticker_data,
        table_pseudoticker_tooltip_data,
        table_pseudoticker_selected_rows
    )


##############################################################

if __name__ == '__main__':
    app.run(debug = True, port = 8887)
