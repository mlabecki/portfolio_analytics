# from dash import dcc, html, Input, Output, callback, register_page

from dash import Dash, dcc, html, Input, Output, State, ALL, MATCH, callback, dash_table, register_page
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import yfinance as yf
import pandas as pd
import numpy as np
from operator import itemgetter
from mapping_plot_attributes import *
from mapping_portfolio_downloads import *
from mapping_tickers import *
from css_portfolio_analytics import *
from utils import *

register_page(
    __name__,
    path = '/'
)

category_option_container_css = {
    'width': '385px',
    'margin-top': '10px',
    'margin-left': '10px',
    'padding-left': '10px',
}
category_option_css = {
    'display': 'block',
    'font-size': '14px',
    'font-weight': 'bold',
    'color': '#007ea7',  # rgb(0, 126, 167) - this is native for the YETI theme
    'vertical-align': 'middle',
    'height': '30px',
    'margin-top': '0px',
    'margin-bottom': '2px',
    'margin-left': '10px',
    'padding-left': '10px',
    'padding-top': '3px',
    'border': '2px solid #007ea7'
}
popover_info_category_option_css = {
    'max-width': '405px',
    'padding': '12px 12px 12px 12px',
    'border': '2px solid rgb(0, 126, 167)',
    'border-radius': '5px',
    'background-color': 'rgb(230, 250, 255)',
    'color': 'black',
    'font-family': 'Helvetica',
    'font-size': '13px',
    # 'font-weight': 'bold'
}

