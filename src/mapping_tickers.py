### URL TO YFINANCE TICKER MAP ###
# Some websites may use tickers that differ from the YF tickers, hence the following map
# The keys are tickers on the websites, values are YF tickers
url_to_yf_ticker_map = {
    'BRK.B': 'BRK-B'
}

indices_custom_info = {
    '^GSPC': {
        'category': 'Large Cap Stock',
        'description': 
            """
            The Standard and Poor's 500, or simply the S&P 500, is a stock market index tracking the stock
            performance of 500 of the largest companies listed on stock exchanges in the United States. It is 
            one of the most commonly followed equity indices and includes approximately 80% of the total market
            cap of U.S. public companies, with more than $50 trillion aggregate market cap as of December 2024.
            """
    },
    '^GSPTSE': {
        'category': 'Large Cap Stock',
        'description': 
        """
        The S&P/TSX Composite Index has provided investors with a premier indicator of market activity for Canadian 
        equity markets since its launch in 1977. With approximately 95% coverage of the Canadian equities market, 
        it is the primary gauge for Canadian-based, Toronto Stock Exchange (TSX) listed companies, representing roughly 
        70% of the total market capitalization on the TSX. It is designed to serve a dual purpose, offering both the 
        representation of a broad benchmark index while maintaining the liquidity characteristics of narrower indices. 
        This unique combination makes the S&P/TSX Composite Index ideal for portfolio management and index replication.
        """
    },
    '^DJI': {
        'category': 'Large Cap Stock',
        'description': 
        """
        The Dow Jones Industrial Average, Dow Jones, or simply the Dow, is a stock market index of 30 publicly-owned companies
        listed on the NASDAQ or the New York Stock Exchange (NYSE). The DJIA is one of the oldest and most commonly followed equity indexes,
        created in 1896 by the Dow & Jones Company founder and Wall Street Journal editor Charles Dow. Initially comprised of only 12 US 
        industrial companies, it has changed over the years, now including companies in other sectors such as technology, health, and retail. 
        The index is price-weighted, unlike other common indexes such as the Nasdaq Composite or S&P 500, which use market capitalization.
        """
    },
    '^IXIC': {
        'category': 'Large Cap Stock',
        'description': 
        """
        The NASDAQ Composite is a stock market index that includes over 3,000 stocks listed on the Nasdaq stock exchange. 
        Its composition is heavily weighted towards companies in the technology sector, which represent almost half of its total market cap.
        Consumer services rank second, with close to 20% market cap, while health care is third at almost 10%. Next in the weightage order
        are consumer goods, financials, and industrials, with allocations of 7.61%, 6.61%, and 6.09%, respectively. Industries such as 
        utilities, oil & gas, basic materials, and telecommunications each have weights of less than 1%. In terms of the number of companies
        from a specific industry, health care clearly dominates with more than 900 companies.
        """
    },
    '^NDX': {
        'category': 'Large Cap Stock',
        'description': 
        """
        The NASDAQ 100 is a stock market index made up of equity securities issued by 100 of the largest non-financial companies listed on the 
        Nasdaq stock exchange. It was launched in 1985 by the National Associate of Securities Dealers (NASD), alongside its sister index
        NASDAQ Financial 100. It includes companies in areas such as industrial, technology, retail, telecommunication, biotechnology, health care, 
        transportation, and media.
        """
    },
    '^IXF': {
        'category': 'Large Cap Stock',
        'description': 
        """
        The NASDAQ Financial 100 is a stock market index made up of equity securities issued by 100 of the largest financial companies listed on the 
        Nasdaq stock exchange. It was launched in 1985 by the National Associate of Securities Dealers (NASD), alongside its more widely followed 
        sister index NASDAQ 100. NASDAQ Financial 100 covers areas such as banking, insurance, mortgages and securities trading.
        """
    },
    '^NYA': {
        'category': 'Large Cap Stock',
        'description': 
        """
        The NYSE Composite is a stock market index covering all common stock listed on the New York Stock Exchange, including American depositary receipts (ADRs),
        real estate investment trusts, tracking stocks, and foreign listings. It covers over 2,000 stocks, of which over 1,600 are from the U.S. corporations and 
        over 360 are foreign listings. However, foreign companies constitute over a half of the largest companies in the index by market capitalization. 
        The index uses free-float market cap weighting.
        """
    },
    '^RUT': {
        'category': 'Small Cap Stock',
        'description': 
        """
        The Russell 2000 Index is a U.S. stock market index that makes up the smallest 2,000 stocks in the Russell Index. It was started
        in 1984 by the Frank Russell Company and is maintained by FTSE Russell, a subsidiary of the London Stock Exchange Group (LSEG). 
        Russell 2000 is by far the most common benchmark for small-cap mutual funds and is the most widely quoted measure of the overall 
        performance of small- to mid-cap company shares. It is commonly considered an indicator of the condition of the U.S. economy because of
        its focus on small companies in the U.S. market. Russell 2000 represents approximately 7% of the total market cap of the Russell 3000 Index.
        """
    },
    '^HSI': {
        'category': '',
        'description': ''
    },
    '^N225': {
        'category': '',
        'description': ''
    },
    '^FTSE': {
        'category': '',
        'description': ''
    },
    '^GDAXI': {
        'category': '',
        'description': ''
    },
    '^IBEX': {
        'category': '',
        'description': ''
    },
    '^FCHI': {
        'category': '',
        'description': ''
    },
    '^STOXX': {
        'category': '',
        'description': ''
    },
    '^AXJO': {
        'category': '',
        'description': ''
    },
    '000001.SS': {
        'category': 'Large Cap Stock',
        'description': 
        """
        The SSE Composite Index is a stock market index of all stocks traded at the Shanghai Stock Exchange (SSE).
        It is considered to be a broad indicator of the condition of the Chinese economy, assessing its performance 
        at the level of a variety of sectors and companies.
        """
    },
    '^KS11': {
        'category': 'Large Cap',
        'description': 
        """
        The Korea Composite Stock Price Index (KOSPI) tracks all common stocks traded on the Korea Stock Exchange,
        similarly to the S&P 500 in the United States. KOSPI was introduced in 1983, replacing the Dow-style Korea
        Composite Stock Price Index.
        """
    },
    '^BSESN': {
        'category': 'Large Cap Stock',
        'description': 
        """
        The BSE SENSEX, also known as the S&P Bombay Stock Exchange Sensitive Index or simply SENSEX, tracks the performance of 30
        major companies representative of various industrial sectors of the Indian economy and listed on the Bombay Stock Exchange.
        """
    },
    '^VIX': {
        'category': 'Stock Volatility',
        'description': 
        """
        The CBOE Volatility Index (VIX) is a popular measure of the stock market's expectation of volatility, calculated and disseminated 
        in real time by CBOE. It is derived from the S&P 500 option prices for the 30 days following the measurement date, with each option price 
        representing the market's expectation of the 30-day forward-looking volatility. VIX cannot be bought or sold directly; instead, it can be
        traded and exchanged via derivative contracts, derived ETFs, and ETNs which most commonly track VIX futures indexes.
        """
    },
    '^VXD': {
        'category': 'Stock Volatility',
        'description': 
        """
        The CBOE DJIA Volatility Index is an estimate of the expected 30-day volatility of Dow Jones Industrial Avedrage (DJIA) stock index returns. 
        Similarly to VIX, VXD is calculated based on the 30-day forward-looking DJIA option prices.
        """
    },
    '^VXN': {
        'category': 'Stock Volatility',
        'description': 
        """
        The CBOE NASDAQ 100 Volatility Index is a key measure of market expectations of near-term volatility conveyed by NASDAQ 100 Index option prices.
        It measures the market's expectation of 30-day volatility implicit in the prices of near-term NASDAQ 100 options.
        """
    },
    '^MOVE': {
        'category': 'Bond Volatility',
        'description': 
        """
        The Intercontinental Exchange (ICE) Bank of America Merrill Lynch MOVE index is a measure of the expected volatility
        of US Treasury bonds. It is calculated by taking the weighted average of the implied volatilities of a range of options
        on US Treasury bonds. The index is expressed in basis points (bps) and is published by ICE Benchmark Administration Ltd.
        """
    },
    '^GVZ': {
        'category': 'Commodity Volatility',
        'description': 
        """
        The CBOE Gold ETF Volatility Index is an estimate of the expected 30-day volatility of returns on the SPDR Gold Shares ETF (GLD). 
        Similarly to VIX, GVZ is calculated based on the 30-day forward-looking prices of GLD options.
        """
    },
    '^SPGSCI': {
        'category': 'Commodities Broad Basket',
        'description': 
        """
        The S&P GSCI, originally developed in 1991 by Goldman Sachs, serves as a benchmark for investment in the commodity markets
        and as a measure of commodity performance over time. It is the first major investable commodity index, designed that way 
        by including the most liquid commodity futures and providing diversification with low correlations to other asset classes.
        The index currently comprises 24 commodities from all commodity sectors - energy products, industrial metals, agricultural 
        products, livestock products and precious metals. It contains a much higher exposure to energy than other commodity price 
        indices such as the Bloomberg Commodity Index (BCOM). S&P GSCI is being traded at the Chicago Mercantile Exchange (CME).
        """
    },
    '^BCOM': {
        'category': 'Commodities Broad Basket',
        'description': 
        """
        The Bloomberg Commodity Index (BCOM) is a broadly diversified commodity price index tracking prices of futures 
        contracts on physical commodities. It was originally launched as the Dow Jones-AIG Commodity Index in 1998; later renamed
        to Dow Jones-UBS Commodity Index in 2009, when UBS acquired it from AIG; and finally rebranded under its current name in 2014. 
        The BCOM is designed to minimize concentration in any one commodity or sector - it currently includes 23 commodity 
        futures in six sectors.
        """
    },
    '^TNX': {
        'category': 'Treasury Bond',
        'description': 
        """
        The CBOE Interest Rate 10-Year Treasury Note Index (TNX) is a benchmark index that tracks the yield of U.S. Treasury
        10-year notes. It is often considered to be a risk-free investment because of its backing by the U.S. government.
        """
    },
    '^IRX': {
        'category': 'Treasury Bond',
        'description': 
        """
        The 13-Week Treasury Bill Index is a benchmark index that tracks the yield of U.S. Treasury 13-week bills.
        It is often considered a risk-free investment because of its backing by the U.S. government.
        """
    }
}

