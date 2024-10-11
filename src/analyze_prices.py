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
from operator import itemgetter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mapping_tickers import *
from utils import *
from mapping_plot_attributes import *

class AnalyzePrices():

    def __init__(
        self,
        end_date: datetime,
        start_date: datetime,
        tickers = []
    ):
        """
        end_date:   defaults to today's date, can be changed by user
        start_date: can be specified explicitly or derived based on desired length of history
        tickers:    user-specified based on suggested lists or a custom synthetic portfolio 
        """
        self.end_date = end_date
        self.start_date = start_date
        self.tickers = tickers


    ##### WELLES WILDER MOVING AVERAGE #####

    def wilder_moving_average(
        self,
        df_tk,
        n
    ):
        """
        J. Welles Wilder's EMA 
        https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python

        """
        wwma = df_tk.ewm(alpha = 1 / n, adjust = False).mean()
        
        return wwma


    ##### AVERAGE TRUE RATE #####

    def average_true_rate(
        self,
        close_tk,
        high_tk,
        low_tk,
        n = 14
    ):
        """
        https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python

        """
        tr_cols = ['tr0', 'tr1', 'tr2']
        df_tr = pd.DataFrame(columns = tr_cols, index = close_tk.index)

        df_tr['tr0'] = abs(high_tk - low_tk)
        df_tr['tr1'] = abs(high_tk - close_tk.shift())
        df_tr['tr2'] = abs(low_tk - close_tk.shift())
        tr = df_tr[tr_cols].max(axis = 1)

        atr = self.wilder_moving_average(tr, n)
        atrp = atr / close_tk * 100
        atr_data = {
            'atr': atr,
            'atrp': atrp
        }

        return atr_data


    ##### WEIGHTED MEAN #####

    def weighted_mean(
        self,
        values
    ):
        """
        values: a list, tuple or series of numerical values
        """
        if isinstance(values, (list, tuple)):
            values = pd.Series(values)

        n = len(values)
        weight_sum = n * (n + 1) / 2
        weights = range(n + 1)[1:]
        wm = values @ weights / weight_sum

        return wm


    ##### MOVING AVERAGE #####

    def moving_average(
        self,
        df_tk,
        ma_type,
        ma_window,
        min_periods = 1
    ):
        """
        df_tk:      
            a series of price values, taken as a column of df_close or df_adj_close for ticker tk
        ma_type:    
            simple ('sma'),
            exponential ('ema'),
            double exponential ('dema'),
            triple exponential ('tema'),
            weighted ('wma'),
            Welles Wilder ('wwma')
        window:
            length in days
        Returns ma
        """

        if not isinstance(df_tk, pd.Series):
            print('Incorrect format of input data')
            exit

        if ma_type in ['ema', 'dema', 'tema']:
            ma = df_tk.ewm(span = ma_window).mean()
            if ma_type in ['dema', 'tema']:
                ma = ma.ewm(span = ma_window).mean()
                if ma_type == 'tema':
                    ma = ma.ewm(span = ma_window).mean()

        elif ma_type == 'wma':
            ma = df_tk.rolling(window = ma_window, min_periods = min_periods).apply(lambda x: self.weighted_mean(x))

        elif ma_type == 'wwma':
            ma = self.wilder_moving_average(df_tk, ma_window)

        else:  # 'sma' or anything else
            ma = df_tk.rolling(window = ma_window, min_periods = min_periods).mean()

        return ma


    ##### CREATE TEMPLATE #####

    def create_template(
        self,
        date_index,
        deck_type = 'triple',
        secondary_y = False,
        plot_width = 1600,
        n_ticks_max = 52,
        plot_height_1 = None,
        plot_height_2 = None,
        plot_height_3 = None,
        n_yticks_max_1 = None,
        n_yticks_max_2 = None,
        n_yticks_max_3 = None,
        top_margin = 60,
        theme = 'dark'
    ):
        """
        Info whether the deck is a single, double or triple will come from user's input.
        Then the name of the deck (deck_type) will be translated into a number;, e.g. 'lower'
        will be translated to 2 in a double deck, while 'middle' and 'lower' will be translated 
        to 2 and 3, respectively, in a triple deck.

        legendgrouptitle will be an empty dictionary for a single and double deck, and will
        be populated with the appropriate deck name in a triple deck.

        date_index:
            series or list of dates (e.g. close_tk.index)
        deck_type:
            'single', 'double' or 'triple'

        The default n_yticks values should really be some function of plot height,
        except in special cases where it can be specified customly.

        There should be a separate function to update the y axis in any deck based
        on the custom-specified number of ticks.
        Likewise to update the x axis to select a different width (1280, 1450, 1600)

        """

        map_deck_type = {'single': 1, 'double': 2, 'triple': 3}
        n_rows = map_deck_type[deck_type]

        # Set up dictionaries for convenience

        plot_height = {}

        if (deck_type == 'single'):
            plot_height_1 = 750 if plot_height_1 is None else plot_height_1
            plot_height.update({1: plot_height_1})

        elif (deck_type == 'double'):
            plot_height_1 = 750 if plot_height_1 is None else plot_height_1
            plot_height_2 = 250 if plot_height_2 is None else plot_height_2
            plot_height.update({
                1: plot_height_1,
                2: plot_height_2
            })

        elif (deck_type == 'triple'):
            plot_height_1 = 600 if plot_height_1 is None else plot_height_1
            plot_height_2 = 200 if plot_height_2 is None else plot_height_2
            plot_height_3 = 200 if plot_height_3 is None else plot_height_3
            plot_height.update({
                1: plot_height_1,
                2: plot_height_2,
                3: plot_height_3
            })

        n_yticks_max_1 = n_yticks_map[plot_height_1] if n_yticks_max_1 is None else n_yticks_max_1
        n_yticks_max_2 = n_yticks_map[plot_height_2] if n_yticks_max_2 is None else n_yticks_max_2
        n_yticks_max_3 = n_yticks_map[plot_height_3] if n_yticks_max_1 is None else n_yticks_max_3
        n_yticks = {
            1: n_yticks_max_1,
            2: n_yticks_max_2,
            3: n_yticks_max_3
        }

        df_dummy = pd.Series(index = date_index)
        for _, idx in enumerate(date_index):
            df_dummy[idx] = 0

        x_min = str(min(df_dummy.index).date())
        x_max = str(max(df_dummy.index).date())

        height_pct = {}
        row_heights = []
        plot_height_total = sum(h for h in plot_height.values())
        for k, h in plot_height.items():
            h_pct = h / plot_height_total
            height_pct.update({k: h_pct})
            row_heights.append(h_pct)

        if deck_type == 'single':
            y_range = {
                1: {
                    'y0': 0,
                    'y1': 1
                }
            }
            specs_list = [
                [{'secondary_y': True}]
            ]

        elif deck_type == 'double': 
            y_range = {
                1: {
                    'y0': height_pct[2],
                    'y1': 1
                },
                2: {
                    'y0': 0,
                    'y1': height_pct[2]
                }
            }
            specs_list = [
                [{'secondary_y': True}],
                [{'secondary_y': False}]
            ]

        elif deck_type == 'triple': 
            y_range = {
                1: {
                    'y0': height_pct[2] + height_pct[3],
                    'y1': 1
                },
                2: {
                    'y0': height_pct[3],
                    'y1': height_pct[2] + height_pct[3]
                },
                3: {
                    'y0': 0,
                    'y1': height_pct[3]
                }
            }
            specs_list = [
                [{'secondary_y': True}],
                [{'secondary_y': False}],
                [{'secondary_y': False}]
            ]

        title_y_pos = 1 - 0.5 * top_margin / plot_height_total
        title_x_pos = 0.435 if secondary_y else 0.45

        style = theme_style[theme]

        if secondary_y:
            fig = make_subplots(
                rows = n_rows,
                cols = 1,
                shared_xaxes = True,
                vertical_spacing = 0,
                row_heights = row_heights,
                specs = specs_list
            )
        else:
            fig = make_subplots(
                rows = n_rows,
                cols = 1,
                shared_xaxes = True,
                vertical_spacing = 0,
                row_heights = row_heights
            )

        for k in range(n_rows + 1)[1:]:

            # Add dummy traces
            fig.add_trace(
                go.Scatter(
                    x = df_dummy.index.astype(str),
                    y = df_dummy,
                    line_width = 0,         
                    showlegend = False,     
                    legendgroup = 'dummy',
                    hoverinfo = 'skip'
                ),
                row = k, col = 1
            )

            # Add plot borders
            fig.add_shape(
                type = 'rect',
                xref = 'x',  # use 'x' because 'paper' does not work correctly with stacked plots
                yref = 'paper',
                x0 = x_min,
                x1 = x_max,
                y0 = y_range[k]['y0'],
                y1 = y_range[k]['y1'],
                line_color = style['x_linecolor'],
                line_width = 2
            )

            # Update axes
            fig.update_xaxes(
                type = 'category',
                showgrid = True,
                gridcolor = style['x_gridcolor'],
                nticks = n_ticks_max,
                tickangle = -90,
                ticks = 'outside',
                ticklen = 8,
                row = k, col = 1
            )
            fig.update_yaxes(
                showgrid = True,
                gridcolor = style['y_gridcolor'],
                zerolinecolor = style['x_gridcolor'],
                zerolinewidth = 1,
                nticks = n_yticks[k],
                ticks = 'outside',
                ticklen = 8,
                showticklabels = False,
                row = k, col = 1
            )

        # Update layout
        fig.update_layout(
            margin_t = top_margin,
            width = plot_width,
            height = plot_height_total,
            xaxis_rangeslider_visible = False,
            template = style['template'],
            legend_groupclick = 'toggleitem'
        )

        y_min = {1: None, 2: None, 3: None}
        y_max = {1: None, 2: None, 3: None}

        fig_data = {
            'fig': fig,
            'y_min': y_min,
            'y_max': y_max,
            'plot_height': plot_height,
            'deck_type': deck_type,
            'title_x_pos': title_x_pos,
            'title_y_pos': title_y_pos,
            'color_map': {}
        }

        return fig_data

    ##### ADJUST LEGEND POSITION #####

    def adjust_legend_position(
        fig_data,
        deck_type,
        legend_title_height = 21
    ):
        """
        legend_title_height:
            upper title height to be subtracted for triple deck, depends on the legend title font size, 21 is for size 16
        """

        n_traces_upper = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '1') & (x['showlegend'] if x['showlegend'] is not None else True)])
        n_traces_middle = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '2') & (x['showlegend'] if x['showlegend'] is not None else True)])
        n_traces_lower = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '3') & (x['showlegend'] if x['showlegend'] is not None else True)])
        n_traces_total = n_traces_upper + n_traces_middle + n_traces_lower

        legend_item_height = abs(legend_gap['double']['slope'])

        # NOTE: The middle and lower plots in the triple deck should be of the same height
        height_upper = fig_data['plot_height'][1]
        height_lower = fig_data['plot_height'][2]

        a0 = -118.3
        a_upper = 0.94258
        a_lower = 0.17954
    
        if (deck_type == 'double') | (n_traces_lower == 0):

            intercept = a0 + a_upper * height_upper + a_lower * height_lower
            legend_groupgap = intercept - legend_item_height * n_traces_upper

        elif deck_type == 'triple':

            if n_traces_middle == 0:

                intercept = a0 + a_upper * (height_upper + height_lower) + a_lower * height_lower
                legend_groupgap = intercept - n_traces_upper * legend_item_height - legend_title_height

            else:
                # a0 = legend_gap['triple']['intercept'][height_lower]
                # a1 = legend_gap['triple']['slope'][height_lower]

                a0 = -177
                legend_groupgap = (a0 + height_upper + 2 * height_lower - n_traces_total * legend_item_height - 3 * legend_title_height) / 2
    
        legend_tracegroupgap = max(legend_groupgap, 0)

        return legend_tracegroupgap


    ##### STOCHASTIC OSCILLATOR #####

    def stochastic_oscillator(
        self,
        close_tk,
        high_tk,
        low_tk,
        fast_k_period = 14,
        smoothing_period = 3,
        sma_d_period = 3,
        stochastic_type = 'Slow'
    ):
        """
        stochastic_type: 'Fast', 'Slow', 'Full'
        NOTES:
        1) fast_k_period is also know as the look--back period
        2) smoothing_period is the period used in slow %K and full %K
        3) sma_d_period is the %D averaging period used in fast, slow and full stochastics
        4) if sma_d_period == smoothing_period, then the slow and full stochastics become equivalent

        """
        fast_low = low_tk.rolling(window = fast_k_period, min_periods = 1).min()
        fast_high = high_tk.rolling(window = fast_k_period, min_periods = 1).max()
        fast_k_line = 100 * (close_tk - fast_low) / (fast_high - fast_low)

        if stochastic_type.lower() == 'fast':

            k_line = fast_k_line.copy()    
            d_line = k_line.rolling(window = sma_d_period, min_periods = 1).mean()
            stochastic_label = f'({fast_k_period}, {sma_d_period})'
            stochastic_type = 'Fast'

        elif (stochastic_type.lower() == 'full') | (sma_d_period != smoothing_period):

            k_line = fast_k_line.rolling(window = smoothing_period, min_periods = 1).mean()
            d_line = k_line.rolling(window = sma_d_period, min_periods = 1).mean()
            stochastic_label = f'({fast_k_period}, {smoothing_period}, {sma_d_period})'
            stochastic_type = 'Full'

        else:
            # This includes the case of 
            # (stochastic_type == 'slow') | (sma_d_period == smoothing_period)
            # and any other stochastic_type specified.

            k_line = fast_k_line.rolling(window = smoothing_period, min_periods = 1).mean()
            d_line = k_line.rolling(window = sma_d_period, min_periods = 1).mean()
            stochastic_label = f'({fast_k_period}, {sma_d_period})'
            stochastic_type = 'Slow'

        k_line.index = k_line.index.astype(str)
        d_line.index = d_line.index.astype(str)

        stochastic_data = {
            'k_line': k_line,
            'd_line': d_line,
            'label': stochastic_label,
            'type': stochastic_type
        }

        return stochastic_data


    ##### ADD STOCHASTIC #####

    def add_stochastic(
        self,
        fig_data,
        stochastic_data,
        tk,
        target_deck = 2,
        oversold_threshold = 20,
        overbought_threshold = 80,
        add_threshold_overlays = True,
        n_yticks_max = None,
        add_title = False,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        stochastic_data: output from stochastic_oscillator()
        tk: ticker for which to plot the stochastic %K and %D lines

        """

        fig_stochastic = fig_data['fig']
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']

        k_line = stochastic_data['k_line']
        d_line = stochastic_data['d_line']
        stochastic_label = stochastic_data['label']
        stochastic_type = stochastic_data['type']

        style = theme_style[theme]

        title_stochastic = f'{tk} {stochastic_type} {stochastic_label} Stochastic Oscillator (%)'
        yaxis_title = f'Stochastic (%)'

        if n_yticks_max is None:
            deck_height = fig_data['plot_height'][target_deck]
            n_yticks_max = n_yticks_map[deck_height]

        y_max = 99.99 if target_deck > 1 else 100

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'bold'
            )

        fig_stochastic.add_trace(
            go.Scatter(
                x = k_line.index,
                y = k_line,
                line_color = style['kline_linecolor'],
                line_width = 2,
                legendgroup = f'{target_deck}',
                legendgrouptitle = legendgrouptitle,
                name = f'{stochastic_type} {stochastic_label} %K Line'
            ),
            row = target_deck, col = 1
        )
        fig_stochastic.add_trace(
            go.Scatter(
                x = d_line.index,
                y = d_line,
                line_color = style['dline_linecolor'],
                line_width = 2,
                legendgroup = f'{target_deck}',
                legendgrouptitle = legendgrouptitle,
                name = f'{stochastic_type} {stochastic_label} %D Line'
            ),
            row = target_deck, col = 1
        )

        if add_threshold_overlays:

            stochastic_hlines = pd.DataFrame(
                {
                    'oversold': oversold_threshold,
                    'overbought': overbought_threshold,
                    'y_max': y_max
                },
                index = k_line.index
            )
            fig_stochastic.add_trace(
                go.Scatter(
                    x = stochastic_hlines.index,
                    y = stochastic_hlines['y_max'],
                    line_color = 'black',
                    line_width = 0,
                    hoverinfo = 'skip',
                    showlegend = False
                ),
                row = target_deck, col = 1
            )
            fig_stochastic.add_trace(
                go.Scatter(
                    x = stochastic_hlines.index,
                    y = stochastic_hlines['overbought'],
                    line_color = style['overbought_linecolor'],
                    line_width = 2,
                    fill = 'tonexty',  # fill to previous scatter trace
                    fillcolor = style['overbought_fillcolor'],
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    name = f'Overbought > {overbought_threshold}%'
                ),
                row = target_deck, col = 1
            )

            fig_stochastic.add_trace(
                go.Scatter(
                    x = stochastic_hlines.index,
                    y = stochastic_hlines['oversold'],
                    line_color = style['oversold_linecolor'],
                    line_width = 2,
                    fill = 'tozeroy',
                    fillcolor = style['oversold_fillcolor'],
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    name = f'Oversold < {oversold_threshold}%'
                ),
                row = target_deck, col = 1
            )

        # Update layout and axes
        if add_title:
            fig_stochastic.update_layout(
                title = dict(
                    text = title_stochastic,
                    font_size = title_font_size,
                    y = title_y_pos,
                    x = title_x_pos,
                    xanchor = 'center',
                    yanchor = 'middle'
                )
            )

        fig_stochastic.update_yaxes(
            range = (0, y_max),
            title = yaxis_title,
            showticklabels = True,
            nticks = n_yticks_max,
            row = target_deck, col = 1
        )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_stochastic.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'fig': fig_stochastic})
        fig_data['y_min'].update({target_deck: 0})
        fig_data['y_max'].update({target_deck: y_max})

        return fig_data


    ##### PLOT STOCHASTIC PLOTLY #####

    def plot_stochastic_plotly(
        elf,
        stochastic_data,
        tk,
        oversold_threshold = 20,
        overbought_threshold = 80,
        n_ticks_max = 48,
        plot_width = 1450,
        plot_height = 750,
        title_font_size = 32,
        theme = 'dark',
        overlay_price = False,
        prices = None
    ):
        """
        stochastic_data: output from stochastic_oscillator()
        tk: ticker for which to plot the stochastic %K and %D lines
        prices: close_tk (if overlay_price is True)

        """

        k_line = stochastic_data['k_line']
        d_line = stochastic_data['d_line']
        stochastic_label = stochastic_data['label']
        stochastic_type = stochastic_data['type']

        style = theme_style[theme]

        title_stochastic = f'{tk} {stochastic_label} {stochastic_type} Stochastic Oscillator (%)'

        if overlay_price:
            price_name = 'Close'
            prices.index = prices.index.astype(str)
            fig_stochastic = make_subplots(specs=[[{'secondary_y': True}]])
        else:
            fig_stochastic = make_subplots(rows = 1, cols = 1)

        x_min = k_line.index.min()
        x_max = k_line.index.max()

        stochastic_hlines = pd.DataFrame(
            {
                'oversold': oversold_threshold,
                'overbought': overbought_threshold,
                '100': 100
            },
            index = k_line.index
        )

        # For some reason, the price overlay trace shows first in the legend if it's added last
        if overlay_price:
            fig_stochastic.add_trace(
                go.Scatter(
                    x = prices.index,
                    y = prices,
                    # y = close_tk,
                    line_color = style['basecolor'],
                    name = price_name
                ),
                secondary_y = True
            )
        fig_stochastic.add_trace(
            go.Scatter(
                x = stochastic_hlines.index,
                y = stochastic_hlines['oversold'],
                line_color = style['oversold_linecolor'],
                line_width = 2,
                fill = 'tozeroy',
                fillcolor = style['oversold_fillcolor'],
                name = f'Oversold < {oversold_threshold}%'
            ),
            secondary_y = False
        )
        fig_stochastic.add_trace(
            go.Scatter(
                x = stochastic_hlines.index,
                y = stochastic_hlines['100'],
                line_color = 'black',
                line_width = 0,
                showlegend = False
            ),
            secondary_y = False
        )
        fig_stochastic.add_trace(
            go.Scatter(
                x = stochastic_hlines.index,
                y = stochastic_hlines['overbought'],
                line_color = style['overbought_linecolor'],
                line_width = 2,
                fill = 'tonexty',  # fill to previous scatter trace
                fillcolor = style['overbought_fillcolor'],
                name = f'Overbought > {overbought_threshold}%'
            ),
            secondary_y = False
        )
        fig_stochastic.add_trace(
            go.Scatter(
                x = d_line.index,
                y = d_line,
                line_color = style['dline_linecolor'],
                line_width = 2,        
                name = f'{stochastic_type} %D Line'
            ),
            secondary_y = False
        )
        fig_stochastic.add_trace(
            go.Scatter(
                x = k_line.index,
                y = k_line,
                line_color = style['kline_linecolor'],
                line_width = 2,        
                name = f'{stochastic_type} %K Line'
            ),
            secondary_y = False
        )

        # Add plot border
        fig_stochastic.add_shape(
            type = 'rect',
            xref = 'x',  # use 'x' because of seconday axis - 'paper' does not work correctly
            yref = 'paper',
            x0 = x_min,
            x1 = x_max,
            y0 = 0,
            y1 = 1,
            line_color = style['x_linecolor'],
            line_width = 0.3
        )

        # Update layout and axes
        fig_stochastic.update_layout(
            width = plot_width,
            height = plot_height,
            xaxis_rangeslider_visible = False,
            template = style['template'],
            yaxis_title = f'Stochastic Oscillator (%)',
            title = dict(
                text = title_stochastic,
                font_size = title_font_size,
                y = 0.95,
                x = 0.45,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        fig_stochastic.update_xaxes(
            type = 'category',
            gridcolor = style['x_gridcolor'],
            showgrid = True,
            nticks = n_ticks_max,
            tickangle = -90,
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10  # not working
        )
        fig_stochastic.update_yaxes(
            secondary_y = False,
            range = (0, 100),
            gridcolor = style['y_gridcolor'],
            showgrid = True,
            nticks = 11,
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10  # not working
        )
        if overlay_price:
            fig_stochastic.update_yaxes(
                title_text = price_name,
                secondary_y = True,
                ticks = 'outside',
                ticklen = 8,
                ticklabelshift = 5,  # not working
                ticklabelstandoff = 10,  # not working
                showgrid = False
            )

        return fig_stochastic
    

    ##### MOVING AVERAGE CONVERGENCE DIVERGENCE #####

    def get_macd(
        self,
        df_tk,
        signal_window = 9      
    ):
        """
        df_tk: a series of price values, taken as a column of df_close or df_adj_close for ticker tk
        """ 

        if not isinstance(df_tk, pd.Series):
            print('Incorrect format of input data')
            exit

        ema_26 = df_tk.ewm(span = 26).mean()
        ema_12 = df_tk.ewm(span = 12).mean()
        macd_line = ema_12 - ema_26

        macd_signal = macd_line.ewm(span = signal_window).mean()
        macd_histogram = macd_line - macd_signal        

        macd_data = {
            'MACD': macd_line,
            'MACD Signal': macd_signal,
            'MACD Signal Window': signal_window,
            'MACD Histogram': macd_histogram
        }

        return macd_data


    ##### MACD-V #####

    def get_macd_v(
        self,
        close_tk,
        high_tk,
        low_tk,
        signal_window = 9      
    ):
        """
        close_tk, high_tk, low_tk: 
            series of Close, High and Low daily price values for ticker tk
        atr_data:
            output from average_true_rate(), containing the ATR and ATRP lines
        """ 

        if not isinstance(close_tk, pd.Series):
            print('Incorrect format of input data')
            exit

        atr_data = self.average_true_rate(close_tk, high_tk, low_tk, n = 26)
        atr = atr_data['atr']

        ema_26 = close_tk.ewm(span = 26).mean()
        ema_12 = close_tk.ewm(span = 12).mean()

        macd_v_line = 100 * (ema_12 - ema_26) / atr

        macd_v_signal = macd_v_line.ewm(span = signal_window).mean()
        macd_v_histogram = macd_v_line - macd_v_signal

        macd_v_data = {
            'MACD': macd_v_line,
            'MACD Signal': macd_v_signal,
            'MACD Signal Window': signal_window,
            'MACD Histogram': macd_v_histogram
        }

        return macd_v_data


    ##### ADD MACD/MACD-V #####

    def add_macd(
        self,
        fig_data,
        tk_macd,
        macd_data,
        volatility_normalized = True,
        histogram_type = 'macd-signal',
        include_signal = True,
        plot_type = 'bar',
        n_yticks_max = None,
        target_deck = 2,
        add_title = False,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        Adds MACD with a signal line to a stacked plot
        volatility_normalized:
            treat input macd_data as MACD-V
        histogram_type:
            'macd-signal': MACD and Signal will be plotted as lines, 
                the green-red histogram will be based on their difference
            'macd-zero': MACD will be plotted as the green-red histogram,
                and the Signal line will be added if include_signal is True
        include_signal:
            this will plot Signal line and MACD-V line in addition to the histogram
        """

        # x_min = start_date if x_min is None else x_min
        # x_max = end_date if x_max is None else x_max

        fig_macd = fig_data['fig']
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']

        if n_yticks_max is None:
            deck_height = fig_data['plot_height'][target_deck]
            n_yticks_max = n_yticks_map[deck_height]

        style = theme_style[theme]

        if volatility_normalized:
            yaxis_title = f'MACD-V'
        else:
            yaxis_title = f'MACD'

        macd = macd_data['MACD']
        macd_histogram = macd_data['MACD Histogram']

        if histogram_type == 'macd-signal':
            macd_legend_positive = f'{yaxis_title} > Signal'
            macd_legend_negative = f'{yaxis_title} < Signal'
        else:
            macd_legend_positive = f'{yaxis_title} > 0'
            macd_legend_negative = f'{yaxis_title} < 0'

        if include_signal:
            macd_signal = macd_data['MACD Signal']
            macd_signal_window = macd_data['MACD Signal Window']
            min_macd = min(min(macd), min(macd_signal))
            max_macd = max(max(macd), max(macd_signal))
        else:
            if histogram_type == 'macd-signal':
                min_macd = min(macd_histogram)
                max_macd = max(macd_histogram)
            else:
                min_macd = min(macd)
                max_macd = max(macd)

        y_macd_min, y_macd_max = set_axis_limits(min_macd, max_macd, max_n_intervals = 8)
        if target_deck > 1:
            y_macd_max *= 0.999

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'bold'
            )

        #####

        if histogram_type == 'macd-zero':

            macd_positive = macd.copy()
            macd_negative = macd.copy()

            if plot_type == 'bar':

                macd_positive.iloc[np.where(macd_positive < 0)] = np.nan
                macd_negative.iloc[np.where(macd_negative >= 0)] = np.nan

                fig_macd.add_trace(
                    go.Bar(
                        x = macd_positive.index.astype(str),
                        y = macd_positive,
                        marker_color = style['green_color'],
                        width = 1,
                        name = macd_legend_positive,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )
                fig_macd.add_trace(
                    go.Bar(
                        x = macd_negative.index.astype(str),
                        y = macd_negative,
                        marker_color = style['red_color'],
                        width = 1,
                        name = macd_legend_negative,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )

            else:
                # 'filled_line' or 'scatter'

                prev_v = macd.iloc[0]
                macd_positive.iloc[0] = prev_v if prev_v >= 0 else np.nan
                macd_negative.iloc[0] = prev_v if prev_v < 0 else np.nan

                for idx in macd.index[1:]:

                    curr_v = macd.loc[idx]

                    if np.sign(curr_v) != np.sign(prev_v):
                        # Set both diff copies to 0 if the value is changing sign
                        macd_positive[idx] = 0
                        macd_negative[idx] = 0
                    else:
                        # Set both diff copies to current value or NaN
                        macd_positive[idx] = curr_v if curr_v >= 0 else np.nan
                        macd_negative[idx] = curr_v if curr_v < 0 else np.nan

                    prev_v = curr_v

                fig_macd.add_trace(
                    go.Scatter(
                        x = macd_positive.index.astype(str),
                        y = macd_positive,
                        line_color = style['diff_green_linecolor'],
                        line_width = 2,
                        fill = 'tozeroy',
                        fillcolor = style['diff_green_fillcolor'],
                        name = macd_legend_positive,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )
                fig_macd.add_trace(
                    go.Scatter(
                        x = macd_negative.index.astype(str),
                        y = macd_negative,
                        line_color = style['diff_red_linecolor'],
                        line_width = 2,
                        fill = 'tozeroy',
                        fillcolor = style['diff_red_fillcolor'],
                        name = macd_legend_negative,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )

        else:
            # histogram_type is 'macd-signal' (default)

            macd_histogram_positive = macd_histogram.copy()
            macd_histogram_negative = macd_histogram.copy()

            if plot_type == 'bar':

                macd_histogram_positive.iloc[np.where(macd_histogram_positive < 0)] = np.nan
                macd_histogram_negative.iloc[np.where(macd_histogram_negative >= 0)] = np.nan

                fig_macd.add_trace(
                    go.Bar(
                        x = macd_histogram_positive.index.astype(str),
                        y = macd_histogram_positive,
                        marker_color = style['green_color'],
                        width = 1,
                        name = macd_legend_positive,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )
                fig_macd.add_trace(
                    go.Bar(
                        x = macd_histogram_negative.index.astype(str),
                        y = macd_histogram_negative,
                        marker_color = style['red_color'],
                        width = 1,
                        name = macd_legend_negative,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )

            else:
                # 'filled_line' or 'scatter'

                prev_v = macd_histogram.iloc[0]
                macd_histogram_positive.iloc[0] = prev_v if prev_v >= 0 else np.nan
                macd_histogram_negative.iloc[0] = prev_v if prev_v < 0 else np.nan

                for idx in macd_histogram.index[1:]:

                    curr_v = macd_histogram.loc[idx]

                    if np.sign(curr_v) != np.sign(prev_v):
                        # Set both diff copies to 0 if the value is changing sign
                        macd_histogram_positive[idx] = 0
                        macd_histogram_negative[idx] = 0
                    else:
                        # Set both diff copies to current value or NaN
                        macd_histogram_positive[idx] = curr_v if curr_v >= 0 else np.nan
                        macd_histogram_negative[idx] = curr_v if curr_v < 0 else np.nan

                    prev_v = curr_v

                fig_macd.add_trace(
                    go.Scatter(
                        x = macd_histogram_positive.index.astype(str),
                        y = macd_histogram_positive,
                        line_color = style['diff_green_linecolor'],
                        line_width = 2,
                        fill = 'tozeroy',
                        fillcolor = style['diff_green_fillcolor'],
                        name = macd_legend_positive,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )
                fig_macd.add_trace(
                    go.Scatter(
                        x = macd_histogram_negative.index.astype(str),
                        y = macd_histogram_negative,
                        line_color = style['diff_red_linecolor'],
                        line_width = 2,
                        fill = 'tozeroy',
                        fillcolor = style['diff_red_fillcolor'],
                        name = macd_legend_negative,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )

        if include_signal:

            if histogram_type != 'macd-zero':

                fig_macd.add_trace(
                    go.Scatter(
                        x = macd.index.astype(str),
                        y = macd,
                        line = dict(color = style['basecolor']),
                        name = yaxis_title,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle,
                        showlegend = True
                    ),
                    row = target_deck, col = 1
                )

            fig_macd.add_trace(
                go.Scatter(
                    x = macd_signal.index.astype(str),
                    y = macd_signal,
                    line = dict(color = style['signal_color']),
                    name = f'EMA {macd_signal_window} Signal',
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    showlegend = True
                ),
                row = target_deck, col = 1
            )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_data['fig'].update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        if add_title & (target_deck == 1):

            if volatility_normalized:
                title_macd = f'{tk_macd} Volatility-Normalized MACD(12, 26)'
            else:
                title_macd = f'{tk_macd} MACD(12, 26)'

        fig_macd.update_layout(
            title = dict(
                text = title_macd,
                font_size = title_font_size,
                y = title_y_pos,
                x = title_x_pos,
                xanchor = 'center',
                yanchor = 'middle'
            )
        )

        fig_macd.update_yaxes(
            title_text = yaxis_title,
            range = (y_macd_min, y_macd_max),
            showticklabels = True,        
            nticks = n_yticks_max,
            row = target_deck, col = 1
        )

        fig_data.update({'fig': fig_macd})
        fig_data['y_min'].update({target_deck: y_macd_min})
        fig_data['y_max'].update({target_deck: y_macd_max})

        return fig_data 


    ##### PLOT MACD PLOTLY #####

    def plot_macd_plotly(
        self,
        tk_macd,
        macd_data,
        df_tk,
        n_ticks_max = 48,
        n_yticks_max = 16,
        plot_width = 1450,
        plot_height = 750,
        title_font_size = 32,
        theme = 'dark',
        overlay_price = False,
        price_type = 'close'
    ):
        """
        MACD plot with a signal line and the original price line overlayed, if desired
        price_type: Normally 'adjusted close' or 'close' or whatever MACD is based on
        """

        macd = macd_data['MACD']
        macd_signal = macd_data['MACD Signal']
        macd_signal_window = macd_data['MACD Signal Window']
    
        x_min = str(macd.index.min().date())
        x_max = str(macd.index.max().date())
    
        min_macd = min(min(macd), min(macd_signal))
        max_macd = max(max(macd), max(macd_signal))
        y_macd_min, y_macd_max = set_axis_limits(min_macd, max_macd)

        macd_positive = macd.copy()
        macd_positive.iloc[np.where(macd_positive < 0)] = np.nan
        macd_negative = macd.copy()
        macd_negative.iloc[np.where(macd_negative >= 0)] = np.nan

        title_macd = f'{tk_macd} Moving Average Convergence Divergence (EMA 12-26)'

        price_types = ['adjusted close', 'adj close', 'close', 'open', 'high', 'low']
        if price_type in price_types:
            price_name = 'Adjusted Close' if price_type == 'adj close' else price_type.title()
        else:
            price_name = 'Adjusted Close'

        style = theme_style[theme]

        if overlay_price:
            fig_macd = make_subplots(specs=[[{'secondary_y': True}]])
        else:
            fig_macd = make_subplots(rows = 1, cols = 1)

        fig_macd.add_trace(
            go.Bar(
                x = macd_positive.index.astype(str),
                y = macd_positive,
                marker_color = style['green_color'],
                width = 1,
                name = 'MACD > 0'
            ),
            secondary_y = False
        )
        fig_macd.add_trace(
            go.Bar(
                x = macd_negative.index.astype(str),
                y = macd_negative,
                marker_color = style['red_color'],
                width = 1,
                name = 'MACD < 0'
            ),
            secondary_y = False
        )
        fig_macd.add_trace(
            go.Scatter(
                x = macd_signal.index.astype(str),
                y = macd_signal,
                line = dict(color = style['signal_color']),
                # name = 'Signal Line'  # 9-day span is a standard, no need to customise it
                name = f'{macd_signal_window}-Day Signal Line'
            ),
            secondary_y = False
        )
        if overlay_price:
            fig_macd.add_trace(
                go.Scatter(
                    x = macd.index.astype(str),
                    y = df_tk,
                    line = dict(color = style['basecolor']),
                    name = price_name
                ),
                secondary_y = True    
            )

        # Add plot border
        fig_macd.add_shape(
            type = 'rect',
            xref = 'x',  # use 'x' because of seconday axis - 'paper' does not work correctly
            yref = 'paper',
            x0 = x_min,
            x1 = x_max,
            y0 = 0,
            y1 = 1,
            line_color = style['x_linecolor'],
            line_width = 0.3
        )

        # Update layout and axes
        fig_macd.update_layout(
            width = plot_width,
            height = plot_height,
            xaxis_rangeslider_visible = False,
            template = style['template'],
            title = dict(
                text = title_macd,
                font_size = title_font_size,
                y = 0.95,
                x = 0.45,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        fig_macd.update_yaxes(
            title_text = f'MACD',
            range = (y_macd_min, y_macd_max),
            nticks = n_yticks_max,
            secondary_y = False,
            gridcolor = style['x_gridcolor'],
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10,  # not working
        )
        if overlay_price:
            fig_macd.update_yaxes(
                title_text = price_name,
                secondary_y = True,
                ticks = 'outside',
                ticklen = 8,
                ticklabelshift = 5,  # not working
                ticklabelstandoff = 10,  # not working
                showgrid = False
            )
        fig_macd.update_xaxes(
            type = 'category',
            nticks = n_ticks_max,
            tickangle = -90,
            gridcolor = style['y_gridcolor'],
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10,  # not working
            showgrid = True
        )

        return fig_macd


    ##### PLOT RSI HLINES PLOTLY #####

    def plot_rsi_hlines_plotly(
        self,
        df_rsi,
        tk,
        n_ticks_max = 48,
        plot_width = 1450,
        plot_height = 750,
        title_font_size = 32,
        theme = 'dark',
        overlay_price = False,
        df_price = None,
        price_type = 'close'
    ):
        """
        df_rsi:     RSI dataframe/series
        tk:         ticker for which ro plot RSI
        price_type: normally 'adjusted close' or 'close', whatever the RSI is based on
        df_price:   dataframe/series of prices to overlay (if overlay_price is True)

        """

        style = theme_style[theme]

        title_rsi = f'{tk} Relative Strength Index (%)'
        price_types = ['adjusted close', 'adj close', 'close', 'open', 'high', 'low']

        if price_type in price_types:
            price_name = 'Adjusted Close' if price_type == 'adj close' else price_type.title()
        else:
            price_name = 'Adjusted Close'

        if overlay_price:
            fig_rsi = make_subplots(specs=[[{'secondary_y': True}]])
        else:
            fig_rsi = make_subplots(rows = 1, cols = 1)

        x_min = df_rsi.index.min()
        x_max = df_rsi.index.max()

        df_rsi_hlines = pd.DataFrame({'30': 30, '70': 70, '100': 100}, index=df_rsi.index)

        # For some reason, the price overlay trace shows first in the legend if it's added last
        if overlay_price:
            fig_rsi.add_trace(
                go.Scatter(
                    x = df_rsi.index,
                    y = df_price,
                    line = dict(color = style['basecolor']),
                    name = price_name
                ),
                secondary_y = True
            )
        fig_rsi.add_trace(
            go.Scatter(
                x = df_rsi_hlines.index,
                y = df_rsi_hlines['30'],
                line = dict(color = style['rsi_30_linecolor']),
                line_width = 2,
                fill = 'tozeroy',
                fillcolor = style['rsi_30_fillcolor'],
                name = 'Oversold < 30%'
            ),
            secondary_y = False
        )
        fig_rsi.add_trace(
            go.Scatter(
                x = df_rsi_hlines.index,
                y = df_rsi_hlines['100'],
                line = dict(color='black'),
                line_width = 0,
                showlegend = False
            ),
            secondary_y = False
        )
        fig_rsi.add_trace(
            go.Scatter(
                x = df_rsi_hlines.index,
                y = df_rsi_hlines['70'],
                line = dict(color = style['rsi_70_linecolor']),
                line_width = 2,
                fill = 'tonexty',  # fill to previous scatter trace
                fillcolor = style['rsi_70_fillcolor'],
                name = 'Overbought > 70%'
            ),
            secondary_y = False
        )
        fig_rsi.add_trace(
            go.Scatter(
                x = df_rsi.index,
                y = df_rsi[tk],
                line = dict(color=style['rsi_linecolor']),
                line_width = 2,        
                name = 'RSI (%)'
            ),
            secondary_y = False
        )

        # Add plot border
        fig_rsi.add_shape(
            type = 'rect',
            xref = 'x',  # use 'x' because of seconday axis - 'paper' does not work correctly
            yref = 'paper',
            x0 = x_min,
            x1 = x_max,
            y0 = 0,
            y1 = 1,
            line_color = style['x_linecolor'],
            line_width = 0.3
        )

        # Update layout and axes
        fig_rsi.update_layout(
            width = plot_width,
            height = plot_height,
            xaxis_rangeslider_visible = False,
            template = style['template'],
            yaxis_title = f'RSI (%)',
            title = dict(
                text = title_rsi,
                font_size = title_font_size,
                y = 0.95,
                x = 0.45,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        fig_rsi.update_xaxes(
            type = 'category',
            nticks = n_ticks_max,
            tickangle = -90,
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10,  # not working
        )
        fig_rsi.update_yaxes(
            secondary_y = False,
            range = (0, 100),
            nticks = 11,
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10,  # not working
        )
        if overlay_price:
            fig_rsi.update_yaxes(
                title_text = price_name,
                secondary_y = True,
                ticks = 'outside',
                ticklen = 8,
                ticklabelshift = 5,  # not working
                ticklabelstandoff = 10,  # not working
                showgrid = False
            )

        return fig_rsi


    ##### LONGEST DRAWDOWN #####

    def longest_drawdown(
        self,
        dd,
        tk
    ):
        """
        dd:  series (column) of drawdowns for ticker tk
        tk:  ticker
        returns dictionary longest_drawdown_data = {
            'Longest Drawdown': df_longest,
            'Total Length': total_length,
            'Length To Trough': length_to_trough,
            'Trough': trough,
            'Trough Date': trough_date
            }
        """

        dd_tk = pd.DataFrame(dd, columns=[tk], index=dd.index)
        df_longest = pd.DataFrame(columns=[tk])

        total_length = 0

        for i, idx in enumerate(dd_tk.index):

            # Is it a peak?
            if dd_tk.loc[idx, tk] == 0:
                # If so, let's mark it
                peak_idx = idx
                # Let's look at the subset from the peak to the end of the data
                sub_dd_tk = dd_tk.iloc[i + 1:]  # dd_tk[i + 1:] works too

                # Are there any zeros, i.e. other peaks, in this subset?
                if sub_dd_tk[tk].max() == 0:
                    # If so, then take the earliest of them as a candidate to mark the recovery from this drawdown
                    end_idx = sub_dd_tk.index[sub_dd_tk[tk] == 0].min()
                else:
                    # If not, then it must be the last drawdown of the historical period, not yet recovered
                    end_idx = sub_dd_tk.index[-1]

                # Does this subset have a negative minimum or is it just a flat segment of zeros?
                if dd_tk.loc[peak_idx: end_idx, tk].min() < 0:
                    # If it does have a negative minimum, then is this drawdown the longest one so far?
                    if len(dd_tk[peak_idx: end_idx]) > total_length:
                        # If so, then update the longest drawdown and its length
                        df_longest = dd_tk[peak_idx: end_idx].copy()
                        total_length = len(df_longest)

        trough = df_longest[tk].min()
        trough_datetime = df_longest.index[df_longest[tk] == trough][0]
        trough_date = trough_datetime.date()
        length_to_trough = len(df_longest[df_longest.index <= trough_datetime])

        longest_drawdown_data = {
            'Longest Drawdown': df_longest,
            'Total Length': total_length,
            'Length To Trough': length_to_trough,
            'Trough': trough,
            'Trough Date': trough_date
        }

        return longest_drawdown_data


    ##### SUMMARIZE PORTFOLIO DRAWDOWNS #####

    def summarize_portfolio_drawdowns(
        self,
        df,
        tickers
    ):
        """
        df:         input dataframe of historical prices, such as df_adj_close
        tickers:    Yahoo!Finance tickers in the portfolio
        return:     drawdown_data = {
                        'Drawdown Stats': df_drawdown_stats
                    }
        """

        drawdown_metrics = [
            'Max Drawdown Trough (%)',
            'Max Drawdown Trough Date',
            'Max Drawdown Length (Days)',
            'Average Drawdown Trough (%)',
            'Longest Drawdown (Days)',
            'Longest Drawdown Trough (%)',
            'Longest Drawdown Trough Date',
            'Total Ulcer Index (%)',
            'Max 14-Day Ulcer Index (%)',
            'Max 14-Day Ulcer Date'
        ]
        df_drawdown_stats = pd.DataFrame(columns=tickers, index=drawdown_metrics).astype(str)

        df_drawdowns = pd.DataFrame(columns=tickers, index=df.index)
        returns = df / df.shift(1) - 1
        df_returns = pd.DataFrame(returns, columns=tickers, index=df.index).dropna()

        for tk in tickers:
            df_drawdowns.loc[df_drawdowns.index[0], tk] = 0

        for i, idx in enumerate(df_drawdowns.index[1:]):
            idx_prev = df_drawdowns.index[i]
            for tk in tickers:
                current_drawdown = (1 + df_returns.loc[idx, tk]) * (1 + df_drawdowns.loc[idx_prev, tk]) - 1
                df_drawdowns.loc[idx, tk] = np.min([current_drawdown, 0])

        df_drawdowns = df_drawdowns.astype(float) * 100
        max_index = max(df_drawdowns.index)
        print(max_index)

        df_drawdowns_squared = df_drawdowns * df_drawdowns
        n = len(df_drawdowns_squared)

        roll_ulcer = np.sqrt(df_drawdowns_squared.rolling(window=14, min_periods=1).sum() / 14)
        df_roll_ulcer = pd.DataFrame(roll_ulcer, columns=tickers)

        for tk in tickers:

            drawdowns_tk = df_drawdowns[tk]

            max_drawdown_trough = drawdowns_tk.min()
            max_drawdown_trough_datetime = df_drawdowns.index[drawdowns_tk == max_drawdown_trough][0]
            max_drawdown_trough_date = max_drawdown_trough_datetime.date()

            max_drawdown_peak = max(drawdowns_tk.index[(drawdowns_tk.index < max_drawdown_trough_datetime) & (drawdowns_tk == 0)])
            index_recovery = drawdowns_tk.index[(drawdowns_tk.index > max_drawdown_trough_datetime) & (drawdowns_tk == 0)]
            if len(index_recovery) == 0:
                max_drawdown_recovery = max_index
            else:
                max_drawdown_recovery = min(index_recovery)
            max_drawdown_length = len(drawdowns_tk[max_drawdown_peak: max_drawdown_recovery])

            df_drawdown_stats.loc['Max Drawdown Trough (%)', tk] = f'{drawdowns_tk.min():.2f}'
            df_drawdown_stats.loc['Max Drawdown Trough Date', tk] = f'{max_drawdown_trough_date}'
            df_drawdown_stats.loc['Max Drawdown Length (Days)', tk] = f'{max_drawdown_length}'
            df_drawdown_stats.loc['Average Drawdown Trough (%)', tk] = f'{drawdowns_tk.mean():.2f}'

            longest_drawdown_data = self.longest_drawdown(drawdowns_tk, tk)
            longest_drawdown_length = longest_drawdown_data['Total Length']
            longest_drawdown_trough = longest_drawdown_data['Trough']
            longest_drawdown_trough_date = longest_drawdown_data['Trough Date']
            df_drawdown_stats.loc['Longest Drawdown (Days)', tk] = f'{longest_drawdown_length}'
            df_drawdown_stats.loc['Longest Drawdown Trough (%)', tk] = f'{longest_drawdown_trough:.2f}'
            df_drawdown_stats.loc['Longest Drawdown Trough Date', tk] = f'{longest_drawdown_trough_date}'

            roll_ulcer_tk = df_roll_ulcer[tk]
            ulcer_index = np.sqrt(df_drawdowns_squared[tk].sum() / n)
            df_drawdown_stats.loc['Total Ulcer Index (%)', tk] = f'{ulcer_index:.2f}'
            max_14d_ulcer = roll_ulcer_tk.max()
            max_14d_ulcer_date = df_roll_ulcer.index[roll_ulcer_tk == max_14d_ulcer][0].date()
            df_drawdown_stats.loc['Max 14-Day Ulcer Index (%)', tk] = f'{max_14d_ulcer:.2f}'
            df_drawdown_stats.loc['Max 14-Day Ulcer Date', tk] = f'{max_14d_ulcer_date}'

        return df_drawdown_stats


    ##### SUMMARIZE TK DRAWDOWNS #####

    def summarize_tk_drawdowns(
            self,
            df_price,
            tk,
            sort_by,
            n_top = 5
    ):
        """
        df_price:   series/dataframe of historical prices, such as df_adj_close
        tk:         ticker for which to perform the analysis
        sort_by:    column to sort by, should be a based on user input
        n_top:      number of top drawdowns to include in df_tk_deepest_drawdowns
        return:     drawdown_data = {
                        'Drawdown Stats': df_tk_drawdowns,
                        'Deepest Drawdowns': df_tk_deepest_drawdowns,
                        'Longest Drawdowns': df_tk_longest_drawdowns
                    }
        """

        if isinstance(df_price, pd.Series):
            df_tk = df_price.copy()
        elif isinstance(df_price, pd.DataFrame):
            df_tk = df_price[tk]
        else:
            print('Incorrect format of input data')
            exit

        df_roll_max = pd.DataFrame(index=df_tk.index)
        drawdown_columns = [
            'Peak',
            'Trough',
            '% Drawdown',
            'Peak Date',
            'Trough Date',
            'Recovery Date',
            'Total Length',
            'Peak To Trough',
            'Trough To Recovery'
        ]
        cols_float = [
            'Peak',
            'Trough',
            '% Drawdown'
        ]
        cols_int = [
            'Total Length',
            'Peak To Trough',
            'Trough To Recovery'
        ]
        cols_str = [
            'Peak Date',
            'Trough Date',
            'Recovery Date'
        ]

        df_tk_drawdowns = pd.DataFrame(columns=drawdown_columns)
        df_tk_deepest_drawdowns = pd.DataFrame(columns=drawdown_columns)
        df_tk_longest_drawdowns = pd.DataFrame(columns=drawdown_columns)
        df_tk_drawdowns_str = pd.DataFrame(columns=drawdown_columns)
        df_tk_deepest_drawdowns_str = pd.DataFrame(columns=drawdown_columns)
        df_tk_longest_drawdowns_str = pd.DataFrame(columns=drawdown_columns)

        n = len(df_tk)
        df_roll_max[tk] = df_tk.rolling(n, min_periods=1).max()
        unique_max_list = df_roll_max[tk].unique()

        for peak in unique_max_list:

            # Define a segment corresponding to vmax 
            cond = df_roll_max[tk] == peak
            seg = df_roll_max.loc[cond, tk]
            n_seg = len(seg)

            # There was no drop within a segment if its length is 1 or 2
            if n_seg > 2:

                # The first date of the segment (min_date_seg) may not necessarily be the first date of the drawdown; e.g. 
                # if the segment starts with a flat section. In that case the last date of the flat part becomes the min_date.

                min_date_seg = seg.index.min()
                max_date = seg.index.max()
                max_iloc = df_price.index.get_loc(max_date)

                cond_below_max = df_tk < peak
                cond_in_range = (df_price.index >= min_date_seg) & (df_price.index <= max_date) & cond_below_max

                min_date = df_price.loc[cond_in_range].index.min()
                min_iloc = df_price.index.get_loc(min_date)
                peak_date = min_date if min_iloc == 0 else df_price.index[min_iloc - 1]

                # trough = df.loc[cond_in_range, tk].min()
                trough = df_tk[cond_in_range].min()
                cond_trough = cond_in_range & (df_tk == trough)
                trough_date = df_price[cond_trough].index[0]
                recovery_date = max_date if max_iloc == n - 1 else df_price.index[max_iloc + 1]

                # NOTE: If the last Adj Close in the last segment is less than that segment's rolling max, then 
                # there was no recovery in that segment. It should still be reported if the drawdown in that segment is
                # significant, must marked somehow to indicate no recovery (e.g. as 0 or -1)

                cond_to_trough = (df_price.index >= min_date) & (df_price.index <= trough_date) & cond_below_max
                cond_recovery = (df_price.index > trough_date) & (df_price.index <= max_date) & cond_below_max
                n_to_trough = len(seg[cond_to_trough]) + 1
                n_recovery = len(seg[cond_recovery]) + 1
                n_length = n_to_trough + n_recovery
                drawdown = trough / peak - 1

                df_tk_drawdowns.loc[peak, 'Peak'] = peak
                df_tk_drawdowns.loc[peak, 'Trough'] = trough
                df_tk_drawdowns.loc[peak, 'Peak Date'] = peak_date
                df_tk_drawdowns.loc[peak, 'Trough Date'] = trough_date
                df_tk_drawdowns.loc[peak, 'Recovery Date'] = recovery_date
                df_tk_drawdowns.loc[peak, '% Drawdown'] = 100 * drawdown
                df_tk_drawdowns.loc[peak, 'Total Length'] = n_length
                df_tk_drawdowns.loc[peak, 'Peak To Trough'] = n_to_trough
                df_tk_drawdowns.loc[peak, 'Trough To Recovery'] = n_recovery

        n_top = min(n_top, len(df_tk_drawdowns))

        ascending = True if sort_by in cols_float + cols_str else False
        df_tk_drawdowns = df_tk_drawdowns.sort_values(by=sort_by, ascending=ascending)
        df_tk_drawdowns = df_tk_drawdowns.reset_index(drop=True)

        df_tk_deepest_drawdowns = df_tk_drawdowns.sort_values(by='% Drawdown', ascending=True)
        df_tk_deepest_drawdowns = df_tk_deepest_drawdowns.reset_index(drop=True)[:n_top]
    
        df_tk_longest_drawdowns = df_tk_drawdowns.sort_values(by='Total Length', ascending=False)
        df_tk_longest_drawdowns = df_tk_longest_drawdowns.reset_index(drop=True)[:n_top]

        # Convert output to strings

        for idx in df_tk_drawdowns.index:
            df_tk_drawdowns_str.loc[idx, 'Peak'] = f"{df_tk_drawdowns.loc[idx, 'Peak']:.2f}"
            df_tk_drawdowns_str.loc[idx, 'Trough'] = f"{df_tk_drawdowns.loc[idx, 'Trough']:.2f}"
            df_tk_drawdowns_str.loc[idx, 'Peak Date'] = f"{df_tk_drawdowns.loc[idx, 'Peak Date'].date()}"
            df_tk_drawdowns_str.loc[idx, 'Trough Date'] = f"{df_tk_drawdowns.loc[idx, 'Trough Date'].date()}"
            df_tk_drawdowns_str.loc[idx, 'Recovery Date'] = f"{df_tk_drawdowns.loc[idx, 'Recovery Date'].date()}"
            df_tk_drawdowns_str.loc[idx, '% Drawdown'] = f"{(df_tk_drawdowns.loc[idx, '% Drawdown']):.2f}"
            df_tk_drawdowns_str.loc[idx, 'Total Length'] = f"{df_tk_drawdowns.loc[idx, 'Total Length']}"
            df_tk_drawdowns_str.loc[idx, 'Peak To Trough'] = f"{df_tk_drawdowns.loc[idx, 'Peak To Trough']}"
            df_tk_drawdowns_str.loc[idx, 'Trough To Recovery'] = f"{df_tk_drawdowns.loc[idx, 'Trough To Recovery']}"

        for idx in df_tk_deepest_drawdowns.index:
            df_tk_deepest_drawdowns_str.loc[idx, 'Peak'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Peak']:.2f}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Trough'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Trough']:.2f}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Peak Date'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Peak Date'].date()}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Trough Date'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Trough Date'].date()}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Recovery Date'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Recovery Date'].date()}"
            df_tk_deepest_drawdowns_str.loc[idx, '% Drawdown'] = f"{(df_tk_deepest_drawdowns.loc[idx, '% Drawdown']):.2f}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Total Length'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Total Length']}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Peak To Trough'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Peak To Trough']}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Trough To Recovery'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Trough To Recovery']}"

        for idx in df_tk_longest_drawdowns.index:
            df_tk_longest_drawdowns_str.loc[idx, 'Peak'] = f"{df_tk_longest_drawdowns.loc[idx, 'Peak']:.2f}"
            df_tk_longest_drawdowns_str.loc[idx, 'Trough'] = f"{df_tk_longest_drawdowns.loc[idx, 'Trough']:.2f}"
            df_tk_longest_drawdowns_str.loc[idx, 'Peak Date'] = f"{df_tk_longest_drawdowns.loc[idx, 'Peak Date'].date()}"
            df_tk_longest_drawdowns_str.loc[idx, 'Trough Date'] = f"{df_tk_longest_drawdowns.loc[idx, 'Trough Date'].date()}"
            df_tk_longest_drawdowns_str.loc[idx, 'Recovery Date'] = f"{df_tk_longest_drawdowns.loc[idx, 'Recovery Date'].date()}"
            df_tk_longest_drawdowns_str.loc[idx, '% Drawdown'] = f"{(df_tk_longest_drawdowns.loc[idx, '% Drawdown']):.2f}"
            df_tk_longest_drawdowns_str.loc[idx, 'Total Length'] = f"{df_tk_longest_drawdowns.loc[idx, 'Total Length']}"
            df_tk_longest_drawdowns_str.loc[idx, 'Peak To Trough'] = f"{df_tk_longest_drawdowns.loc[idx, 'Peak To Trough']}"
            df_tk_longest_drawdowns_str.loc[idx, 'Trough To Recovery'] = f"{df_tk_longest_drawdowns.loc[idx, 'Trough To Recovery']}"

        drawdown_data = {
            'Drawdown Stats': df_tk_drawdowns,
            'Deepest Drawdowns': df_tk_deepest_drawdowns,
            'Longest Drawdowns': df_tk_longest_drawdowns,
            'Drawdown Stats Str': df_tk_drawdowns_str,
            'Deepest Drawdowns Str': df_tk_deepest_drawdowns_str,
            'Longest Drawdowns Str': df_tk_longest_drawdowns_str
        }

        return drawdown_data


    ##### PLOT DRAWDOWNS PLOTLY #####

    def plot_drawdowns_plotly(
        self,
        df_price,
        tk,
        drawdown_data,
        n_top_drawdowns,
        x_min,
        x_max,
        n_ticks_max,
        n_yticks_max = 16,
        top_by = 'depth',
        show_trough_to_recovery = False,
        plot_width = 1450,
        plot_height = 750,
        title_font_size = 32,
        theme = 'dark'
    ):

        if isinstance(df_price, pd.Series):
            df_tk = df_price.copy()
        elif isinstance(df_price, pd.DataFrame):
            df_tk = df_price[tk]
        else:
            print('Incorrect format of input data')
            exit

        df_tk_deepest_drawdowns = drawdown_data['Deepest Drawdowns']
        df_tk_longest_drawdowns = drawdown_data['Longest Drawdowns']
        df_tk_deepest_drawdowns_str = drawdown_data['Deepest Drawdowns Str']
        df_tk_longest_drawdowns_str = drawdown_data['Longest Drawdowns Str']

        style = theme_style[theme]
        template = style['template']
        top_by_color = style['red_color']

        # Alpha = opacity. Since opacity of 1 covers the gridlines, alpha_max is reduced here.
        if theme == 'dark':
            alpha_min, alpha_max = 0.15, 0.6  # max intensity covers the grid
        else:
            alpha_min, alpha_max = 0.1, 0.8  # max intensity covers the grid

        if top_by == 'depth':
            top_list = list(df_tk_deepest_drawdowns['% Drawdown'])
            top_cmap = map_values(top_list, alpha_min, alpha_max, ascending=True)
        else:
            top_list = list(df_tk_longest_drawdowns['Total Length'])
            top_cmap = map_values(top_list, alpha_min, alpha_max, ascending=False)

        fig = make_subplots(rows = 1, cols = 1)
   
        min_y = min(df_tk)
        max_y = max(df_tk)
        y_min, y_max = set_axis_limits(min_y, max_y)

        x_min = str(df_tk.index.min().date())
        x_max = str(df_tk.index.max().date())

        if top_by == 'depth':
            top_drawdowns = df_tk_deepest_drawdowns
            top_drawdowns_str = df_tk_deepest_drawdowns_str
        else:
            top_drawdowns = df_tk_longest_drawdowns
            top_drawdowns_str = df_tk_longest_drawdowns_str   

        n_top_drawdowns = min(n_top_drawdowns, len(top_drawdowns))

        if show_trough_to_recovery | (top_by == 'length'):
            zip_drawdown_parameters = zip(
                top_drawdowns_str.index,
                top_drawdowns_str['Peak Date'],
                top_drawdowns_str['Recovery Date'],
                top_drawdowns['% Drawdown'],
                top_drawdowns['Total Length']
            )
            title_drawdowns = f'{tk} {n_top_drawdowns} Top Drawdowns by {top_by.capitalize()} - Peak To Recovery'    
        else:
            zip_drawdown_parameters = zip(
                top_drawdowns_str.index,
                top_drawdowns_str['Peak Date'],
                top_drawdowns_str['Trough Date'],
                top_drawdowns['% Drawdown'],
                top_drawdowns['Peak To Trough']  # This corresponds to the width of the Peak-To-Trough band
            )
            title_drawdowns = f'{tk} {n_top_drawdowns} Top Drawdowns by {top_by.capitalize()} - Peak To Trough'

        # Add the price line here to make sure it's first in the legend
        fig.add_trace(
            go.Scatter(
                x = df_tk.index.astype(str),
                y = df_tk,
                line = dict(color = style['basecolor']),
                line_width = 2,
                name = 'Adjusted Close',
                showlegend = True
            )
        )

        for _, x1, x2, depth, length in zip_drawdown_parameters:

            if top_by == 'depth':
                alpha_deepest = top_cmap[depth]
                name = f'{depth:.1f}%, {length}d'
            else:
                alpha_deepest = top_cmap[length]
                name = f'{length}d, {depth:.1f}%'

            fillcolor = top_by_color.replace('1)', f'{alpha_deepest})')
            
            fig.add_trace(
                go.Scatter(
                    x = [x1, x2, x2, x1, x1],
                    y = [y_min, y_min, y_max, y_max, y_min],
                    mode = 'lines',
                    line_width = 2,
                    line_color = 'brown',                    
                    fill = 'toself',
                    fillcolor = fillcolor,
                    name = name
                )
            )

        # Add the price line here to make sure it's on top of other layers
        fig.add_trace(
            go.Scatter(
                x = df_tk.index.astype(str),
                y = df_tk,
                line = dict(color = style['basecolor']),
                showlegend = False
            )
        )

        # Add plot border
        fig.add_shape(
            type = 'rect',
            xref = 'x',  # use 'x' because of the seconday axis - 'paper' does not work correctly
            yref = 'paper',
            x0 = x_min,
            x1 = x_max,
            y0 = 0,
            y1 = 1,
            line_color = style['x_linecolor'],
            line_width = 0.3
        )

        # Update layout and axes
        fig.update_layout(
            width = plot_width,
            height = plot_height,
            xaxis_rangeslider_visible = False,
            template = template,
            legend_groupclick = 'toggleitem',            
            yaxis_title = f'Price',
            margin_t = 60,
            title = dict(
                text = title_drawdowns,
                font_size = title_font_size,
                y = 0.975,
                x = 0.45,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        fig.update_xaxes(
            type = 'category',
            showgrid = True,
            gridcolor = style['x_gridcolor'],
            nticks = n_ticks_max,
            tickangle = -90,
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10  # not working
        )
        fig.update_yaxes(
            range = (y_min, y_max),
            showgrid = True,
            gridcolor = style['y_gridcolor'],
            nticks = n_yticks_max,
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 20  # not working
        )

        return fig
        # MUST RETURN A DICTIONARY so overlays can be added


    ##### RSI #####

    def relative_strength(
        self,    
        prices,
        period = 14
    ):
        """
        http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
        http://www.investopedia.com/terms/r/rsi.asp
        """

        deltas = np.diff(prices)
        seed = deltas[:period + 1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down
        array_rsi = np.zeros_like(prices)
        array_rsi[:period] = 100. - 100. / (1. + rs)

        for i in range(period, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter

            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period

            rs = up / down
            array_rsi[i] = 100. - 100. / (1. + rs)

        rsi = pd.Series(data = array_rsi, index = prices.index.astype(str))
        rsi_type = f'{period}'

        rsi_data = {
            'rsi': rsi,
            'type': rsi_type
        }

        return rsi_data


    ##### ADD RSI #####

    def add_rsi(
        self,
        fig_data,
        rsi_data,
        tk,
        target_deck = 2,
        oversold_threshold = 30,
        overbought_threshold = 70,
        add_threshold_overlays = True,
        n_yticks_max = None,
        add_title = False,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        rsi_data:   output from relative_strength()
        tk:         ticker for which to plot RSI
        price_type: normally 'adjusted close' or 'close', whatever the RSI is based on
        df_price:   dataframe/series of prices to overlay (if overlay_price is True)

        """

        rsi = rsi_data['rsi']
        rsi_type = rsi_data['type']

        fig_rsi = fig_data['fig']    
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']

        style = theme_style[theme]

        title_rsi = f'{tk} Relative Strength Index {rsi_type} (%)'
        yaxis_title = f'RSI (%)'

        if n_yticks_max is None:
            deck_height = fig_data['plot_height'][target_deck]
            n_yticks_max = n_yticks_map[deck_height]

        y_max = 99.99 if target_deck > 1 else 100

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'bold'
            )

        fig_rsi.add_trace(
            go.Scatter(
                x = rsi.index,
                y = rsi,
                line_color = style['rsi_linecolor'],
                line_width = 2,
                legendgroup = f'{target_deck}',
                legendgrouptitle = legendgrouptitle,            
                name = f'RSI {rsi_type} (%)'
            ),
            row = target_deck, col = 1
        )

        if add_threshold_overlays:
            rsi_hlines = pd.DataFrame(
                {
                    'oversold': oversold_threshold,
                    'overbought': overbought_threshold,
                    'y_max': y_max
                },
                index = rsi.index
            )
            fig_rsi.add_trace(
                go.Scatter(
                    x = rsi_hlines.index,
                    y = rsi_hlines['y_max'],
                    line_color = 'black',
                    line_width = 0,
                    hoverinfo = 'skip',                
                    showlegend = False
                ),
                row = target_deck, col = 1
            )
            fig_rsi.add_trace(
                go.Scatter(
                    x = rsi_hlines.index,
                    y = rsi_hlines['overbought'],
                    line_color = style['overbought_linecolor'],
                    line_width = 2,
                    fill = 'tonexty',  # fill to previous scatter trace
                    fillcolor = style['overbought_fillcolor'],
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    name = f'Overbought > {overbought_threshold}%'
                ),
                row = target_deck, col = 1
            )
            fig_rsi.add_trace(
                go.Scatter(
                    x = rsi_hlines.index,
                    y = rsi_hlines['oversold'],
                    line_color = style['oversold_linecolor'],
                    line_width = 2,
                    fill = 'tozeroy',
                    fillcolor = style['oversold_fillcolor'],
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    name = f'Oversold < {oversold_threshold}%'
                ),
                row = target_deck, col = 1
            )

        # Update layout and axes
        if add_title:
            fig_rsi.update_layout(
                title = dict(
                    text = title_rsi,
                    font_size = title_font_size,
                    y = title_y_pos,
                    x = title_x_pos,
                    xanchor = 'center',
                    yanchor = 'middle'
                )
            )

        fig_rsi.update_yaxes(
            range = (0, y_max),
            title = yaxis_title,
            showticklabels = True,
            nticks = n_yticks_max,
            row = target_deck, col = 1
        )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_rsi.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
                # legend_traceorder = 'grouped+reversed'
            )

        fig_data.update({'fig': fig_rsi})
        fig_data['y_min'].update({target_deck: 0})
        fig_data['y_max'].update({target_deck: y_max})

        return fig_data


    ##### PLOT RSI PLOTLY #####

    def plot_rsi_plotly(
        self,
        df_rsi,
        tk_rsi,
        n_ticks_max = 48,
        n_yticks_max = 16,
        plot_width = 1450,
        plot_height = 750,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        theme: either dark (template 'plotly_dark') or light (modified template 'plotly')
        """

        style = theme_style[theme]
        title_rsi = f'{tk_rsi} Relative Strength Index (%)'

        fig_rsi = make_subplots(rows = 1, cols = 1)

        df_rsi_hlines = pd.DataFrame({'30': 30, '70': 70, '100': 100}, index=df_rsi.index)

        fig_rsi.add_trace(
            go.Scatter(
                x = df_rsi_hlines.index,
                y = df_rsi_hlines['30'],
                line = dict(color = style['rsi_30_linecolor']),
                line_width = 2,
                fill = 'tozeroy',
                fillcolor = style['rsi_30_fillcolor'],
                name = 'Oversold < 30%'
            )
        )
        fig_rsi.add_trace(
            go.Scatter(
                x = df_rsi_hlines.index,
                y = df_rsi_hlines['100'],
                line = dict(color='black'),
                line_width = 0,
                showlegend = False
            )
        )
        fig_rsi.add_trace(
            go.Scatter(
                x = df_rsi_hlines.index,
                y = df_rsi_hlines['70'],
                line = dict(color = style['rsi_70_linecolor']),
                line_width = 2,
                fill = 'tonexty',  # fill to previous scatter trace
                fillcolor = style['rsi_70_fillcolor'],
                name = 'Overbought > 70%'
            )
        )
        fig_rsi.add_trace(
            go.Scatter(
                x = df_rsi.index,
                y = df_rsi[tk_rsi],
                line = dict(color=style['basecolor']),
                line_width = 2,        
                name = 'RSI (%)'
            )
        )
        # Add plot border
        fig_rsi.add_shape(
            type = 'rect',
            xref = 'paper',
            yref = 'paper',
            x0 = 0,
            x1 = 1,
            y0 = 0,
            y1 = 1,
            line_color = style['x_linecolor'],
            line_width = 0.3
        )

        # Update layout and axes
        fig_rsi.update_layout(
            width = plot_width,
            height = plot_height,
            xaxis_rangeslider_visible = False,
            template = style['template'],
            yaxis_title = f'{tk_rsi} RSI (%)',
            title = dict(
                text = title_rsi,
                font_size = title_font_size,
                y = 0.95,
                x = 0.45,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        fig_rsi.update_xaxes(
            type = 'category',
            gridcolor = style['x_gridcolor'],
            nticks = n_ticks_max,
            tickangle = -90,
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10,  # not working
        )
        fig_rsi.update_yaxes(
            range = (0, 100),
            gridcolor = style['y_gridcolor'],
            nticks = n_yticks_max,
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10,  # not working
        )

        return fig_rsi


    ##### BOLLINGER BANDS #####

    def bollinger_bands(
        prices,
        window = 20,
        n_std = 2.0,
        n_bands = 1
    ):
        """
        prices:
            series of ticker prices ('adjusted close', 'open', 'high', 'low' or 'close')
        window:
            size of the rolling window in days, defaults to 20
        n_std:
            width of the upper and lower bands in standard deviations, defaults to 2.0
        n_bands:
            number of pairs of bands to be created, defaults to 1, max 3

        Returns a list of bollinger band dictionaries
        """

        eps = 1e-6

        n_bands = min(3, n_bands)

        df_sma = prices.rolling(window = window, min_periods = 1).mean()
        df_std = prices.rolling(window = window, min_periods = 1).std(ddof=0)

        bollinger_list = [{
            'data': df_sma,
            'name': f'SMA {window}',
            'idx_offset': 0,
            'showlegend': True
        }]

        k = 0
        # k = 0 if each band_width is an integer within the accuray of eps    
        for i in range(n_bands + 1)[1:]:
            band_width = i * n_std
            if abs(float(int(band_width)) - band_width) > eps:
                k = 1
                break

        for i in range(n_bands + 1)[1:]:
        
            band_width = i * n_std

            upper_band = df_sma + band_width * df_std
            upper_name = f'({window}, {band_width:.{k}f}) Upper Bollinger'
            bollinger_list.append({
                'data': upper_band,
                'name': upper_name,
                'idx_offset': i,
                'showlegend': True
            })

            lower_band = df_sma - band_width * df_std        
            lower_name = f'({window}, {band_width:.{k}f}) Lower Bollinger'
            bollinger_list.append({
                'data': lower_band,
                'name': lower_name,
                'idx_offset': -i,
                'showlegend': True
            })

        bollinger_list = sorted(bollinger_list, key = itemgetter('idx_offset'), reverse = True)

        return bollinger_list


    ##### MOVING AVERAGE ENVELOPES #####

    def ma_envelopes(
        self,
        prices,
        ma_type = None,
        window = 20,
        prc_offset = 5,
        n_bands = 3
    ):
        """
        prices:
            series of ticker prices ('adjusted close', 'open', 'high', 'low' or 'close')
        ma_type:
            one of 'sma', 'ema', dema', tema'
        window:
            size of the rolling window in days
        prc_offset: 
            vertical offset from base moving average in percentage points (-99% to 99%)
        n_bands:
            number of pairs of envelopes to be created, defaults to 3 (max)

        Returns a list of ma envelope dictionaries
        """

        eps = 1e-6

        if ma_type is None:
            ma_type = 'sma'

        n_bands = min(3, n_bands)
        if abs(prc_offset) > 99:
            prc_offset = math.sign(prc_offset) * 99

        base_ma = self.moving_average(prices, ma_type, window)

        base_name = f'{ma_type.upper()} {window}'

        ma_envelope_list = [{
            'data': base_ma,
            'name': base_name,
            'idx_offset': 0,
            'showlegend': True
        }]

        k = 0
        # k = 0 if each ma_offset is an integer within the accuray of eps
        for i in range(n_bands + 1)[1:]:
            ma_offset = i * prc_offset
            if abs(float(int(ma_offset)) - ma_offset) > eps:
                k = 1
                break

        for i in range(n_bands + 1)[1:]:
        
            ma_offset = i * prc_offset
            
            upper_band = base_ma * (1 + ma_offset / 100)
            upper_name = f'({window}, {ma_offset:.{k}f}%) Upper Envelope'
            ma_envelope_list.append({
                'data': upper_band,
                'name': upper_name,
                'idx_offset': i,
                'showlegend': True
            })

            lower_band = base_ma * (1 - ma_offset / 100)
            lower_name = f'({window}, {ma_offset:.{k}f}% Lower Envelope'
            ma_envelope_list.append({
                'data': lower_band,
                'name': lower_name,
                'idx_offset': -i,
                'showlegend': True
            })

        ma_envelope_list = sorted(ma_envelope_list, key = itemgetter('idx_offset'), reverse = True)

        return ma_envelope_list


    ##### ADD OVERLAY #####

    def add_overlay(
        self,
        fig_data,
        df,
        name,
        color_idx,
        showlegend = True,
        target_deck = 1,
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        fig_data: a dictionary of the underlying figure data

        y_min_fig: y_min on the existing fig
        y_max_fig: y_max on the existing fig
        color_idx: an integer (0, ...) indicating the color from those available in theme_style
        showlegend: whether or not to show line in legend (e.g. we only need one Bollinger band in legend)
        legendgroup: 'upper' is top graph in subplots (row 1), 'lower' is the stacked lower graph (row 2)

        Returns the updated fig_data dictionary
        """

        style = theme_style[theme]
        overlay_colors = style['overlay_color_theme'][color_theme]

        fig = fig_data['fig']
        y_min_fig = fig_data['y_min'][target_deck]
        y_max_fig = fig_data['y_max'][target_deck]
        deck_type = fig_data['deck_type']

        min_y = min(df)
        max_y = max(df)
        y_min, y_max = set_axis_limits(min_y, max_y)

        # ESSENTIALLY THERE SHOULD BE NO OVERLAYS ADDED TO AN EMPTY DECK so this may not be necessary
        try:
            new_y_min, new_y_max = set_axis_limits(min(y_min, y_min_fig), max(y_max, y_max_fig))
        except:
            # if the existing y_min and y_max are None
            new_y_min, new_y_max = y_min, y_max

        if target_deck > 1:
            new_y_max *= 0.999

        if color_idx >= len(overlay_colors):
            # Take the last overlay color from the available list
            color_idx = -1

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'bold'
            )

        fig.add_trace(
            go.Scatter(
                x = df.index.astype(str),
                y = df,
                line = dict(color = overlay_colors[color_idx]),
                name = name,
                showlegend = showlegend,
                legendgroup = f'{target_deck}',
                legendgrouptitle = legendgrouptitle
            ),
            row = target_deck, col = 1    
        )

        fig.update_yaxes(
            range = (new_y_min, new_y_max),
            showticklabels = True,
            ticks = 'outside',
            ticklen = 8,
            row = target_deck, col = 1
        )

        fig_data.update({'fig': fig})
        fig_data['y_min'].update({target_deck: new_y_min})
        fig_data['y_max'].update({target_deck: new_y_max})

        return fig_data


    ##### ADD MOVING AVERAGE OVERLAYS #####

    def add_ma_overlays(
        self,
        fig_data,
        df_price,
        ma_list,
        target_deck = 1,
        x_min = None,
        x_max = None,
        add_yaxis_title = False,
        yaxis_title = 'Moving Average',
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        df_price: 
            df_close or df_adj_close, depending on the underlying figure
        ma_list: 
            list of ma overlay dictionaries, containing
             - ma_idx ma index (1, 2,...)
             - ma_type: 'sma' (default), 'ema', 'dema', 'tema', 'wma' or 'wwma'
             - ma_window, in days
             - showlegend: include in plot legend or not
        """

        x_min = self.start_date if x_min is None else x_min
        x_max = self.end_date if x_max is None else x_max

        deck_type = fig_data['deck_type']

        n_ma = len(ma_list)

        style = theme_style[theme]
        overlay_color_idx = style['overlay_color_selection'][color_theme][n_ma]

        current_names = [trace['name'] for trace in fig_data['fig']['data'] if (trace['legendgroup'] == str(target_deck))]

        ma_overlays = []

        for i, ma in enumerate(ma_list):

            ma_type = ma['ma_type']
            ma_window = ma['ma_window']
            ma_name = f'{ma_type.upper()} {ma_window}'

            if ma_name not in current_names:  # MUST ALSO CHECK THE DECK

                ma_data = self.moving_average(
                    df_price[x_min: x_max],
                    ma_type,
                    ma_window
                )
                ma_color_idx = overlay_color_idx[i]
                ma_showlegend = ma['showlegend']

                ma_overlays.append({
                    'data': ma_data,
                    'name': ma_name,
                    'color_idx': ma_color_idx,
                    'showlegend': ma_showlegend
                })

        # color_map = fig_data['color_map']
        color_map = {}

        for overlay in ma_overlays:
            fig_data = self.add_overlay(
                fig_data,
                overlay['data'],
                overlay['name'],
                overlay['color_idx'],
                overlay['showlegend'],
                target_deck = target_deck,
                theme = theme,
                color_theme = color_theme
            )        
            color_map.update({overlay['name']: overlay['color_idx']})

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_data['fig'].update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        if add_yaxis_title:
            fig_data['fig'].update_yaxes(
                title = yaxis_title,
                row = target_deck, col = 1
            )

        fig_data.update({'color_map': color_map})

        return fig_data


    ##### ADD BOLLINGER OVERLAYS #####

    def add_bollinger_overlays(
        self,
        fig_data,
        bollinger_list,
        target_deck = 1,
        x_min = None,
        x_max = None,
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        df_price: df_close or df_adj_close, depending on the underlying figure in fig_data

        """

        x_min = self.start_date if x_min is None else x_min
        x_max = self.end_date if x_max is None else x_max

        deck_type = fig_data['deck_type']

        n_boll = int((len(bollinger_list) + 1) / 2)

        style = theme_style[theme]
        overlay_color_idx = style['overlay_color_selection'][color_theme][n_boll]

        current_names = [tr['name'] for tr in fig_data['fig']['data'] if (tr['legendgroup'] == str(target_deck))]

        bollinger_overlays = []

        for boll in bollinger_list:

            if boll['name'] not in current_names:
                bollinger_overlays.append({
                    'data': boll['data'][x_min: x_max],
                    'name': boll['name'],
                    'color_idx': overlay_color_idx[abs(boll['idx_offset'])],
                    'showlegend': boll['showlegend']
                })

        # color_map = fig_data['color_map']
        color_map = {}

        for overlay in bollinger_overlays:
            fig_data = self.add_overlay(
                fig_data,
                overlay['data'],
                overlay['name'],
                overlay['color_idx'],
                overlay['showlegend'],
                target_deck = target_deck,
                theme = theme,
                color_theme = color_theme
            )
            color_map.update({overlay['name']: overlay['color_idx']})

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_data['fig'].update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'color_map': color_map})

        return fig_data


    ##### ADD MOVING AVERAGE ENVELOPE OVERLAYS #####

    def add_ma_envelope_overlays(
        self,
        fig_data,
        ma_envelope_list,
        target_deck = 1,    
        x_min = None,
        x_max = None,
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        """

        x_min = self.start_date if x_min is None else x_min
        x_max = self.end_date if x_max is None else x_max

        deck_type = fig_data['deck_type']

        n_env = int((len(ma_envelope_list) + 1) / 2)

        style = theme_style[theme]
        overlay_color_idx = style['overlay_color_selection'][color_theme][n_env]

        current_names = [tr['name'] for tr in fig_data['fig']['data'] if (tr['legendgroup'] == str(target_deck))]

        ma_envelope_overlays = []

        for env in ma_envelope_list:

            if env['name'] not in current_names:
                ma_envelope_overlays.append({
                   'data': env['data'][x_min: x_max],
                   'name': env['name'],
                   'color_idx': overlay_color_idx[abs(env['idx_offset'])],
                   'showlegend': env['showlegend']
                })

        color_map = {}

        for overlay in ma_envelope_overlays:
            fig_data = self.add_overlay(
                fig_data,
                overlay['data'],
                overlay['name'],
                overlay['color_idx'],
                overlay['showlegend'],
                target_deck = target_deck,
                theme = theme,
                color_theme = color_theme
            )
            color_map.update({overlay['name']: overlay['color_idx']})

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_data['fig'].update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'color_map': color_map})

        return fig_data


    ##### UPDATE OVERLAY COLOR THEME #####

    def update_color_theme(
        self,
        fig,
        color_map,
        theme,
        color_theme,
        invert = False
    ):
        """
        fig = fig_data['fig']
        color_map = fig_data['color_map']: an overlay color map dictionary
        theme: existing theme ('dark' or light')
        color_theme: new color theme to apply to overlays in fig
        invert: invert the palette from lightest-darkest to darkest-lightest or vice versa?
        Returns updated fig
        """

        style = theme_style[theme]
        overlay_colors = style['overlay_color_theme'][color_theme]

        for name, color_idx in color_map.items():

            if invert:
                color_idx = len(color_map) - color_idx - 1

            fig.update_traces(
                line_color = overlay_colors[color_idx],
                selector = dict(name = name)
            )

        return fig


    ##### ADD HISTORICAL PRICE/VOLUME #####

    def add_hist_price(
        self,
        fig_data,
        df_price,
        tk,
        target_deck = 1,
        secondary_y = False,
        plot_type = 'scatter',
        n_yticks_max = None,
        price_type = 'adjusted close',
        add_title = True,
        title = None,
        title_font_size = 32,
        theme = 'dark',
        color_theme = None,
        fill_below = False
    ):
        """
        fig_data:
            template to add the plot to
        target_deck:
            1 (upper), 2 (second from top), 3 (third from top)
        plot_type:
            'scatter' or 'bar'
        price_type:
            one of 'adjusted close', 'close', 'open', 'high', 'low', 'volume', 'dollar volume'

        """

        if isinstance(df_price, pd.Series):
            df_tk = df_price.copy()
        elif isinstance(df_price, pd.DataFrame):
            df_tk = df_price[tk]
        else:
            print('Incorrect format of input data')
            exit

        legend_name = price_type.title()
        yaxis_title = price_type.title()
        if add_title & (title is None):
            title = f'{tk} {price_type.title()}'

        fig = fig_data['fig']
        fig_y_min = fig_data['y_min'][target_deck]
        fig_y_max = fig_data['y_max'][target_deck]
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']

        if n_yticks_max is None:
            deck_height = fig_data['plot_height'][target_deck]
            n_yticks_max = n_yticks_map[deck_height]

        style = theme_style[theme]

        if color_theme is None:
            linecolor = style['basecolor']
        else:
            color_idx = style['overlay_color_selection'][color_theme][1][0]
            linecolor = style['overlay_color_theme'][color_theme][color_idx]

        # Must be specified as RGBA
        if plot_type == 'bar':
            opacity = 0.9
        else:
            opacity = 0.6

        fillcolor = linecolor.replace(', 1)', f', {opacity})')

        # print(linecolor, fillcolor)

        if fill_below:
            fill = 'tozeroy'
        else:
            fill = 'none'

        min_y = min(df_tk)
        max_y = max(df_tk)
        y_min, y_max = set_axis_limits(min_y, max_y)

        if fig_y_min is not None:
            y_min = min(fig_y_min, y_min)
        if fig_y_max is not None:
            y_max = max(fig_y_max, y_max)

        if target_deck > 1:
            y_max *= 0.999

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'bold'
            )

        # Add trace
        if plot_type == 'bar':
            fig.add_trace(
                go.Bar(
                    x = df_tk.index.astype(str),
                    y = df_tk,
                    marker_color = fillcolor,
                    width = 1,
                    name = legend_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    showlegend = True
                ),
                row = target_deck, col = 1
            )

        else:
            fig.add_trace(
                go.Scatter(
                    x = df_tk.index.astype(str),
                    y = df_tk,
                    line_color = linecolor,
                    fill = fill,
                    fillcolor = fillcolor,
                    showlegend = True,
                    name = legend_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle
                ),
                row = target_deck, col = 1,
                secondary_y = secondary_y
            )

        # Update layout and axes
        if add_title:
            fig.update_layout(
                title = dict(
                    text = title,
                    font_size = title_font_size,
                    y = title_y_pos,
                    x = title_x_pos,
                    xanchor = 'center',
                    yanchor = 'middle'
                )
            )

        y_range = None if secondary_y else (y_min, y_max)
        fig.update_yaxes(
            range = y_range,
            title = yaxis_title,
            showticklabels = True,
            nticks = n_yticks_max,
            secondary_y = secondary_y,
            showgrid = not secondary_y,
            row = target_deck, col = 1
        )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'fig': fig})
        fig_data['y_min'].update({target_deck: y_min})
        fig_data['y_max'].update({target_deck: y_max})

        return fig_data


    ##### PLOT HISTORICAL PLOTLY #####

    def plot_hist_plotly(
        self,
        df_price,
        tk,
        n_ticks_max = 48,
        n_yticks_max = 16,
        plot_width = 1450,
        plot_height = 750,
        title_font_size = 32,
        theme = 'dark',
        price_type = 'adjusted close'
    ):
        """
        price_type: one of ['adjusted close', 'close', 'open', 'high', 'low']

        """

        if isinstance(df_price, pd.Series):
            df_tk = df_price.copy()
        elif isinstance(df_price, pd.DataFrame):
            df_tk = df_price[tk]
        else:
            print('Incorrect format of input data')
            exit

        style = theme_style[theme]

        min_y = min(df_tk)
        max_y = max(df_tk)
        y_min, y_max = set_axis_limits(min_y, max_y)

        fig = make_subplots(rows = 1, cols = 1)

        fig.add_trace(
            go.Scatter(
                x = df_tk.index.astype(str),
                y = df_tk,
                line = dict(color = style['basecolor']),
                showlegend = True,
                legendgroup = 'upper',
                name = price_type.title()
            )
        )
        # Add plot border
        fig.add_shape(
            type = 'rect',
            xref = 'paper',
            yref = 'paper',
            x0 = 0,
            x1 = 1,
            y0 = 0,
            y1 = 1,
            line_color = style['x_linecolor'],
            line_width = 0.3
        )
        # Update layout and axes
        fig.update_layout(
            width = plot_width,
            height = plot_height,
            xaxis_rangeslider_visible = False,
            template = style['template'],
            legend_groupclick = 'toggleitem',            
            yaxis_title = f'{price_type.title()}',
            title = dict(
                text = f'{tk} {price_type.title()}',
                font_size = title_font_size,
                y = 0.95,
                x = 0.45,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        fig.update_xaxes(
            type = 'category',
            gridcolor = style['x_gridcolor'],        
            nticks = n_ticks_max,
            tickangle = -90,
            ticks = 'outside',
            ticklen = 8
        )
        fig.update_yaxes(
            range = (y_min, y_max),
            gridcolor = style['y_gridcolor'],
            nticks = n_yticks_max,            
            ticks = 'outside',
            ticklen = 8
        )

        fig_data = {
            'fig': fig,
            'y_min': y_min,
            'y_max': y_max
        }

        return fig_data


    ##### ADD CANDLESTICK #####

    def add_candlestick(
        self,
        fig_data,
        df_ohlc,
        tk,
        candle_type = 'hollow',
        target_deck = 1,
        n_yticks_max = None,
        add_title = True,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        candle_type: 'hollow' or 'traditional'

        """

        style = theme_style[theme]

        # Colors must be in the RGBA format
        red_color = style['red_color']
        green_color = style['green_color']
        red_fill_color = red_color
        green_fill_color = green_color
        red_fill_color_hollow = red_color.replace(', 1)', ', 0.2)')
        green_fill_color_hollow = green_color.replace(', 1)', ', 0.2)')

        df = df_ohlc.copy()

        min_y = min(df['Low'])
        max_y = max(df['High'])
        y_min, y_max = set_axis_limits(min_y, max_y)

        if target_deck > 1:
            y_max *= 0.999

        df['Date'] = df.index.astype(str)

        fig = fig_data['fig']
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']

        if n_yticks_max is None:
            deck_height = fig_data['plot_height'][target_deck]
            n_yticks_max = n_yticks_map[deck_height]
            print(deck_height)
            print(n_yticks_max)

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'bold'
            )

        if candle_type == 'traditional':

            if add_title:
                title = f'{tk} Prices - Traditional Candles'

            shown_green = False
            shown_red = False

            for _, row in df.iterrows():

                if row['Close'] >= row['Open']:
                    color_dict = dict(
                        fillcolor = green_fill_color,
                        line = dict(color = green_color)
                    )
                    name = 'Close > Open'
                    current_candle = 'green'
                else:
                    color_dict = dict(
                        fillcolor = red_fill_color,
                        line = dict(color = red_color)
                    )
                    name = 'Open > Close'
                    current_candle = 'red'

                # Make sure each candle type appears only once in the legend
                if (not shown_green) & (current_candle == 'green'):
                    showlegend = True
                    shown_green = True
                elif (not shown_red) & (current_candle == 'red'):
                    showlegend = True
                    shown_red = True
                else:
                    showlegend = False

                fig.add_trace(
                    go.Candlestick(
                        x = [row['Date']],
                        open = [row['Open']],
                        high = [row['High']],
                        low = [row['Low']],
                        close = [row['Close']],
                        name = name,
                        increasing = color_dict,
                        decreasing = color_dict,
                        showlegend = showlegend,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle
                    ),
                    row = target_deck, col = 1
                )

        else:  # candle_type == 'hollow'

            if add_title:
                title = f'{tk} Prices - Hollow Candles'

            df['previousClose'] = df['Close'].shift(1)

            # Define color based on close and previous close
            df['color'] = np.where(df['Close'] > df['previousClose'], green_color, red_color)

            df['fill'] = np.where(
                df['color'] == green_color,
                np.where(df['Close'] > df['Open'], green_fill_color_hollow, green_color),
                np.where(df['Close'] > df['Open'], red_fill_color_hollow, red_color)
            )

            shown_red_fill = False
            shown_red_hollow = False
            shown_green_fill = False
            shown_green_hollow = False

            for _, row in df.iterrows():

                if (row['color'] == green_color) & (row['fill'] == green_color):
                    name = 'Open > Close > Prev Close'
                    current_candle = 'green_fill'
                elif (row['color'] == green_color) & (row['fill'] == green_fill_color_hollow):
                    name = 'Prev Close < Close > Open'
                    current_candle = 'green_hollow'
                elif (row['color'] == red_color) & (row['fill'] == red_color):
                    name = 'Open > Close < Prev Close'
                    current_candle = 'red_fill'
                elif (row['color'] == red_color) & (row['fill'] == red_fill_color_hollow):
                    name = 'Prev Close > Close > Open'
                    current_candle = 'red_hollow'
                else:
                    name = 'Hollow Candles'


                # Make sure each candle type appears only once in the legend
                if (not shown_green_fill) & (current_candle == 'green_fill'):
                    showlegend = True
                    shown_green_fill = True
                elif (not shown_green_hollow) & (current_candle == 'green_hollow'):
                    showlegend = True
                    shown_green_hollow = True
                elif (not shown_red_fill) & (current_candle == 'red_fill'):
                    showlegend = True
                    shown_red_fill = True
                elif (not shown_red_hollow) & (current_candle == 'red_hollow'):
                    showlegend = True
                    shown_red_hollow = True
                else:
                    showlegend = False

                color_dict = dict(
                    fillcolor = row['fill'],
                    line=dict(color = row['color'])
                )

                fig.add_trace(
                    go.Candlestick(
                        x = [row['Date']],
                        open = [row['Open']],
                        high = [row['High']],
                        low = [row['Low']],
                        close = [row['Close']],
                        name = name,                    
                        increasing = color_dict,
                        decreasing = color_dict,
                        showlegend = showlegend,
                        legendgroup = f'{target_deck}',
                        legendgrouptitle = legendgrouptitle
                    ),
                    row = target_deck, col = 1
                )

        # Update layout and axes
        if add_title:
            fig.update_layout(
                title = dict(
                    text = title,
                    font_size = title_font_size,
                    y = title_y_pos,
                    x = title_x_pos,
                    xanchor = 'center',
                    yanchor = 'middle'
                )
            )
        fig.update_xaxes(
            rangeslider_visible=False
        )
        fig.update_yaxes(
            range = (y_min, y_max),
            title = f'Price',
            nticks = n_yticks_max,        
            showticklabels = True,
            row = target_deck, col = 1
        )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        print(f'Candlestick legend_tracegroupgap = {legend_tracegroupgap}')

        fig_data.update({'fig': fig})
        fig_data['y_min'].update({target_deck: y_min})
        fig_data['y_max'].update({target_deck: y_max})

        return fig_data


    ##### PLOT CANDLESTICK PLOTLY #####

    def plot_candlestick_plotly(
        self,
        df_ohlc,
        tk,
        candle_type = 'hollow',
        n_ticks_max = 48,
        n_yticks_max = 16,
        plot_width = 1450,
        plot_height = 750,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        candle_type: 'hollow' or 'traditional'

        """

        style = theme_style[theme]
        red_color = style['red_color']
        green_color = style['green_color']

        df = df_ohlc.copy()

        min_y = min(df['Low'])
        max_y = max(df['High'])
        y_min, y_max = set_axis_limits(min_y, max_y)

        df['Date'] = df.index.astype(str)
        x_min = df['Date'].min()
        x_max = df['Date'].max()

        fig = make_subplots(rows = 1, cols = 1)

        if candle_type == 'traditional':

            title = f'{tk} Prices - Traditional Candles'

            shown_green = False
            shown_red = False

            for idx, row in df.iterrows():

                if row['Close'] >= row['Open']:
                    color_dict = dict(
                        fillcolor = 'rgba(0, 255, 0, 0.3)',
                        line = dict(color = green_color)
                    )
                    name = 'Close > Open'
                    current_candle = 'green'
                else:
                    color_dict = dict(
                        fillcolor = 'rgba(255, 0, 0, 0.6)',
                        line = dict(color = red_color)
                    )
                    name = 'Open > Close'
                    current_candle = 'red'

                # Make sure each candle type appears only once in the legend
                if (not shown_green) & (current_candle == 'green'):
                    showlegend = True
                    shown_green = True
                elif (not shown_red) & (current_candle == 'red'):
                    showlegend = True
                    shown_red = True
                else:
                    showlegend = False

                fig.add_trace(
                    go.Candlestick(
                        x = [row['Date']],
                        open = [row['Open']],
                        high = [row['High']],
                        low = [row['Low']],
                        close = [row['Close']],
                        name = name,
                        increasing = color_dict,
                        decreasing = color_dict,
                        showlegend = showlegend,
                        legendgroup = 'upper'
                    )
                )

        else:  # candle_type == 'hollow'

            title = f'{tk} Prices - Hollow Candles'

            df['previousClose'] = df['Close'].shift(1)

            # Define color based on close and previous close
            df['color'] = np.where(df['Close'] > df['previousClose'], green_color, red_color)

            # Set fill to transparent if close > open and the previously defined color otherwise
            df['fill'] = np.where(df['Close'] > df['Open'], 'rgba(255, 0, 0, 0)', df['color'])

            shown_red_fill = False
            shown_red_hollow = False
            shown_green_fill = False
            shown_green_hollow = False

            for _, row in df.iterrows():

                if (row['color'] == green_color) & (row['fill'] == green_color):
                    name = 'Open > Close > Prev Close'
                    current_candle = 'green_fill'
                elif (row['color'] == green_color) & (row['fill'] == 'rgba(255, 0, 0, 0)'):
                    name = 'Prev Close < Close > Open'
                    current_candle = 'green_hollow'
                elif (row['color'] == red_color) & (row['fill'] == red_color):
                    name = 'Open > Close < Prev Close'
                    current_candle = 'red_fill'
                elif (row['color'] == red_color) & (row['fill'] == 'rgba(255, 0, 0, 0)'):
                    name = 'Prev Close > Close > Open'
                    current_candle = 'red_hollow'
                else:
                    name = 'Hollow Candles'

                # Make sure each candle type appears only once in the legend
                if (not shown_green_fill) & (current_candle == 'green_fill'):
                    showlegend = True
                    shown_green_fill = True
                elif (not shown_green_hollow) & (current_candle == 'green_hollow'):
                    showlegend = True
                    shown_green_hollow = True
                elif (not shown_red_fill) & (current_candle == 'red_fill'):
                    showlegend = True
                    shown_red_fill = True
                elif (not shown_red_hollow) & (current_candle == 'red_hollow'):
                    showlegend = True
                    shown_red_hollow = True
                else:
                    showlegend = False

                color_dict = dict(
                    fillcolor = row['fill'],
                    line=dict(color = row['color'])
                )

                fig.add_trace(
                    go.Candlestick(
                        x = [row['Date']],
                        open = [row['Open']],
                        high = [row['High']],
                        low = [row['Low']],
                        close = [row['Close']],
                        increasing = color_dict,
                        decreasing = color_dict,
                        showlegend = showlegend,
                        legendgroup = 'upper',
                        name = name
                    )
                )

        # Add plot border
        fig.add_shape(
            type = 'rect',
            xref = 'x',  # use 'x' to avoid double lines at x_min and x_max
            yref = 'paper',
            x0 = x_min,
            x1 = x_max,
            y0 = 0,
            y1 = 1,
            line_color = style['x_linecolor'],
            line_width = 0.3
        )
        # Update layout and axes
        fig.update_layout(
            width = plot_width,
            height = plot_height,
            xaxis_rangeslider_visible = False,
            template = style['template'],
            legend_groupclick = 'toggleitem',
            yaxis_title = f'Price',
            title = dict(
                text = title,
                font_size = title_font_size,
                y = 0.95,
                x = 0.45,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        fig.update_xaxes(
            type = 'category',
            gridcolor = style['x_gridcolor'],
            nticks = n_ticks_max,
            tickangle = -90,
            ticks = 'outside',
            ticklen = 8
        )
        fig.update_yaxes(
            range = (y_min, y_max),
            gridcolor = style['y_gridcolor'],
            nticks = n_yticks_max,
            ticks = 'outside',
            ticklen = 8
        )

        candles_data = {
            'fig': fig,
            'y_min': y_min,
            'y_max': y_max
        }

        return candles_data


    ##### ADD PRICE OVERLAY PLOTLY #####

    def add_price_overlays(
        self,
        fig_data,
        price_list,
        x_min = None,
        x_max = None,
        target_deck = 1,
        add_yaxis_title = False,
        yaxis_title = 'Price',
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        fig_data:
            A dictionary containing the underlying figure data
        price_list: 
            list of dictionaries with keys
             - 'name': 'Adjusted Close', 'Close', 'Open', 'High', 'Low', 'Average True Rate', etc.
             - 'show': True / False - include in plot or not
        x_min, x_max:
            minimum and maximum dates in the datetime format
        """

        x_min = self.start_date if x_min is None else x_min
        x_max = self.end_date if x_max is None else x_max

        deck_type = fig_data['deck_type']

        # Count lines that will be overlaid ('show' is True)

        selected_prices = [x for x in price_list if x['show']]
        n_price = len(selected_prices)

        style = theme_style[theme]
        overlay_color_idx = style['overlay_color_selection'][color_theme][n_price]

        current_names = [trace['name'] for trace in fig_data['fig']['data'] if (trace['legendgroup'] == str(target_deck))]

        price_overlays = []

        for i, price in enumerate(selected_prices):

            price_name = price['name']

            if price_name not in current_names:

                price_data = price['data']  # [x_min: x_max]
                color_idx = overlay_color_idx[i]

                price_overlays.append({
                    'data': price_data,
                    'name': price_name,
                    'color_idx': color_idx
                })

        color_map = {}

        for overlay in price_overlays:
            fig_data = self.add_overlay(
                fig_data,
                overlay['data'],
                overlay['name'],
                overlay['color_idx'],
                target_deck = target_deck,
                theme = theme,
                color_theme = color_theme
            )        
            color_map.update({overlay['name']: overlay['color_idx']})

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_data['fig'].update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        if add_yaxis_title:
            fig_data['fig'].update_yaxes(
                title = yaxis_title,
                row = target_deck, col = 1
            )

        fig_data.update({'color_map': color_map})

        return fig_data


    ##### ADD OSCILLATOR (DIFFERENTIAL) PLOT #####

    def add_diff(
        self,
        fig_data,
        tk,
        diff_data,
        price_type_map,
        stochastic_data = None,
        target_deck = 2,
        reverse_diff = False,
        plot_type = 'filled_line',
        add_signal = True,
        n_yticks_max = None,
        add_yaxis_title = True,
        add_title = False,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        price_type_map = {
            'Adj Close': adj_close_tk,
            'Adjusted Close': adj_close_tk,
            'Close': close_tk,
            'Open': open_tk,
            'High': high_tk,
            'Low': low_tk
        }
        reverse_diff:
            if True, the (p2 - p1) difference will be used instead of (p1 - p2)
        add_signal:
            if True, a signal will be added that is a moving average of the calculated difference
        """

        base = diff_data['p_base']
        p_base_name = base.title()
        p_base = price_type_map[p_base_name]

        p1_type = diff_data['p1_type']
        p2_type = diff_data['p2_type']
        p1_window = diff_data['p1_window']
        p2_window = diff_data['p2_window']
        signal_type = diff_data['signal_type']
        signal_window = diff_data['signal_window']

        fig_diff = fig_data['fig']
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'bold'
            )

        if n_yticks_max is None:
            deck_height = fig_data['plot_height'][target_deck]
            n_yticks_max = n_yticks_map[deck_height]

        style = theme_style[theme]

        price_types = ['adjusted close', 'adj close', 'close', 'open', 'high', 'low']
        ma_types = ['sma', 'ema', 'dema', 'tema', 'wma', 'wwma']
        stochastic_types = ['k-line', 'k_line', 'kline', 'd-line', 'd_line', 'dline']

        if p1_type in price_types:
            p1_name = 'Adjusted Close' if p1_name == 'adj close' else p1_type.title()
            yaxis_title = 'Price Oscillator'
            try:
                p1 = price_type_map[p1_name]
            except:
                p1 = price_type_map['Adj Close']

        elif p1_type in ma_types:
            p1 = self.moving_average(p_base, p1_type, p1_window)
            p1_name = f'{p1_type.upper()} {p1_window}'
            yaxis_title = 'MA Oscillator'

        elif p1_type in stochastic_types:
            
            # NEEDS FIXING - LIKELY SPLIT THE STOCHASTIC CASE INTO A SEPARATE FUNCTION
            if stochastic_data is None:
                stochastic_data = self.stochastic_oscillator()
            else:
                stochastic_data = stochastic_data
        
            stochastic_type = stochastic_data['type']
            stochastic_label = stochastic_data['label']
            p1 = stochastic_data['k_line']
            p2 = stochastic_data['d_line']
            if p1_type.lower().startswith('k'):
                p1_name = '%K Line'
                p2_name = '%D Line'
                yaxis_title = f'Stochastic %K-%D'    
            else:
                p1_name = '%D Line'
                p2_name = '%K Line'
                yaxis_title = f'Stochastic %D-%K'

        #####

        if p2_type in price_types:
            p2_name = 'Adjusted Close' if p2_name == 'adj close' else p2_type.title()
            try:
                p2 = price_type_map[p2_name]
            except:
                p2 = price_type_map['Adj Close']

        elif p2_type in ma_types:
            p2 = self.moving_average(p_base, p2_type, p2_window)
            p2_name = f'{p2_type.upper()} {p2_window}'

        if p1_type in stochastic_types:
            if p1_name == '%K Line':
                diff = p1 - p2
                diff_title = f'{stochastic_type} {stochastic_label} %K-%D Line Oscillator'
                diff_positive_name = f'{p1_name} > {p2_name}'
                diff_negative_name = f'{p1_name} < {p2_name}'
            else:
                diff = p2 - p1
                diff_title = f'{stochastic_type} {stochastic_label} %D-%K Line Oscillator'
                diff_positive_name = f'{p2_name} > {p1_name}'
                diff_negative_name = f'{p2_name} < {p1_name}'

        else:
            if not reverse_diff:
                diff = p1 - p2
                diff_title = f'{tk} {p_base_name} {p1_name} - {p2_name} Oscillator'
                diff_positive_name = f'{stochastic_type} {stochastic_label} {p1_name} > {p2_name}'
                diff_negative_name = f'{stochastic_type} {stochastic_label} {p1_name} < {p2_name}'
            else:
                diff = p2 - p1
                diff_title = f'{tk} {p_base_name} {p2_name} - {p1_name} Oscillator'
                diff_positive_name = f'{p2_name} > {p1_name}'
                diff_negative_name = f'{p2_name} < {p1_name}'

        diff_signal = self.moving_average(diff, signal_type, signal_window)
        signal_name = f'{signal_type.upper()} {signal_window} Signal'

        min_diff = min(diff)
        max_diff = max(diff)

        y_diff_min, y_diff_max = set_axis_limits(min_diff, max_diff)
        if target_deck > 1:
            y_diff_max *= 0.999 

        diff_positive = diff.copy()
        diff_negative = diff.copy()

        if plot_type == 'bar':

            diff_positive.iloc[np.where(diff_positive < 0)] = np.nan
            diff_negative.iloc[np.where(diff_negative >= 0)] = np.nan

            fig_diff.add_trace(
                go.Bar(
                    x = diff_positive.index.astype(str),
                    y = diff_positive,
                    marker_color = style['green_color'],
                    width = 1,
                    name = diff_positive_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    showlegend = True
                ),
                row = target_deck, col = 1
            )
            fig_diff.add_trace(
                go.Bar(
                    x = diff_negative.index.astype(str),
                    y = diff_negative,
                    marker_color = style['red_color'],
                    width = 1,
                    name = diff_negative_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    showlegend = True
                ),
                row = target_deck, col = 1
            )

        else:
            # 'filled_line' or 'scatter'

            prev_v = diff.iloc[0]
            diff_positive.iloc[0] = prev_v if prev_v >= 0 else np.nan
            diff_negative.iloc[0] = prev_v if prev_v < 0 else np.nan

            for idx in diff.index[1:]:

                curr_v = diff.loc[idx]

                if np.sign(curr_v) != np.sign(prev_v):
                    # Set both diff copies to 0 if the value is changing sign
                    diff_positive[idx] = 0
                    diff_negative[idx] = 0
                else:
                    # Set both diff copies to current value or NaN
                    diff_positive[idx] = curr_v if curr_v >= 0 else np.nan
                    diff_negative[idx] = curr_v if curr_v < 0 else np.nan

                prev_v = curr_v

            fig_diff.add_trace(
                go.Scatter(
                    x = diff_positive.index.astype(str),
                    y = diff_positive,
                    line_color = style['diff_green_linecolor'],
                    line_width = 2,
                    fill = 'tozeroy',
                    fillcolor = style['diff_green_fillcolor'],
                    name = diff_positive_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    showlegend = True
                ),
                row = target_deck, col = 1
            )
            fig_diff.add_trace(
                go.Scatter(
                    x = diff_negative.index.astype(str),
                    y = diff_negative,
                    line_color = 'darkred',
                    line_width = 2,
                    fill = 'tozeroy',
                    fillcolor = style['diff_red_fillcolor'],
                    name = diff_negative_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    showlegend = True
                ),
                row = target_deck, col = 1
            )

        if add_signal:
            fig_diff.add_trace(
                go.Scatter(
                    x = diff_signal.index.astype(str),
                    y = diff_signal,
                    line_color = style['signal_color'],
                    line_width = 2,
                    name = signal_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle,
                    showlegend = True
                ),
                row = target_deck, col = 1
            )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_data['fig'].update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        # Update layout and axes

        if add_title & (target_deck == 1):

            fig_diff.update_layout(
                title = dict(
                    text = diff_title,
                    font_size = title_font_size,
                    y = title_y_pos,
                    x = title_x_pos,
                    xanchor = 'center',
                    yanchor = 'middle'
                )
            )

        fig_diff.update_yaxes(
            range = (y_diff_min, y_diff_max),
            showticklabels = True,
            nticks = n_yticks_max,
            row = target_deck, col = 1
        )

        if add_yaxis_title:
            fig_data['fig'].update_yaxes(
                title = yaxis_title,
                row = target_deck, col = 1
            )

        fig_data.update({'fig': fig_diff})
        fig_data['y_min'].update({target_deck: y_diff_min})
        fig_data['y_max'].update({target_deck: y_diff_max})

        return fig_data


    ##### PLOT DIFFERENTIAL PLOTLY #####

    def plot_diff_plotly(
        self,
        tk,
        diff_data,
        price_type_map,
        reverse_diff = False,
        add_signal = True,
        n_ticks_max = 48,
        n_yticks_max = 16,
        plot_width = 1450,
        plot_height = 750,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        price_type_map = {
            'Adj Close': adj_close_tk,
            'Adjusted Close': adj_close_tk,
            'Close': close_tk,
            'Open': open_tk,
            'High': high_tk,
            'Low': low_tk
        }
        reverse_diff:
            if True, the (p2 - p1) difference will be used instead of (p1 - p2)
        add_signal:
            if True, a signal will be added that is a moving average of the calculated difference
        """

        base = diff_data['p_base']
        p_base_name = base.title()
        p_base = price_type_map[p_base_name]

        p1_type = diff_data['p1_type']
        p2_type = diff_data['p2_type']
        p1_window = diff_data['p1_window']
        p2_window = diff_data['p2_window']
        signal_type = diff_data['signal_type']
        signal_window = diff_data['signal_window']

        price_types = ['adjusted close', 'adj close', 'close', 'open', 'high', 'low']
        ma_types = ['sma', 'ema', 'dema', 'tema', 'wma']

        if p1_type in price_types:
            p1_name = 'Adjusted Close' if p1_name == 'adj close' else p1_type.title()
            try:
                p1 = price_type_map[p1_name]
            except:
                p1 = price_type_map['Adj Close']
        elif p1_type in ma_types:
            p1 = self.moving_average(p_base, p1_type, p1_window)
            p1_name = f'{p1_type.upper()} {p1_window}'

        if p2_type in price_types:
            p2_name = 'Adjusted Close' if p2_name == 'adj close' else p2_type.title()
            try:
                p2 = price_type_map[p2_name]
            except:
                p2 = price_type_map['Adj Close']
        elif p2_type in ma_types:
            p2 = self.moving_average(p_base, p2_type, p2_window)
            p2_name = f'{p2_type.upper()} {p2_window}'

        if not reverse_diff:
            diff = p1 - p2
            diff_title = f'{tk} {p_base_name} {p1_name} - {p2_name} Differential'
            diff_positive_name = f'{p1_name} > {p2_name}'
            diff_negative_name = f'{p1_name} < {p2_name}'
        else:
            diff = p2 - p1
            diff_title = f'{tk} {p_base_name} {p2_name} - {p1_name} Differential'
            diff_positive_name = f'{p2_name} > {p1_name}'
        diff_negative_name = f'{p2_name} < {p1_name}'

        diff_signal = self.moving_average(diff, signal_type, signal_window)
        signal_name = f'Diff {signal_type.upper()} {signal_window} Signal'

        x_min = str(diff.index.min().date())
        x_max = str(diff.index.max().date())
    
        min_diff = min(diff)
        max_diff = max(diff)

        y_diff_min, y_diff_max = set_axis_limits(min_diff, max_diff)

        diff_positive = diff.copy()
        diff_negative = diff.copy()

        prev_v = diff.iloc[0]
        diff_positive.iloc[0] = prev_v if prev_v >= 0 else np.nan
        diff_negative.iloc[0] = prev_v if prev_v < 0 else np.nan

        for idx in diff.index[1:]:

            curr_v = diff.loc[idx]

            if np.sign(curr_v) != np.sign(prev_v):
                # Set both diff copies to 0 if the value is changing sign
                diff_positive[idx] = 0
                diff_negative[idx] = 0
            else:
                # Set both diff copies to current value or NaN
                diff_positive[idx] = curr_v if curr_v >= 0 else np.nan
                diff_negative[idx] = curr_v if curr_v < 0 else np.nan

            prev_v = curr_v

        style = theme_style[theme]

        fig_diff = make_subplots(rows = 1, cols = 1)

        fig_diff.add_trace(
            go.Scatter(
                x = diff_positive.index.astype(str),
                y = diff_positive,
                line_color = style['diff_green_linecolor'],
                line_width = 2,
                fill = 'tozeroy',
                fillcolor = style['diff_green_fillcolor'],
                name = diff_positive_name
            )
        )
        fig_diff.add_trace(
            go.Scatter(
                x = diff_negative.index.astype(str),
                y = diff_negative,
                line_color = 'darkred',
                line_width = 2,
                fill = 'tozeroy',
                fillcolor = style['diff_red_fillcolor'],
                name = diff_negative_name
            )
        )
        if add_signal:
            fig_diff.add_trace(
                go.Scatter(
                    x = diff_signal.index.astype(str),
                    y = diff_signal,
                    line_color = style['signal_color'],
                    line_width = 2,
                    name = signal_name
                )
            )

        # Add plot border
        fig_diff.add_shape(
            type = 'rect',
            xref = 'x',  # use 'x' because of seconday axis - 'paper' does not work correctly
            yref = 'paper',
            x0 = x_min,
            x1 = x_max,
            y0 = 0,
            y1 = 1,
            line_color = style['x_linecolor'],
            line_width = 0.3
        )
        # Update layout and axes
        fig_diff.update_layout(
            width = plot_width,
            height = plot_height,
            xaxis_rangeslider_visible = False,
            template = style['template'],
            title = dict(
                text = diff_title,
                font_size = title_font_size,
                y = 0.95,
                x = 0.45,
                xanchor = 'center',
                yanchor = 'top'
            )
        )
        fig_diff.update_yaxes(
            title_text = f'{p_base_name} Differential',
            range = (y_diff_min, y_diff_max),
            secondary_y = False,
            nticks = n_yticks_max,
            gridcolor = style['x_gridcolor'],
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10,  # not working
        )
        fig_diff.update_xaxes(
            type = 'category',
            nticks = n_ticks_max,
            tickangle = -90,
            gridcolor = style['y_gridcolor'],
            ticks = 'outside',
            ticklen = 8,
            ticklabelshift = 5,  # not working
            ticklabelstandoff = 10,  # not working
            showgrid = True
        )

        return fig_diff


    ##### PLOT HISTORICAL MATPLOTLIB #####

    def plot_hist_matplotlib(
        self,
        tk,
        df,
        start_date,
        end_date,
        title=None,
        y_min=None,
        y_max=None,
        y_tick_spacing=None,
        add_xlabel=False,
        plot_type='line',
        color=None,
        fill=False,
        x_dim=12,
        y_dim=8,
        grid='both'
    ):
        """
        Create a plot of a historical profile
        tk: ticker profile to be plotted
        df: dataframe containing data for ticker tk
        """

        if isinstance(df, pd.Series):
            df_tk = df.copy()
        elif isinstance(df, pd.DataFrame):
            df_tk = df[tk]
        else:
            print('df must a a series or a dataframe')
            exit

        if title is None:
            title = tk
        if color is None:
            color = 'tab:blue'  # same as '#1f77b4'

        # Set x-axis limits
        if isinstance(start_date, datetime):
            x_min = str(start_date.date())
        elif isinstance(start_date, date):
            x_min = str(start_date)
        elif isinstance(start_date, str):
            x_min = start_date
        else:
            print('Incorrect format of start_date')
            exit

        if isinstance(end_date, datetime):
            x_max = str(end_date.date())
        elif isinstance(end_date, date):
            x_max = str(end_date)
        elif isinstance(end_date, str):
            x_max = end_date
        else:
            print('Incorrect format of end_date')
            exit

        if x_min not in df_tk.index:
            while x_min not in df_tk.index:
                new_start_date = datetime.strptime(x_min, '%Y-%m-%d') + timedelta(1)
                x_min = str(new_start_date.date())

        if x_max not in df_tk.index:
            while x_max not in df_tk.index:
                new_end_date = datetime.strptime(x_max, '%Y-%m-%d') - timedelta(1)
                x_max = str(new_end_date.date())

        print(f'x_min = {x_min} (type {type(x_min)}), x_max = {x_max} (type {type(x_max)})')

        y_lower, y_upper = set_axis_limits(min(df_tk), max(df_tk))
        if y_min is None:
            y_min = y_lower
        if y_max is None:
            y_max = y_upper

        print(f'y_min = {y_min} (type {type(y_min)}), y_max = {y_max} (type {type(y_max)})')

        # Set tick spacing based on the total number of date points
        n_ticks_max = 48
        cond_start = df_tk.index >= x_min
        cond_end = df_tk.index <= x_max
        n = len(df_tk.loc[cond_start & cond_end])
        x_tick_spacing = max(1, round(n / n_ticks_max))

        fig, ax = plt.subplots(figsize=(x_dim, y_dim))

        if plot_type == 'bar':
            plt.bar(df_tk.index, df_tk, label=tk, width=1)
        else:
            plt.plot(df_tk.index, df_tk, label=tk, color=color)

        plt.axis([x_min, x_max, y_min, y_max])
        plt.title(title)
        plt.xticks(rotation=90)
        if add_xlabel:
            plt.xlabel('Date')
        if fill:
            ax.fill_between(df_tk.index, df_tk, color=color)

        if grid in ['x', 'y', 'both']:
            plt.grid(axis=grid)

        ax.xaxis.set_major_locator(plticker.MultipleLocator(x_tick_spacing))
        if y_tick_spacing is not None:
            ax.yaxis.set_major_locator(plticker.MultipleLocator(y_tick_spacing))

        return fig, ax

    ##### PLOT HISTORICAL 2 COLORS MATPLOTLIB #####

    def plot_hist_2colors_matplotlib(
        self,
        tk,
        df,
        start_date,
        end_date,
        title=None,
        y_min=None,
        y_max=None,
        y_tick_spacing=None,
        add_xlabel=False,
        plot_type='line',
        color_positive=None,
        color_negative=None,
        fill_positive=False,
        fill_negative=False,
        x_dim=12,
        y_dim=6,
        grid='both'
    ):
        """
        Create a plot of a historical profile
        tk: ticker profile to be plotted
        df: dataframe containing data for ticker tk
        """

        if isinstance(df, pd.Series):
            df_tk = df.copy()
        elif isinstance(df, pd.DataFrame):
            df_tk = df[tk]
        else:
            print('df must a a series or a dataframe')
            exit

        if title is None:
            title = tk
        if color_positive is None:
            color_positive = 'tab:blue'  # same as '#1f77b4'
        if color_negative is None:
            color_negative = 'tab:blue'  # same as '#1f77b4'

        # Set x-axis limits
        if isinstance(start_date, datetime):
            x_min = str(start_date.date())
        elif isinstance(start_date, date):
            x_min = str(start_date)
        elif isinstance(start_date, str):
            x_min = start_date
        else:
            print('Incorrect format of start_date')
            exit

        if isinstance(end_date, datetime):
            x_max = str(end_date.date())
        elif isinstance(end_date, date):
            x_max = str(end_date)
        elif isinstance(end_date, str):
            x_max = end_date
        else:
            print('Incorrect format of end_date')
            exit

        if x_min not in df_tk.index:
            while x_min not in df_tk.index:
                new_start_date = datetime.strptime(x_min, '%Y-%m-%d') + timedelta(1)
                x_min = str(new_start_date.date())

        if x_max not in df_tk.index:
            while x_max not in df_tk.index:
                new_end_date = datetime.strptime(x_max, '%Y-%m-%d') - timedelta(1)
                x_max = str(new_end_date.date())

        y_lower, y_upper = set_axis_limits(min(df_tk), max(df_tk))
        if y_min is None:
            y_min = y_lower
        if y_max is None:
            y_max = y_upper
        print(y_min, y_max)

        # Set tick spacing based on the total number of date points
        n_ticks_max = 48
        cond_start = df_tk.index >= x_min
        cond_end = df_tk.index <= x_max
        n = len(df_tk.loc[cond_start & cond_end])
        tick_spacing = max(1, round(n / n_ticks_max))

        fig, ax = plt.subplots(figsize=(x_dim, y_dim))

        df_tk_positive = df_tk.copy()
        df_tk_positive.iloc[np.where(df_tk_positive < 0)] = np.nan
        df_tk_negative = df_tk.copy()
        df_tk_negative.iloc[np.where(df_tk >= 0)] = np.nan

        if plot_type == 'bar':
            plt.bar(df_tk.index, df_tk_positive, label=tk, color=color_positive, width=1)
            plt.bar(df_tk.index, df_tk_negative, label=tk, color=color_negative, width=1)
        else:
            plt.plot(df_tk.index, df_tk_positive, label=tk, color=color_positive)
            if fill_positive:
                plt.fill_between(df_tk.index, df_tk_positive, where = df_tk_positive > 0, color = color_positive)
            plt.plot(df_tk.index, df_tk_negative, label=tk, color=color_negative)
            if fill_negative:
                plt.fill_between(df_tk.index, df_tk_negative, where = df_tk_negative < 0, color = color_negative)

        plt.axis([x_min, x_max, y_min, y_max])
        plt.title(title)
        plt.xticks(rotation=90)
        if add_xlabel:
            plt.xlabel('Date')
        if grid in ['x', 'y', 'both']:
            plt.grid(axis=grid)

        ax.xaxis.set_major_locator(plticker.MultipleLocator(tick_spacing))
        if y_tick_spacing is not None:
            ax.yaxis.set_major_locator(plticker.MultipleLocator(y_tick_spacing))

        return fig, ax
