etf_categories = [
    'biggest_etfs',
    'fixed_income_etfs',
    'ai_etfs',
    'commodity_etfs',
    'currency_etfs',
    'crypto_etfs'
]

input_table_columns_indices =    ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency']
input_table_columns_futures =    ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency']
input_table_columns_equities =   ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Industry', 'Sector', 'Exchange', 'Currency']
input_table_columns_etfs =       ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Category', 'Exchange', 'Currency']
input_table_columns_cryptos =    ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency']
input_table_columns_fx =         ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Exchange', 'Currency', 'Currency Name']
input_table_columns_benchmarks = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Category', 'Exchange', 'Currency']

custom_ticker_table_columns = {
    'INDEX':            ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Exchange', 'Currency'],
    'FUTURE':           ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Exchange', 'Currency'],
    'EQUITY':           ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Industry', 'Sector', 'Exchange', 'Currency'],
    'ETF':              ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Category', 'Exchange', 'Currency'],
    'CRYPTOCURRENCY':   ['Ticker', 'Name', 'Data Start', 'Data End', 'Type', 'Exchange', 'Currency'],
    'CURRENCY':         ['Ticker', 'Name', 'Currency Name', 'Data Start', 'Data End', 'Type', 'Exchange']
}

table_selected_tickers_columns = ['No.', 'Ticker', 'Name', 'Data Start', 'Data End', 'Length*', 'Type', 'Category', 'Industry', 'Sector', 'Exchange', 'Currency']
plots_table_selected_tickers_columns = ['No.', 'Ticker', 'Name', 'Type', 'Category', 'Industry', 'Sector', 'Exchange', 'Currency']

ticker_category_info_map = {
    'biggest_companies': {
        'columns': input_table_columns_equities,
        'id_string': 'biggest-companies',
        'collapse_title': 'BIGGEST COMPANIES'
    },
    'sp500': {
        'columns': input_table_columns_equities,
        'id_string': 'sp500',
        'collapse_title': 'S&P 500 COMPANIES'
    },
    'nasdaq100': {
        'columns': input_table_columns_equities,
        'id_string': 'nasdaq100',
        'collapse_title': 'NASDAQ 100 COMPANIES'
    },
    'dow_jones': {
        'columns': input_table_columns_equities,
        'id_string': 'dow-jones',
        'collapse_title': 'DOW JONES INDUSTRIAL AVERAGE COMPANIES'
    },
    'biggest_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'biggest-etfs',
        'collapse_title': 'BIGGEST ETFs'
    },
    'fixed_income_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'fixed-income-etfs',
        'collapse_title': 'FIXED INCOME ETFs'
    },
    'ai_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'ai-etfs',
        'collapse_title': 'ARTIFICIAL INTELLIGENCE ETFs'
    },
    'commodity_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'commodity-etfs',
        'collapse_title': 'COMMODITY ETFs'
    },
    'currency_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'currency-etfs',
        'collapse_title': 'CURRENCY ETFs'
    },
    'cryptos': {
        'columns': input_table_columns_cryptos,
        'id_string': 'cryptos',
        'collapse_title': 'CRYPTOCURRENCIES'
    },
    'crypto_etfs': {
        'columns': input_table_columns_etfs,
        'id_string': 'crypto-etfs',
        'collapse_title': 'CRYPTOCURRENCY ETFs'
    },
    'futures': {
        'columns': input_table_columns_futures,
        'id_string': 'futures',
        'collapse_title': 'COMMODITY FUTURES'
    },
    'fx': {
        'columns': input_table_columns_fx,
        'id_string': 'fx',
        'collapse_title': 'CURRENCY EXCHANGE RATES'
    },    
    'precious_metals': {
        'columns': input_table_columns_futures,
        'id_string': 'precious-metals',
        'collapse_title': 'PRECIOUS METALS'
    },    
    'stock_indices': {
        'columns': input_table_columns_indices,
        'id_string': 'stock-indices',
        'collapse_title': 'STOCK INDICES'
    },
    'volatility_indices': {
        'columns': input_table_columns_indices,
        'id_string': 'volatility-indices',
        'collapse_title': 'VOLATILITY INDICES'
    },
    'benchmarks': {
        'columns': input_table_columns_indices,
        'id_string': 'benchmarks',
        'collapse_title': 'BENCHMARKS'
    }
}