### BENCHMARKS ###

benchmark_tickers = {
    '^GSPC':    'S&P 500 Index',
    '^DJI':     'Dow Jones Industrial Average',
    '^IXIC':    'NASDAQ Composite',
    '^RUT':     'Russell 2000',
    'VTI':      'Vanguard Total Stock Market Index Fund ETF Shares',
    'VOO':      'Vanguard S&P 500 ETF',
    'SPY':      'SPDR S&P 500 ETF Trust',
    '^VIX':     'CBOE Volatility Index',
    '^MOVE':    'ICE BofAML MOVE (Merrill Lynch Option Volatility Estimate) Index',
    '^SPGSCI':  'S&P GSCI Index',
    '^BCOM':    'BBG Commodity',
    'GLD':      'SPDR Gold Shares',
    'DBC':      'Invesco DB Commodity Index Tracking Fund',
    'GSG':      'iShares S&P GSCI Commodity-Indexed Trust',
    'BND':      'Vanguard Total Bond Market Index Fund',
    'AGG':      'iShares Core U.S. Aggregate Bond ETF',    
    '^TNX':     '10-Year US Treasury Note',
    '^IRX':     '3-Month US Treasury Bill',
    'IBIT':     'iShares Bitcoin Trust',
    'GBTC':     'Grayscale Bitcoin Trust ETF (BTC)'
}

