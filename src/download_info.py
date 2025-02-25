import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
from mapping_portfolio_downloads import *
from mapping_tickers import *
import sys

class DownloadInfo():

    def download_yf_info(
        self,
        tickers,
        tk_market
     ):
        """
        NOTE: This function is currently unused.
        """

        dict_info = {}
        all_tickers = tickers if tk_market in tickers else tickers + [tk_market]

        for tk in all_tickers:

            try:
                info_tk = yf.Ticker(tk).info
                tk_type = info_tk['quoteType']
                fields = info_fields[tk_type]
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


    def numstring_to_float(self, x: str):
        """
        Convert a numeric string x to a float by removing dollar ('$', trillion ('T'), billion ('B'), 
        million ('M') and thousand ('K') symbols and applying a corresponding multiplier
        """

        x = x.replace(',', '').replace('$', '')

        if 'T' in x:
            return float(x.replace('T', '')) * 1e12
        elif 'B' in x:
            return float(x.replace('B', '')) * 1e9
        elif 'M' in x:
            return float(x.replace('M', '')) * 1e6
        elif ('k' in x) | ('K' in x):
            return float(x.replace('k', '').replace('K', '')) * 1e3
        elif (x.replace('.', '').isdigit()):
            return float(x)
        else:
            return 0.0


    def get_usd_fx_rate(self, currency):
        """
        Get the latest exchange rate of currency to USD
        """
        tk = currency + '=X'
        end = datetime.today()
        start = end - timedelta(days = 5)
        # This is to make sure that the latest available rate is returned, even if it's not today's
        fx_rate = yf.download(tk, start = start, end = end, progress = False)['Close'].iloc[-1].values[0]
        return fx_rate


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
                sep = ' - '
                df['Full Name'] = df['Name']
                df['Name'] = df['Name'].apply(lambda x: x.split(sep)[1] if sep in x else x)

            if ticker_category == 'crypto_etfs':
                # Remove records where the sort_by column value does not contain a decimal dot, 
                # e.g. in the output of https://stockanalysis.com/list/crypto-etfs/
                # sort_by is in cols_final, that's why the columns must be renamed above
                df = df.loc[df[sort_by].str.contains('\.')]
                sep = ' - '
                df['Full Name'] = df['Name']
                df['Name'] = df['Name'].apply(lambda x: x.split(sep)[1] if sep in x else x)

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
            
            if ticker_category == 'cryptos_coin360':
                # https://coin360.com/coin
                # NOTE: Not all tickers may be properly mapped to Yahoo tickers, especially for smaller tickers,
                # so yf_custom_crypto_tickers should be periodically checked and updated.
                # For this reason it may be preferable to download from Yahoo ('cryptos_yf'), which is also much faster.

                df['YF Symbol'] = df['Symbol'] + '-USD'
                for symbol in yf_custom_crypto_tickers.keys():
                    if symbol in list(df['Symbol']):
                        df.loc[df['Symbol'] == symbol, 'YF Symbol'] = yf_custom_crypto_tickers[symbol]

                # Check if the YF ticker is correct for the crypto symbol 
                for i in df.index:
                    try:
                        tk = df.loc[i, 'YF Symbol']
                        _ = yf.Ticker(tk).info
                    except:
                        crypto_symbol = df.loc[i, 'Symbol']
                        print(f'WARNING: Incorrect ticker {tk} for {crypto_symbol}')
                        continue
                
                # Rename columns so 'Symbol' contains YF tickers
                df = df.rename(columns = {'Symbol': 'Coin360 Symbol', 'YF Symbol': 'Symbol'})
            
            elif ticker_category == 'cryptos':
                # https://finance.yahoo.com/markets/crypto/all/?start=0&count=100
                
                # The syntax below is to take care of Symbols such as 'R RENDER-USD Render USD'
                # df['YF Symbol'] = df['Symbol'].apply(lambda x: x.split('-USD')[0].split()[-1] + '-USD')
                df['Symbol'] = df['Symbol'].apply(lambda x: x.split('-USD')[0].split()[-1] + '-USD')
                # df['Name'] = df['Symbol'].apply(lambda x: ' '.join(x.split('-USD ')[0].split()[: -1]))
                df['Name'] = df['Name'].apply(lambda x: x[: -4])

            # for tk in url_to_yf_ticker_map.keys():
            #     df['Symbol'] = np.where(df['Symbol'] == tk, url_to_yf_ticker_map[tk], df['Symbol'])

            return df

        else:
            
            print('WARNING: Could not download tickers from {url}')
            
