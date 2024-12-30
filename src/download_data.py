import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from mapping_portfolio_downloads import *
from mapping_tickers import *
import sys

class DownloadData():

    def __init__(
        self,
        end_date: datetime,
        start_date: datetime #,
        # tickers,
    ):
    
        """
        end_date:   defaults to today's date, can be changed by user
        start_date: can be specified explicitly or derived based on desired length of history
        tickers:    user-specified based on suggested lists or a custom synthetic portfolio 
        """

        self.end_date = end_date
        self.start_date = start_date
        # self.tickers = tickers


    def download_yf_data(
        self,
        start_date,
        end_date,
        tickers,
        tk_market
     ):
        """
        tk_market:  market benchmark needed for Beta, Alpha, Treynor, defaulting to S&P500
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
        # ### Do we? -- The user can always select it from the Benchmarks category
        tickers_market = tickers
        if tk_market not in tickers:
            tickers_market += [tk_market]
        
        tickers_to_be_removed = []
        for tk in tickers_market:

            data = yf.download(tk, start = start_date, end = end_date, progress = False)

            # NOTE:
            # Maybe use yf.history() instead, which would allow to extract adjusted ohlc, not just adj_close.
            # This would then require downloading both adjusted and unadjusted data.
            #
            # Question:
            #   In the calculation of dollar volume as price times volume, is the price normally adjusted (for stock splits and dividends) or not, or does it depend and - if so - on what?
            # 
            # Copilot:
            #   In the calculation of dollar volume (price times volume), the price is typically adjusted for stock splits and dividends to ensure consistency and comparability over time [1]. 
            #   However, volume is usually not adjusted for dividends. Here's a brief overview:
            #   
            #   Stock Splits: 
            #   Both price and volume are adjusted [2]. For example, in a 2-for-1 stock split, the price is halved, and the volume is doubled to maintain consistency [2].
            #   
            #   Dividends: 
            #   Only the price is adjusted [2]. Cash dividends do not affect the volume, but stock dividends (additional shares issued) do result in adjustments to both price and volume [2].
            #   
            #   This approach helps in accurately reflecting the historical performance and making meaningful comparisons over time [3].
            # 
            # [1] https://leiq.bus.umich.edu/docs/crsp_calculations_splits.pdf
            # [2] https://forum.alpaca.markets/t/why-is-price-but-not-volume-adjusted-for-dividends/12345
            # [3] https://help.stockcharts.com/data-and-ticker-symbols/data-availability/price-data-adjustments

            if tk in yf.shared._ERRORS.keys():
                print(f'WARNING: Data is unavailable for {tk}, ticker will be removed from the portfolio')
                # Should suggest that the user change the dates range or remove the ticker
                tickers_to_be_removed.append(tk)

            else:
                
                data_index = data.index

                adj_close_tk = pd.DataFrame({tk: data['Adj Close']}, index = data_index)
                df_adj_close = pd.concat([df_adj_close, adj_close_tk], axis = 1)
                
                close_tk = pd.DataFrame({tk: data['Close']}, index = data_index)
                df_close = pd.concat([df_close, close_tk], axis = 1)

                volume_tk = pd.DataFrame({tk: data['Volume']}, index = data_index)
                df_volume = pd.concat([df_volume, volume_tk], axis = 1)

                dollar_volume_tk = pd.DataFrame({tk: data['Volume'] * data['Adj Close']}, index = data_index)
                df_dollar_volume = pd.concat([df_dollar_volume, dollar_volume_tk], axis = 1)

                # df_adj_close[tk] = data['Adj Close']
                # df_close[tk] = data['Close']
                # df_volume[tk] = data['Volume']
                # df_dollar_volume[tk] = data['Adj Close'].copy() * data['Volume'].copy()
                
                df_adj_close = df_adj_close.dropna() 
                df_volume = df_volume.dropna()
                df_dollar_volume = df_dollar_volume.dropna()

                df_ohlc = data[ohlc_cols]
                df_ohlc = df_ohlc.dropna() 
                dict_ohlc.update({tk: df_ohlc})

        # Must not modify the tickers list inside the loop over it
        for tk in tickers_to_be_removed:
            tickers.remove(tk)
 
        print(f'removed tickers:{tickers_to_be_removed}')

        # print(f'df_adj_close before dropna()\n{df_adj_close}')

        df_adj_close = df_adj_close.dropna()
        if len(df_adj_close) == 0:
            error_msg = f'ERROR: No overlapping data found for the selected portfolio within the time period specified.\n'
            error_msg += '       Please consider removing some tickers and/or changing the historical date range.'
            downloaded_data = {
                'error_msg': error_msg
            }
            return downloaded_data

        # Refresh tickers, as some may have been removed by dropna()
        tickers = list(df_adj_close.columns)

        df_volume = df_volume.dropna()                  # NOTE: 
        df_dollar_volume = df_dollar_volume.dropna()    # Need to handle volumes separately from df_close/df_adj_close
        
        # print(f'df_adj_close after dropna()\n{df_adj_close}')

        # NOTE: We want to keep dates as index, so there is no reset_index()

        # Dropping dates with NaNs now in order to avoid dropping two consecutive dates for each NaN later
        # (each log return is based on two consecutive dates, so log returns at both of them would be NaN
        # if any of them is NaN)

        # Below are checks on when the data starts for any ticker, i.e. when the initial NaNs end.
        # E.g. dropping NaNs for etf_tickers shortens the historical period from 3 years to 2.5 years because
        # of the missing data for DJIA.

        # Check for Adj Close data start. Volume and Close data start together with Adj Close data,
        # so there is no need to check df_volume.  ### Not necessarily correct, e.g. for some cryptos.

        df_adj_close_start = pd.DataFrame(columns=['Adj Close Start Date'])
        last_date_tk = df_adj_close.index.max().date()
        missing_end_date_tickers = []

        for tk in tickers:

            # print(f'{tk}\n\tdf_adj_close[tk] = {df_adj_close[tk]}')

            start_date_tk = df_adj_close.index[df_adj_close[tk].notna()].min().date()
            last_nan_date_tk = df_adj_close.index[df_adj_close[tk].isna()].max().date()

            # print(f'{tk}\n\tstart_date = {start_date_tk}')

            if (start_date_tk > start_date.date()) & (not pd.isnull(last_nan_date_tk)):
                if last_nan_date_tk < start_date_tk:
                    df_adj_close_start.loc[tk, 'Adj Close Start Date'] = start_date_tk

            if (not pd.isnull(last_nan_date_tk)) & (last_nan_date_tk == end_date.date()):
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
            'error_msg': '',
            'Adj Close': df_adj_close,
            'Close': df_close,
            'Volume': df_volume,
            'Dollar Volume': df_dollar_volume,
            'OHLC': dict_ohlc
        }

        return downloaded_data
    

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
            df_risk_free_rate[tk_desc] = yf.download(tk, start=start_date, end=end_date, progress = False)['Adj Close']
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
                df_risk_free_rate[custom_risk_free_instrument] = yf.download(tk, start=start_date, end=end_date, progress = False)['Adj Close']
                custom_risk_free_rate = np.mean(df_risk_free_rate[tk_desc])
                custom_risk_free_rate /= 100

            except:
                print(f'WARNING: Could not download data for {tk}\nUsing the rate for {risk_free_instrument} instead.')
                sys.exit()

        print(f'Risk-Free Rate Instrument:\t{risk_free_instrument}\nMean of Period:\t\t\t{risk_free_rate:.6f}')

        risk_free_rate_data = {
            'Historical Rate': risk_free_rate,
            'Historical Instrument': risk_free_instrument,
            'Custom Rate': custom_risk_free_rate,
            'Custom Instrument': custom_risk_free_instrument
        }

        return risk_free_rate_data