### STOCKS ###

# Stock market benchmarks
# tickers = ['^SPX', '^GSPC', '^GSPTSE', '^DJI', ' ^NDX', '^IXIC', '^MOVE']
# ^SPX is essentially the same as ^GSPC (S&P 500) - same numbers
# ^GSPTSE is S&P/TSX Composite index
# ^IXIC is NASDAQ Composite (> 2500 stocks), ^NDX is NASDAQ-100 Index (100 stocks)
# ^DJI is Dow Jones Industrial Average. You cannot invest in ^DJI itself, 
# but you can invest in DJIA, which is an ETF holding DJIA stocks
# and selling call options on the underlying (covered call strategy).
# QQQ is Invesco QQQ Trust, an ETF investing in NASDAQ-100 Index.
# 
# NOTE: The benchmarks can be indices, not necessarily investable
#

# NOTE: stock_index_tickers will not be downloaded from url, should be listed in the app menu
stock_index_tickers = {
    '^GSPC': 'S&P 500 Index',
    '^GSPTSE': 'S&P/TSX Composite Index',
    '^DJI': 'Dow Jones Industrial Average',
    '^IXIC': 'NASDAQ Composite',
    '^NDX': 'NASDAQ 100',
    '^IXF': 'NASDAQ Financial 100',
    '^NYA': 'NYSE COMPOSITE (DJ)',
    '^RUT': 'Russell 2000',
    '^HSI': 'HANG SENG INDEX',
    '^N225': 'Nikkei 225',
    '^FTSE': 'FTSE 100',  # based on 100 largest blue chips stocks listed on London Stock Exchange
    '^GDAXI': 'DAX PERFORMANCE-INDEX',  # Berlin
    '^IBEX': 'IBEX 35...',  # tracking 35 Spanish companish on Bolsa De Madrid
    '^FCHI': 'CAC 40',  # benchmark French stock index
    '^STOXX': 'STXE 600 PR.EUR',  # Index of stocks from 17 European exchanges
    '^AXJO': 'S&P/ASX 200',  # based on the 200 largest stocks on Australian Securities Exchange
    '000001.SS': 'SSE Composite Index',  # Shanghai Composite
    '^KS11': 'KOSPI Composite Index',  # Korean Composite Index
    '^BSESN': 'S&P BSE SENSEX'  # Index tracking top 30 India's companies
}