popover_markdown_category = {
# NOTE: Must use <BR/>, not <BR>, to break the line inside the popover    

    'biggest_companies': 
    """<DIV><H6>BIGGEST COMPANIES</H6>
<B>Content:</B> 100 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Apple, NVidia, Microsoft, Amazon, Alphabet, Meta, Berkshire Hathaway, Broadcom, Tesla, Taiwan Semiconductor Manufacturing, Eli Lilly, Walmart ...</DIV>""",

    'sp500': 
    """<DIV><H6>S&P 500 COMPANIES</H6>
<B>Content:</B> 100 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Apple, NVidia, Microsoft, Amazon, Alphabet, Meta, Berkshire Hathaway, Broadcom, Tesla, Eli Lilly, Walmart, JP Morgan, Visa, Mastercard, Exxon Mobil ...</DIV>""",

    'nasdaq100': 
    """<DIV><H6>NASDAQ 100 COMPANIES</H6>
<B>Content:</B> 101 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Apple, NVidia, Microsoft, Amazon, Alphabet, Meta, Broadcom, Tesla, Costco, Netflix, T-Mobile, ASML Holding, Cisco Systems, Astra Zeneca, Linde, PepsiCo ...</DIV>""",

    'dow_jones': 
    """<DIV><H6>DOW JONES INDUSTRIAL AVERAGE COMPANIES</H6>
<B>Content:</B> 30 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Apple, NVidia, Microsoft, Amazon, Walmart, JP Morgan, Visa, United Health, Procter & Gamble, Johnson & Johnson, Home Depot, Coca-Cola, Salesforce ...</DIV>""",

    'car_companies': 
    """<DIV><H6>CAR COMPANIES</H6>
<B>Content:</B> 63 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Tesla, Toyota, Xiaomi, BYD, Ferrari, Mercedes-Benz, Porsche, Volkswagen, BMW, General Motors, Maruti Suzuki India, Stellantis, Honda, Ford, Hyundai ...</DIV>""",

    'rare_metals_companies':
    """<DIV><H6>RARE METALS COMPANIES</H6>
<B>Content:</B> 16 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Southern Copper, SQM Chile, Lynas, MP Materials, Sibanye Stillwater, Iluka, Constellium, Tronox, Energy Fuels, Neo Performance Materials, Arafura ...</DIV>""",

    'biggest_etfs': 
    """<DIV><H6>BIGGEST ETFs</H6>
<B>Content:</B> 100 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Vanguard Total Stock, Vanguard S&P 500, iShares Core S&P 500, SPDR S&P 500, Vanguard Growth, Vanguard FTSE Developed Markets, Invesco QQQ, Vanguard Value ...</DIV>""",

    'fixed_income_etfs': 
    """<DIV><H6>FIXED INCOME ETFs</H6>
<B>Content:</B> 100 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Vanguard Total Bond Market Index, iShares Core US Aggregate Bond, Vanguard Total International Bond, iShares 20+ Year Treasury Bond, BTC iShares MBS ...</DIV>""",

    'ai_etfs': 
    """<DIV><H6>ARTIFICIAL INTELLIGENCE ETFs</H6>
<B>Content:</B> 28 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Global X AI &Technology, Global X Robotics & AI, ROBO Global Robotics & Automation Index, ARK Autonomous Technology & Robotics, iShares Future AI & Tech ...</DIV>""",

    'commodity_etfs': 
    """<DIV><H6>COMMODITY ETFs</H6>
<B>Content:</B> 16 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> SPDR Gold Shares, iShares Gold Trust, iShares Silver Trust, Physical Silver Shares, abrdn Physical Platinum Shares, VanEck Gold Miners, Global X Copper Miners ...</DIV>""",

    'currency_etfs': 
    """<DIV><H6>CURRENCY ETFs</H6>
<B>Content:</B> 9 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Invesco Currencyshares JPY, Invesco DB USD Index Bullish, WisdomTree Bloomberg USD Bullish, Invesco CurrencyShares EUR, Invesco CurrencyShares CHF ...</DIV>""",

    'cryptos': 
    """<DIV><H6>CRYPTOCURRENCIES</H6>
<B>Content:</B> 100 cryptocurrencies sorted by Market Capitalization<BR/>
<B>Examples:</B> Bitcoin, Ethereum, Tether USDt, XRP, BNB, Solana, USD Coin, Dogecoin, Cardano, Lido Staked ETH, Wrapped TRON, TRON, Wrapped Bitcoin, Lido wstETH, Litecoin ...</DIV>""",

    'crypto_etfs': 
    """<DIV><H6>CRYPTOCURRENCY ETFs</H6>
<B>Content:</B> 73 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> iShares Bitcoin, Fidelity Wise Origin Bitcoin, Grayscale Bitcoin, ARK 21Shares Bitcoin, Bitwise Bitcoin, iShares Ethereum, Grayscale Ethereum, 2x Bitcoin Strategy ...</DIV>""",

    'futures': 
    """<DIV><H6>COMMODITY FUTURES</H6>
<B>Content:</B> 37 futures sorted by Open Interest<BR/>
<B>Examples:</B> 5-Year US Treasury, E-Mini S&P 500, US Treasury Bond, Corn, E-Mini Russell 2000, Soybean, Gold, Sugar, Crude Oil, Natural Gas, Live Cattle, Cotton, Copper ...</DIV>""",

    'precious_metals': 
    """<DIV><H6>PRECIOUS METALS</H6>
<B>Content:</B> 5 futures sorted by Open Interest<BR/>
<B>Examples:</B> Gold, Copper, Silver, Platinum, Palladium</DIV>""",

    'stock_indices': 
    """<DIV><H6>STOCK INDICES</H6>
<B>Content:</B> 19 indices<BR/>
<B>Examples:</B> S&P 500, S&P/TSX Composite, Dow Jones, Nasdaq Composite, Nasdaq 100, Russell 2000, Hang Seng, Nikkei, FTSE 100, DAX, IBEX 35, CAC 40, STOXX 600, S&P/ASX 200 ...</DIV>""",

    'volatility_indices': 
    """<DIV><H6>VOLATILITY INDICES</H6>
<B>Content:</B> 5 indices<BR/>
<B>Examples:</B> CBOE Volatility, DJIA Volatility, CBOE NASDAQ 100 Volatility, ICE BofAML MOVE, CBOE Gold Volatility</DIV>""",

    'benchmarks': 
    """<DIV><H6>BENCHMARKS</H6>
<B>Content:</B> 5 indices<BR/>
<B>Examples:</B> S&P 500, Dow Jones, Nasdaq Composite, Vanguard Total Stock, CBOE Volatility, ICE BofAML MOVE, S&P GSCI, BBG Commodity, 10-Year US Treasury, 3-Month US Treasury ...</DIV>""",

}

