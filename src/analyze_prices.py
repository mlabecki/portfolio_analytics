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
        self
        # end_date: datetime,
        # start_date: datetime,
        # tickers = []
    ):
        """
        end_date:   defaults to today's date, can be changed by user
        start_date: can be specified explicitly or derived based on desired length of history
        tickers:    user-specified based on suggested lists or a custom synthetic portfolio 
        """
        # self.end_date = end_date
        # self.start_date = start_date
        # self.tickers = tickers


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
            'atrp': atrp,
            'atr name': f'ATR {n}',
            'atrp name': f'ATRP {n}'
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


    ##### WEIGHTED MEAN #####

    def weighted_standard_deviation(
        self,
        values
    ):
        """
        values: a list, tuple or series of numerical values
        """
        if isinstance(values, (list, tuple)):
            values = pd.Series(values)

        n = len(values)
        weights = range(n + 1)[1:]

        wm = self.weighted_mean(values)
        wstd = np.sqrt(np.average((values - wm) ** 2, weights = weights))

        return wstd


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
        ma_window:
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


    ##### MOVING AVERAGE RIBBON #####

    def get_ma_ribbon(
        self,
        ma_type,
        ma_window,
        n_ma = 6
    ):
        """
        ma_type:    
            simple ('sma'),
            exponential ('ema'),
            double exponential ('dema'),
            triple exponential ('tema'),
            weighted ('wma'),
            Welles Wilder ('wwma')
        ma_window:
            length in days
        n_ma:
            number of elements in the ribbon (1-6)
        Returns ma
        """

        n_ma = 6 if n_ma > 6 else 1 if n_ma < 1 else n_ma

        ma_ribbon = []
        for k in range(n_ma + 1)[1:]:
            ma_ribbon.append({
                'ma_idx': k,
                'ma_type': ma_type,
                'ma_window': k * ma_window
            })

        return ma_ribbon


    ##### MOVING VOLATILITY / STANDARD DEVIATION #####

    def moving_std_vol(
        self,
        df_tk,
        ma_type,
        ma_window = 10,
        min_periods = 1,
        ddof = 0
    ):
        """
        df_tk:      
            a series of price values, taken as a column of df_close or df_adj_close for ticker tk
        ma_type:
            simple ('sma'),
            exponential ('ema'),
            weighted ('wma')
        ma_window:
            length in days
        Returns moving (rolling) standard deviation m_std and volatility m_vol
        """

        ma_type = 'sma' if ma_type is None else ma_type

        if ma_type == 'ema':
            m_std = df_tk.ewm(span = ma_window).std(ddof = ddof)
            m_vol = df_tk.ewm(span = ma_window).var(ddof = ddof)

        elif ma_type == 'wma':
            m_std = df_tk.rolling(window = ma_window, min_periods = min_periods).apply(lambda x: self.weighted_standard_deviation(x))
            m_vol = df_tk.rolling(window = ma_window, min_periods = min_periods).apply(lambda x: self.weighted_standard_deviation(x) ** 2)

        else:  # 'sma' or anything else
            m_std = df_tk.rolling(window = ma_window, min_periods = min_periods).std(ddof = ddof)
            m_vol = df_tk.rolling(window = ma_window, min_periods = min_periods).var(ddof = ddof)

        mvol_data = {
            'type': ma_type,
            'std': m_std,
            'vol': m_vol,
            'std name': f'MSTD {ma_window}',
            'vol name': f'MVOL {ma_window}'
        }

        return mvol_data


    ##### CREATE TEMPLATE #####

    def create_template(
        self,
        date_index,
        deck_type = 'triple',
        secondary_y = False,
        plot_width = 1600,
        n_ticks_max = None,
        plot_height_1 = None,
        plot_height_2 = None,
        plot_height_3 = None,
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
            series or list of dates (e.g. close_tk.index) in the date format
        deck_type:
            'single', 'double' or 'triple'

        There should be a separate function to update the y axis in any deck based
        on the custom-specified number of ticks.
        Likewise to update the x axis to select a different width (1280, 1450, 1600)

        """

        deck_type = deck_type.lower()
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

        n_ticks_max = round(plot_width / n_xticks_map['width_slope']) if n_ticks_max is None else n_ticks_max
        n_dates_per_xtick = math.floor(len(date_index) / (n_ticks_max - 1))
        x_tickvals = [z for z in reversed([x for x in [y for y in reversed(date_index)][::n_dates_per_xtick]])]

        df_dummy = pd.Series(index = date_index)
        for _, idx in enumerate(date_index):
            df_dummy[idx] = 0

        # x_min = str(min(df_dummy.index).date())
        # x_max = str(max(df_dummy.index).date())

        x_min = str(min(df_dummy.index))
        x_max = str(max(df_dummy.index))

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
                # autorange = False,
                tickvals = x_tickvals,
                type = 'category',
                showgrid = True,
                gridcolor = style['x_gridcolor'],
                # nticks = n_ticks_max,
                tickangle = -90,
                ticks = 'outside',
                ticklen = 8,
                row = k, col = 1
            )
            fig.update_yaxes(
                # autorange = False,
                showgrid = True,
                gridcolor = style['y_gridcolor'],
                zerolinecolor = style['x_gridcolor'],
                zerolinewidth = 1,
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
            legend_groupclick = 'toggleitem',
            modebar_add = [
                "v1hovermode",
                'toggleSpikelines'
            ],
            modebar_remove = [
                'autoScale2d',
                'resetScale2d'
            ]
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
            'overlays': [],
            'has_secondary_y': secondary_y
        }

        return fig_data


    ##### ADJUST LEGEND POSITION #####

    def adjust_legend_position(
        self,
        fig_data,
        deck_type,
        legend_item_height = None,
        legend_title_height = None
    ):
        """
        legend_title_height:
            legend title height to be subtracted for triple deck, depends on the legend title font size, 21 is for size 16
        legend_item_height:
            legend item height to be subtracted from the unadjusted gap, depends on the legend item font size, 19 is for the default size
        """

        legend_item_height = 19 if legend_item_height is None else legend_item_height
        legend_title_height = 21 if legend_title_height is None else legend_title_height

        n_traces_upper = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '1') & (x['showlegend'] if x['showlegend'] is not None else True)])
        n_traces_middle = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '2') & (x['showlegend'] if x['showlegend'] is not None else True)])
        n_traces_lower = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '3') & (x['showlegend'] if x['showlegend'] is not None else True)])
        n_traces_total = n_traces_upper + n_traces_middle + n_traces_lower

        # NOTE: The middle and lower plots in the triple deck should be of the same height
        height_upper = fig_data['plot_height'][1]
        height_lower = fig_data['plot_height'][2]

        intercept_double = legend_gap['double']['intercept']
        slope_upper_double = legend_gap['double']['slope_upper']
        slope_lower_double = legend_gap['double']['slope_lower']
    
        if (deck_type == 'double') | (n_traces_lower == 0):

            legend_groupgap_unadjusted = intercept_double + slope_upper_double * height_upper + slope_lower_double * height_lower
            legend_groupgap = legend_groupgap_unadjusted - legend_item_height * n_traces_upper

        elif deck_type == 'triple':

            if n_traces_middle == 0:
                legend_groupgap_unadjusted = intercept_double + slope_upper_double * (height_upper + height_lower) + slope_lower_double * height_lower
                legend_groupgap = legend_groupgap_unadjusted - n_traces_upper * legend_item_height - legend_title_height

            else:
                intercept_triple = legend_gap['triple']['intercept']
                slope_upper_triple = legend_gap['triple']['slope_upper']
                slope_lower_triple = legend_gap['triple']['slope_lower']

                legend_groupgap_unadjusted = intercept_triple + slope_upper_triple * height_upper + slope_lower_triple * height_lower
                legend_groupgap = (legend_groupgap_unadjusted - n_traces_total * legend_item_height - 3 * legend_title_height) / 2
    
        legend_tracegroupgap = max(legend_groupgap, 0)

        return legend_tracegroupgap


    ##### ADD AVERAGE TRUE RATE (PERCENTAGE) #####

    def add_atr(
        self,
        fig_data,
        atr_data,
        atr_type = 'atr',
        target_deck = 2,
        secondary_y = False,
        add_yaxis_title = None,
        yaxis_title = None,
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        secondary_y is True if target_deck == 1
        secondary_y is False if target_deck == 2 or 3
        atr_type: 
            'atr'   - Average True Rate
            'atrp'  - Average True Rate Percentage
        """

        theme = theme.lower()
        color_theme = color_theme.lower()

        fig = fig_data['fig']
        fig_y_min = fig_data['y_min'][target_deck]
        fig_y_max = fig_data['y_max'][target_deck]
        plot_height = fig_data['plot_height'][target_deck]        
        deck_type = fig_data['deck_type']
        fig_overlays = fig_data['overlays']
        has_secondary_y = fig_data['has_secondary_y']

        # Plot on secondary axis only if it has been created in subplots
        # Plot on primary axis of upper deck only if it is available, i.e. if there are no traces plotted there

        if target_deck == 1:
            if secondary_y:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
            else:
                # Must check if there are traces on the primary y axis
                n_traces_upper = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '1') & (x['showlegend'] if x['showlegend'] is not None else True)])
                # If the primary y axis is unavailable, then refuse to plot
                if n_traces_upper > 0:
                    print(f'ERROR: Can only plot {atr_type.upper()} on the secondary y axis or in the middle/lower deck')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set secondary_y to False and continue
            secondary_y = False

        #####

        add_yaxis_title = secondary_y if add_yaxis_title is None else add_yaxis_title

        if atr_type == 'atrp':
            atr_line = atr_data['atrp']
            yaxis_title = 'ATRP' if yaxis_title is None else yaxis_title
            legend_name = atr_data['atrp name']
        else:
            # atr_type is 'atr' or anything else
            atr_line = atr_data['atr']
            yaxis_title = 'ATR' if yaxis_title is None else yaxis_title
            legend_name = atr_data['atr name']

        current_names = [trace['name'] for trace in fig_data['fig']['data'] if (trace['legendgroup'] == str(target_deck))]

        if legend_name in current_names:
            print(f'{legend_name} has already been plotted in this deck')

        else:
            style = theme_style[theme]

            color_idx = style['overlay_color_selection'][color_theme][1][0]
            linecolor = style['overlay_color_theme'][color_theme][color_idx]

            # Adjust y range if necessary
            reset_y_limits = False

            min_y = min(atr_line[~atr_line.isna()])
            max_y = max(atr_line[~atr_line.isna()])
            
            if fig_y_min is None:
                new_y_min = min_y
                reset_y_limits = True
            else:
                new_y_min = min(min_y, fig_y_min)
                if new_y_min < fig_y_min:
                    reset_y_limits = True

            if fig_y_max is None:
                new_y_max = max_y
                reset_y_limits = True
            else:
                new_y_max = max(max_y, fig_y_max)
                if new_y_max > fig_y_max:
                    reset_y_limits = True

            if not secondary_y:

                # Find new y limits and delta if the y range is expanded
                if reset_y_limits:
                    min_n_intervals = n_yintervals_map['min'][plot_height]
                    max_n_intervals = n_yintervals_map['max'][plot_height]
                    y_lower_limit, y_upper_limit, y_delta = set_axis_limits(new_y_min, new_y_max, min_n_intervals, max_n_intervals)
                    if target_deck > 1:
                        y_upper_limit *= 0.999

                    y_range = (y_lower_limit, y_upper_limit)
                    fig.update_yaxes(
                        range = y_range,
                        showticklabels = True,
                        tick0 = y_lower_limit,
                        dtick = y_delta,
                        showgrid = True,
                        zeroline = True,
                        row = target_deck, col = 1
                    )

            else:
                fig.update_yaxes(
                    range = None,
                    secondary_y = True,
                    showgrid = False,
                    zeroline = False,
                    row = target_deck, col = 1
                )

            legendgrouptitle = {}
            if deck_type == 'triple':
                legendtitle = tripledeck_legendtitle[target_deck]
                legendgrouptitle = dict(
                    text = legendtitle,
                    font_size = 16,
                    font_weight = 'normal'
                )

            fig.add_trace(
                go.Scatter(
                    x = atr_line.index.astype(str),
                    y = atr_line,
                    line_color = linecolor,
                    name = legend_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle
                ),
                row = target_deck, col = 1,
                secondary_y = secondary_y
            )

            # Update layout and axes

            if add_yaxis_title:

                yaxes = [y for y in dir(fig['layout']) if y.startswith('yaxis')]
                yaxis_idx = target_deck - 1 + has_secondary_y
                current_title = fig['layout'][yaxes[yaxis_idx]]['title']['text']

                if current_title is None:
                    new_yaxis_title = yaxis_title
                else:
                    new_yaxis_title = f'{current_title}<BR>{yaxis_title}' if target_deck > 1 else current_title

                fig.update_yaxes(
                    title = new_yaxis_title,
                    row = target_deck, col = 1,
                    secondary_y = secondary_y
                )

            if deck_type in ['double', 'triple']:
                legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
                fig.update_layout(
                    legend_tracegroupgap = legend_tracegroupgap,
                    legend_traceorder = 'grouped'
                )

            fig_data.update({'fig': fig})
            fig_data['y_min'].update({target_deck: new_y_min})
            fig_data['y_max'].update({target_deck: new_y_max})

            color_map = {legend_name: color_idx}
            overlay_idx = len(fig_overlays) + 1
            overlay_name = f'OV{overlay_idx}'
            overlay_components = legend_name
            fig_overlays.append({
                'name': overlay_name,
                'deck': target_deck,
                'color_theme': color_theme,
                'components': overlay_components,
                'color_map': color_map
            })
            fig_data.update({'overlays': fig_overlays})

        return fig_data


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
            'price': close_tk,
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
        add_price = False,
        target_deck = 2,
        oversold_threshold = 20,
        overbought_threshold = 80,
        add_threshold_overlays = True,
        add_title = False,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        stochastic_data: 
            output from stochastic_oscillator()
        tk: 
            ticker for which to plot the stochastic %K and %D lines
        add_price:
            Can only add price to secondary_y, which means target_deck must be 1.
            Except for price on secondary_y, no other overlays will be available.
            None of the traces added by add_stochastic() will be appended to the overlay list.
            Note that, because of the way Stochastic is defined, it only makes sense to 
            overlay it with the Close price.

        """

        k_line = stochastic_data['k_line']
        d_line = stochastic_data['d_line']
        df_price = stochastic_data['price']
        stochastic_label = stochastic_data['label']
        stochastic_type = stochastic_data['type']

        fig_stochastic = fig_data['fig']
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']
        has_secondary_y = fig_data['has_secondary_y']

        # Plot price on secondary axis of the upper deck only if it has been created in subplots

        if target_deck == 1:
            if add_price:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set add_price to False and continue
            add_price = False

        min_stochastic = min(min(k_line), min(d_line))
        max_stochastic = max(max(k_line), max(d_line))

        style = theme_style[theme]

        title_stochastic = f'{tk} {stochastic_type} {stochastic_label} Stochastic Oscillator (%)'
        yaxis_title = f'Stochastic (%)'

        y_upper_limit = 99.99 if target_deck > 1 else 100

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
            )

        fig_stochastic.add_trace(
            go.Scatter(
                x = k_line.index,
                y = k_line,
                line_color = style['kline_linecolor'],
                line_width = 2,
                legendgroup = f'{target_deck}',
                legendgrouptitle = legendgrouptitle,
                name = f'{stochastic_type} {stochastic_label} %K'
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
                name = f'{stochastic_type} {stochastic_label} %D'
            ),
            row = target_deck, col = 1
        )

        if add_threshold_overlays:

            stochastic_hlines = pd.DataFrame(
                {
                    'oversold': oversold_threshold,
                    'overbought': overbought_threshold,
                    'y_max': y_upper_limit
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

        if add_price:
            fig_stochastic.add_trace(
                go.Scatter(
                    x = k_line.index,
                    y = df_price,
                    line_color = style['basecolor'],
                    showgrid = False,
                    name = 'Close',
                    title = 'Close'
                ),
                secondary_y = True
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
            range = (0, y_upper_limit),
            title = yaxis_title,
            showticklabels = True,
            row = target_deck, col = 1
        )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_stochastic.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'fig': fig_stochastic})
        fig_data['y_min'].update({target_deck: min_stochastic})
        fig_data['y_max'].update({target_deck: max_stochastic})

        return fig_data


    ##### MOVING AVERAGE CONVERGENCE DIVERGENCE #####

    def get_macd(
        self,
        close_tk,
        signal_window = 9      
    ):
        """
        Only Close price is used to calculate MACD
        """ 

        if not isinstance(close_tk, pd.Series):
            print('Incorrect format of input data')
            exit

        ema_26 = close_tk.ewm(span = 26).mean()
        ema_12 = close_tk.ewm(span = 12).mean()
        macd_line = ema_12 - ema_26

        macd_signal = macd_line.ewm(span = signal_window).mean()
        macd_histogram = macd_line - macd_signal        

        macd_data = {
            'MACD': macd_line,
            'MACD Signal': macd_signal,
            'MACD Signal Window': signal_window,
            'MACD Histogram': macd_histogram,
            'price': close_tk
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
            'MACD Histogram': macd_v_histogram,
            'price': close_tk
        }

        return macd_v_data


    ##### ADD MACD/MACD-V #####

    def add_macd(
        self,
        fig_data,
        tk_macd,
        macd_data,
        add_price = False, 
        volatility_normalized = True,
        histogram_type = 'macd-signal',
        include_signal = True,
        plot_type = 'bar',
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
        add_price:
            Can only add price to secondary_y, which means target_deck must be 1.
            Except for price on secondary_y, no other overlays will be available.
            None of the traces added by add_macd will be appended to the overlay list.
            To simplify, and because of the way MACD-V is defined, the only price option
            available for overlay is Close.
        """

        fig_macd = fig_data['fig']
        plot_height = fig_data['plot_height'][target_deck]
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']
        has_secondary_y = fig_data['has_secondary_y']        

        # Plot price on secondary axis of the upper deck only if it has been created in subplots

        if target_deck == 1:
            if add_price:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set add_price to False and continue
            add_price = False

        style = theme_style[theme]

        if volatility_normalized:
            yaxis_title = f'MACD-V'
        else:
            yaxis_title = f'MACD'

        macd = macd_data['MACD']
        macd_histogram = macd_data['MACD Histogram']
        df_price = macd_data['price']

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

        min_n_intervals = n_yintervals_map['min'][plot_height]
        max_n_intervals = n_yintervals_map['max'][plot_height]
        y_macd_min, y_macd_max, y_delta = set_axis_limits(min_macd, max_macd, min_n_intervals = min_n_intervals, max_n_intervals = max_n_intervals)

        if target_deck > 1:
            y_macd_max *= 0.999

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
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

        if add_price:
            fig_macd.add_trace(
                go.Scatter(
                    x = df_price.index,
                    y = df_price,
                    line_color = style['basecolor'],
                    showgrid = False,
                    name = 'Close',
                    title = 'Close'
                ),
                secondary_y = True
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
            tick0 = y_macd_min,
            dtick = y_delta,
            showticklabels = True,        
            row = target_deck, col = 1
        )

        fig_data.update({'fig': fig_macd})
        fig_data['y_min'].update({target_deck: min_macd})
        fig_data['y_max'].update({target_deck: max_macd})

        return fig_data 


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
        sort_by
    ):
        """
        df_price:   series of historical prices for a certain ticker
        sort_by:    column to sort by, should be a based on user input
        return:     drawdown_data = {
                        'Drawdown Stats': df_tk_drawdowns,
                        'Deepest Drawdowns': df_tk_deepest_drawdowns,
                        'Longest Drawdowns': df_tk_longest_drawdowns
                    }
        """

        df_tk = df_price.copy()
        df_roll_max_tk = pd.DataFrame(index = df_tk.index)

        drawdown_columns = [
            'Peak',
            'Trough',
            '% Depth',
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
            '% Depth'
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
        df_roll_max_tk = df_tk.rolling(n, min_periods = 1).max()
        unique_max_list = df_roll_max_tk.unique()

        # print(f'df_roll_max:\n{df_roll_max}')
        # print(f'unique_max_list:\n{unique_max_list}')

        for peak in unique_max_list:

            # Define a segment corresponding to vmax 
            cond = df_roll_max_tk == peak
            seg = df_roll_max_tk[cond]
            n_seg = len(seg)

            # print(f'unique_max_list peak:\n{peak}')
            # print(f'n_seg:\n{n_seg}')
            # print(f'seg:\n{seg}')

            # There was no drop within a segment if its length is 1 or 2
            if n_seg > 2:

                # The first date of the segment (min_date_seg) may not necessarily be the first date of the drawdown; e.g. 
                # if the segment starts with a flat section. In that case the last date of the flat part becomes the min_date,
                # unless the flat part is followed by a rise in price.

                min_date_seg = seg.index.min()
                max_date = seg.index.max()
                max_iloc = df_price.index.get_loc(max_date)

                # print(f'min_date_seg:\n{min_date_seg}')

                cond_below_max = df_tk < peak
                cond_in_range = (df_price.index >= min_date_seg) & (df_price.index <= max_date) & cond_below_max

                # print(f'df_price in_range:\n{df_price.loc[cond_in_range]}')
                # print(f'df_price.iloc[30: 40]:\n{df_price.iloc[30: 40]}')
                # print(df_price.index)

                # The peak is false if the initial flat part is followed by a price increase, i.e.
                # df_price.loc[cond_in_range] is empty - skip it in such a case

                if len(df_price.loc[cond_in_range]) > 0:
                
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
                    df_tk_drawdowns.loc[peak, '% Depth'] = 100 * drawdown
                    df_tk_drawdowns.loc[peak, 'Total Length'] = n_length
                    df_tk_drawdowns.loc[peak, 'Peak To Trough'] = n_to_trough
                    df_tk_drawdowns.loc[peak, 'Trough To Recovery'] = n_recovery

        ascending = True if sort_by in cols_float + cols_str else False
        df_tk_drawdowns = df_tk_drawdowns.sort_values(by=sort_by, ascending=ascending)
        df_tk_drawdowns = df_tk_drawdowns.reset_index(drop=True)

        df_tk_deepest_drawdowns = df_tk_drawdowns.sort_values(by='% Depth', ascending=True)
        df_tk_deepest_drawdowns = df_tk_deepest_drawdowns.reset_index(drop=True)
    
        df_tk_longest_drawdowns = df_tk_drawdowns.sort_values(by='Total Length', ascending=False)
        df_tk_longest_drawdowns = df_tk_longest_drawdowns.reset_index(drop=True)

        # Convert output to strings

        for idx in df_tk_drawdowns.index:
            df_tk_drawdowns_str.loc[idx, 'Peak'] = f"{df_tk_drawdowns.loc[idx, 'Peak']:.2f}"
            df_tk_drawdowns_str.loc[idx, 'Trough'] = f"{df_tk_drawdowns.loc[idx, 'Trough']:.2f}"
            df_tk_drawdowns_str.loc[idx, 'Peak Date'] = f"{df_tk_drawdowns.loc[idx, 'Peak Date']}"
            df_tk_drawdowns_str.loc[idx, 'Trough Date'] = f"{df_tk_drawdowns.loc[idx, 'Trough Date']}"
            df_tk_drawdowns_str.loc[idx, 'Recovery Date'] = f"{df_tk_drawdowns.loc[idx, 'Recovery Date']}"
            df_tk_drawdowns_str.loc[idx, '% Depth'] = f"{(df_tk_drawdowns.loc[idx, '% Depth']):.2f}%"
            df_tk_drawdowns_str.loc[idx, 'Total Length'] = f"{df_tk_drawdowns.loc[idx, 'Total Length']}"
            df_tk_drawdowns_str.loc[idx, 'Peak To Trough'] = f"{df_tk_drawdowns.loc[idx, 'Peak To Trough']}"
            df_tk_drawdowns_str.loc[idx, 'Trough To Recovery'] = f"{df_tk_drawdowns.loc[idx, 'Trough To Recovery']}"

        for idx in df_tk_deepest_drawdowns.index:
            df_tk_deepest_drawdowns_str.loc[idx, 'Peak'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Peak']:.2f}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Trough'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Trough']:.2f}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Peak Date'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Peak Date']}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Trough Date'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Trough Date']}"
            df_tk_deepest_drawdowns_str.loc[idx, 'Recovery Date'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Recovery Date']}"
            df_tk_deepest_drawdowns_str.loc[idx, '% Depth'] = f"{(df_tk_deepest_drawdowns.loc[idx, '% Depth']):.2f}%"
            df_tk_deepest_drawdowns_str.loc[idx, 'Total Length'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Total Length']}d"
            df_tk_deepest_drawdowns_str.loc[idx, 'Peak To Trough'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Peak To Trough']}d"
            df_tk_deepest_drawdowns_str.loc[idx, 'Trough To Recovery'] = f"{df_tk_deepest_drawdowns.loc[idx, 'Trough To Recovery']}d"

        for idx in df_tk_longest_drawdowns.index:
            df_tk_longest_drawdowns_str.loc[idx, 'Peak'] = f"{df_tk_longest_drawdowns.loc[idx, 'Peak']:.2f}"
            df_tk_longest_drawdowns_str.loc[idx, 'Trough'] = f"{df_tk_longest_drawdowns.loc[idx, 'Trough']:.2f}"
            df_tk_longest_drawdowns_str.loc[idx, 'Peak Date'] = f"{df_tk_longest_drawdowns.loc[idx, 'Peak Date']}"
            df_tk_longest_drawdowns_str.loc[idx, 'Trough Date'] = f"{df_tk_longest_drawdowns.loc[idx, 'Trough Date']}"
            df_tk_longest_drawdowns_str.loc[idx, 'Recovery Date'] = f"{df_tk_longest_drawdowns.loc[idx, 'Recovery Date']}"
            df_tk_longest_drawdowns_str.loc[idx, '% Depth'] = f"{(df_tk_longest_drawdowns.loc[idx, '% Depth']):.2f}%"
            df_tk_longest_drawdowns_str.loc[idx, 'Total Length'] = f"{df_tk_longest_drawdowns.loc[idx, 'Total Length']}d"
            df_tk_longest_drawdowns_str.loc[idx, 'Peak To Trough'] = f"{df_tk_longest_drawdowns.loc[idx, 'Peak To Trough']}d"
            df_tk_longest_drawdowns_str.loc[idx, 'Trough To Recovery'] = f"{df_tk_longest_drawdowns.loc[idx, 'Trough To Recovery']}d"

        drawdown_data = {
            'Total Drawdowns': len(df_tk_drawdowns),
            'Drawdown Stats': df_tk_drawdowns,
            'Deepest Drawdowns': df_tk_deepest_drawdowns,
            'Longest Drawdowns': df_tk_longest_drawdowns,
            'Drawdown Stats Str': df_tk_drawdowns_str,
            'Deepest Drawdowns Str': df_tk_deepest_drawdowns_str,
            'Longest Drawdowns Str': df_tk_longest_drawdowns_str
        }

        return drawdown_data


    ##### SELECT TK DRAWDOWNS #####

    def select_tk_drawdowns(
        self,
        drawdown_data,
        n_top = 5
    ):
        """
        n_top:      
            number of top drawdowns to include in the tables/graphs
        return:     
            selected_drawdown_data = {
                'Deepest Drawdowns': df_tk_deepest_drawdowns,
                'Longest Drawdowns': df_tk_longest_drawdowns,
                'Deepest Drawdowns Str': df_tk_deepest_drawdowns,
                'Longest Drawdowns Str': df_tk_longest_drawdowns
            }
        """

        drawdown_data_list = [
            'Deepest Drawdowns',                  
            'Longest Drawdowns',
            'Deepest Drawdowns Str',                  
            'Longest Drawdowns Str'
        ]

        n_top = min(n_top, drawdown_data['Total Drawdowns'])

        selected_drawdown_data = {}
        for dd in drawdown_data_list:
            selected_drawdown_data.update({dd: drawdown_data[dd][:n_top]})

        return selected_drawdown_data


    ##### ADD DRAWDOWNS #####

    def add_drawdowns(
        self,
        fig_data,
        df_price,
        tk,
        drawdown_data,
        n_top_drawdowns = 5,
        target_deck = 1,
        add_price = True,
        price_type = 'close',
        top_by = 'depth',
        show_trough_to_recovery = False,
        add_title = True,
        title_font_size = 32,
        theme = 'dark',
        price_color_theme = None,
        drawdown_color = None
    ):
        """
        fig_data:
            template to add the plot to
        target_deck:
            1 (upper), 2 (second from top), 3 (third from top)
            Normally drawdowns should only go into deck 1 and the title should be added.
        add_price:
            Normally True, and the y-axis range will be set based on the price range.
            Should be forced to True if fig_y_min/fig_y_max are None (empty deck) 
                -- No, the user may want to plot drawdowns before adding the price
            However, there might be some interest in adding drawdowns as an overlay on a
            different plot, in which case:
              - add_price could be False, and the y-axis range will not be reset; e.g. drawdowns
                could be overlaid onto a MACD or DIFF plot
              - add_price could be True, and the y-axis would be reset or not based on the price
                range and the existing y-value range (stored in data_fig['y_min/y_max'][target_deck])
        price_type:
            one of 'adjusted close', 'close', 'open', 'high', 'low'
        """

        drawdown_color = 'red' if drawdown_color is None else drawdown_color.lower()
        price_color_theme = 'base' if price_color_theme is None else price_color_theme.lower()

        if isinstance(df_price, pd.Series):
            df_tk = df_price.copy()
        elif isinstance(df_price, pd.DataFrame):
            df_tk = df_price[tk]
        else:
            print('Incorrect format of input data')
            exit

        fig = fig_data['fig']
        fig_y_min = fig_data['y_min'][target_deck]
        fig_y_max = fig_data['y_max'][target_deck]
        plot_height = fig_data['plot_height'][target_deck]        
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']

        # NOTE: Cancelled because the user may want to plot drawdowns before adding the price
        # Even if add_price is False, the y-range must be worked out
        #
        # if (fig_y_min is None) | (fig_y_max is None):
        #     add_price = True

        df_tk_deepest_drawdowns = drawdown_data['Deepest Drawdowns']
        df_tk_longest_drawdowns = drawdown_data['Longest Drawdowns']
        df_tk_deepest_drawdowns_str = drawdown_data['Deepest Drawdowns Str']
        df_tk_longest_drawdowns_str = drawdown_data['Longest Drawdowns Str']

        style = theme_style[theme]

        top_by_color = style['drawdown_colors'][drawdown_color]['fill']
        drawdown_border_color = style['drawdown_colors'][drawdown_color]['border']
                
        legend_name = price_type.title()

        # Alpha = opacity. Since opacity of 1 covers the gridlines, alpha_max is reduced here.
        if theme == 'dark':
            alpha_min, alpha_max = 0.15, 0.7  # max intensity covers the grid
        else:
            alpha_min, alpha_max = 0.1, 0.8  # max intensity covers the grid

        if top_by == 'depth':
            top_list = list(df_tk_deepest_drawdowns['% Depth'])
            top_cmap = map_values(top_list, alpha_min, alpha_max, ascending=True)
        else:
            # length_col = 'Total Length' if show_trough_to_recovery else 'Peak To Trough'
            length_col = 'Total Length'
            top_list = list(df_tk_longest_drawdowns[length_col])
            top_cmap = map_values(top_list, alpha_min, alpha_max, ascending=False)

        color_idx = style['overlay_color_selection'][price_color_theme][1][0]
        linecolor = style['overlay_color_theme'][price_color_theme][color_idx]

        reset_y_limits = False
        
        min_y = min(df_tk[~df_tk.isna()])
        max_y = max(df_tk[~df_tk.isna()])

        # print(f'tk, min_y, max_y = {tk, min_y, max_y}')
        # print(f'tk, fig_y_min, fig_y_max = {tk, fig_y_min, fig_y_max}')

        if fig_y_min is None:
            new_y_min = min_y
            reset_y_limits = True
        else:
            new_y_min = min(min_y, fig_y_min)
            if new_y_min < fig_y_min:
                reset_y_limits = True

        if fig_y_max is None:
            new_y_max = max_y
            reset_y_limits = True
        else:
            new_y_max = max(max_y, fig_y_max)
            if new_y_max > fig_y_max:
                reset_y_limits = True

        # print(f'tk, new_y_min, new_y_max = {tk, new_y_min, new_y_max}')

        if reset_y_limits:
                
            min_n_intervals = n_yintervals_map['min'][plot_height]
            max_n_intervals = n_yintervals_map['max'][plot_height]
            y_lower_limit, y_upper_limit, y_delta = set_axis_limits(new_y_min, new_y_max, min_n_intervals, max_n_intervals)

            if target_deck > 1:
                y_upper_limit *= 0.999
        
            # print(f'min_n_intervals, max_n_intervals = {min_n_intervals, max_n_intervals}')
            # print(f'y_lower_limit, y_upper_limit, y_delta = {y_lower_limit, y_upper_limit, y_delta}')
            # print(f'FINAL new_y_min, new_y_max, y_delta = {new_y_min, new_y_max, y_delta}')

            y_range = (y_lower_limit, y_upper_limit)
            fig.update_yaxes(
                range = y_range,
                title = legend_name,
                showticklabels = True,
                tick0 = y_lower_limit,
                dtick = y_delta,
                showgrid = True,
                zeroline = True,
                row = target_deck, col = 1
            )

        infinity = 2 * y_upper_limit  # Reset Axes refresh takes very long if this is too high

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
            )

        if top_by == 'depth':
            top_drawdowns = df_tk_deepest_drawdowns
            top_drawdowns_str = df_tk_deepest_drawdowns_str
        else:
            top_drawdowns = df_tk_longest_drawdowns
            top_drawdowns_str = df_tk_longest_drawdowns_str   

        n_top_drawdowns = min(n_top_drawdowns, len(top_drawdowns))

        if top_by == 'length':
            title_text = 'Total Length'
        else:
            title_text = '% Depth'
            
        # if show_trough_to_recovery | (top_by == 'length'):
        if show_trough_to_recovery:
            zip_drawdown_parameters = zip(
                top_drawdowns_str.index,
                top_drawdowns_str['Peak Date'],
                top_drawdowns_str['Recovery Date'],
                top_drawdowns['% Depth'],
                top_drawdowns['Peak To Trough'],
                top_drawdowns['Total Length']
            )
            title_drawdowns = f'{tk} {n_top_drawdowns} Top Drawdowns by {title_text} - Peak To Recovery'    
        else:
            zip_drawdown_parameters = zip(
                top_drawdowns_str.index,
                top_drawdowns_str['Peak Date'],
                top_drawdowns_str['Trough Date'],
                top_drawdowns['% Depth'],
                top_drawdowns['Peak To Trough'],
                top_drawdowns['Total Length']
            )
            title_drawdowns = f'{tk} {n_top_drawdowns} Top Drawdowns by {title_text} - Peak To Trough'

        if add_price:
            # Add the price line here to make sure it's first in the legend
            fig.add_trace(
                go.Scatter(
                    x = df_tk.index.astype(str),
                    y = df_tk,
                    line_color = linecolor,
                    line_width = 2,
                    showlegend = True,
                    hoverinfo = 'skip',
                    name = legend_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle                    
                ),
                row = target_deck, col = 1
            )
        
        for idx, x1, x2, depth, peak_to_trough, total_length in zip_drawdown_parameters:

            # length = total_length if show_trough_to_recovery else peak_to_trough
            length = total_length

            if top_by == 'depth':
                alpha_deepest = top_cmap[depth]
                name = f'{depth:.1f}%, {peak_to_trough}d / {total_length}d'
            else:
                alpha_deepest = top_cmap[length]
                name = f'{peak_to_trough}d / {total_length}d, {depth:.1f}%'

            fillcolor = top_by_color.replace('1)', f'{alpha_deepest})')

            fig.add_trace(
                go.Scatter(
                    x = [x1, x2, x2, x1, x1],
                    y = [0, 0, infinity, infinity, 0],
                    # y = [0, 0, y_upper_limit, y_upper_limit, 0],
                    mode = 'lines',
                    line_width = 2,
                    line_color = drawdown_border_color,
                    fill = 'toself',
                    fillcolor = fillcolor,
                    name = name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle
                ),
                row = target_deck, col = 1
            )

        if add_price:
            # Add the price line here to make sure it's on top of other layers
            fig.add_trace(
                go.Scatter(
                    x = df_tk.index.astype(str),
                    y = df_tk,
                    line_color = linecolor,
                    line_width = 2,
                    showlegend = False,
                    name = legend_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle
                ),
                row = target_deck, col = 1
            )

        # Update layout and axes

        if add_title:
            fig.update_layout(
                title = dict(
                    text = title_drawdowns,
                    font_size = title_font_size,
                    y = title_y_pos,
                    x = title_x_pos,
                    xanchor = 'center',
                    yanchor = 'middle'
                )
            )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'fig': fig})
        
        if reset_y_limits:
            fig_data['y_min'].update({target_deck: new_y_min})
            fig_data['y_max'].update({target_deck: new_y_max})
        # print(f"tk, fig_data_y_min, fig_data_y_max = {tk, fig_data['y_min'], fig_data['y_max']}")

        return fig_data


    ##### RSI #####

    def relative_strength(
        self,    
        prices,
        period = 14
    ):
        """
        prices:
            this should be close_tk
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
            'price': prices,
            'rsi_type': rsi_type
        }

        return rsi_data


    ##### ADD RSI #####

    def add_rsi(
        self,
        fig_data,
        rsi_data,
        tk,
        add_price = False,
        target_deck = 2,
        oversold_threshold = 30,
        overbought_threshold = 70,
        add_threshold_overlays = True,
        add_title = False,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        rsi_data:
            output from relative_strength()
        tk:
            ticker for which to plot RSI
        add_price:
            Can only add price to secondary_y, which means target_deck must be 1.
            Except for price on secondary_y, no other overlays will be available.
            None of the traces added by add_rsi() will be appended to the overlay list.
        df_price:
            dataframe/series of prices to overlay (if add_price is True)

        """

        rsi = rsi_data['rsi']
        rsi_type = rsi_data['rsi_type']
        df_price = rsi_data['price']         # must be consistent with RSI construction

        fig_rsi = fig_data['fig']    
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']
        has_secondary_y = fig_data['has_secondary_y']

        # Plot price on secondary axis of the upper deck only if it has been created in subplots

        if target_deck == 1:
            if add_price:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set add_price to False and continue
            add_price = False

        min_rsi = min(rsi)
        max_rsi = max(rsi)

        style = theme_style[theme]

        title_rsi = f'{tk} Relative Strength Index {rsi_type} (%)'
        yaxis_title = f'RSI (%)'

        y_upper_limit = 99.99 if target_deck > 1 else 100

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
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
                    'y_max': y_upper_limit
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

        if add_price:
            fig_rsi.add_trace(
                go.Scatter(
                    x = rsi.index,
                    y = df_price,
                    line_color = style['basecolor'],
                    showgrid = False,
                    name = 'Close',
                    title = 'Close'
                ),
                secondary_y = True
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
            range = (0, y_upper_limit),
            title = yaxis_title,
            showticklabels = True,
            row = target_deck, col = 1
        )

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig_rsi.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'fig': fig_rsi})
        fig_data['y_min'].update({target_deck: min_rsi})
        fig_data['y_max'].update({target_deck: max_rsi})

        return fig_data


    ##### BOLLINGER BANDS #####

    def bollinger_bands(
        self,
        prices,
        ma_type,
        window = None,
        n_std = None,
        n_bands = None,
        ddof = 0
    ):
        """
        prices:
            series of ticker prices ('adjusted close', 'open', 'high', 'low' or 'close')
        ma_type:
            simple ('sma'),
            exponential ('ema'),
            weighted ('wma')
        window:
            size of the rolling window in days, defaults to 20
        n_std:
            width of the upper and lower bands in standard deviations, defaults to 2.0
        n_bands:
            number of pairs of bands to be created, defaults to 1, max 5

        Returns a list of bollinger band dictionaries
        """

        ma_type = 'sma' if ma_type is None else ma_type        

        max_n_bands = 5
        window = 20 if (window is None) else window
        n_std = 2.0 if (n_std is None) else n_std
        n_bands = 1 if (n_bands is None) else min(n_bands, max_n_bands)

        eps = 1e-6

        df_mean = self.moving_average(prices, ma_type, window)
        df_std = self.moving_std_vol(prices, ma_type, window)['std']

        bollinger_list = [{
            'data': df_mean,
            'name': f'{ma_type.upper()} {window}',
            'idx_offset': 0
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

            upper_band = df_mean + band_width * df_std
            upper_name = f'({window}, {band_width:.{k}f}) Upper Bollinger'
            bollinger_list.append({
                'data': upper_band,
                'name': upper_name,
                'idx_offset': i
            })

            lower_band = df_mean - band_width * df_std        
            lower_name = f'({window}, {band_width:.{k}f}) Lower Bollinger'
            bollinger_list.append({
                'data': lower_band,
                'name': lower_name,
                'idx_offset': -i
            })

        upper_band_1 = [x['data'] for x in bollinger_list if x['idx_offset'] == 1][0]
        lower_band_1 = [x['data'] for x in bollinger_list if x['idx_offset'] == -1][0]

        pct_bollinger = (prices - lower_band_1) / (upper_band_1 - lower_band_1)
        pct_bollinger = pct_bollinger.fillna(0)        

        bollinger_width = 100 * (upper_band_1 - lower_band_1) / df_mean

        bollinger_list = sorted(bollinger_list, key = itemgetter('idx_offset'), reverse = True)

        bollinger_data = {
            'list': bollinger_list,
            '%B': pct_bollinger,
            '%B name': f'({window}, {n_std:.{k}f}) %B',
            'width': bollinger_width,
            'width name': f'({window}, {n_std:.{k}f}) B-Width'        
        }

        return bollinger_data


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
            one of 'sma', 'ema', dema', tema', 'wma', 'wwma'
        window:
            size of the rolling window in days
        prc_offset: 
            vertical offset from base moving average in percentage points (-99% to 99%)
        n_bands:
            number of pairs of envelopes to be created, defaults to 3, max 5

        Returns a list of ma envelope dictionaries
        """

        eps = 1e-6

        if ma_type is None:
            ma_type = 'sma'

        n_bands = min(5, n_bands)
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
                'idx_offset': i
            })

            lower_band = base_ma * (1 - ma_offset / 100)
            lower_name = f'({window}, {ma_offset:.{k}f}%) Lower Envelope'
            ma_envelope_list.append({
                'data': lower_band,
                'name': lower_name,
                'idx_offset': -i
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

        fig_y_min: y_min on the existing fig
        fig_y_max: y_max on the existing fig
        color_idx: an integer (0, ...) indicating the color from those available in theme_style
        showlegend:
        legendgroup:

        Returns the updated fig_data dictionary
        """

        theme = theme.lower()
        color_theme = color_theme.lower()

        style = theme_style[theme]
        overlay_colors = style['overlay_color_theme'][color_theme]

        fig = fig_data['fig']
        fig_y_min = fig_data['y_min'][target_deck]
        fig_y_max = fig_data['y_max'][target_deck]
        plot_height = fig_data['plot_height'][target_deck]
        deck_type = fig_data['deck_type']

        # print(f'\nOVERLAY: {name}')

        # Adjust y range if necessary
        reset_y_limits = False

        min_y = min(df[~df.isna()])
        max_y = max(df[~df.isna()])

        if fig_y_min is None:
            new_y_min = min_y
            reset_y_limits = True
        else:
            new_y_min = min(min_y, fig_y_min)
            if new_y_min < fig_y_min:
                reset_y_limits = True
        if fig_y_max is None:
            new_y_max = max_y
            reset_y_limits = True
        else:
            new_y_max = max(max_y, fig_y_max)
            if new_y_max > fig_y_max:
                reset_y_limits = True

            # Find new y limits and delta if the y range is expanded
            if reset_y_limits:
                
                min_n_intervals = n_yintervals_map['min'][plot_height]
                max_n_intervals = n_yintervals_map['max'][plot_height]
                y_lower_limit, y_upper_limit, y_delta = set_axis_limits(new_y_min, new_y_max, min_n_intervals, max_n_intervals)

                if target_deck > 1:
                    y_upper_limit *= 0.999

                # print(f'min_n_intervals, max_n_intervals = {min_n_intervals, max_n_intervals}')
                # print(f'y_lower_limit, y_upper_limit, y_delta = {y_lower_limit, y_upper_limit, y_delta}')
                # print(f'FINAL new_y_min, new_y_max, y_delta = {new_y_min, new_y_max, y_delta}')

                y_range = (y_lower_limit, y_upper_limit)
                fig.update_yaxes(
                    range = y_range,
                    showticklabels = True,
                    tick0 = y_lower_limit,
                    dtick = y_delta,
                    showgrid = True,
                    zeroline = True,
                    row = target_deck, col = 1
                )

        if color_idx >= len(overlay_colors):
            # Take the last overlay color from the available list
            color_idx = -1

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
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

        fig_data.update({'fig': fig})
        fig_data['y_min'].update({target_deck: new_y_min})
        fig_data['y_max'].update({target_deck: new_y_max})

        return fig_data


    ##### ADD MOVING AVERAGE OVERLAYS #####

    def add_ma_overlays(
        self,
        fig_data,
        df_price,
        ma_ribbon_list,
        target_deck = 1,
        add_yaxis_title = False,
        yaxis_title = 'Moving Average',
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        df_price: 
            df_close or df_adj_close, depending on the underlying figure
        ma_ribbon_list: 
            list of ma overlay dictionaries (called ma_ribbon in the get_ma_ribbon() function), containing
             - ma_idx ma index (1, 2,...)
             - ma_type: 'sma' (default), 'ema', 'dema', 'tema', 'wma' or 'wwma'
             - ma_window, in days
        """

        theme = theme.lower()
        color_theme = color_theme.lower()

        deck_type = fig_data['deck_type']
        fig_overlays = fig_data['overlays']

        n_ma = len(ma_ribbon_list)

        style = theme_style[theme]
        overlay_color_idx = style['overlay_color_selection'][color_theme][n_ma]

        current_names = [trace['name'] for trace in fig_data['fig']['data'] if (trace['legendgroup'] == str(target_deck))]

        ma_overlays = []
        ma_overlay_names = []

        for i, ma in enumerate(ma_ribbon_list):

            ma_type = ma['ma_type']
            ma_window = ma['ma_window']
            ma_name = f'{ma_type.upper()} {ma_window}'

            if ma_name not in current_names:

                ma_data = self.moving_average(
                    df_price,
                    ma_type,
                    ma_window
                )
                ma_color_idx = overlay_color_idx[i]

                ma_overlays.append({
                    'data': ma_data,
                    'name': ma_name,
                    'color_idx': ma_color_idx
                })
                ma_overlay_names.append(ma_name)

        if len(ma_overlays) > 0:

            color_map = {}

            for overlay in ma_overlays:
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

            overlay_idx = len(fig_overlays) + 1
            overlay_name = f'OV{overlay_idx}'
            overlay_components = ma_overlay_names[0]
            for name in ma_overlay_names[1:]:
                overlay_components += f', {name}'
            fig_overlays.append({
                'name': overlay_name,
                'deck': target_deck,
                'color_theme': color_theme,
                'components': overlay_components,
                'color_map': color_map
            })

            fig_data.update({'overlays': fig_overlays})

        else:
            print('No new overlays added - all of the selected overlays are already plotted')

        return fig_data


    ##### ADD BOLLINGER OVERLAYS #####

    def add_bollinger_overlays(
        self,
        fig_data,
        bollinger_list,
        target_deck = 1,
        theme = None,
        color_theme = None
    ):
        """
        df_price: df_close or df_adj_close, depending on the underlying figure in fig_data
        """

        theme = 'dark' if theme is None else theme.lower()
        color_theme = 'gold' if color_theme is None else color_theme.lower()

        deck_type = fig_data['deck_type']
        fig_overlays = fig_data['overlays']

        n_boll = int((len(bollinger_list) + 1) / 2)

        style = theme_style[theme]
        overlay_color_idx = style['overlay_color_selection'][color_theme.lower()][n_boll]

        current_names = [tr['name'] for tr in fig_data['fig']['data'] if (tr['legendgroup'] == str(target_deck))]

        bollinger_overlays = []
        bollinger_overlay_names = []

        for boll in bollinger_list:

            if boll['name'] not in current_names:
                bollinger_overlays.append({
                    'data': boll['data'],
                    'name': boll['name'],
                    'color_idx': overlay_color_idx[abs(boll['idx_offset'])]
                })
                bollinger_overlay_names.append(boll['name'])

        if len(bollinger_overlays) > 0:

            color_map = {}

            for overlay in bollinger_overlays:
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

            overlay_idx = len(fig_overlays) + 1
            overlay_name = f'OV{overlay_idx}'
            overlay_components = bollinger_overlay_names[0]
            for name in bollinger_overlay_names[1:]:
                overlay_components += f', {name}'
            fig_overlays.append({
                'name': overlay_name,
                'deck': target_deck,
                'color_theme': color_theme,
                'components': overlay_components,
                'color_map': color_map
            })

            fig_data.update({'overlays': fig_overlays})

        else:
            print('No new overlays added - all of the selected overlays are already plotted')

        return fig_data


    ##### ADD BOLLINGER WIDTH / %B #####

    def add_bollinger_width(
        self,
        fig_data,
        bollinger_data,
        bollinger_type = 'width',
        target_deck = 2,
        secondary_y = False,
        add_yaxis_title = None,
        yaxis_title = None,
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        bollinger_type:
            'width' - Bollinger Width
            '%B'    - Bollinger %B Line
        secondary_y is True if target_deck == 1
        secondary_y is False if target_deck == 2 or 3

        """

        theme = theme.lower()
        color_theme = color_theme.lower()

        style = theme_style[theme]

        fig = fig_data['fig']
        fig_y_min = fig_data['y_min'][target_deck]
        fig_y_max = fig_data['y_max'][target_deck]
        plot_height = fig_data['plot_height'][target_deck]
        deck_type = fig_data['deck_type']
        fig_overlays = fig_data['overlays']
        has_secondary_y = fig_data['has_secondary_y'] 

        # Plot on secondary axis only if it has been created in subplots
        # Plot on primary axis of upper deck only if it is available, i.e. if there are no traces plotted there

        if target_deck == 1:
            if secondary_y:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
            else:
                # Must check if there are traces on the primary y axis
                n_traces_upper = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '1') & (x['showlegend'] if x['showlegend'] is not None else True)])
                # If the primary y axis is unavailable, then refuse to plot
                if n_traces_upper > 0:
                    print(f'ERROR: Can only plot {bollinger_type.title()} on the secondary y axis or in the middle/lower deck')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set secondary_y to False and continue
            secondary_y = False

        #####

        add_yaxis_title = secondary_y if add_yaxis_title is None else add_yaxis_title

        if bollinger_type == '%B':
            b_line = bollinger_data['%B']
            yaxis_title = '%B' if yaxis_title is None else yaxis_title
            legend_name = bollinger_data['%B name']
        else:
            # bollinger_type is 'width' or anything else
            b_line = bollinger_data['width']
            yaxis_title = 'B-Width' if yaxis_title is None else yaxis_title
            legend_name = bollinger_data['width name']

        current_names = [trace['name'] for trace in fig_data['fig']['data'] if (trace['legendgroup'] == str(target_deck))]

        if legend_name in current_names:
            print(f'{legend_name} has already been plotted in this deck')

        else:
            
            style = theme_style[theme]
            color_idx = style['overlay_color_selection'][color_theme][1][0]
            linecolor = style['overlay_color_theme'][color_theme][color_idx]

            # Adjust y range if necessary

            reset_y_limits = False
            
            min_y = min(b_line[~b_line.isna()])
            max_y = max(b_line[~b_line.isna()])
            
            if fig_y_min is None:
                new_y_min = min_y
                reset_y_limits = True
            else:
                new_y_min = min(min_y, fig_y_min)
                if new_y_min < fig_y_min:
                    reset_y_limits = True
            
            if fig_y_max is None:
                new_y_max = max_y
                reset_y_limits = True
            else:
                new_y_max = max(max_y, fig_y_max)
                if new_y_max > fig_y_max:
                    reset_y_limits = True

            print(f'\nADD BOLLINGER WIDTH')
            print(f'min_y, max_y = {min_y, max_y}')
            print(f'fig_y_min, fig_y_max = {fig_y_min, fig_y_max}')
            print(f'new_y_min, new_y_max = {new_y_min, new_y_max}')

            if not secondary_y:

                # Find new y limits and delta if the y range is expanded
                if reset_y_limits:

                    min_n_intervals = n_yintervals_map['min'][plot_height]
                    max_n_intervals = n_yintervals_map['max'][plot_height]
                    y_lower_limit, y_upper_limit, y_delta = set_axis_limits(new_y_min, new_y_max, min_n_intervals, max_n_intervals)

                    if target_deck > 1:
                        y_upper_limit *= 0.999

                    print(f'min_n_intervals, max_n_intervals = {min_n_intervals, max_n_intervals}')
                    print(f'y_lower_limit, y_upper_limit, y_delta = {y_lower_limit, y_upper_limit, y_delta}')
                    print(f'FINAL new_y_min, new_y_max, y_delta = {new_y_min, new_y_max, y_delta}')

                    y_range = (y_lower_limit, y_upper_limit)
                    fig.update_yaxes(
                        range = y_range,
                        showticklabels = True,
                        tick0 = y_lower_limit,
                        dtick = y_delta,
                        # secondary_y = False,
                        showgrid = True,
                        zeroline = True,
                        row = target_deck, col = 1
                    )
            
            else:

                fig.update_yaxes(
                    range = None,
                    secondary_y = True,
                    showgrid = False,
                    zeroline = False,
                    row = target_deck, col = 1
                )

            legendgrouptitle = {}
            if deck_type == 'triple':
                legendtitle = tripledeck_legendtitle[target_deck]
                legendgrouptitle = dict(
                    text = legendtitle,
                    font_size = 16,
                    font_weight = 'normal'
                )

            fig.add_trace(
                go.Scatter(
                    x = b_line.index.astype(str),
                    y = b_line,
                    line_color = linecolor,
                    name = legend_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle
                ),
                row = target_deck, col = 1,
                secondary_y = secondary_y
            )

            # Update layout and axes

            if add_yaxis_title:

                yaxes = [y for y in dir(fig['layout']) if y.startswith('yaxis')]
                yaxis_idx = target_deck - 1 + has_secondary_y
                current_title = fig['layout'][yaxes[yaxis_idx]]['title']['text']

                if current_title is None:
                    new_yaxis_title = yaxis_title
                else:
                    new_yaxis_title = f'{current_title}<BR>{yaxis_title}' if target_deck > 1 else current_title

                fig.update_yaxes(
                    title = new_yaxis_title,
                    row = target_deck, col = 1,
                    secondary_y = secondary_y
                )

            if deck_type in ['double', 'triple']:
                legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
                fig.update_layout(
                    legend_tracegroupgap = legend_tracegroupgap,
                    legend_traceorder = 'grouped'
                )

            fig_data.update({'fig': fig})
            fig_data['y_min'].update({target_deck: new_y_min})
            fig_data['y_max'].update({target_deck: new_y_max})

            color_map = {legend_name: color_idx}
            overlay_idx = len(fig_overlays) + 1
            overlay_name = f'OV{overlay_idx}'
            overlay_components = legend_name
            fig_overlays.append({
                'name': overlay_name,
                'deck': target_deck,
                'color_theme': color_theme,
                'components': overlay_components,
                'color_map': color_map
            })
            fig_data.update({'overlays': fig_overlays})

        return fig_data


    ##### ADD MOVING AVERAGE ENVELOPE OVERLAYS #####

    def add_ma_envelope_overlays(
        self,
        fig_data,
        ma_envelope_list,
        target_deck = 1,    
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        """

        theme = theme.lower()
        color_theme = color_theme.lower()

        deck_type = fig_data['deck_type']
        fig_overlays = fig_data['overlays']

        n_env = int((len(ma_envelope_list) + 1) / 2)

        style = theme_style[theme]
        overlay_color_idx = style['overlay_color_selection'][color_theme][n_env]

        current_names = [tr['name'] for tr in fig_data['fig']['data'] if (tr['legendgroup'] == str(target_deck))]

        ma_envelope_overlays = []
        ma_envelope_overlay_names = []

        for env in ma_envelope_list:

            if env['name'] not in current_names:
                ma_envelope_overlays.append({
                   'data': env['data'],
                   'name': env['name'],
                   'color_idx': overlay_color_idx[abs(env['idx_offset'])]
                })
                ma_envelope_overlay_names.append(env['name'])

        if len(ma_envelope_overlays) > 0:

            color_map = {}

            for overlay in ma_envelope_overlays:
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

            overlay_idx = len(fig_overlays) + 1
            overlay_name = f'OV{overlay_idx}'
            overlay_components = ma_envelope_overlay_names[0]
            for name in ma_envelope_overlay_names[1:]:
                overlay_components += f', {name}'
            fig_overlays.append({
                'name': overlay_name,
                'deck': target_deck,
                'color_theme': color_theme,
                'components': overlay_components,
                'color_map': color_map
            })

            fig_data.update({'overlays': fig_overlays})

        else:
            print('No new overlays added - all of the selected overlays are already plotted')

        return fig_data


    ##### ADD MOVING VOLATILITY / STANDARD DEVIATION #####

    def add_mvol(
        self,
        fig_data,
        mvol_data,
        mvol_type = 'vol',
        target_deck = 2,
        secondary_y = False,
        add_yaxis_title = None,
        yaxis_title = None,
        theme = 'dark',
        color_theme = 'gold'
    ):
        """
        secondary_y is True if target_deck == 1
        secondary_y is False if target_deck == 2 or 3
        mvol_type: 
            'vol' - moving volatility
            'std' - moving standard deviation
        """

        theme = theme.lower()
        color_theme = color_theme.lower()

        style = theme_style[theme]

        fig = fig_data['fig']
        fig_y_min = fig_data['y_min'][target_deck]
        fig_y_max = fig_data['y_max'][target_deck]
        plot_height = fig_data['plot_height'][target_deck]
        deck_type = fig_data['deck_type']
        fig_overlays = fig_data['overlays']
        has_secondary_y = fig_data['has_secondary_y']

        # Plot on secondary axis only if it has been created in subplots
        # Plot on primary axis of upper deck only if it is available, i.e. if there are no traces plotted there

        if target_deck == 1:
            if secondary_y:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
            else:
                # Must check if there are traces on the primary y axis
                n_traces_upper = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '1') & (x['showlegend'] if x['showlegend'] is not None else True)])
                # If the primary y axis is unavailable, then refuse to plot
                if n_traces_upper > 0:
                    print(f'ERROR: Can only plot MVOL/MSTD on the secondary y axis or in the middle/lower deck')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set secondary_y to False and continue
            secondary_y = False

        #####

        add_yaxis_title = secondary_y if add_yaxis_title is None else add_yaxis_title

        if mvol_type == 'std':
            m_line = mvol_data['std']
            if yaxis_title is None:
                yaxis_title = 'MSTD' if target_deck > 1 else 'Moving Standard Deviation'
            else:
                yaxis_title
            legend_name = mvol_data['std name']
        else:
            # mvol_type is 'vol' or anything else
            m_line = mvol_data['vol']
            if yaxis_title is None:
                yaxis_title = 'MVOL' if target_deck > 1 else 'Moving Volatility'
            else:
                yaxis_title
            legend_name = mvol_data['vol name']
    
        current_names = [trace['name'] for trace in fig_data['fig']['data'] if (trace['legendgroup'] == str(target_deck))]

        if legend_name in current_names:
            print(f'{legend_name} has already been plotted in this deck')

        else:

            style = theme_style[theme]

            color_idx = style['overlay_color_selection'][color_theme][1][0]
            linecolor = style['overlay_color_theme'][color_theme][color_idx]

            # Adjust y range if necessary
            reset_y_limits = False

            min_y = min(m_line[~m_line.isna()])
            max_y = max(m_line[~m_line.isna()])

            if fig_y_min is None:
                new_y_min = min_y
                reset_y_limits = True
            else:
                new_y_min = min(min_y, fig_y_min)
                if new_y_min < fig_y_min:
                    reset_y_limits = True

            if fig_y_max is None:
                new_y_max = max_y
                reset_y_limits = True
            else:
                new_y_max = max(max_y, fig_y_max)
                if new_y_max > fig_y_max:
                    reset_y_limits = True

            print(f'\nADD MVOL')
            print(f'min_y, max_y = {min_y, max_y}')
            print(f'fig_y_min, fig_y_max = {fig_y_min, fig_y_max}')
            print(f'new_y_min, new_y_max = {new_y_min, new_y_max}')

            if not secondary_y:
            
                # Find new y limits and delta if the y range is expanded
                if reset_y_limits:
                    
                    min_n_intervals = n_yintervals_map['min'][plot_height]
                    max_n_intervals = n_yintervals_map['max'][plot_height]
                    y_lower_limit, y_upper_limit, y_delta = set_axis_limits(new_y_min, new_y_max, min_n_intervals, max_n_intervals)

                    if target_deck > 1:
                        y_upper_limit *= 0.999

                    print(f'min_n_intervals, max_n_intervals = {min_n_intervals, max_n_intervals}')
                    print(f'y_lower_limit, y_upper_limit, y_delta = {y_lower_limit, y_upper_limit, y_delta}')
                    print(f'FINAL new_y_min, new_y_max, y_delta = {new_y_min, new_y_max, y_delta}')

                    y_range = (y_lower_limit, y_upper_limit)
                    fig.update_yaxes(
                        range = y_range,
                        showticklabels = True,
                        tick0 = y_lower_limit,
                        dtick = y_delta,
                        showgrid = True,
                        zeroline = True,
                        row = target_deck, col = 1
                    )

            else:

                fig.update_yaxes(
                    range = None,
                    secondary_y = True,
                    showgrid = False,
                    zeroline = False,
                    row = target_deck, col = 1
                )

            legendgrouptitle = {}
            if deck_type == 'triple':
                legendtitle = tripledeck_legendtitle[target_deck]
                legendgrouptitle = dict(
                    text = legendtitle,
                    font_size = 16,
                    font_weight = 'normal'
                )

            fig.add_trace(
                go.Scatter(
                    x = m_line.index.astype(str),
                    y = m_line,
                    line_color = linecolor,
                    name = legend_name,
                    legendgroup = f'{target_deck}',
                    legendgrouptitle = legendgrouptitle
                ),
                row = target_deck, col = 1,
                secondary_y = secondary_y
            )

            # Update layout and axes

            if add_yaxis_title:

                yaxes = [y for y in dir(fig['layout']) if y.startswith('yaxis')]
                yaxis_idx = target_deck - 1 + has_secondary_y
                current_title = fig['layout'][yaxes[yaxis_idx]]['title']['text']

                if current_title is None:
                    new_yaxis_title = yaxis_title
                else:
                    new_yaxis_title = f'{current_title}<BR>{yaxis_title}' if target_deck > 1 else current_title

                fig.update_yaxes(
                    title = new_yaxis_title,
                    row = target_deck, col = 1,
                    secondary_y = secondary_y
                )

            if deck_type in ['double', 'triple']:
                legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
                fig.update_layout(
                    legend_tracegroupgap = legend_tracegroupgap,
                    legend_traceorder = 'grouped'
                )

            fig_data.update({'fig': fig})
            fig_data['y_min'].update({target_deck: new_y_min})
            fig_data['y_max'].update({target_deck: new_y_max})

            color_map = {legend_name: color_idx}
            overlay_idx = len(fig_overlays) + 1
            overlay_name = f'OV{overlay_idx}'
            overlay_components = legend_name
            fig_overlays.append({
                'name': overlay_name,
                'deck': target_deck,
                'color_theme': color_theme,
                'components': overlay_components,
                'color_map': color_map
            })
            fig_data.update({'overlays': fig_overlays})

        return fig_data


    ##### UPDATE OVERLAY COLOR THEME #####

    def update_color_theme(
        self,
        fig_data,
        theme,
        new_color_theme,
        overlay_name = 'OV1',
        invert = False
    ):
        """
        fig = fig_data['fig']
        theme: existing theme ('dark' or light')
        color_theme: new color theme to apply to overlays in fig
        invert: invert the palette from lightest-darkest to darkest-lightest or vice versa

        Returns updated fig
        """

        fig_overlays = fig_data['overlays']

        if len(fig_overlays) == 0:

            print('There are no overlays to update the color theme')
            exit

        else:

            overlay = [x for x in fig_data['overlays'] if x['name'] == overlay_name][0]
            overlay_idx = fig_data['overlays'].index(overlay)
            style = theme_style[theme]
            overlay_colors = style['overlay_color_theme'][new_color_theme]
            color_map = overlay['color_map']

            for name, color_idx in color_map.items():

                selector = dict(name = name)

                if invert:
                    color_idx = len(color_map) - color_idx - 1

                fig_data['fig'].update_traces(
                    line_color = overlay_colors[color_idx],
                    selector = selector
                )

                fig_data['overlays'][overlay_idx]['color_map'][name] = color_idx

            fig_data['overlays'][overlay_idx]['color_theme'] = new_color_theme

        return fig_data


    ##### ADD HISTORICAL PRICE/VOLUME #####

    def add_hist_price(
        self,
        fig_data,
        df_price,
        tk,
        target_deck = 1,
        secondary_y = False,
        plot_type = 'scatter',
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
        plot_height = fig_data['plot_height'][target_deck]
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']
        fig_overlays = fig_data['overlays']
        has_secondary_y = fig_data['has_secondary_y']

        # Plot on secondary axis only if it has been created in subplots
        # Plot on primary axis of upper deck only if it is available, i.e. if there are no traces plotted there

        if target_deck == 1:
            if secondary_y:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
            else:
                # Must check if there are traces on the primary y axis
                n_traces_upper = len([x for x in fig_data['fig']['data'] if (x['legendgroup'] == '1') & (x['showlegend'] if x['showlegend'] is not None else True)])
                # This is NOT an overlay, so if the primary y axis is unavailable, then refuse to plot, regardless if it's volume or price
                # Price overlays can be added through add_price_overlays()
                if n_traces_upper > 0:
                    print(f'ERROR: Can only plot {price_type} on the secondary y axis or in the middle/lower deck')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set secondary_y to False and continue
            secondary_y = False

        #####

        theme = theme.lower()
        style = theme_style[theme]
        color_theme = 'base' if color_theme is None else color_theme.lower()
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

        # Adjust y range if necessary

        reset_y_limits = False

        min_y = min(df_tk[~df_tk.isna()])
        max_y = max(df_tk[~df_tk.isna()])

        if fig_y_min is None:
            new_y_min = min_y
            reset_y_limits = True
        else:
            new_y_min = min(min_y, fig_y_min)
            if new_y_min < fig_y_min:
                reset_y_limits = True
        
        if fig_y_max is None:
            new_y_max = max_y
            reset_y_limits = True
        else:
            new_y_max = max(max_y, fig_y_max)
            if new_y_max > fig_y_max:
                reset_y_limits = True

        if not secondary_y:
            # Find new y limits and delta if the y range is expanded
            if reset_y_limits:
                min_n_intervals = n_yintervals_map['min'][plot_height]
                max_n_intervals = n_yintervals_map['max'][plot_height]
                y_lower_limit, y_upper_limit, y_delta = set_axis_limits(new_y_min, new_y_max, min_n_intervals, max_n_intervals)
                if target_deck > 1:
                    y_upper_limit *= 0.999
                y_range = (y_lower_limit, y_upper_limit)
                fig.update_yaxes(
                    range = y_range,
                    title = yaxis_title,
                    showticklabels = True,
                    tick0 = y_lower_limit,
                    dtick = y_delta,
                    showgrid = True,
                    zeroline = True,
                    row = target_deck, col = 1
                )
        
        else:
            fig.update_yaxes(
                range = None,
                title = yaxis_title,
                secondary_y = True,
                showgrid = False,
                zeroline = False,
                row = target_deck, col = 1
            )

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
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

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'fig': fig})
        fig_data['y_min'].update({target_deck: new_y_min})
        fig_data['y_max'].update({target_deck: new_y_max})

        color_map = {legend_name: color_idx}
        overlay_idx = len(fig_overlays) + 1
        overlay_name = f'OV{overlay_idx}'
        overlay_components = legend_name
        fig_overlays.append({
            'name': overlay_name,
            'deck': target_deck,
            'color_theme': color_theme,
            'components': overlay_components,
            'color_map': color_map
        })
        fig_data.update({'overlays': fig_overlays})

        return fig_data


    ##### ADD CANDLESTICK #####

    def add_candlestick(
        self,
        fig_data,
        df_ohlc,
        tk,
        candle_type = 'hollow',
        target_deck = 1,
        add_title = True,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        candle_type: 'hollow' or 'traditional'

        """

        style = theme_style[theme]

        fig = fig_data['fig']
        fig_y_min = fig_data['y_min'][target_deck]
        fig_y_max = fig_data['y_max'][target_deck]        
        plot_height = fig_data['plot_height'][target_deck]
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']

        # Colors must be in the RGBA format
        red_color = style['red_color']
        green_color = style['green_color']
        red_fill_color = red_color
        green_fill_color = green_color
        red_fill_color_hollow = red_color.replace(', 1)', ', 0.2)')
        green_fill_color_hollow = green_color.replace(', 1)', ', 0.2)')

        df = df_ohlc.copy()

        # Adjust y range if necessary
        reset_y_limits = False

        min_y = min(df['Low'][~df.isna()])
        max_y = max(df['High'][~df.isna()])

        if fig_y_min is None:
            new_y_min = min_y
            reset_y_limits = True
        else:
            new_y_min = min(min_y, fig_y_min)
            if new_y_min < fig_y_min:
                reset_y_limits = True
        if fig_y_max is None:
            new_y_max = max_y
            reset_y_limits = True
        else:
            new_y_max = max(max_y, fig_y_max)
            if new_y_max > fig_y_max:
                reset_y_limits = True

            # Find new y limits and delta if the y range is expanded
            if reset_y_limits:
                
                min_n_intervals = n_yintervals_map['min'][plot_height]
                max_n_intervals = n_yintervals_map['max'][plot_height]
                y_lower_limit, y_upper_limit, y_delta = set_axis_limits(new_y_min, new_y_max, min_n_intervals, max_n_intervals)

                if target_deck > 1:
                    y_upper_limit *= 0.999

                # print(f'min_n_intervals, max_n_intervals = {min_n_intervals, max_n_intervals}')
                # print(f'y_lower_limit, y_upper_limit, y_delta = {y_lower_limit, y_upper_limit, y_delta}')
                # print(f'FINAL new_y_min, new_y_max, y_delta = {new_y_min, new_y_max, y_delta}')

                y_range = (y_lower_limit, y_upper_limit)
                fig.update_yaxes(
                    range = y_range,
                    showticklabels = True,
                    tick0 = y_lower_limit,
                    dtick = y_delta,
                    showgrid = True,
                    zeroline = True,
                    row = target_deck, col = 1
                )

        df['Date'] = df.index.astype(str)

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
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

        if deck_type in ['double', 'triple']:
            legend_tracegroupgap = self.adjust_legend_position(fig_data, deck_type)
            fig.update_layout(
                legend_tracegroupgap = legend_tracegroupgap,
                legend_traceorder = 'grouped'
            )

        fig_data.update({'fig': fig})
        fig_data['y_min'].update({target_deck: new_y_min})
        fig_data['y_max'].update({target_deck: new_y_max})

        return fig_data


    ##### ADD PRICE OVERLAYS #####

    def add_price_overlays(
        self,
        fig_data,
        price_list,
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
        """

        theme = theme.lower()
        color_theme = color_theme.lower()

        deck_type = fig_data['deck_type']
        fig_overlays = fig_data['overlays']

        # Count lines that will be overlaid ('show' is True)

        selected_prices = [x for x in price_list if x['show']]
        n_price = len(selected_prices)

        style = theme_style[theme]
        overlay_color_idx = style['overlay_color_selection'][color_theme][n_price]

        current_names = [trace['name'] for trace in fig_data['fig']['data'] if (trace['legendgroup'] == str(target_deck))]

        price_overlays = []
        price_overlay_names = []

        for i, price in enumerate(selected_prices):

            price_name = price['name']

            if price_name not in current_names:

                price_data = price['data']
                color_idx = overlay_color_idx[i]

                price_overlays.append({
                    'data': price_data,
                    'name': price_name,
                    'color_idx': color_idx
                })
                price_overlay_names.append(price_name)

        if len(price_overlays) > 0:

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

            overlay_idx = len(fig_overlays) + 1
            overlay_name = f'OV{overlay_idx}'
            overlay_components = price_overlay_names[0]
            for name in price_overlay_names[1:]:
                overlay_components += f', {name}'
            fig_overlays.append({
                'name': overlay_name,
                'deck': target_deck,
                'color_theme': color_theme,
                'components': overlay_components,
                'color_map': color_map
            })

            fig_data.update({'overlays': fig_overlays})

        else:
            print('No new overlays added - all of the selected overlays are already plotted')

        return fig_data


    ##### ADD OSCILLATOR (DIFFERENTIAL) PLOT #####

    def add_diff(
        self,
        fig_data,
        tk,
        diff_data,
        price_type_map,
        target_deck = 2,
        reverse_diff = False,
        plot_type = 'filled_line',
        add_signal = True,
        add_price = False,        
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
        add_price:
            Can only add price to secondary_y, which means target_deck must be 1.
            Except for price on secondary_y, no other overlays will be available.
            None of the traces added by add_macd will be appended to the overlay list.
        price_type is base in diff_data
        df_price is p_base after mapping through price_type_map
        """

        fig_diff = fig_data['fig']
        plot_height = fig_data['plot_height'][target_deck]
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']
        has_secondary_y = fig_data['has_secondary_y']

        # Plot price on secondary axis of the upper deck only if it has been created in subplots

        if target_deck == 1:
            if add_price:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set add_price to False and continue
            add_price = False

        base = diff_data['p_base']
        p_base_name = base.title()
        p_base = price_type_map[p_base_name]

        p1_type = diff_data['p1_type']
        p2_type = diff_data['p2_type']
        p1_window = diff_data['p1_window']
        p2_window = diff_data['p2_window']
        signal_type = diff_data['signal_type']
        signal_window = diff_data['signal_window']

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
            )

        style = theme_style[theme]

        price_types = ['adjusted close', 'adj close', 'close', 'open', 'high', 'low']
        ma_types = ['sma', 'ema', 'dema', 'tema', 'wma', 'wwma']

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
            diff_title = f'{tk} {p_base_name} {p1_name} - {p2_name} Oscillator'
            diff_positive_name = f'{p1_name} > {p2_name}'
            diff_negative_name = f'{p1_name} < {p2_name}'
        else:
            diff = p2 - p1
            diff_title = f'{tk} {p_base_name} {p2_name} - {p1_name} Oscillator'
            diff_positive_name = f'{p2_name} > {p1_name}'
            diff_negative_name = f'{p2_name} < {p1_name}'

        diff_signal = self.moving_average(diff, signal_type, signal_window)
        signal_name = f'{signal_type.upper()} {signal_window} Signal'

        # By definition, the range of signal will not exceed the range of diff
        min_diff = min(diff)
        max_diff = max(diff)
        min_n_intervals = n_yintervals_map['min'][plot_height]
        max_n_intervals = n_yintervals_map['max'][plot_height]
        y_lower_limit, y_upper_limit, y_delta = set_axis_limits(min_diff, max_diff, min_n_intervals = min_n_intervals, max_n_intervals = max_n_intervals)

        if target_deck > 1:
            y_upper_limit *= 0.999 

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

        if add_price:
            fig_diff.add_trace(
                go.Scatter(
                    x = p_base.index,
                    y = p_base,
                    line_color = style['basecolor'],
                    showgrid = False,
                    name = p_base_name,
                    title = p_base_name
                ),
                secondary_y = True
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
            range = (y_lower_limit, y_upper_limit),
            showticklabels = True,
            tick0 = y_lower_limit,
            dtick = y_delta,
            row = target_deck, col = 1
        )

        if add_yaxis_title:
            fig_data['fig'].update_yaxes(
                title = yaxis_title,
                row = target_deck, col = 1
            )

        fig_data.update({'fig': fig_diff})
        fig_data['y_min'].update({target_deck: min_diff})
        fig_data['y_max'].update({target_deck: max_diff})

        return fig_data


    ##### ADD STOCHASTIC DIFFERENCE PLOT #####

    def add_diff_stochastic(
        self,
        fig_data,
        tk,
        stochastic_data,
        target_deck = 2,
        reverse_diff = False,    
        plot_type = 'filled_line',
        add_signal = False,
        add_price = False,
        signal_type = 'sma',
        signal_window = 10,
        add_yaxis_title = True,
        add_title = False,
        title_font_size = 32,
        theme = 'dark'
    ):
        """
        reverse_diff:
            if True, the %D-%K line difference will be plotted instead of %K-%D
        add_signal:
            if True, signal will be added that is a moving average of the k-d line difference
        """

        fig_diff = fig_data['fig']
        plot_height = fig_data['plot_height'][target_deck]        
        deck_type = fig_data['deck_type']
        title_x_pos = fig_data['title_x_pos']
        title_y_pos = fig_data['title_y_pos']
        has_secondary_y = fig_data['has_secondary_y']

        # Plot price on secondary axis of the upper deck only if it has been created in subplots

        if target_deck == 1:
            if add_price:
                if not has_secondary_y:
                    print('ERROR: Secondary y axis must be selected when creating the plotting template')
                    return fig_data
        else:
            # If it's the middle or lower deck, just set add_price to False and continue
            add_price = False

        stochastic_type = stochastic_data['type']
        stochastic_label = stochastic_data['label']
        p1 = stochastic_data['k_line']
        p2 = stochastic_data['d_line']
        df_price = stochastic_data['price']

        legendgrouptitle = {}
        if deck_type == 'triple':
            legendtitle = tripledeck_legendtitle[target_deck]
            legendgrouptitle = dict(
                text = legendtitle,
                font_size = 16,
                font_weight = 'normal'
            )

        style = theme_style[theme]

        if not reverse_diff:
            p1_name = '%K'
            p2_name = '%D'
            diff = p1 - p2
            diff_title = f'{tk} {stochastic_type} {stochastic_label} Stochastic %K-%D Difference'
            yaxis_title = f'%K-%D'

        else:
            p1_name = '%D'
            p2_name = '%K'
            diff = p2 - p1
            diff_title = f'{tk} {stochastic_type} {stochastic_label} Stochastic %D-%K Difference'
            yaxis_title = f'%D-%K'

        diff_positive_name = f'{stochastic_label} {p1_name} > {p2_name}'
        diff_negative_name = f'{stochastic_label} {p1_name} < {p2_name}'        

        diff_signal = self.moving_average(diff, signal_type, signal_window)
        signal_name = f'{signal_type.upper()} {signal_window} Signal'

        # By definition, the range of signal will not exceed the range of diff
        min_diff = min(diff)
        max_diff = max(diff)
        min_n_intervals = n_yintervals_map['min'][plot_height]
        max_n_intervals = n_yintervals_map['max'][plot_height]
        y_lower_limit, y_upper_limit, y_delta = set_axis_limits(min_diff, max_diff, min_n_intervals = min_n_intervals, max_n_intervals = max_n_intervals)

        if target_deck > 1:
            y_upper_limit *= 0.999 

        ######

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

        if add_price:
            fig_diff.add_trace(
                go.Scatter(
                    x = df_price.index,
                    y = df_price,
                    line_color = style['basecolor'],
                    showgrid = False,
                    name = 'Close',
                    title = 'Close'
                ),
                secondary_y = True
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
            range = (y_lower_limit, y_upper_limit),
            showticklabels = True,
            tick0 = y_lower_limit,
            dtick = y_delta,
            row = target_deck, col = 1
        )

        if add_yaxis_title:
            fig_data['fig'].update_yaxes(
                title = yaxis_title,
                row = target_deck, col = 1
            )

        fig_data.update({'fig': fig_diff})
        fig_data['y_min'].update({target_deck: min_diff})
        fig_data['y_max'].update({target_deck: max_diff})

        return fig_data