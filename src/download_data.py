import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from mapping_portfolio_downloads import *
from mapping_tickers import *

class DownloadData():

    def __init__(
        self,
        end_date: datetime,
        start_date: datetime,
        tickers,
        tk_market: str
    ):
    
        """
        end_date:   defaults to today's date, can be changed by user
        start_date: can be specified explicitly or derived based on desired length of history
        tickers:    user-specified based on suggested lists or a custom synthetic portfolio 
        tk_market:  market benchmark needed for Beta, Alpha, Treynor, defaulting to S&P500
        """

        self.end_date = end_date
        self.start_date = start_date
        self.tickers = tickers
        self.tk_market = tk_market


    def download_yh_data(
        self,
        start_date,
        end_date,
        tickers,
        tk_market
     ):
        """
        """

        # For most functions, the user should be offered a choice between Close and Adjusted Close.
        # One exception will be Candlestick, where Adjusted Close will NOT be used.
        # Adjusted Close are more accurate than regular Close because they include dividends and stock splits.
        # NOTE: Dollar Volume is only used for Amihud liquidity measure and will only be based on Adj Close.
        
        if isinstance(tickers, dict):
            tickers = list(tickers.keys())

        df_adj_close = pd.DataFrame()
        df_close = pd.DataFrame()           # mainly for Candlestick, unless selected by user
        df_ohlc = pd.DataFrame()            # Open, High, Low, Close for Candlestick
        df_volume = pd.DataFrame()          
        df_dollar_volume = pd.DataFrame()   # For Amihud liquidity measure calculation
        ohlc_cols = ['Open', 'High', 'Low', 'Close']
        dict_ohlc = {}

        # Analysis, stats, graphs, etc. will only be for user specified tickers 
        # but we want to include benchmark data here
        tickers_market = tickers
        if tk_market not in tickers:
            tickers_market += [tk_market]
            
        for tk in tickers_market:

            data = yf.download(tk, start=start_date, end=end_date)
            df_adj_close[tk] = data['Adj Close']
            df_close[tk] = data['Close']
            df_volume[tk] = data['Volume']
            df_dollar_volume[tk] = data['Adj Close'] * data['Volume']

            df_ohlc = data[ohlc_cols]
            df_ohlc = df_ohlc.dropna() 
            dict_ohlc.update({tk: df_ohlc})

        df_adj_close = df_adj_close.dropna() 
        df_volume = df_volume.dropna()
        df_dollar_volume = df_dollar_volume.dropna()

        # NOTE: We want to keep dates as index, so there is no reset_index()

        # Dropping dates with NaNs now in order to avoid dropping two consecutive dates for each NaN later
        # (each log return is based on two consecutive dates, so log returns at both of them would be NaN
        # if any of them is NaN)

        # Below are checks on when the data starts for any ticker, i.e. when the initial NaNs end.
        # E.g. dropping NaNs for etf_tickers shortens the historical period from 3 years to 2.5 years because
        # of the missing data for DJIA.

        # Check for Adj Close data start. Volume and Close data start together with Adj Close data,
        # so there is no need to check df_volume.

        df_adj_close_start = pd.DataFrame(columns=['Adj Close Start Date'])
        last_date_tk = df_adj_close.index.max().date()
        missing_end_date_tickers = []

        for tk in tickers:
            start_date_tk = df_adj_close.index[~df_adj_close[tk].isna()].min().date()
            last_nan_date_tk = df_adj_close.index[df_adj_close[tk].isna()].max().date()

            if (start_date_tk > start_date.date()) & ~pd.isnull(last_nan_date_tk):
                if last_nan_date_tk < start_date_tk:
                    df_adj_close_start.loc[tk, 'Adj Close Start Date'] = start_date_tk

            if ~pd.isnull(last_nan_date_tk) & (last_nan_date_tk == end_date.date()):
                missing_end_date_tickers.append(tk)

        if len(df_adj_close_start) > 0:
            min_start_date_adj_close_tk = df_adj_close_start['Adj Close Start Date'].min()
            print(f'WARNING: Data for these tickers start after the selected start date of {start_date.date()}.')
            for tk in df_adj_close_start.index:
                print(f"\t{tk}:\t{df_adj_close_start.loc[tk, 'Adj Close Start Date']}")
            print(f'The whole portfolio data will be truncated to start at {min_start_date_adj_close_tk}.')
            print(f'Please consider adjusting the start date or removing some tickers if you wish to avoid that.')

        if last_date_tk < end_date.date():
            print(f'WARNING: No data available for the selected portfolio tickers at the end date of {end_date.date()}.')
            print(f'The portfolio data will be truncated to end at the latest available date of {last_date_tk}.')
        elif len(missing_end_date_tickers) > 0:
            print(f'WARNING: Data for these tickers is missing for the selected end date of {end_date.date()}.')
            print(missing_end_date_tickers)
            print(f'The whole portfolio data will be truncated to end at the latest date containing data for all tickers.')
        
        # Pack downloaded data into a single dictionary

        downloaded_data = {
            'Adj Close': df_adj_close,
            'Close': df_close,
            'Volume': df_volume,
            'Dollar Volume': df_dollar_volume,
            'OHLC': dict_ohlc
        }

        return downloaded_data
    

    def download_yh_info(
        self,
        tickers,
        tk_market
     ):
        """
        """

        dict_info = {}
        all_tickers = tickers if tk_market in tickers else tickers + [tk_market]

        for tk in all_tickers:

            try:
                info_tk = yf.Ticker(tk).info
                quote_type = info_tk['quoteType']
                fields = info_fields[quote_type]
                dict_info_tk = {}
                for field in fields:
                    try:
                        dict_info_tk.update({field: info_tk[field]})
                        dict_info.update({tk: dict_info_tk})
                    except:
                        # print(f'WARNING: No {field} info found for {tk}')
                        continue
            except:
                print(f'WARNING: No info found for {tk}')
                continue

        return dict_info


    def get_risk_free_rate(
        self,
        start_date,
        end_date,
        tk_custom = None
    ):
        """
        NOTE: 
        1) set start_date = end_date if using only a single date
        2) if end_date > start_date, then use the mean of the period
        3) risk_free_tk is a user-specified ticker; if None, then the lower rate of default treasury tickers will be used

        Should offer the user the choices of:
          - risk-free instrument (note that the rate must be annualised);
          - mean of historical period (AAGR - there's no compunding);
          - initial value of historical period;
          - custom date, e.g. as-of-today;
          - lower of the two means or lower of the two daily values;
          - custom value.

        The annual risk-free rate from the beginning of the historical period (start of investment) was used e.g. by NEDL in https://www.youtube.com/watch?v=zvChPqsKZjc

        The risk-free instrument could be:
          - the 13-week (3-month) US Treasury Bill; or
          - the 10-year US Treasury Note; or
          - as specified by the user.
        """

        df_risk_free_rate = pd.DataFrame()
        
        for tk, tk_desc in risk_free_treasury_tickers.items():
            
            dict_mean_risk_free_rate = {}
            df_risk_free_rate[tk_desc] = yf.download(tk, start=start_date, end=end_date)['Adj Close']
            dict_mean_risk_free_rate.update({tk_desc: np.mean(df_risk_free_rate[tk_desc])})
        
        # Get the mean risk-free rate over the historical period
        risk_free_rate = 100
        risk_free_instrument = df_risk_free_rate.columns[0]
        # Take the risk free rate as the lowest for all instruments
        for tk_desc, rate in dict_mean_risk_free_rate.items():
            if rate < risk_free_rate:
                risk_free_rate = rate
                risk_free_instrument = tk_desc

        risk_free_rate /= 100

        # Check if custom ticker may be the preferred one of the two treasury tickers.
        # Offer the user to use the other treasury rate, if lower than that corresponding to the custom ticker.

        if (tk_custom is not None) & (tk_custom in risk_free_treasury_tickers.keys()):
            custom_risk_free_rate = dict_mean_risk_free_rate[tk_custom]
            custom_risk_free_rate /= 100
            custom_risk_free_instrument = risk_free_treasury_tickers[tk_custom]
      
        # Check custom ticker, if specified. 
        # Keep the treasury-based rate available, offer to use it instead of the custom rate if lower than the latter. 

        if (tk_custom is not None) & (tk_custom not in risk_free_treasury_tickers.keys()):
            
            try:
                custom_risk_free_instrument = yf.Ticker(tk).info['shortName']
                df_risk_free_rate[custom_risk_free_instrument] = yf.download(tk, start=start_date, end=end_date)['Adj Close']
                custom_risk_free_rate = np.mean(df_risk_free_rate[tk_desc])
                custom_risk_free_rate /= 100

            except:
                print(f'WARNING: Could not download data for {tk}\nUsing the rate for {risk_free_instrument} instead.')
                exit

        print(f'Risk-Free Rate Instrument:\t{risk_free_instrument}\nMean of Period:\t\t\t{risk_free_rate:.6f}')

        risk_free_rate_data = {
            'Historical Rate': risk_free_rate,
            'Historical Instrument': risk_free_instrument,
            'Custom Rate': custom_risk_free_rate,
            'Custom Instrument': custom_risk_free_instrument
        }

        return risk_free_rate_data


    def numstring_to_float(self, x: str):
        """
        Convert a numeric string x to a float by removing trillion ('T'), billion ('B'), 
        million ('M') and thousand ('K') symbols and applying a corresponding multiplier
        """

        x = x.replace(',', '')
        if 'T' in x:
            return float(x.replace('T', '')) * 1e12
        if 'B' in x:
            return float(x.replace('B', '')) * 1e9
        elif 'M' in x:
            return float(x.replace('M', '')) * 1e6
        elif ('k' in x) | ('K' in x):
            return float(x.replace('k', '').replace('K', '')) * 1e3
        elif (x.replace('.', '').isdigit()):
            return float(x)
        else:
            return 0.0


    def download_from_url(
        self,
        ticker_category,
        max_tickers
    ):
        """
        ticker_category: url_settings.keys(), except 'global', i.e.:
            'nasdaq100', 'sp500', 'dow_jones', 'biggest_companies',
            'biggest_etfs', 'crypto_etfs', 'cryptos_yf', 'cryptos', 'futures'
        max_tickers: limits the number of tickers to download

        The variables below will be defined using url_settings[ticker_category]:
        url:            web page from which to download
        cols:           columns to download with their original names
        cols_final:     renamed columns to keep
        sort_by:        column by which to sort the list of tickers
        sort_by_factor: factor by which to divide the sort_by column
        sort_by_type:   data type of the sort_by column
        """

        category = url_settings[ticker_category]
        url = category['url']
        cols = category['cols']
        cols_final = category['cols_final']
        sort_by = category['sort_by']
        sort_by_factor = category['sort_by_factor']
        sort_by_type = category['sort_by_type']
        print(ticker_category, url)
        s = requests.Session()
        headers = url_settings['global']['headers']
        res = s.get(url, headers=headers)

        if res.status_code == 200:

            df = pd.read_html(res.content)[0][cols]

            dict_cols = dict(zip(cols, cols_final))
            df.rename(columns=dict_cols, inplace=True)

            ### Some custom cleanup

            # Remove NAs first for 'str.contains' to work (it is sensitive to NAs)
            df = df.dropna()

            if ticker_category == 'biggest_etfs':
                # This cleans up the output of https://8marketcap.com/etfs/ (top ETFs),
                # which contains records with ads
                df = df.loc[~df['Symbol'].str.contains('Close Ad')]
            
            if ticker_category == 'crypto_etfs':
                # Remove records where the sort_by column value does not contain a decimal dot, 
                # e.g. in the output of https://stockanalysis.com/list/crypto-etfs/
                # sort_by is in cols_final, that's why the columns must be renamed above
                df = df.loc[df[sort_by].str.contains('\.')]

            ### End of custom cleanup

            df = df.reset_index(drop=True)
            if max_tickers is None:
                max_tickers = len(df)

            df = df[:max_tickers]
            
            # Make sure sort_by column is a string before we use numstring_to_float()
            # E.g. https://coin360.com/coin has Market Cap (USD) as int64

            df[sort_by] = df[sort_by].astype(str)
            df[sort_by] = df.apply(lambda x: self.numstring_to_float(x[sort_by]), axis=1).astype(sort_by_type) / sort_by_factor
            df = df.sort_values(by=sort_by, ascending=False)
            df = df.reset_index(drop=True)
            
            if ticker_category == 'cryptos':
                # https://coin360.com/coin
                # NOTE: Not all tickers may be properly mapped to Yahoo tickers, especially for smaller tickers,
                # so yf_custom_crypto_tickers should be periodically checked and updated.
                # For this reason it may be preferable to download from Yahoo ('cryptos_yf'), which is also much faster.

                df['YF Symbol'] = df['Crypto Symbol'] + '-USD'
                for symbol in yf_custom_crypto_tickers.keys():
                    if symbol in list(df['Crypto Symbol']):
                        df.loc[df['Crypto Symbol'] == symbol, 'YF Symbol'] = yf_custom_crypto_tickers[symbol]

                # Check if the YF ticker is correct for the Crypto Symbol 
                for i in df.index:
                    try:
                        tk = df.loc[i, 'YF Symbol']
                        _ = yf.Ticker(tk).info
                    except:
                        crypto_symbol = df.loc[i, 'Crypto Symbol']
                        print(f'WARNING: Incorrect ticker {tk} for {crypto_symbol}')
                        continue
            
            elif ticker_category == 'cryptos_yf':
                # https://finance.yahoo.com/markets/crypto/all/?start=0&count=100
                
                # The syntax below is to take care of Symbols such as 'R RENDER-USD Render USD'
                df['YF Symbol'] = df['Symbol'].apply(lambda x: x.split('-USD')[0].split()[-1] + '-USD')
                df['Name'] = df['Symbol'].apply(lambda x: ' '.join(x.split('-USD ')[1].split()[: -1]))

            return df
        
        else:
            
            print('WARNING: Could not download tickers from {url}')
            exit