# NOTE: Magnificent 7 tickers should be listed in the app menu
magnificent_7_tickers = {
    'NVDA': 'NVIDIA Corporation',
    'AAPL': 'Apple Inc.',
    'TSLA': 'Tesla, Inc.',
    'MSFT': 'Microsoft Corporation',
    'AMZN': 'Amazon.com, Inc.',
    'META': 'Meta Platforms, Inc.',
    'GOOG': 'Alphabet Inc.'
}

### VOLATILITY ###
volatility_tickers = {
    '^VIX': 'CBOE Volatility Index',
    '^VXD': 'DJIA VOLATILITY',
    '^VXN': 'CBOE NASDAQ 100 Volatility',
    '^MOVE': 'ICE BofAML MOVE Index',  # 'ICE BofAML MOVE (Merrill Lynch Option Volatility Estimate) Index',
    '^GVZ': 'CBOE Gold Volatility Index'
}

### FUTURES
# NOTE: Add various Index, stocks and commodities futures - it will usually be the next 
# delivery date. e.g. Sep 24 as of Aug 5
# These have been included in a download from url

### BONDS ###

# NOTE: The lower of the two ticker rates will be used 
risk_free_treasury_tickers = {
    '^TNX': '10-Year US Treasury Note',
    '^IRX': '3-Month US Treasury Bill'
}

# 13 WEEK TREASURY BILL
treasury_3m_ticker = '^IRX'

# CBOE Interest Rate 10 Year Treasury Note
treasury_10y_ticker = '^TNX'

