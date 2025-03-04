# Dictionaries
url_settings = {
    'global': {
        'headers': {'user-agent': 'Mozilla/5.0 (compatible; Windows NT 10.0; Win64; x64; MSIE 6.0; .NET CLR 1.0.3705) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    },
    'nasdaq100': {
        'category_name': 'NASDAQ 100 Companies',
        'url': 'https://stockanalysis.com/list/nasdaq-100-stocks/',
        'cols': ['Symbol', 'Company Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        # 'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'sp500': {
        'category_name': 'S&P 500 Companies',
        'url': 'https://stockanalysis.com/list/sp-500-stocks/',
        'cols': ['Symbol', 'Company Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        # 'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'dow_jones': {
        'category_name': 'Dow Jones Companies',
        'url': 'https://stockanalysis.com/list/dow-jones-stocks/',
        'cols': ['Symbol', 'Company Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        # 'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'biggest_companies': {
        'category_name': 'Biggest Companies',
        'url': 'https://stockanalysis.com/list/biggest-companies/',
        'cols': ['Symbol', 'Company Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        # 'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'car_companies': {
        'category_name': 'Car Companies',
        'url': 'https://companiesmarketcap.com/cad/automakers/largest-automakers-by-market-cap/',
        'cols': ['Name', 'Market Cap'],
        'cols_final': ['Name', 'Market Cap'],
        # 'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        # 'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap',
        'sort_by_factor': 1e6,
        'sort_by_type': float
    },
    'biggest_etfs': {
        'category_name': 'Biggest ETFs',
        'url': 'https://8marketcap.com/etfs/',
        'cols': ['Symbol', 'Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Name', 'Assets ($B)'],
        # NOTE: YF ETF's totalAssets are equivalent of Market Cap on this page
        'sort_by': 'Assets ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'crypto_etfs': {
        'category_name': 'Crypto ETFs',
        'url': 'https://stockanalysis.com/list/crypto-etfs/',
        'cols': ['Symbol', 'Fund Name', 'Assets'],
        # 'cols_final': ['Symbol', 'Fund Name', 'Assets ($MM)'],
        'cols_final': ['Symbol', 'Name', 'Assets ($MM)'],
        'sort_by': 'Assets ($MM)',
        'sort_by_factor': 1e6,
        'sort_by_type': float
    },
    # NOTE: Stock Analysis ETF lists were temporarily unavailable on March 3rd, 2025    
    # 'crypto_etfs': {
    #     'category_name': 'Crypto ETFs',
    #     'url': 'https://etfdb.com/etfs/currency/cryptocurrency/',
    #     'cols': [' Symbol ', ' ETF Name ', ' Total Assets* '],
    #     'cols_final': ['Symbol', 'Name', 'Assets ($MM)'],
    #     'sort_by': 'Assets ($MM)',
    #     'sort_by_factor': 1e6,
    #     'sort_by_type': float
    # },
    # NOTE: The Total Assets on the VettaFi page below do not agree with YF totalAssets.
    # This source is only included for comparison with fixed_income_etfs from Stock Analysis.
    # 'bond_etfs_vettafi': {
    #     'category_name': 'Bond ETFs VettaFi',
    #     'url': 'https://etfdb.com/etfdb-category/total-bond-market/',
    #     'cols': [' Symbol ', ' ETF Name ', ' Total Assets* '],
    #     'cols_final': ['Symbol', 'Name', 'Assets ($MM)'],
    #     'sort_by': 'Assets ($MM)',
    #     'sort_by_factor': 1e6,
    #     'sort_by_type': float
    # },
    'fixed_income_etfs': {
        'category_name': 'Fixed Income ETFs',
        'url': 'https://stockanalysis.com/list/fixed-income-etfs/',
        'cols': ['Symbol', 'Fund Name', 'Assets'],
        'cols_final': ['Symbol', 'Name', 'Assets ($MM)'],
        'sort_by': 'Assets ($MM)',
        'sort_by_factor': 1e6,
        'sort_by_type': float
    },
    # NOTE: Stock Analysis ETF lists were temporarily unavailable on March 3rd, 2025
    # 'fixed_income_etfs': {
    #     'category_name': 'Fixed Income ETFs',
    #     'url': 'https://etfdb.com/etfs/asset-class/bond/',
    #     'cols': [' Symbol ', ' ETF Name ', ' Total Assets ($MM) '],
    #     'cols_final': ['Symbol', 'Name', 'Assets ($MM)'],
    #     'sort_by': 'Assets ($MM)',
    #     'sort_by_factor': 1e6,
    #     'sort_by_type': float
    # },
    'ai_etfs': {
        'category_name': 'Artificial Intelligence ETFs',
        'url': 'https://stockanalysis.com/list/artificial-intelligence-etfs/',
        'cols': ['Symbol', 'Fund Name', 'Assets'],
        'cols_final': ['Symbol', 'Name', 'Assets ($MM)'],
        'sort_by': 'Assets ($MM)',
        'sort_by_factor': 1e6,
        'sort_by_type': float
    },
    # NOTE: Stock Analysis ETF lists were temporarily unavailable on March 3rd, 2025
    # 'ai_etfs': {
    #     'category_name': 'Artificial Intelligence ETFs',
    #     'url': 'https://etfdb.com/themes/artificial-intelligence-etfs/',
    #     'cols': [' Symbol ', ' ETF Name ', ' Total Assets* '],
    #     'cols_final': ['Symbol', 'Name', 'Assets ($MM)'],
    #     'sort_by': 'Assets ($MM)',
    #     'sort_by_factor': 1e6,
    #     'sort_by_type': float
    # },
    'cryptos': {
        'category_name': 'Cryptos',
        'url': 'https://finance.yahoo.com/markets/crypto/all/?start=0&count=100',
        'cols': ['Symbol', 'Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    # 'cryptos_coin360': {
        # 'category_name': 'Cryptos Coin360',
        # 'url': 'https://coin360.com/coin',
        # 'cols': ['Symbol', 'Name', 'Market Cap (USD)'],
        # 'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        # 'sort_by': 'Market Cap ($B)',
        # 'sort_by_factor': 1e9,
        # 'sort_by_type': float
    # },
    'futures': {
        'category_name': 'Futures',
        'url': 'https://finance.yahoo.com/commodities/',
        'cols': ['Symbol', 'Name', 'Volume', 'Open Interest'],
        'cols_final': ['Symbol', 'Name', 'Volume', 'Open Interest'],
        'sort_by': 'Open Interest',
        'sort_by_factor': 1,
        'sort_by_type': float
    }
    # 'forex': {
        # 'category_name': 'Forex',
        # 'url': 'https://www.centralcharts.com/en/price-list-ranking/ALL/desc/ts_48-forex-128-currency-pairs--qc_1-alphabetical-order',
        # 'cols': ['Financial instrument', 'Current price', 'Volume'],
        # 'cols_final': ['Symbol', 'Price', 'Volume'],
        # 'sort_by': 'Volume',
        # 'sort_by_factor': 1,
        # 'sort_by_type': float
    # }
}

# Ticker info
base_info_fields = ['quoteType', 'currency', 'exchange', 'shortName', 'longName']
etf_extra_fields = ['category', 'fundFamily', 'totalAssets', 'longBusinessSummary']
# NOTE: crypto_etf_extra_fields = etf_extra_fields
# NOTE: commodity_etf_extra_fields = etf_extra_fields
# NOTE: some fields within a given quoteType may be missing for some tickers - 
# - e.g. some cryptos do not have longName or description - so download_yh_info() checks 
# if a field exists
crypto_extra_fields = ['description', 'marketCap']
equity_extra_fields = ['industry', 'sector', 'marketCap', 'longBusinessSummary']
info_fields = {
    'INDEX': base_info_fields,
    'ETF': base_info_fields + etf_extra_fields,
    'EQUITY': base_info_fields + equity_extra_fields,
    'CRYPTOCURRENCY': base_info_fields + crypto_extra_fields,
    'FUTURE': ['quoteType', 'currency', 'exchange', 'shortName']
}

category_titles_ids = {
    'biggest_companies': {
        'id_string': 'biggest-companies',
        'collapse_title': 'BIGGEST COMPANIES'
    },
    'sp500': {
        'id_string': 'sp500',
        'collapse_title': 'S&P 500 COMPANIES'
    },
    'nasdaq100': {
        'id_string': 'nasdaq100',
        'collapse_title': 'NASDAQ 100 COMPANIES'
    },
    'dow_jones': {
        'id_string': 'dow-jones',
        'collapse_title': 'DOW JONES INDUSTRIAL AVERAGE COMPANIES'
    },
    'car_companies': {
        'id_string': 'car-companies',
        'collapse_title': 'CAR COMPANIES'
    },
    'rare_metals_companies': {
        'id_string': 'rare-metals-companies',
        'collapse_title': 'RARE METAL COMPANIES'
    },
    'quantum_companies': {
        'id_string': 'quantum-companies',
        'collapse_title': 'QUANTUM COMPUTING COMPANIES'
    },    
    'biggest_etfs': {
        'id_string': 'biggest-etfs',
        'collapse_title': 'BIGGEST ETFs'
    },
    'fixed_income_etfs': {
        'id_string': 'fixed-income-etfs',
        'collapse_title': 'FIXED INCOME ETFs'
    },
    'ai_etfs': {
        'id_string': 'ai-etfs',
        'collapse_title': 'ARTIFICIAL INTELLIGENCE ETFs'
    },
    'precious_metals': {
        'id_string': 'precious-metals',
        'collapse_title': 'PRECIOUS METAL ETFs'
    },
    'commodity_etfs': {
        'id_string': 'commodity-etfs',
        'collapse_title': 'COMMODITY ETFs'
    },
    'currency_etfs': {
        'id_string': 'currency-etfs',
        'collapse_title': 'CURRENCY ETFs'
    },
    'cryptos': {
        'id_string': 'cryptos',
        'collapse_title': 'CRYPTOCURRENCIES'
    },
    'crypto_etfs': {
        'id_string': 'crypto-etfs',
        'collapse_title': 'CRYPTOCURRENCY ETFs'
    },
    'futures': {
        'id_string': 'futures',
        'collapse_title': 'COMMODITY FUTURES'
    },
    'stock_indices': {
        'id_string': 'stock-indices',
        'collapse_title': 'STOCK INDICES'
    },
    'volatility_indices': {
        'id_string': 'volatility-indices',
        'collapse_title': 'VOLATILITY INDICES'
    },
    'benchmarks': {
        'id_string': 'benchmarks',
        'collapse_title': 'BENCHMARKS'
    }
}

init_ticker_category_info_map = {
    'biggest_companies': {
        'sort_by': '',
        'id_string': 'biggest-companies',
        'collapse_title': 'BIGGEST COMPANIES'
    },
    'sp500': {
        'sort_by': '',
        'id_string': 'sp500',
        'collapse_title': 'S&P 500 COMPANIES'
    },
    'nasdaq100': {
        'sort_by': '',
        'id_string': 'nasdaq100',
        'collapse_title': 'NASDAQ 100 COMPANIES'
    },
    'dow_jones': {
        'sort_by': '',
        'id_string': 'dow-jones',
        'collapse_title': 'DOW JONES INDUSTRIAL AVERAGE COMPANIES'
    },
    'car_companies': {
        'sort_by': 'marketCap',
        'id_string': 'car-companies',
        'collapse_title': 'CAR COMPANIES'
    },
    'rare_metals_companies': {
        'sort_by': 'marketCap',
        'id_string': 'rare-metals-companies',
        'collapse_title': 'RARE METAL COMPANIES'
    },
    'quantum_companies': {
        'sort_by': 'marketCap',
        'id_string': 'quantum-companies',
        'collapse_title': 'QUANTUM COMPUTING COMPANIES'
    },
    'biggest_etfs': {
        'sort_by': '',
        'id_string': 'biggest-etfs',
        'collapse_title': 'BIGGEST ETFs'
    },
    'fixed_income_etfs': {
        'sort_by': '',
        'id_string': 'fixed-income-etfs',
        'collapse_title': 'FIXED INCOME ETFs'
    },
    'ai_etfs': {
        'sort_by': '',
        'id_string': 'ai-etfs',
        'collapse_title': 'ARTIFICIAL INTELLIGENCE ETFs'
    },
    'precious_metals': {  # ETFs
        'sort_by': 'totalAssets',
        'id_string': 'precious-metals',
        'collapse_title': 'PRECIOUS METAL ETFs'
    },
    'commodity_etfs': {
        'sort_by': 'totalAssets',
        'id_string': 'commodity-etfs',
        'collapse_title': 'COMMODITY ETFs'
    },
    'currency_etfs': {
        'sort_by': 'totalAssets',
        'id_string': 'currency-etfs',
        'collapse_title': 'CURRENCY ETFs'
    },
    'cryptos': {
        'sort_by': '',
        'id_string': 'cryptos',
        'collapse_title': 'CRYPTOCURRENCIES'
    },
    'crypto_etfs': {
        'sort_by': '',
        'id_string': 'crypto-etfs',
        'collapse_title': 'CRYPTOCURRENCY ETFs'
    },
    'futures': {
        'sort_by': '',
        'id_string': 'futures',
        'collapse_title': 'COMMODITY FUTURES'
    },
    'stock_indices': {
        'sort_by': '',  # Only some indices have 'volume' in info
        'id_string': 'stock-indices',
        'collapse_title': 'STOCK INDICES'
    },
    'volatility_indices': {
        'sort_by': '',  # No 'volume' in info
        'id_string': 'volatility-indices',
        'collapse_title': 'VOLATILITY INDICES'
    },
    'benchmarks': {
        'sort_by': '',
        'id_string': 'benchmarks',
        'collapse_title': 'BENCHMARKS'
    }
}
