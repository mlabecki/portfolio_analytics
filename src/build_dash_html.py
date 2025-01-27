import dash
from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_loading_spinners as dls

import yfinance as yf
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta, date
import time
import seaborn as sns
from operator import itemgetter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mapping_plot_attributes import *

from mapping_portfolio_downloads import *
from mapping_tickers import *
from mapping_input_tables import *
from css_portfolio_analytics import *
from utils import *


class BuildDashHtml():

    def __init__(
        self
    ):
        """"""
        
    def display_color_themes(
        self
    ):
        
        # theme = theme.lower()
        dark_style = theme_style['dark']
        light_style = theme_style['light']

        ### Overlay color themes

        overlay_color_themes = [x for x in dark_style['overlay_color_theme'].keys()]
        overlay_color_themes_keys = []
        overlay_color_themes_values_dark = []
        overlay_color_themes_values_light = []

        for oct in overlay_color_themes:

            n = len(dark_style['overlay_color_theme'][oct])

            overlay_color_themes_keys += [html.Span(oct.title()), html.Br()]

            for i in range(n):
                
                oct_dark_span = html.Span(
                    id = f'{oct}-dark-{i}',
                    className = 'plots-color-icon',
                    style = {
                        'background-color': dark_style['overlay_color_theme'][oct][i],
                        'border-color': 'black'
                    }
                )
                overlay_color_themes_values_dark.append(oct_dark_span)

                oct_light_span = html.Span(
                    id = f'{oct}-light-{i}',
                    className = 'plots-color-icon',
                    style = {
                        'background-color': light_style['overlay_color_theme'][oct][i],
                        'border-color': 'rgb(229, 236, 246)'  # background of plotly standard theme
                    }
                )
                overlay_color_themes_values_light.append(oct_light_span)

            overlay_color_themes_values_dark.append(html.Br())
            overlay_color_themes_values_light.append(html.Br())

        ### Candlestick color themes

        candle_colors = [x for x in dark_style['candle_colors'].keys()]
        candle_colors_keys = []
        candle_colors_values_dark = []
        candle_colors_values_light = []

        for cc in candle_colors:
            
            n = len(dark_style['candle_colors'][cc])

            candle_colors_keys += [html.Span(cc.title()), html.Br()]

            for color in ['green_color', 'red_color']:
                cc_dark_span = html.Span(
                    id = f'{cc}-dark-{i}',
                    className = 'plots-color-icon',
                    style = {
                        'background-color': dark_style['candle_colors'][cc][color],
                        'border-color': 'black'
                    }
                )
                candle_colors_values_dark.append(cc_dark_span)
                cc_light_span = html.Span(
                    id = f'{cc}-light-{i}',
                    className = 'plots-color-icon',
                    style = {
                        'background-color': light_style['candle_colors'][cc][color],
                        'border-color': 'rgb(229, 236, 246)'  # background of plotly standard theme
                    }
                )
                candle_colors_values_light.append(cc_light_span)

            candle_colors_values_dark.append(html.Br())
            candle_colors_values_light.append(html.Br())

        ##############

        color_themes_popover = html.Div(

            id = 'color-themes-popover-container',

            children = [

                html.Div(
                    dbc.Button(
                        'COLOR THEME GUIDE',
                        id = 'popover-color-themes-button',
                        class_name = 'ma-1',
                        color = 'primary',
                        size = 'sm',
                        n_clicks = 0,
                        style = collapse_button_css
                    )
                ),

                dbc.Popover(
                    [
                    # Overlay color themes
                        html.B(
                            'OVERLAYS',
                            style = popover_color_themes_top_header_css
                        ), 
                        html.Div([
                            html.Div(
                                style = {'display': 'inline-block', 'width': '90px'}
                            ),
                            html.Div(
                                html.B('Dark'),
                                style = {'display': 'inline-block', 'width': '100px'}
                            ),
                            html.Div(style = {'display': 'inline-block', 'width': '10px'}),
                            html.Div(
                                html.B('Light'),
                                style = {'display': 'inline-block', 'width': '100px'}
                            ),
                        ]),
                        html.Div([
                            html.Div(
                                overlay_color_themes_keys,
                                id = 'popover-overlay-color-themes-keys',
                                style = popover_overlay_color_themes_keys_css
                            ),
                            html.Div(
                                overlay_color_themes_values_dark,
                                id = 'popover-overlay-color-themes-values-dark',
                                style = popover_overlay_color_themes_values_dark_css
                            ),
                            html.Div(style = {'display': 'inline-block', 'width': '10px'}),
                            html.Div(
                                overlay_color_themes_values_light,
                                id = 'popover-overlay-color-themes-values-light',
                                style = popover_overlay_color_themes_values_light_css
                            )
                        ]),
                    # Candle colors
                        html.B(
                            'CANDLESTICK & OSCILLATORS',
                            style = popover_color_themes_header_css
                        ), 
                        html.Div([
                            html.Div(
                                style = {'display': 'inline-block', 'width': '100px'}
                            ),
                            html.Div(
                                html.B('Dark'),
                                style = {'display': 'inline-block', 'width': '40px'}
                            ),
                            html.Div(style = {'display': 'inline-block', 'width': '10px'}),
                            html.Div(
                                html.B('Light'),
                                style = {'display': 'inline-block', 'width': '40px'}
                            ),
                        ]),
                        html.Div([
                            html.Div(
                                candle_colors_keys,
                                id = 'popover-candle-colors-keys',
                                style = popover_candle_colors_keys_css
                            ),
                            html.Div(
                                candle_colors_values_dark,
                                id = 'popover-candle-colors-dark',
                                style = popover_candle_colors_values_dark_css
                            ),
                            html.Div(style = {'display': 'inline-block', 'width': '10px'}),
                            html.Div(
                                candle_colors_values_light,
                                id = 'popover-candle-colors-light',
                                style = popover_candle_colors_values_light_css
                            )
                        ]),
                        html.Div(style = {'margin-bottom': '5px'}),

                    ],
                    id = 'popover-color-themes',
                    target = 'popover-color-themes-button',
                    body = True,
                    trigger = 'click',
                    hide_arrow = True,
                    style = popover_color_themes_css
                ),
            ],
        )

        return color_themes_popover