### BOND ETFS ###
# Bond tickers based on Asset Under Management
# Source: https://etfdb.com/etfdb-category/total-bond-market/
bond_etf_tickers = {
    'BND': 'Vanguard Total Bond Market Index Fund',
    'AGG': 'iShares Core U.S. Aggregate Bond ETF',
    'BNDX': 'Vanguard Total International Bond ETF',
    'BSV': 'Vanguard Short Term Bond ETF',
    'IUSB': 'iShares Core Total USD Bond Market ETF',
    'BIV': 'Vanguard Intermediate-Term Bond ETF',
    'FBND': 'Fidelity Total Bond ETF',
    'MINT': 'PIMCO Enhanced Short Maturity Active Exchange-Traded Fund',
    'PULS': 'PGIM Ultra Short Bond ETF',
    'SCHZ': 'Schwab U.S. Aggregate Bond ETF',
    'SPAB': 'SPDR Portfolio Aggregate Bond ETF',
    'IAGG': 'iShares Core International Aggregate Bond ETF',
    'FTSM': 'First Trust Enhanced Short Maturity ETF',
    'DFCF': 'Dimensional Core Fixed Income ETF',
    'BLV': 'Vanguard Long-Term Bond ETF',
    'FIXD': 'First Trust TCW Opportunistic Fixed Income ETF',
    'BOND': 'PIMCO Active Bond Exchange-Traded Fund',
    'JCPB': 'JPMorgan Core Plus Bond ETF',
    'ISTB': 'iShares Core 1-5 Year USD Bond ETF',
    'CGCP': 'Capital Group Core Plus Income ETF',
    'EAGG': 'iShares ESG Aware US Aggregate Bond ETF',
    'GVI': 'iShares Intermediate Government/Credit Bond ETF',
    'TOTL': 'SPDR DoubleLine Total Return Tactical ETF',
    'UCON': 'First Trust TCW Unconstrained Plus Bond ETF',
    'NEAR': 'iShares Short Duration Bond Active ETF',
    'JMST': 'JPMorgan Ultra-Short Municipal Income ETF',
    'UITB': 'VictoryShares Core Intermediate Bond ETF',
    'FLCB': 'Franklin U.S. Core Bond ETF',
    'JPIE': 'JPMorgan Income ETF',
    'PYLD': 'PIMCO Multisector Bond Active Exchange-Traded Fund',
    'BKAG': 'BNY Mellon Core Bond ETF',
    'JMUB': 'JPMorgan Municipal ETF',
    'HTRB': 'Hartford Total Return Bond ETF',
    'GTO': 'Invesco Total Return Bond ETF',
    'BBAG': 'JPMorgan BetaBuilders U.S. Aggregate Bond ETF',
    'RAVI': 'FlexShares Ultra-Short Income Fund',
    'VRIG': 'Invesco Variable Rate Investment Grade ETF',
    'AVIG': 'Avantis Core Fixed Income ETF',
    'AGGY': 'WisdomTree Yield Enhanced U.S. Aggregate Bond Fund',
    'BNDW': 'Vanguard Total World Bond ETF',
    'LDUR': 'PIMCO Enhanced Low Duration Active ETF',
    'PCEF': 'Invesco CEF Income Composite ETF',
    'USTB': 'VictoryShares Short-Term Bond ETF',
    'AGZ': 'iShares Agency Bond ETF',
    'EUSB': 'iShares ESG Advanced Total USD Bond Market ETF',
    'ILTB': 'iShares Core 10+ Year USD Bond ETF',
    'JSCP': 'JPMorgan Short Duration Core Plus ETF',
    'AVSF': 'Avantis Short-Term Fixed Income ETF',
    'ULST': 'SPDR SSgA Ultra Short Term Bond ETF',
    'JPIB': 'JPMorgan International Bond Opportunities ETF'
}

### PRECIOUS METALS SPOT/FUTURES ###
precious_metals = {
    'GC=F': 'Gold (CMX)',
    'SI=F': 'Silver (CMX)',
    'HG=F': 'Copper (CMX)',
    'PL=F': 'Platinum (NYM)',
    'PA=F': 'Palladium (NYM)'
}

### COMMODITIES ###
commodity_etf_tickers = {
    'GLD':      'SPDR Gold Shares',
    'IAU':      'iShares Gold Trust',
    'SLV':      'iShares Silver Trust',
    'SIVR':     'Physical Silver Shares ETF',
    'PPLT':     'abrdn Physical Platinum Shares ETF',
    'GDX':      'VanEck Gold Miners ETF',
    'COPX':     'Global X Copper Miners ETF',
    'FTGC':     'First Trust Global Tactical Commodity Strategy Fund',
    'DBC':      'Invesco DB Commodity Index Tracking Fund',
    'USO':      'United States Oil Fund',
    'UNG':      'United States Natural Gas Fund',
    'DBA':      'Invesco DB Agriculture Fund',
    'BOIL':     'ProShares Ultra Bloomberg Natural Gas',
    'UCO':      'ProShares Ultra Bloomberg Crude Oil',
    'DJP':      'iPath Bloomberg Commodity Index'
}

