# Dictionaries
url_settings = {
    'global': {
        'headers': {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    },
    'nasdaq100': {
        'url': 'https://stockanalysis.com/list/nasdaq-100-stocks/',
        'cols': ['Symbol', 'Company Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'sp500': {
        'url': 'https://stockanalysis.com/list/sp-500-stocks/',
        'cols': ['Symbol', 'Company Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'dow_jones': {
        'url': 'https://stockanalysis.com/list/dow-jones-stocks/',
        'cols': ['Symbol', 'Company Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'biggest_companies': {
        'url': 'https://stockanalysis.com/list/biggest-companies/',
        'cols': ['Symbol', 'Company Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Company Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'biggest_etfs': {
        'url': 'https://8marketcap.com/etfs/',
        'cols': ['Symbol', 'Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Fund Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'crypto_etfs': {
        'url': 'https://stockanalysis.com/list/crypto-etfs/',
        'cols': ['Symbol', 'Fund Name', 'Assets'],
        'cols_final': ['Symbol', 'Fund Name', 'Assets ($MM)'],
        'sort_by': 'Assets ($MM)',
        'sort_by_factor': 1e6,
        'sort_by_type': float
    },
    'cryptos_yf': {
        'url': 'https://finance.yahoo.com/markets/crypto/all/?start=0&count=100',
        'cols': ['Symbol', 'Name', 'Market Cap'],
        'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'cryptos': {
        'url': 'https://coin360.com/coin',
        'cols': ['Symbol', 'Name', 'Market Cap (USD)'],
        'cols_final': ['Symbol', 'Name', 'Market Cap ($B)'],
        'sort_by': 'Market Cap ($B)',
        'sort_by_factor': 1e9,
        'sort_by_type': float
    },
    'futures': {
        'url': 'https://finance.yahoo.com/commodities/',
        'cols': ['Symbol', 'Name', 'Volume', 'Open Interest'],
        'cols_final': ['Symbol', 'Name', 'Volume', 'Open Interest'],
        'sort_by': 'Open Interest',
        'sort_by_factor': 1,
        'sort_by_type': int
    }
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