import pandas as pd
from datetime import datetime
from mapping_tickers import *
from mapping_portfolio_downloads import *
from download_data import DownloadData
from download_info import DownloadInfo


end_date = datetime.today()
y_hist, m_hist, d_hist = 1, 0, 0
start_date = datetime(end_date.year - y_hist, end_date.month - m_hist, end_date.day - d_hist)

tk_market = '^GSPC'
# tickers = magnificent_7_tickers
# tk_market = 'BTC-USD'
# tickers = list(bond_etf_tickers.keys())
# tickers = ['USDE-USD', 'APT-USD', 'FDUSD-USD', 'RENDER-USD']

hist_data = DownloadData(end_date, start_date)
hist_info = DownloadInfo()

if __name__ == '__main__':
    
    # ticker_data = hist_data.download_yf_data(start_date, end_date, tickers, tk_market)
    # print(ticker_data['Adj Close'])
    # print(ticker_data['OHLC']['AAPL'])
    
    df = hist_info.download_from_url('fixed_income_etfs', 100)
    # df = pd.DataFrame()
    # df = hist_data.download_from_url('bond_etfs', 10)
    
    # df = hist_data.download_from_url('cryptos', 10)
    # print(df.loc[df['Symbol'].str.contains('RENDER'), :])
    # df.to_csv('../data/downloads/cryptos_yf_from_url.csv', index=False)
    # df.to_csv('../data/downloads/cryptos_from_url.csv', index=False)

    print(df)

    # if (len(tickers) == 0) | (tickers is None): 
    #     tickers = list(df['Symbol'])
    
    # dict_info = hist_data.download_yf_info(tickers, tk_market)
    # print(hist_data.start_date)
    # 
    # for tk in dict_info:
# 
        # print(f'{tk}:')
        # dict_info_tk = dict_info[tk]
# 
        # for field in dict_info_tk.keys():
            # print(f'\t{field}:\t{dict_info_tk[field]}')
# 
        # print('')
    # 