### NON-CRYPTO CURRENCY ETFS ###
# Source: https://etfdb.com/etfdb-category/currency/
currency_etf_tickers = {
    'FXY': 'Invesco Currencyshares Japanese Yen Trust',
    'UUP': 'Invesco DB US Dollar Index Bullish Fund',
    'USDU': 'WisdomTree Bloomberg U.S. Dollar Bullish Fund',
    'FXE': 'Invesco CurrencyShares Euro Trust',
    'FXF': 'Invesco CurrencyShares Swiss Franc Trust',
    'FXC': 'Invesco CurrencyShares Canadian Dollar Trust',
    'FXA': 'Invesco CurrencyShares Australian Dollar Trust',
    'FXB': 'Invesco CurrencyShares British Pound Sterling Trust',
    'UDN': 'Invesco DB US Dollar Index Bearish Fund'
}

### CRYPTOS ###
# Crypto market benchmarks
crypto_benchmark_tickers = {
    # 'BITW': 'Bitwise 10 Crypto Index Fund',  
    # NOTE: BITW is traded on OTC markets, so Yahoo categorizes it as EQUITY but info does not
    # include industry and sector. See also https://bitwiseinvestments.com/crypto-funds/bitw
    'GBTC': 'Grayscale Bitcoin Trust ETF (BTC)'
}

# NOTE: Cryptos will be downloaded from url. Most crypto symbols can be listed relative to USD
# as 'tk-USD', e.g. 'BTC-USD' for Bitcoin USD. Those that do not follow this rule should be taken
# from yf_custom_crypto_tickers below, which should be used to update the dictionary of crypto
# symbols to their corresponding YF tickers.

yf_custom_crypto_tickers = {
    'UNI': 'UNI7083-USD',           # 'Uniswap' NOTE: UNI-USD is UNICORN Token USD in Yahoo!Finance
    'PEPE': 'PEPE24478-USD',        # 'Pepe' NOTE: PEPE-USD is PEPEGOLD, a different cryptocurrency launched in 2024
    'ARB': 'ARB11841-USD',          # 'Arbitrum' NOTE: ARB-USD is Arbit USD in Yahoo!Finance)
    'MNT': 'MNT27075-USD',          # 'Mantle' NOTE: MNT-USD is microNFT USD in Yahoo!Finance
    'STX': 'STX4847-USD',           # 'Stacks' NOTE: STX-USD is stox USD in Yahoo!Finance
    'IMX': 'IMX10603-USD',          # 'Immutable X' NOTE: IMX-USD is Impermax USD in Yahoo!Finance
    'SUI': 'SUI20947-USD',          # 'Sui USD' NOTE: SUI-USD is Salmonation USD in Yahoo!Finance
    'BEAMX': 'BEAM28298-USD',       # 'Beam'
    'GRT': 'GRT6719-USD',           # 'The Graph' NOTE: GRT-USD is Golden Ratio Token USD in Yahoo!Finance)
    'TON': 'TON11419-USD',          # 'Toncoin'
    'APT': 'APT21794-USD',          # 'Aptos'
    'USDE': 'USDE29470-USD',        # 'Ethena USDe'
    'POL': 'POL28321-USD',          # 'POL (ex-MATIC)' (YF) or 'Polygon Ecosystem Token' (Coin360)
    'USDS': 'USDS33039-USD',        # 'USDS USD'
    'POPCAT': 'POPCAT28782-USD',    # 'Popcat (SOL)'
    'MEW': 'MEW30126-USD',          # 'cat in a dogs world'
    'BRETT': 'BRETT29743-USD',      # 'Brett (Based)'
}

######################################################################################################

