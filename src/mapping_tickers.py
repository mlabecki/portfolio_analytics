### URL TO YFINANCE TICKER MAP ###
# Some websites may use tickers that differ from the YF tickers, hence the following map
# The keys are tickers on the websites, values are YF tickers
url_to_yf_ticker_map = {
    'BRK.B': 'BRK-B'
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

# VOLATILITY ###
volatility_tickers = {
    '^VIX': 'CBOE Volatility Index',
    '^VXD': 'DJIA VOLATILITY',
    '^VXN': 'CBOE NASDAQ 100 Volatility',
    '^MOVE': 'ICE BofAML MOVE (Merrill Lynch Option Volatility Estimate) Index',
    '^GVZ': 'CBOE Gold Volatility Index'
}

# NOTE: Allow mixing of valatility tickers with any other tickers in the app menu

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
    'DBA':      'Invesco DB Agriculture Fund'
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