layout = html.Div([

    html.Div(
        id = 'category-options-container',
        children = [

            html.Div(
                'BIGGEST COMPANIES',
                id = 'category-option-biggest-companies',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['biggest_companies'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-biggest-companies',
                target = 'category-option-biggest-companies',
                body = False,
                trigger = 'hover',
                # trigger = 'click',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'S&P 500 COMPANIES',
                id = 'category-option-sp500',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['sp500'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-sp500',
                target = 'category-option-sp500',
                body = False,
                trigger = 'hover',
                # trigger = 'click',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'NASDAQ 100 COMPANIES',
                id = 'category-option-nasdaq100',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['nasdaq100'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-nasdaq100',
                target = 'category-option-nasdaq100',
                body = False,
                trigger = 'hover',
                # trigger = 'click',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'DOW JONES INDUSTRIAL AVERAGE COMPANIES',
                id = 'category-option-dow-jones',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['dow_jones'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-dow-jones',
                target = 'category-option-dow-jones',
                body = False,
                trigger = 'hover',
                # trigger = 'click',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'CAR COMPANIES',
                id = 'category-option-car-companies',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['car_companies'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-car-companies',
                target = 'category-option-car-companies',
                body = False,
                trigger = 'hover',
                # trigger = 'click',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'RARE METALS COMPANIES',
                id = 'category-option-rare-metals-companies',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['rare_metals_companies'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-rare-metals-companies',
                target = 'category-option-rare-metals-companies',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'BIGGEST ETFs',
                id = 'category-option-biggest-etfs',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['biggest_etfs'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-biggest-etfs',
                target = 'category-option-biggest-etfs',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'FIXED INCOME ETFs',
                id = 'category-option-fixed-income-etfs',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['fixed_income_etfs'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-fixed-income-etfs',
                target = 'category-option-fixed-income-etfs',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'ARTIFICIAL INTELLIGENCE ETFs',
                id = 'category-option-ai-etfs',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['ai_etfs'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-ai-etfs',
                target = 'category-option-ai-etfs',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'COMMODITY ETFs',
                id = 'category-option-commodity-etfs',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['commodity_etfs'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-commodity-etfs',
                target = 'category-option-commodity-etfs',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'CURRENCY ETFs',
                id = 'category-option-currency-etfs',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['currency_etfs'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-currency-etfs',
                target = 'category-option-currency-etfs',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'CRYPTOCURRENCIES',
                id = 'category-option-cryptos',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['cryptos'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-cryptos',
                target = 'category-option-cryptos',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'CRYPTOCURRENCY ETFs',
                id = 'category-option-crypto-etfs',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['crypto_etfs'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-crypto-etfs',
                target = 'category-option-crypto-etfs',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'COMMODITY FUTURES',
                id = 'category-option-futures',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['futures'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-futures',
                target = 'category-option-futures',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'PRECIOUS METALS',
                id = 'category-option-precious-metals',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['precious_metals'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-precious-metals',
                target = 'category-option-precious-metals',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'STOCK INDICES',
                id = 'category-option-stock-indices',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['stock_indices'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-stock-indices',
                target = 'category-option-stock-indices',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'VOLATILITY INDICES',
                id = 'category-option-volatility-indices',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['volatility_indices'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-volatility-indices',
                target = 'category-option-volatility-indices',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),

            html.Div(
                'BENCHMARKS',
                id = 'category-option-benchmarks',
                style = category_option_css
            ),
            dbc.Popover([
                dcc.Markdown(popover_markdown_category['benchmarks'], dangerously_allow_html = True)
                ], 
                id = 'popover-category-option-benchmarks',
                target = 'category-option-benchmarks',
                body = False,
                trigger = 'hover',
                hide_arrow = True,
                style = popover_info_category_option_css
            ),


        ],
        style = {
            'width': '380px',
            'margin-top': '10px',
            'margin-left': '10px',
            'padding-left': '10px',
        }
    ),

    html.Div(
        id = 'dates-link-container',
        children = [
            dcc.Link('Go to Preliminary Ticker Selection', href='/preliminary_ticker_selection_v3'),
            html.Br(),
            # dcc.Link('Go to Ticker Info & Portfolio Selection', href='/test_ticker_input_v3'),
        ],
        style = link_container_css
    )

    # html.Div(id = 'test-output-div')

])