# NOTE: Nasdaq 100 tickers will be downloaded from url, no need to include these below
ndx_top30_components = {
    'TSLA':	'Tesla, Inc.',
    'AAPL':	'Apple Inc.',
    'META':	'Meta Platforms, Inc.',
    'SBUX':	'Starbucks Corporation',
    'ARM': 'Arm Holdings plc',
    'MRVL': 'Marvell Technology, Inc.',
    'MDLZ': 'Mondelez International, Inc.',
    'MCHP': 'Microchip Technology Incorporated',
    'BKR': 'Baker Hughes Company',
    'KDP': 'Keurig Dr Pepper Inc.',
    'AMAT':	'Applied Materials, Inc.',
    'TXN': 'Texas Instruments Incorporated',
    'FTNT': 'Fortinet, Inc.',
    'DDOG':	'Datadog, Inc.',
    'MRNA': 'Moderna, Inc.',
    'CSGP': 'CoStar Group, Inc.',
    'AZN': 'AstraZeneca PLC',
    'HON': 'Honeywell International Inc.',
    'DLTR':	'Dollar Tree, Inc.',
    'ILMN': 'Illumina, Inc.',
    'CEG': 'Constellation Energy Corporation',
    'AMGN': 'Amgen Inc.',
    'PCAR': 'PACCAR Inc',
    'MAR': 'Marriott International, Inc.',
    'ZS': 'Zscaler, Inc.',
    'CCEP':	'Coca-Cola Europacific Partners PLC',
    'INTU':	'Intuit Inc.',
    'CDW': 'CDW Corporation',
    'VRSK':	'Verisk Analytics, Inc.',
    'MELI': 'MercadoLibre, Inc.'
}

# NOTE: ETF tickers will be downloaded from url, no need to include these below
etf_tickers = {
    'ARKK': 'ARK Innovation ETF',
    'DJIA': 'Global X Dow 30 Covered Call ETF',
    'SPY': 'SPDR S&P 500 ETF Trust',
    'QQQ': 'Invesco QQQ Trust, NASDAQ 100 Index ETF',
    'VOO': 'Vanguard S&P 500 ETF',
    'VTI': 'Vanguard Total Stock Market Index Fund ETF Shares',
    'VWO': 'Vanguard Emerging Markets Stock Index Fund',
    'XLF': 'The Financial Select Sector SPDR Fund',
    'AAXJ': 'iShares MSCI All Country Asia ex Japan ETF',
    'IEUR': 'iShares Core MSCI Europe ETF'
}

# NOTE: Dow Jones tickers will be downloaded from url, no need to include these below
djia_components = {
    'AAPL': 'Apple Inc.',
    'AMGN': 'Amgen Inc.',
    'AMZN': 'Amazon.com, Inc.',
    'AXP': 'American Express Company',
    'BA': 'The Boeing Company',
    'CAT': 'Caterpillar, Inc.',
    'CRM': 'Salesforce, Inc.',
    'CSCO': 'Cisco Systems, Inc.',
    'CVX': 'Chevron Corporation',
    'DIS': 'The Walt Disney Company',
    'DOW': 'Dow Inc.',
    'GS': 'The Goldman Sachs Group, Inc.',
    'HD': 'The Home Depot, Inc.',
    'HON': 'Honeywell International Inc.',
    'IBM': 'International Business Machines Corporation',
    'INTC': 'Intel Corporation',
    'JNJ': 'Johnson & Johnson',
    'JPM': 'JP Morgan Chase & Co.',
    'KO': 'The Coca-Cola Company',
    'MCD': 'McDonald\'s Corporation',
    'MMM': '3M Company',
    'MRK': 'Merck & Company, Inc.',
    'MSFT': 'Microsoft Corporation',
    'NKE': 'Nike, Inc.',
    'PG': 'The Procter & Gamble Company',
    'TRV': 'The Travelers Companies, Inc.',
    'UNH': 'UnitedHealth Group Incorporated',
    'V': 'Visa Inc.',
    'VZ': 'Verizon Communications Inc.',
    'WMT': 'Walmart Inc.'
}

