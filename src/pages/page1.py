import dash
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
    'width': '410px',
    'margin-top': '10px',
    'margin-bottom': '10px',
    'margin-left': '10px',
    'padding-left': '10px',
}
checkmark_css = {
    'display': 'inline-block',
    'width': '20px',
    'color': 'white',
    'background-color': 'white',
    'font-size': '18px',
    'font-weight': 'bold',
    'padding-left': '5px',
    'padding-right': '5px'
}
checkmark_selected_css = {
    'display': 'inline-block',
    'width': '20px',
    'color': 'rgb(0, 126, 167)',
    'background-color': 'white',
    'font-size': '18px',
    'font-weight': 'bold',
    'padding-left': '5px',
    'padding-right': '5px'
}
category_option_css = {
    'display': 'inline-block',
    'width': '365px',
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
category_option_selected_css = {
    'display': 'inline-block',
    'width': '365px',
    'font-size': '14px',
    'font-weight': 'bold',
    'color': 'white',
    'vertical-align': 'middle',
    'height': '30px',
    'margin-top': '0px',
    'margin-bottom': '2px',
    'margin-left': '10px',
    'padding-left': '10px',
    'padding-top': '3px',
    'border': '2px solid #007ea7',
    'background-color': '#007ea7'   # rgb(0, 126, 167) - this is native for the YETI theme
}
popover_info_category_option_css = {
    'max-width': '405px',
    'padding': '12px 12px 12px 12px',
    'border': '2px solid rgb(0, 126, 167)',
    'border-radius': '5px',
    'background-color': 'rgb(230, 250, 255)',
    'color': 'black',
    'font-family': 'Helvetica',
    'font-size': '13px'
}

popover_markdown_category = {
# NOTE: Must use <BR/>, not <BR>, to break the line inside the popover    

    'biggest_companies': 
    """<DIV><H6>BIGGEST COMPANIES</H6>
<B>Content:</B> 100 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Apple, NVidia, Microsoft, Amazon, Alphabet, Meta, Berkshire Hathaway, Broadcom, Tesla, Taiwan Semiconductor Manufacturing, Eli Lilly, Walmart, JP Morgan, Visa, Mastercard ...<BR/>
<B>Source:</B> <A HREF='https://stockanalysis.com/list/biggest-companies/'>Stock Analysis</A></DIV>""",

    'sp500': 
    """<DIV><H6>S&P 500 COMPANIES</H6>
<B>Content:</B> 100 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Apple, NVidia, Microsoft, Amazon, Alphabet, Meta, Berkshire Hathaway, Broadcom, Tesla, Eli Lilly, Walmart, JP Morgan, Visa, Mastercard, Exxon Mobil, Costco, Oracle ...<BR/>
<B>Source:</B> <A HREF='https://stockanalysis.com/list/sp-500-stocks/'>Stock Analysis</A></DIV>""",

    'nasdaq100': 
    """<DIV><H6>NASDAQ 100 COMPANIES</H6>
<B>Content:</B> 101 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Apple, NVidia, Microsoft, Amazon, Alphabet, Meta, Broadcom, Tesla, Costco, Netflix, T-Mobile, ASML Holding, Cisco Systems, Astra Zeneca, Linde, PepsiCo, Intuitive, Palantir ...<BR/>
<B>Source:</B> <A HREF='https://stockanalysis.com/list/nasdaq-100-stocks/'>Stock Analysis</A></DIV>""",

    'dow_jones': 
    """<DIV><H6>DOW JONES INDUSTRIAL AVERAGE COMPANIES</H6>
<B>Content:</B> 30 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Apple, NVidia, Microsoft, Amazon, Walmart, JP Morgan, Visa, United Health, Procter & Gamble, Johnson & Johnson, Home Depot, Coca-Cola, Salesforce, Chevron, Cisco ...<BR/>
<B>Source:</B> <A HREF='https://stockanalysis.com/list/dow-jones-stocks/'>Stock Analysis</A></DIV>""",

    'car_companies': 
    """<DIV><H6>CAR COMPANIES</H6>
<B>Content:</B> 63 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Tesla, Toyota, Xiaomi, BYD, Ferrari, Mercedes-Benz, Porsche, Volkswagen, BMW, General Motors, Maruti Suzuki India, Stellantis, Honda, Ford, Hyundai, Tata Motors, Li Auto ...<BR/>
<B>Source:</B> <A HREF='https://companiesmarketcap.com/cad/automakers/largest-automakers-by-market-cap/'>CompaniesMarketCap</A></DIV>""",

    'rare_metals_companies':
    """<DIV><H6>RARE METALS COMPANIES</H6>
<B>Content:</B> 16 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Southern Copper, SQM Chile, Lynas, MP Materials, Sibanye Stillwater, Iluka, Constellium, Tronox, Energy Fuels, Neo Performance Materials, Arafura, NioCorp, Aclara Resources ...<BR/>
<B>Source:</B> 1. <A HREF='https://investingnews.com/top-rare-earth-stocks/'>Investing News</A>, 2. <A HREF='https://finance.yahoo.com/news/14-best-rare-earth-stocks-181008216.html'>Yahoo Finance</A></DIV>""",

    'quantum_companies': 
    """<DIV><H6>QUANTUM COMPUTING COMPANIES</H6>
<B>Content:</B> 42 equities sorted by Market Capitalization<BR/>
<B>Examples:</B> Rigetti Computing, Quantum Computing, D-Wave Quantum, IonQ, Spectral Capital, Mphasis, BTQ Technologies, Booz Allen Hamilton, Arqit Quantum, Quantum eMotion  ...<BR/>
<B>Source:</B> 1. <A HREF='https://quantumzeitgeist.com/contact-quantum-zeitgeist/'>Quantum Zeitgeist</A>, 2. <A HREF='https://quantumcomputingreport.com/public-companies/'>Quantum Computing Report</A>,<BR/>
3. <A HREF='https://www.fool.com/investing/stock-market/market-sectors/information-technology/ai-stocks/quantum-computing-stocks/'>The Motley Fool</A>, 4. <A HREF='https://greenstocknews.com/stocks/quantum-computing-stocks/'>Green Stock News</A></DIV>""", 

    'biggest_etfs': 
    """<DIV><H6>BIGGEST ETFs</H6>
<B>Content:</B> 100 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Vanguard Total Stock, Vanguard S&P 500, iShares Core S&P 500, SPDR S&P 500, Vanguard Growth, Vanguard FTSE Developed Markets, Invesco QQQ, Vanguard Value ...<BR/>
<B>Source:</B> <A HREF='https://8marketcap.com/etfs/'>Infinite Market Cap</A></DIV>""",

    'fixed_income_etfs': 
    """<DIV><H6>FIXED INCOME ETFs</H6>
<B>Content:</B> 100 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Vanguard Total Bond Market Index, iShares Core US Aggregate Bond, Vanguard Total International Bond, iShares 20+ Year Treasury Bond, BTC iShares MBS ...<BR/>
<B>Source:</B> <A HREF='https://stockanalysis.com/list/fixed-income-etfs/'>Stock Analysis</A></DIV>""",

    'ai_etfs': 
    """<DIV><H6>ARTIFICIAL INTELLIGENCE ETFs</H6>
<B>Content:</B> 28 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Global X AI &Technology, Global X Robotics & AI, ROBO Global Robotics & Automation Index, ARK Autonomous Technology & Robotics, iShares Future AI & Tech ...<BR/>
<B>Source:</B> <A HREF='https://stockanalysis.com/list/artificial-intelligence-etfs/'>Stock Analysis</A></DIV>""",

    'precious_metals': 
    """<DIV><H6>PRECIOUS METAL ETFs</H6>
<B>Content:</B> 20 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> SPDR Gold Shares, iShares Gold Trust, iShares Silver Trust, VanEck Gold Miners, abrdn Physical Gold Shares, Global X Copper Miners, Physical Silver Shares ...<BR/>
<B>Source:</B> <A HREF='https://etfdb.com/etfdb-category/precious-metals/'>VettaFi</A></DIV>""",

    'commodity_etfs': 
    """<DIV><H6>COMMODITY ETFs</H6>
<B>Content:</B> 47 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Invesco Optimum Yield Diversified Commodity Strategy No K-1, First Trust Global Tactical Commodity Strategy, Global X Copper Miners, United States Oil Fund ...<BR/>
<B>Source:</B> <A HREF='https://etfdb.com/etfdb-category/commodities/'>VettaFi</A></DIV>""",

    'currency_etfs': 
    """<DIV><H6>CURRENCY ETFs</H6>
<B>Content:</B> 10 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> Invesco Currencyshares JPY, Invesco DB USD Index Bullish, WisdomTree Bloomberg USD Bullish, Invesco CurrencyShares EUR, Invesco CurrencyShares CHF ...<BR/>
<B>Source:</B> <A HREF='https://etfdb.com/etfdb-category/currency/'>VettaFi</A></DIV>""",

    'cryptos': 
    """<DIV><H6>CRYPTOCURRENCIES</H6>
<B>Content:</B> 100 cryptocurrencies sorted by Market Capitalization<BR/>
<B>Examples:</B> Bitcoin, Ethereum, Tether USDt, XRP, BNB, Solana, USD Coin, Dogecoin, Cardano, Lido Staked ETH, Wrapped TRON, TRON, Wrapped Bitcoin, Lido wstETH, Litecoin ...<BR/>
<B>Source:</B> <A HREF='https://finance.yahoo.com/markets/crypto/all/?start=0&count=100'>Yahoo Finance</A></DIV>""",

    'crypto_etfs': 
    """<DIV><H6>CRYPTOCURRENCY ETFs</H6>
<B>Content:</B> 73 ETFs sorted by Total Assets Under Management<BR/>
<B>Examples:</B> iShares Bitcoin, Fidelity Wise Origin Bitcoin, Grayscale Bitcoin, ARK 21Shares Bitcoin, Bitwise Bitcoin, iShares Ethereum, Grayscale Ethereum, 2x Bitcoin Strategy ...<BR/>
<B>Source:</B> <A HREF='https://stockanalysis.com/list/crypto-etfs/'>Stock Analysis</A></DIV>""",

    'futures': 
    """<DIV><H6>COMMODITY FUTURES</H6>
<B>Content:</B> 37 futures sorted by Open Interest<BR/>
<B>Examples:</B> 5-Year US Treasury, E-Mini S&P 500, US Treasury Bond, Corn, E-Mini Russell 2000, Soybean, Gold, Sugar, Crude Oil, Natural Gas, Live Cattle, Cotton, Copper, RBOB Gasoline ...<BR/>
<B>Source:</B> <A HREF='https://finance.yahoo.com/commodities/'>Yahoo Finance</A></DIV>""",

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
<B>Content:</B> 20 indices<BR/>
<B>Examples:</B> S&P 500, Dow Jones, Nasdaq Composite, Vanguard Total Stock, CBOE Volatility, ICE BofAML MOVE, S&P GSCI, BBG Commodity, 10-Year US Treasury, 3-Month US Treasury ...</DIV>""",

}

layout = html.Div([

    html.Div(
        id = 'category-options-container',
        children = [

            html.Div([
                html.Div(
                    id = 'checkmark-biggest-companies',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'BIGGEST COMPANIES',
                    id = 'category-option-biggest-companies',
                    className = 'category-div-class',                
                    style = category_option_css
                ),
                dbc.Popover([
                    dcc.Markdown(popover_markdown_category['biggest_companies'], dangerously_allow_html = True)
                    ], 
                    id = 'popover-category-option-biggest-companies',
                    target = 'category-option-biggest-companies',
                    body = False,
                    trigger = 'hover',
                    hide_arrow = True,
                    style = popover_info_category_option_css
                )
            ]),
            
            html.Div([
                html.Div(
                    id = 'checkmark-sp500',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'S&P 500 COMPANIES',
                    id = 'category-option-sp500',
                    className = 'category-div-class',                
                    style = category_option_css
                ),
                dbc.Popover([
                    dcc.Markdown(popover_markdown_category['sp500'], dangerously_allow_html = True)
                    ], 
                    id = 'popover-category-option-sp500',
                    target = 'category-option-sp500',
                    body = False,
                    trigger = 'hover',
                    hide_arrow = True,
                    style = popover_info_category_option_css
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-nasdaq100',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'NASDAQ 100 COMPANIES',
                    id = 'category-option-nasdaq100',
                    className = 'category-div-class',                
                    style = category_option_css
                ),
                dbc.Popover([
                    dcc.Markdown(popover_markdown_category['nasdaq100'], dangerously_allow_html = True)
                    ], 
                    id = 'popover-category-option-nasdaq100',
                    target = 'category-option-nasdaq100',
                    body = False,
                    trigger = 'hover',
                    hide_arrow = True,
                    style = popover_info_category_option_css
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-dow-jones',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'DOW JONES INDUSTRIAL AVERAGE COMPANIES',
                    id = 'category-option-dow-jones',
                    className = 'category-div-class',                
                    style = category_option_css
                ),
                dbc.Popover([
                    dcc.Markdown(popover_markdown_category['dow_jones'], dangerously_allow_html = True)
                    ], 
                    id = 'popover-category-option-dow-jones',
                    target = 'category-option-dow-jones',
                    body = False,
                    trigger = 'hover',
                    hide_arrow = True,
                    style = popover_info_category_option_css
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-car-companies',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'CAR COMPANIES',
                    id = 'category-option-car-companies',
                    className = 'category-div-class',                
                    style = category_option_css
                ),
                dbc.Popover([
                    dcc.Markdown(popover_markdown_category['car_companies'], dangerously_allow_html = True)
                    ], 
                    id = 'popover-category-option-car-companies',
                    target = 'category-option-car-companies',
                    body = False,
                    trigger = 'hover',
                    hide_arrow = True,
                    style = popover_info_category_option_css
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-rare-metals-companies',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'RARE METALS COMPANIES',
                    id = 'category-option-rare-metals-companies',
                    className = 'category-div-class',     
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-quantum-companies',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'QUANTUM COMPUTING COMPANIES',
                    id = 'category-option-quantum-companies',
                    className = 'category-div-class',                
                    style = category_option_css
                ),
                dbc.Popover([
                    dcc.Markdown(popover_markdown_category['quantum_companies'], dangerously_allow_html = True)
                    ], 
                    id = 'popover-category-option-quantum-companies',
                    target = 'category-option-quantum-companies',
                    body = False,
                    trigger = 'hover',
                    hide_arrow = True,
                    style = popover_info_category_option_css
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-biggest-etfs',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'BIGGEST ETFs',
                    id = 'category-option-biggest-etfs',
                    className = 'category-div-class',                
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-fixed-income-etfs',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'FIXED INCOME ETFs',
                    id = 'category-option-fixed-income-etfs',
                    className = 'category-div-class',                
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-ai-etfs',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'ARTIFICIAL INTELLIGENCE ETFs',
                    id = 'category-option-ai-etfs',
                    className = 'category-div-class',                
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-precious-metals',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'PRECIOUS METAL ETFs',
                    id = 'category-option-precious-metals',
                    className = 'category-div-class',
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-commodity-etfs',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'MIXED COMMODITY ETFs',
                    id = 'category-option-commodity-etfs',
                    className = 'category-div-class',                
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-currency-etfs',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'NON-CRYPTO CURRENCY ETFs',
                    id = 'category-option-currency-etfs',
                    className = 'category-div-class',                
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-cryptos',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'CRYPTOCURRENCIES',
                    id = 'category-option-cryptos',
                    className = 'category-div-class',                
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-crypto-etfs',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'CRYPTOCURRENCY ETFs',
                    id = 'category-option-crypto-etfs',
                    className = 'category-div-class',                
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-futures',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'COMMODITY FUTURES',
                    id = 'category-option-futures',
                    className = 'category-div-class',
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-stock-indices',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'STOCK INDICES',
                    id = 'category-option-stock-indices',
                    className = 'category-div-class',                
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-volatility-indices',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'VOLATILITY INDICES',
                    id = 'category-option-volatility-indices',
                    className = 'category-div-class',
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
                )
            ]),

            html.Div([
                html.Div(
                    id = 'checkmark-benchmarks',
                    children = '✓',
                    hidden = False,
                    style = checkmark_css
                ),
                html.Div(
                    'BENCHMARKS',
                    id = 'category-option-benchmarks',
                    className = 'category-div-class',
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
                )
            ])

        ],
        style = category_option_container_css
    ),

    html.Div(
        id = 'dates-link-container',
        children = [
            dcc.Link('Continue To Preliminary Ticker Selection', href='/preliminary_ticker_selection_v3'),
            html.Br(),
        ],
        style = link_container_css
    )

])  # layout

#######################################

def toggle_select_category(n, id, current_style, current_checkmark):
    ctx = dash.callback_context
    if n:
        if ctx.triggered:
            if ctx.triggered[0]['prop_id'].split('.')[0] == id:
                new_style = category_option_css if current_style == category_option_selected_css else category_option_selected_css
                new_checkmark = checkmark_selected_css if current_checkmark == checkmark_css else checkmark_css
                return new_style, new_checkmark
    else:
        return current_style, current_checkmark


for category in category_titles_ids.keys():
    id_string = category_titles_ids[category]['id_string']
    callback(
        Output(f'category-option-{id_string}', 'style'),
        Output(f'checkmark-{id_string}', 'style'),
        # Output('selected-categories-stored', 'data'),
        Input(f'category-option-{id_string}', 'n_clicks'),
        Input(f'category-option-{id_string}', 'id'),
        State(f'category-option-{id_string}', 'style'),
        State(f'checkmark-{id_string}', 'style'),
        # State('selected-categories-stored', 'data'),
        suppress_callback_exceptions = True
    )(toggle_select_category)


@callback(
    Output('selected-categories-stored', 'data'),

    Input('checkmark-biggest-companies', 'style'),
    Input('checkmark-sp500', 'style'),
    Input('checkmark-nasdaq100', 'style'),
    Input('checkmark-dow-jones', 'style'),
    Input('checkmark-car-companies', 'style'),
    Input('checkmark-rare-metals-companies', 'style'),
    Input('checkmark-quantum-companies', 'style'),
    Input('checkmark-biggest-etfs', 'style'),
    Input('checkmark-fixed-income-etfs', 'style'),
    Input('checkmark-ai-etfs', 'style'),
    Input('checkmark-commodity-etfs', 'style'),
    Input('checkmark-currency-etfs', 'style'),
    Input('checkmark-cryptos', 'style'),
    Input('checkmark-crypto-etfs', 'style'),
    Input('checkmark-futures', 'style'),
    Input('checkmark-precious-metals', 'style'),
    Input('checkmark-stock-indices', 'style'),
    Input('checkmark-volatility-indices', 'style'),
    Input('checkmark-benchmarks', 'style'),

    suppress_callback_exceptions = True
)
def update_selected_categories(
    checkmark_style_biggest_companies,
    checkmark_style_sp500,
    checkmark_style_nasdaq100,
    checkmark_style_dow_jones,
    checkmark_style_car_companies,
    checkmark_style_rare_metals_companies,
    checkmark_style_quantum_companies,
    checkmark_style_biggest_etfs,
    checkmark_style_fixed_income_etfs,
    checkmark_style_ai_etfs,
    checkmark_style_commodity_etfs,
    checkmark_style_currency_etfs,
    checkmark_style_cryptos,
    checkmark_style_crypto_etfs,
    checkmark_style_futures,
    checkmark_style_precious_metals,
    checkmark_style_stock_indices,
    checkmark_style_volatility_indices,
    checkmark_style_benchmarks
):
    
    selected_categories = []
    for category in category_titles_ids.keys():
        id_string = category_titles_ids[category]['id_string']
        suffix = id_string.replace('-', '_')
        current_checkmark = locals()[f'checkmark_style_{suffix}']
        if current_checkmark == checkmark_selected_css:
            selected_categories.append(category)

    # print(f'Category: {category}, Selected Categories: {selected_categories}')

    return selected_categories


# callback(
#     Output('selected-categories-stored', 'data'),
#     Input(f'checkmark-{id_string}', 'style'),
#     State('selected-categories-stored', 'data'),
#     suppress_callback_exceptions = True
# )(update_selected_categories)
