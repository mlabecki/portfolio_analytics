### URL TO YFINANCE TICKER MAP ###
# Some websites may use tickers that differ from the YF tickers, hence the following map
# The keys are tickers on the websites, values are YF tickers
url_to_yf_ticker_map = {
    'BRK.B': 'BRK-B'
}

indices_custom_info = {
    '^GSPC': {
        'category': 'Stock Large Cap',
        'description': 
            """The Standard and Poor's 500, or simply the S&P 500, is a stock market index tracking the stock
            performance of 500 of the largest companies listed on stock exchanges in the United States. It is 
            one of the most commonly followed equity indices and includes approximately 80% of the total market
            cap of U.S. public companies, with more than $50 trillion aggregate market cap as of December 2024.
            """
    },
    '^GSPTSE': {
        'category': 'Stock Large Cap',
        'description': 
        """The S&P/TSX Composite Index has provided investors with a premier indicator of market activity for Canadian 
        equity markets since its launch in 1977. With approximately 95% coverage of the Canadian equities market, 
        it is the primary gauge for Canadian-based, Toronto Stock Exchange (TSX) listed companies, representing roughly 
        70% of the total market capitalization on the TSX. It is designed to serve a dual purpose, offering both the 
        representation of a broad benchmark index while maintaining the liquidity characteristics of narrower indices. 
        This unique combination makes the S&P/TSX Composite Index ideal for portfolio management and index replication.
        """
    },
    '^DJI': {
        'category': 'Stock Large Cap',
        'description': 
        """The Dow Jones Industrial Average, Dow Jones, or simply the Dow, is a stock market index of 30 publicly-owned companies
        listed on the NASDAQ or the New York Stock Exchange (NYSE). The DJIA is one of the oldest and most commonly followed equity indexes,
        created in 1896 by the Dow & Jones Company founder and Wall Street Journal editor Charles Dow. Initially comprised of only 12 US 
        industrial companies, it has changed over the years, now including companies in other sectors such as technology, health, and retail. 
        The index is price-weighted, unlike other common indexes such as the Nasdaq Composite or S&P 500, which use market capitalization.
        """
    },
    '^IXIC': {
        'category': 'Stock Large Cap',
        'description': 
        """The NASDAQ Composite is a stock market index that includes over 3,000 stocks listed on the Nasdaq stock exchange. 
        Its composition is heavily weighted towards companies in the technology sector, which represent almost half of its total market cap.
        Consumer services rank second in the weightage order, with about 20% market cap; health care third with about 10%; consumer goods,
        financials, and industrials, coming next with allocations of about 6-8%; followed by utilities, oil & gas, basic materials, 
        and telecommunications, each having weights of less than 1%. In terms of the number of companies from a specific industry, 
        health care clearly dominates with more than 900 companies.
        """
    },
    '^NDX': {
        'category': 'Stock Large Cap',
        'description': 
        """The NASDAQ 100 is a stock market index made up of equity securities issued by 100 of the largest non-financial companies listed on the 
        Nasdaq stock exchange. It was launched in 1985 by the National Associate of Securities Dealers (NASD), alongside its sister index
        NASDAQ Financial 100. It includes companies in areas such as industrial, technology, retail, telecommunication, biotechnology, health care, 
        transportation, and media.
        """
    },
    '^IXF': {
        'category': 'Stock Large Cap',
        'description': 
        """The NASDAQ Financial 100 is a stock market index made up of equity securities issued by 100 of the largest financial companies listed on the 
        Nasdaq stock exchange. It was launched in 1985 by the National Associate of Securities Dealers (NASD), alongside its more widely followed 
        sister index NASDAQ 100. NASDAQ Financial 100 covers areas such as banking, insurance, mortgages and securities trading.
        """
    },
    '^NYA': {
        'category': 'Stock Large Cap',
        'description': 
        """The NYSE Composite is a stock market index covering all common stock listed on the New York Stock Exchange, including American depositary receipts (ADRs),
        real estate investment trusts, tracking stocks, and foreign listings. It covers over 2,000 stocks, of which over 1,600 are from the U.S. corporations and 
        over 360 are foreign listings. However, foreign companies constitute over a half of the largest companies in the index by market capitalization. 
        The index uses free-float market cap weighting.
        """
    },
    '^RUT': {
        'category': 'Small Cap Stock',
        'description': 
        """The Russell 2000 Index is a U.S. stock market index that makes up the smallest 2,000 stocks in the Russell Index. It was started
        in 1984 by the Frank Russell Company and is maintained by FTSE Russell, a subsidiary of the London Stock Exchange Group (LSEG). 
        Russell 2000 is by far the most common benchmark for small-cap mutual funds and is the most widely quoted measure of the overall 
        performance of small- to mid-cap company shares. It is commonly considered an indicator of the condition of the U.S. economy because of
        its focus on small companies in the U.S. market. Russell 2000 represents approximately 7% of the total market cap of the Russell 3000 Index.
        """
    },
    '^HSI': {
        'category': 'Stock Large Cap',
        'description': 
        """The Hang Seng Index (HSI) is a market cap weighted stock market index, adjusted for free float, that tracks and records daily changes
        in the largest companies listed on the Hong Kong Stock Exchange (HKSE). There are 82 constituent companies of the index, representing over 
        a half of the HKSE market cap. HSI was publicized in 1969 and is currently compiled and maintained by Hang Seng Indexes Company Limited, 
        a wholly owned subsidiary of Hang Seng Bank, one of the largest banks registered and listed in Hong Kong in terms of market cap.
        """
    },
    '^N225': {
        'category': 'Stock Large Cap',
        'description': 
        """The Nikkei 225, or the Nikkei Stock Average, is a stock market index for the Tokyo Stock Exchange (TSE), measuring the performance 
        of 225 highly capitalized and liquid publicly owned companies in Japan from a wide array of industry sectors. It is a price-weighted index,
        calculated every five seconds and operating in the Japanese Yen. Its components are reviewed twice a year. 
        """
    },
    '^FTSE': {
        'category': 'Stock Large Cap',
        'description': 
        """The Financial Times Stock Exchange 100 Index (FTSE 100 or, informally, 'Footsie') is the UK's best-known stock market index of the 100 
        most highly capitalized blue chips listed on the London Stock Exchange (LSE). The index consists of 32 sectors, four of which account 
        for almost a half of the index's market cap - these are pharmaceuticals, oil & gas, metals & mining, and banking services.
        The major companies, together accounting for approximately 30% of the market cap, are Shell, AstraZeneca, HSBC and Unilever.
        The FTSE's constituents are reviewed each calendar quarter, with some companies exiting or entering the index.
        FTSE 100 is calculated in real time and published every second when the market is open.
        """
    },
    '^GDAXI': {
        'category': 'Stock Large Cap',
        'description': 
        """The DAX index tracks the performance of the 40 largest companies listed on the Regulated Market of the Frankfurt Stock
        Exchange (FSE) that fulfill the requirements of being representative of Germany's diversified economy. Constituent 
        selection is based on free-float market capitalization. The DAX has two versions - the more commonly quoted performance index that 
        measures total return, thus including dividends; and the price index, which is more similar to commonly quoted indices in other countries.
        The German benchmark is a popular underlying for ETFs, exchange-traded derivatives and investment certificates.
        """
    },
    '^IBEX': {
        'category': 'Stock Large Cap',
        'description': 
        """The IBEX 35 (IBerian IndEX) is the benchmark stock market index of the Bolsa de Madrid, Spain's principal stock exchange. 
        Initiated in 1992, the index is administered and calculated by Sociedad de Bolsas, a subsidiary of Bolsas y Mercados Españoles
        (BME), the company which runs Spain's securities markets (including the Bolsa de Madrid). It is a market cap 
        weighted index comprising the 35 most liquid Spanish stocks traded in the Madrid Stock Exchange General Index and is reviewed 
        twice annually. Trading on options and futures contracts on the IBEX 35 is provided by MEFF (Mercado Español de Futuros 
        Financieros), another subsidiary of BME.
        """
    },
    '^FCHI': {
        'category': 'Stock Large Cap',
        'description': 
        """CAC 40 is a benchmark French stock market index that tracks the performance of the 40 largest and most active 
        companies listed on the Euronext Paris stock exchange. Its name - Cotation Assistée en Continu or Continuous 
        Assisted Quotation - refers to an automation system that is a version of the Toronto-based first ever fully 
        automated trading system in the world. CAC 40 is a price return index and as such pays no dividends, interest, 
        rights offerings or similar profit distributions. The index operates every working day from 9:00 am to 5:30 pm 
        and is updated every 15 seconds. Its composition is reviewed quarterly by an independent Index Steering Committee.
        """
    },
    '^STOXX': {
        'category': 'Stock Large Cap',
        'description': 
        """STOXX Europe 600 is an index of European stocks designed and introduced by STOXX Ltd in 1998. It has 
        a fixed number of 600 components representing large, mid and small capitalization companies among 17 
        European countries (not limited to the Eurozone) and covers about 90% of the European stock free-float market cap.
        The major countries of the index, contributing over two-thirds of it, are the UK, France, Switzerland and Germany. 
        The other participating countries are Austria, Belgium, Denmark, Finland, Ireland, Italy, Luxembourg, 
        the Netherlands, Norway, Poland, Portugal, Spain, and Sweden. STOXX Europe 600 is available in multiple currency 
        (AUD, CAD, CHF, EUR, GBP, JPY, USD) and return (Price, Net Return, Gross Return) combinations. 
        Its composition is reviewed quarterly. 
        """
    },
    '^AXJO': {
        'category': 'Stock all but Micro Cap',
        'description': 
        """The S&P/ASX 200 index is a market-capitalisation weighted and float-adjusted stock market index of shares listed on the Australian Securities Exchange (ASX). 
        It was started in 2000 and has since been maintained by Standard & Poor's. It is based on the 200 largest ASX listed stocks, which together account for more 
        than 80% of Australia's share market capitalisation. S&P/ASX 200 is considered the benchmark for Australian equity performance. 
        """
    },
    '000001.SS': {
        'category': 'Stock Large Cap',
        'description': 
        """The SSE Composite Index is a stock market index of all stocks traded at the Shanghai Stock Exchange (SSE).
        It is considered to be a broad indicator of the condition of the Chinese economy, assessing its performance 
        at the level of a variety of sectors and companies.
        """
    },
    '^KS11': {
        'category': 'Stock Large Cap',
        'description': 
        """The Korea Composite Stock Price Index (KOSPI) tracks all common stocks traded on the Korea Stock Exchange,
        similarly to the S&P 500 in the United States. KOSPI was introduced in 1983, replacing the Dow-style Korea
        Composite Stock Price Index.
        """
    },
    '^BSESN': {
        'category': 'Stock Large Cap',
        'description': 
        """The BSE SENSEX, also known as the S&P Bombay Stock Exchange Sensitive Index or simply SENSEX, tracks the performance of 30
        major companies representative of various industrial sectors of the Indian economy and listed on the Bombay Stock Exchange.
        """
    },
    '^VIX': {
        'category': 'Stock Volatility',
        'description': 
        """The CBOE Volatility Index (VIX) is a popular measure of the stock market's expectation of volatility, calculated and disseminated 
        in real time by CBOE. It is derived from the S&P 500 option prices for the 30 days following the measurement date, with each option price 
        representing the market's expectation of the 30-day forward-looking volatility. VIX cannot be bought or sold directly; instead, it can be
        traded and exchanged via derivative contracts, derived ETFs, and ETNs which most commonly track VIX futures indexes.
        """
    },
    '^VXD': {
        'category': 'Stock Volatility',
        'description': 
        """The CBOE DJIA Volatility Index is an estimate of the expected 30-day volatility of Dow Jones Industrial Avedrage (DJIA) stock index returns. 
        Similarly to VIX, VXD is calculated based on the 30-day forward-looking DJIA option prices.
        """
    },
    '^VXN': {
        'category': 'Stock Volatility',
        'description': 
        """The CBOE NASDAQ 100 Volatility Index is a key measure of market expectations of near-term volatility conveyed by NASDAQ 100 Index option prices.
        It measures the market's expectation of 30-day volatility implicit in the prices of near-term NASDAQ 100 options.
        """
    },
    '^MOVE': {
        'category': 'Bond Volatility',
        'description': 
        """The Intercontinental Exchange (ICE) Bank of America Merrill Lynch Option Volatility Estimate (MOVE) index is a measure of the 
        expected volatility of US Treasury bonds. It is calculated by taking the weighted average of the implied volatilities of a range of 
        options on US Treasury bonds. The index is expressed in basis points (bps) and is published by ICE Benchmark Administration Ltd.
        """
    },
    '^GVZ': {
        'category': 'Commodity Volatility',
        'description': 
        """The CBOE Gold ETF Volatility Index is an estimate of the expected 30-day volatility of returns on the SPDR Gold Shares ETF (GLD). 
        Similarly to VIX, GVZ is calculated based on the 30-day forward-looking prices of GLD options.
        """
    },
    '^SPGSCI': {
        'category': 'Commodities Broad Basket',
        'description': 
        """The S&P GSCI, originally developed in 1991 by Goldman Sachs, serves as a benchmark for investment in the commodity markets
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
        """The Bloomberg Commodity Index (BCOM) is a broadly diversified commodity price index tracking prices of futures 
        contracts on physical commodities. It was originally launched as the Dow Jones-AIG Commodity Index in 1998; later renamed
        to Dow Jones-UBS Commodity Index in 2009, when UBS acquired it from AIG; and finally rebranded under its current name in 2014. 
        The BCOM is designed to minimize concentration in any one commodity or sector - it currently includes 23 commodity 
        futures in six sectors.
        """
    },
    '^TNX': {
        'category': 'Treasury Bond',
        'description': 
        """The CBOE Interest Rate 10-Year Treasury Note Index (TNX) is a benchmark index that tracks the yield of U.S. Treasury
        10-year notes. It is often considered to be a risk-free investment because of its backing by the U.S. government.
        """
    },
    '^IRX': {
        'category': 'Treasury Bond',
        'description': 
        """The 13-Week Treasury Bill Index is a benchmark index that tracks the yield of U.S. Treasury 13-week bills.
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
    '^MOVE':    'ICE BofAML MOVE Index',
    '^SPGSCI':  'S&P GSCI Index',
    '^BCOM':    'BBG Commodity Index',
    'GLD':      'SPDR Gold Trust',
    'DBC':      'Invesco DB Commodity Index Tracking Fund',
    'GSG':      'iShares S&P GSCI Commodity-Indexed Trust',
    'BND':      'Vanguard Total Bond Market Index Fund',
    'AGG':      'iShares Core U.S. Aggregate Bond ETF',    
    '^TNX':     '10-Year US Treasury Note',
    '^IRX':     '3-Month US Treasury Bill',
    'IBIT':     'iShares Bitcoin Trust',
    'GBTC':     'Grayscale Bitcoin Trust ETF'
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
bond_etfs = {
    'BND': 'Vanguard Total Bond Market Index Fund',
    'AGG': 'iShares Core U.S. Aggregate Bond ETF',
    'BNDX': 'Vanguard Total International Bond ETF',
    'BSV': 'Vanguard Short-Term Bond Index Fund ETF Shares',  # 58.2
    'TLT': 'iShares 20+ Year Treasury Bond ETF', # 53.4
    'VCIT': 'Vanguard Intermediate-Term Corporate Bond Index Fund ETF Shares', # 50.4
    'BIV': 'Vanguard Intermediate-Term Bond ETF', # 43.1
    'VCSH': 'Vanguard Short-Term Corporate Bond Index Fund ETF Shares', # 41.6
    'MUB': 'iShares National Muni Bond ETF', # 40.5
    'VTEB': 'Vanguard Tax-Exempt Bond Index Fund ETF Shares', # 38.8
    'VGIT': 'Vanguard Intermediate-Term Treasury Index Fund ETF Shares', # 38.35
    'BIL': 'SPDR Bloomberg 1-3 Month T-Bill ETF', # 36.8
    'MBB': 'iShares MBS ETF', # 36.6
    'IUSB': 'iShares Core Total USD Bond Market ETF', # 32.32
    'SGOV': 'iShares 0-3 Month Treasury Bond ETF', # 32.29
    'IEF': 'iShares 7-10 Year Treasury Bond ETF', # 32.0
    'LQD': 'iShares iBoxx $ Investment Grade Corporate Bond ETF', # 30.0
    'GOVT': 'iShares U.S. Treasury Bond ETF', # 29.8
    'JPST': 'JPMorgan Ultra-Short Income ETF', # 28.8
    'VGSH': 'Vanguard Short-Term Treasury Index Fund ETF Shares', # 25.7
    'SHY': 'iShares 1-3 Year Treasury Bond ETF', # 23.2
    'VMBS': 'Vanguard Mortgage-Backed Securities Index Fund ETF Shares', # 21.25
    'IGSB': 'iShares 1-5 Year Investment Grade Corporate Bond ETF', # 21.2
    'JAAA': 'Janus Henderson AAA CLO ETF', # 19.9
    'SHV': 'iShares Short Treasury Bond ETF', # 19.07
    'FBND': 'Fidelity Total Bond ETF', # 17.3
    'MINT': 'PIMCO Enhanced Short Maturity Active Exchange-Traded Fund', # 12.3
    'PULS': 'PGIM Ultra Short Bond ETF', # 9.83
    'SCHZ': 'Schwab U.S. Aggregate Bond ETF', # 8.51
    'BLV': 'Vanguard Long-Term Bond ETF', # 8.22
    'SPAB': 'SPDR Portfolio Aggregate Bond ETF', # 8.17
    'IAGG': 'iShares Core International Aggregate Bond ETF', # 7.05
    'FTSM': 'First Trust Enhanced Short Maturity ETF', # 6.24
    'DFCF': 'Dimensional Core Fixed Income ETF', # 6.06
    'JCPB': 'JPMorgan Core Plus Bond ETF', # 5.26
    'BOND': 'PIMCO Active Bond Exchange-Traded Fund', # 5.20
    'FIXD': 'First Trust TCW Opportunistic Fixed Income ETF', # 4.39
    'ISTB': 'iShares Core 1-5 Year USD Bond ETF', # 4.28
    'CGCP': 'Capital Group Core Plus Income ETF', # 4.25
    'EAGG': 'iShares ESG Aware US Aggregate Bond ETF', # 3.68
    'UCON': 'First Trust TCW Unconstrained Plus Bond ETF', # 3.43
    'TOTL': 'SPDR DoubleLine Total Return Tactical ETF', # 3.41
    'PYLD': 'PIMCO Multisector Bond Active Exchange-Traded Fund', # 3.30
    'GVI': 'iShares Intermediate Government/Credit Bond ETF', # 3.28
    'JMST': 'JPMorgan Ultra-Short Municipal Income ETF', # 3.25
    'NEAR': 'iShares Short Duration Bond Active ETF', # 3.05
    'JPIE': 'JPMorgan Income ETF', # 2.69
    'FLCB': 'Franklin U.S. Core Bond ETF', # 2.35
    'UITB': 'VictoryShares Core Intermediate Bond ETF', # 2.34
    'JMUB': 'JPMorgan Municipal ETF', # 2.31
    # 'HTRB': 'Hartford Total Return Bond ETF', # 1.98
    # 'BKAG': 'BNY Mellon Core Bond ETF', # 1.97
    # 'GTO': 'Invesco Total Return Bond ETF', # 1.84
    # 'BBAG': 'JPMorgan BetaBuilders U.S. Aggregate Bond ETF', # 1.45
    # 'SMTH': 'ALPS Smith Core Plus Bond ETF', # 1.41
    # 'VRIG': 'Invesco Variable Rate Investment Grade ETF', # 1.23
    # 'RAVI': 'FlexShares Ultra-Short Income Fund', # 1.20
    # 'BNDW': 'Vanguard Total World Bond ETF', # 1.08
    # 'USTB': 'VictoryShares Short-Term Bond ETF', # 0.97
    # 'AVIG': 'Avantis Core Fixed Income ETF', # 0.96
    # 'AGGY': 'WisdomTree Yield Enhanced U.S. Aggregate Bond Fund', # 0.90
    # 'LDUR': 'PIMCO Enhanced Low Duration Active ETF', # 0.86
    # 'PCEF': 'Invesco CEF Income Composite ETF', # 0.84
    # 'AGZ': 'iShares Agency Bond ETF', # 0.70
    # 'EUSB': 'iShares ESG Advanced Total USD Bond Market ETF', # 0.68
    # 'ILTB': 'iShares Core 10+ Year USD Bond ETF', # 0.60
    # 'AVSF': 'Avantis Short-Term Fixed Income ETF', # 0.59
    # 'UBND': 'VictoryShares Core Plus Intermediate Bond ETF', # 0.58
    # 'JSCP': 'JPMorgan Short Duration Core Plus ETF', # 0.57
    # 'ULST': 'SPDR SSgA Ultra Short Term Bond ETF', # 0.56
    # 'JPIB': 'JPMorgan International Bond Opportunities ETF' # 0.55
}

### PRECIOUS METAL FUTURES ###
precious_metals = {
    'GC=F': 'Gold (CMX)',
    'SI=F': 'Silver (CMX)',
    'HG=F': 'Copper (CMX)',
    'PL=F': 'Platinum (NYM)',
    'PA=F': 'Palladium (NYM)'
}

### RARE METALS COMPANIES and FUNDS ###
rare_metals_companies = {
    # Sorted by marketCap from YF
    # Source: 
    #   1. https://finance.yahoo.com/news/14-best-rare-earth-stocks-181008216.html
    #   2. https://investingnews.com/top-rare-earth-stocks/
    #
    # NOTE: Must convert CAD and AUD to USD for market cap comparison
    #   
    # cadusd = yf.download('CAD=X', start = datetime.today(), progress = False)['Close'].iloc[0].values[0]
    # audusd = yf.download('AUD=X', start = datetime.today(), progress = False)['Close'].iloc[0].values[0]
    #
    'SCCO': 'Southern Copper Corporation',
    'SQM': 'Sociedad Química y Minera de Chile S.A.',
    'LYC.AX': 'Lynas Rare Earths Limited',  #  currency is AUD
    'MP': 'MP Materials Corp.',
    'SBSW': 'Sibanye Stillwater Limited',
    'ILU.AX': 'Iluka Resources Limited',  #  currency is AUD
    'CSTM': 'Constellium SE',
    'TROX': 'Tronox Holdings plc',
    'UUUU': 'Energy Fuels Inc.',
    'NEO.TO': 'Neo Performance Materials Inc.',  # currency is CAD
    'ARU.AX': 'Arafura Rare Earths Limited',    # currency is AUD
    'NB': 'NioCorp Developments Ltd.',
    'ARA.TO': 'Aclara Resources Inc.',  #  currency is CAD
    'MKA.V': 'Mkango Resources Ltd.',   #  currency is CAD
    'UCU.V': 'Ucore Rare Metals Inc.',  #  currency is CAD
    'LICY': 'Li-Cycle Holdings Corp.'
}

rare_metals_etfs_tickers = {
    # Sorted by totalAssets from YF
    # Source: 
    #   https://finance.yahoo.com/news/14-best-rare-earth-stocks-181008216.html
    #
    'PICK': 'iShares MSCI Global Metals & Mining Producers ETF',
    'REMX': 'VanEck Rare Earth and Strategic Metals ETF',
    'HURA.TO': 'Global X Uranium Index ETF'
}

### CAR COMPANIES ###
# Sorted by Market Cap as of 20/02/2025
# Source:
#   https://companiesmarketcap.com/cad/automakers/largest-automakers-by-market-cap/
# Names corrected to use YF longName instead
#
car_companies = {
    'TSLA': 'Tesla, Inc.',
    'TM': 'Toyota Motor Corporation',
    'XIACF': 'Xiaomi Corporation',
    '002594.SZ': 'BYD Company Limited',
    'RACE': 'Ferrari N.V.',
    'MBG.DE': 'Mercedes-Benz Group AG',
    'P911.DE': 'Dr. Ing. h.c. F. Porsche AG',
    'BMW.DE': 'Bayerische Motoren Werke Aktiengesellschaft',
    'VOW3.DE': 'Volkswagen AG',
    'GM': 'General Motors Company',
    'MARUTI.NS': 'Maruti Suzuki India Limited',
    'STLA': 'Stellantis N.V.',
    'HMC': 'Honda Motor Co., Ltd.',
    'M&M.NS': 'Mahindra & Mahindra Limited',
    'F': 'Ford Motor Company',
    'HYMTF': 'Hyundai Motor Company',
    'TATAMOTORS.NS': 'Tata Motors Limited',
    'LI': 'Li Auto Inc.',
    '600104.SS': 'SAIC MOTOR',
    '000270.KS': 'Kia Corporation',
    '601127.SS': 'Seres Group Co.,Ltd',
    '601633.SS': 'Great Wall Motor Company Limited',
    '7269.T': 'Suzuki Motor Corporation',
    '0175.HK': 'GEELY AUTO',
    'XPEV': 'XPeng Inc.',
    '000625.SZ': 'Chongqing Changan Automobile Company Limited',
    'RNO.PA': 'Renault SA',
    'RIVN': 'Rivian Automotive, Inc.',
    '7270.T': 'Subaru Corporation',
    '601238.SS': 'Guangzhou Automobile Group Co., Ltd.',
    '600418.SS': 'JIANGHUAI AUTO',
    '2207.TW': 'Hotai Motor Co.,Ltd.',
    'LCID': 'Lucid Group, Inc.',
    '7201.T': 'Nissan Motor Co., Ltd.',
    '7202.T': 'Isuzu Motors Limited',
    'NIO': 'NIO Inc.',
    'VFS': 'VinFast Auto Ltd.',
    'FROTO.IS': 'Ford Otomotiv Sanayi A.S.',
    'VOLCAR-B.ST': 'Volvo Car AB (publ.)',
    'ZK': 'ZEEKR Intelligent Technology Holding Limited',
    '000800.SZ': 'FAW Jiefang Group Co.,Ltd',
    '9863.HK': 'Zhejiang Leapmotor Technology Co., Ltd.',
    '0489.HK': 'DONGFENG GROUP',
    '7261.T': 'Mazda Motor Corporation',
    '7211.T': 'Mitsubishi Motors Corporation',
    'TOASO.IS': 'Tofas Türk Otomobil Fabrikasi Anonim Sirketi',
    'PII': 'Polaris Inc.',
    'PSNY': 'Polestar Automotive Holding UK PLC',
    'LOT': 'Lotus Technology Inc.',
    '2201.TW': 'Yulon Motor Company Ltd.',
    'AML.L': 'Aston Martin Lagonda Global Holdings plc',
    'FORCEMOT.NS': 'Force Motors Limited',
    '003620.KS': 'KG Mobility Corp.',
    'NWTN': 'NWTN Inc.',
    'REE': 'REE Automotive Ltd.',
    'KNDI': 'Kandi Technologies Group, Inc.',
    'NKLA': 'Nikola Corporation',
    'FFIE': 'Faraday Future Intelligent Electric Inc.',
    'CENN': 'Cenntro Inc.',
    'PEV': 'Phoenix Motor Inc.',
    'MULN': 'Mullen Automotive, Inc.',
    'GOEV': 'Canoo Inc.',
    'FUVV': 'Arcimoto, Inc.'
}

quantum_companies_unsorted = {
    # Source: https://quantumzeitgeist.com/public-quantum-computing-companies/
    'RGTI': 'Rigetti Computing, Inc.',
    'QUBT': 'Quantum Computing Inc.',
    'QBTS': 'D-Wave Quantum Inc.',
    'IONQ': 'IonQ, Inc.',
    'ZPTA': 'Zapata Computing Holdings Inc.',
    'HON': 'Honeywell International Inc.',
    'IBM': 'International Business Machines Corporation',
    'GOOG': 'Alphabet Inc.',
    'MSFT': 'Microsoft Corporation',
    'AMZN': 'Amazon.com, Inc.',
    'NVDA': 'NVIDIA Corporation',
    'INTC': 'Intel Corporation',
    'BABA': 'Alibaba Group Holding Limited',
    'RTX': 'Raytheon Technologies Corporation',
    '6701.T': 'NEC Corporation',
    '6702.T': 'Fujitsu Limited',
    '6588.T': 'Toshiba Tec Corporation',
    # Source: https://quantumcomputingreport.com/public-companies/
    'QNCCF': 'Quantum eMotion Corp.',
    'FCCN': 'Spectral Capital Corporation',
    'REYM.XC': 'Reply S.p.A.',
    'MPHASIS.NS': 'Mphasis Limited',
    'MIELY': 'Mitsubishi Electric Corporation',
    'LMT': 'Lockheed Martin Corporation',
    'IFX.DE': 'Infineon Technologies AG',
    'CSCO': 'Cisco Systems, Inc.',
    'BTQQF': 'BTQ Technologies Corp.',
    'BAH': 'Booz Allen Hamilton Holding Corporation',
    'BIDU': 'Baidu, Inc.',
    'T': 'AT&T Inc.',
    'ARQQ': 'Arqit Quantum Inc.',
    'AXE.AX': 'Archer Materials Limited',
    'AIR.PA': 'Airbus SE',
    'ACN': 'Accenture plc',
    'OONEF': '01 Communique Laboratory Inc.',
    # Source: https://greenstocknews.com/stocks/quantum-computing-stocks/
    'QMCO': 'Quantum Corporation',
    # Source: https://www.fool.com/investing/stock-market/market-sectors/information-technology/ai-stocks/quantum-computing-stocks/
    'FORM': 'FormFactor, Inc.',
    # Source: https://www.fool.com/investing/stock-market/market-sectors/information-technology/ai-stocks/quantum-computing-etf/
    'MSTR': 'MicroStrategy Incorporated',
    'MRVL': 'Marvell Technology, Inc.',
    'COHR': 'Coherent Corp.',
    'NTDTY': 'NTT DATA Group Corporation',
    'WIT': 'Wipro Limited',
    'TSEM': 'Tower Semiconductor Ltd.'
}

quantum_companies = {
    'NVDA': 'NVIDIA Corporation',
    'MSFT': 'Microsoft Corporation',
    'AMZN': 'Amazon.com, Inc.',
    'GOOG': 'Alphabet Inc.',
    'BABA': 'Alibaba Group Holding Limited',
    'CSCO': 'Cisco Systems, Inc.',
    'IBM': 'International Business Machines Corporation',
    'ACN': 'Accenture plc',
    'T': 'AT&T Inc.',
    'RTX': 'Raytheon Technologies Corporation',
    'AIR.PA': 'Airbus SE',
    'HON': 'Honeywell International Inc.',
    'LMT': 'Lockheed Martin Corporation',
    'INTC': 'Intel Corporation',
    'MRVL': 'Marvell Technology, Inc.',
    'MSTR': 'MicroStrategy Incorporated',
    'IFX.DE': 'Infineon Technologies AG',
    '6702.T': 'Fujitsu Limited',
    'WIT': 'Wipro Limited',
    'MIELY': 'Mitsubishi Electric Corporation',
    'BIDU': 'Baidu, Inc.',
    '6701.T': 'NEC Corporation',
    'NTDTY': 'NTT DATA Group Corporation',
    'BAH': 'Booz Allen Hamilton Holding Corporation',
    'COHR': 'Coherent Corp.',
    'REYM.XC': 'Reply S.p.A.',
    'IONQ': 'IonQ, Inc.',
    'MPHASIS.NS': 'Mphasis Limited',
    'TSEM': 'Tower Semiconductor Ltd.',
    'FORM': 'FormFactor, Inc.',
    'RGTI': 'Rigetti Computing, Inc.',
    'QBTS': 'D-Wave Quantum Inc.',
    '6588.T': 'Toshiba Tec Corporation',
    'QUBT': 'Quantum Computing Inc.',  # include in category popover Examples
    'BTQQF': 'BTQ Technologies Corp.',
    'FCCN': 'Spectral Capital Corporation',
    'ARQQ': 'Arqit Quantum Inc.',
    'QNCCF': 'Quantum eMotion Corp.',
    'QMCO': 'Quantum Corporation',
    'AXE.AX': 'Archer Materials Limited',
    'OONEF': '01 Communique Laboratory Inc.',
    'ZPTA': 'Zapata Computing Holdings Inc.'
}

### MIXED COMMODITIES (other than precious metals) ###
# Source:
#   1. https://etfdb.com/etfdb-category/commodities/
#   2. https://etfdb.com/etfdb-category/oil-gas/
#   3. https://etfdb.com/etfdb-category/agricultural-commodities/
#   4. https://etfdb.com/etfdb-category/metals/
#
commodity_etf_tickers = {
    'PDBC':     'Invesco Optimum Yield Diversified Commodity Strategy No K-1 ETF', # 4367 MM
    'FTGC':     'First Trust Global Tactical Commodity Strategy Fund', # 2378 MM
    'COPX':     'Global X Copper Miners ETF', # 2557 MM
    'DBC':      'Invesco DB Commodity Index Tracking Fund', # 1352 MM
    'BCI':      'abrdn Bloomberg All Commodity Strategy K-1 Free ETF', # 1294 MM
    'GSG':      'iShares S&P GSCI Commodity-Indexed Trust', # 1045 MM
    'USO':      'United States Oil Fund, LP', # 1016 MM
    'DBA':      'Invesco DB Agriculture Fund', # 863 MM
    'COMT':     'iShares GSCI Commodity Dynamic Roll Strategy ETF', # 698 MM
    'UNG':      'United States Natural Gas Fund, LP', # 610 MM
    'DJP':      'iPath Bloomberg Commodity Index', # 569 MM
    'UCO':      'ProShares Ultra Bloomberg Crude Oil', # 367 MM
    'CMDT':     'PIMCO Commodity Strategy Active Exchange-Traded Fund', # 359 MM
    'USOI':     'UBS ETRACS Crude Oil Shares Covered Call ETN', # 345 MM
    'CMDY':     'iShares Bloomberg Roll Select Broad Commodity ETF', # 284 MM
    'HGER':     'Harbor Commodity All-Weather Strategy ETF', # 278 MM
    'BOIL':     'ProShares Ultra Bloomberg Natural Gas', # 270 MM
    'BCD':      'abrdn Bloomberg All Commodity Longer Dated Strategy K-1 Free ETF', # 246 MM
    'COM':      'Direxion Auspice Broad Commodity Strategy ETF', # 244 MM
    'KRBN':     'KraneShares Global Carbon ETF', # 204 MM
    'USCI':     'United States Commodity Index Fund, LP', # 203 MM
    'NBCM':     'Neuberger Berman Commodity Strategy ETF', # 198 MM
    'DBO':      'Invesco DB Oil Fund', # 193 MM
    'CPER':     'United States Copper Index Fund', # 169 MM
    'GCC':      'WisdomTree Enhanced Commodity Strategy Fund', # 139 MM
    'DBB':      'Invesco DB Base Metals Fund', # 116 MM
    'KCCA':     'KraneShares California Carbon Allowance ETF', # 103 MM
    'UGA':      'United States Gasoline Fund, LP', # 102 MM
    'BNO':      'United States Brent Oil Fund, LP', # 101 MM
    'FAAR':     'First Trust Alternative Absolute Return Strategy ETF', # 98 MM
    'COMB':     'GraniteShares Bloomberg Commodity Broad Strategy No K-1 ETF', # 86 MM
    'SDCI':     'USCF SummerHaven Dynamic Commodity Strategy No K-1 Fund', # 81.1 MM
    'OILK':     'ProShares K-1 Free Crude Oil ETF', # 80.6 MM  
    'DBE':      'Invesco DB Energy Fund', # 54 MM
    'USL':      'United States 12 Month Oil Fund, LP', # 48 MM
    'BDRY':     'Breakwave Dry Bulk Shipping ETF', # 47 MM  
    'CCRV':     'iShares Commodity Curve Carry Strategy ETF', # 39 MM
    'PIT':      'VanEck Commodity Strategy ETF', # 29 MM
    'GRN':      'iPath Series B Carbon ETN', # 25.5 MM
    'UCIB':     'UBS ETRACS UBS Bloomberg Constant Maturity Commodity Index (CMCI) Total Return ETN Series B', # 25 MM
    'DCMT':     'DoubleLine Commodity Strategy ETF', # 24 MM
    'BCIM':     'abrdn Bloomberg Industrial Metals Strategy K-1 Free ETF', # 20 MM
    'UNL':      'United States 12 Month Natural Gas Fund, LP', # 16 MM
    'HCOM':     'Hartford Schroders Commodity Strategy ETF', # 10 MM
    'KEUA':     'KraneShares European Carbon Allowance Strategy ETF', # 10 MM
    'EVMT':     'Invesco Electric Vehicle Metals Commodity Strategy No K-1 ETF', # 7.4 MM
    'ZSB':      'USCF Sustainable Battery Metals Strategy Fund' # 1.3 MM
}

### PRECIOUS METAL ETFs ###
# Source: https://etfdb.com/etfdb-category/precious-metals/
# NOTE: Copper is not a precious metal, should be listed among commodities instead
precious_metal_etfs = {
    'GLD':      'SPDR Gold Shares', # 78.2
    'IAU':      'iShares Gold Trust', # 35.4
    'SLV':      'iShares Silver Trust', # 14.1
    'GDX':      'VanEck Gold Miners ETF', # 13.9
    'GLDM':     'SPDR Gold MiniShares', # 10.1
    'SGOL':     'abrdn Physical Gold Shares ETF', # 4.0
    'SIVR':     'Physical Silver Shares ETF', # 1.51
    'OUNZ':     'VanEck Merk Gold Trust', # 1.31
    'GLTR':     'abrdn Physical Precious Metals Basket Shares ETF', # 1.14
    'PPLT':     'abrdn Physical Platinum Shares ETF', # 1.06
    'AAAU':     'Goldman Sachs Physical Gold ETF', # 0.98
    'BAR':      'GraniteShares Gold Trust', # 0.91
    'PALL':     'abrdn Physical Palladium Shares ETF', # 0.35
    'SLVO':     'UBS ETRACS Silver Shares Covered Call ETN', # 0.18
    'DBP':      'Invesco DB Precious Metals Fund', # 0.16
    'IGLD':     'FT Vest Gold Strategy Target Income ETF', # 0.14
    'FGDL':     'Franklin Responsibly Sourced Gold ETF', # 0.12
    'GLDI':     'UBS ETRACS Gold Shares Covered Call ETN', # 0.11
    'BGLD':     'FT Vest Gold Strategy Quarterly Buffer ETF', # 0.056
    'PLTM':     'GraniteShares Platinum Trust' # 0.051
}

### NON-CRYPTO CURRENCY ETFS ###
# Source: https://etfdb.com/etfdb-category/currency/
currency_etf_tickers = {
    'FXY': 'Invesco Currencyshares Japanese Yen Trust', # 401 MM
    'UUP': 'Invesco DB US Dollar Index Bullish Fund', # 400 MM
    'USDU': 'WisdomTree Bloomberg U.S. Dollar Bullish Fund', # 304 MM
    'FXE': 'Invesco CurrencyShares Euro Trust', # 154 MM
    'FXF': 'Invesco CurrencyShares Swiss Franc Trust', # 132 MM
    'FXA': 'Invesco CurrencyShares Australian Dollar Trust', # 62 MM
    'FXC': 'Invesco CurrencyShares Canadian Dollar Trust', # 61 MM
    'FXB': 'Invesco CurrencyShares British Pound Sterling Trust', # 48 MM
    'UDN': 'Invesco DB US Dollar Index Bearish Fund',  # 47 MM
    'CEW': 'WisdomTree Emerging Currency Strategy Fund' # 6.9 MM
}

['FXY','UUP','USDU','FXE','FXF','FXC','FXA','FXB','UDN']

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