# Top 50 crypotocurrencies by market cap (current price x circulating amount)
# as of July 10th, 2024
# NOTE: Do not include the tickers below in the app menu, as they will be downloaded from url

crypto_tickers = {
    'BTC-USD': 'Bitcoin USD',
    'ETH-USD': 'Ethereum USD',
    'USDT-USD': 'Tether USD',
    'BNB-USD': 'BNB USD',
    'SOL-USD': 'Solana USD',
    'USDC-USD': 'USDC USD',
    'XRP-USD': 'XRP USD',
    'TON-USD': 'Tokamak Network USD',
    'DOGE-USD': 'Dogecoin USD',
    'ADA-USD': 'Cardano USD',
    'TRX-USD': 'TRON USD',
    'WBTC-USD': 'Wrapped Bitcoin',
    'AVAX-USD': 'Avalanche USD',
    'SHIB-USD': 'Shiba Inu USD',
    'DOT-USD': 'Polkadot USD',
    'LINK-USD': 'Chainlink USD',
    'BCH-USD': 'Bitcoin Cash USD',
    'DAI-USD': 'Dai USD',
    'LEO-USD': 'UNUS SED LEO USD',
    'NEAR-USD': 'NEAR Protocol USD',
    'MATIC-USD': 'Polygon USD',
    'UNI7083-USD': 'Uniswap USD',  # NOTE: UNI-USD is UNICORN Token USD in Yahoo!Finance
    'LTC-USD': 'Litecoin USD',
    'WEETH-USD': 'Wrapped eETH',
    'KAS-USD': 'Kaspa USD',
    'PEPE24478-USD': 'Pepe USD',  # NOTE: PEPE-USD is PEPEGOLD, a different cryptocurrency launched in 2024
    'ICP-USD': 'Internet Computer USD',
    'USDE-USD': 'Energi Dollar USD',
    'ETC-USD': 'Ethereum Classic USD',
    'FET-USD': 'Artificial Superintelligence Alliance USD',
    'XMR-USD': 'Monero USD',
    'WBETH-USD': 'Wrapped Beacon ETH USD',
    'APT-USD': 'Apricot Finance USD',
    'XLM-USD': 'Stellar USD',
    'RNDR-USD': 'Render USD',
    'HBAR-USD': 'Hedera USD',
    'ATOM-USD': 'Cosmos USD',
    'CRO-USD': 'Cronos USD',
    'OKB-USD': 'OKB USD',
    'ARB11841-USD': 'Arbitrum USD',  # NOTE: ARB-USD is ARbit USD in Yahoo!Finance)
    'MNT27075-USD': 'Mantle USD',  # NOTE: MNT-USD is microNFT USD in Yahoo!Finance
    'MKR-USD': 'Maker USD',
    'STX4847-USD': 'Stacks USD',  # NOTE: STX-USD is stox USD in Yahoo!Finance
    'FDUSD-USD': 'First Digital USD USD',
    'VET-USD': 'VeChain USD',
    'IMX10603-USD': 'Immutable USD',  # NOTE: IMX-USD is Impermax USD in Yahoo!Finance
    'INJ-USD': 'Injective USD',
    'SUI20947-USD': 'Sui USD',  # NOTE: SUI-USD is Salmonation USD in Yahoo!Finance
    'WIF-USD': 'dogwifhat USD',
    'GRT6719-USD': 'The Graph USD',  # NOTE: GRT-USD is Golden Ratio Token USD in Yahoo!Finance)
    'NOT-USD': 'Notcoin USD',
    'TAO22974-USD':'TaoPad USD (part of Bittensor network)',
    'OP-USD': 'Optimism USD',
    'BONK-USD': 'Bonk USD'
}

### YouTube Portfolio Optimization example by Ryan O'Connell ###
# https://www.youtube.com/watch?v=9GA2WlYFeBU

yt_example_tickers = {
    'SPY': 'SPDR S&P 500 ETF Trust',
    'BND': 'Vanguard Total Bond Market Index Fund',
    'GLD': 'SPDR Gold Shares',
    'QQQ': 'Invesco QQQ Trust',
    'VTI': 'Vanguard Total Stock Market Index Fund ETF Shares'
}