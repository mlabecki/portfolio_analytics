# https://companiesmarketcap.com/cad/automakers/largest-automakers-by-market-cap/
# Sorted by Market Cap as of 20/02/2025
car_companies = {
    'TSLA': 'Tesla',
    'TM': 'Toyota',
    'XIACF': 'Xiaomi',
    '002594.SZ': 'BYD',
    'RACE': 'Ferrari',
    'MBG.DE': 'Mercedes-Benz',
    'P911.DE': 'Porsche',
    'BMW.DE': 'BMW',
    'VOW3.DE': 'Volkswagen',
    'GM': 'General Motors',
    'MARUTI.NS': 'Maruti Suzuki India',
    'STLA': 'Stellantis',
    'HMC': 'Honda',
    'M&M.NS': 'Mahindra & Mahindra',
    'F': 'Ford',
    'HYMTF': 'Hyundai',
    'TATAMOTORS.NS': 'Tata Motors',
    'LI': 'Li Auto',
    '600104.SS': 'SAIC Motor',
    '000270.KS': 'Kia',
    '601127.SS': 'Seres Group',
    '601633.SS': 'Great Wall Motors',
    # '7269.T': 'Suzuki Motor',
    'SZKMY': 'Suzuki Motor',  # Identical to 7269.T

    '0175.HK': 'Geely',
    'XPEV': 'XPeng',
    '000625.SZ': 'Chongqing Changan',
    'RNO.PA': 'Renault',
    'RIVN': 'Rivian',
    # '7270.T': 'Subaru',
    'FUJHY': 'Subaru',  # Identical to 7270.T
    '601238.SS': 'GAC (Guangzhou Automobile Group)',
    '600418.SS': 'JAC Motors',
    '2207.TW': 'Hotai Motor',
    'LCID': 'Lucid Motors',
    # '7201.T': 'Nissan',
    'NSANY': 'Nissan',
    # '7202.T': 'Isuzu',
    'ISUZY': 'Isuzu',
    'NIO': 'NIO',
    'VFS': 'VinFast Auto',
    'FROTO.IS': 'Ford Otosan',
    'VOLCAR-B.ST': 'Volvo Car AB (publ.)',  # currency: SEK, capMarket in SEK, No US exchange
    # 'VLVLY': 'AB Volvo (publ)',  # trucks, buses, construction equipment, marine & industrial engines engines
    'ZK': 'Zeekr',
    '000800.SZ': 'FAW Jiefang Group Co.,Ltd',  # currency: CNY, capMarket in CNY, No US exchange
    '9863.HK': 'Zhejiang Leapmotor Technology Co., Ltd.',  # currency: CNY, capMarket in CNY, No US exchange
    # '0489.HK': 'DONGFENG GROUP',
    'DNFGY': 'Dongfeng Motor Group Company Limited',  # capMarket in USD, currency CNY, same entity as 0489.HK
    # '7261.T': 'Mazda Motor Corporation',  # capMarket in JPY, currency JPY
    'MZDAY': 'Mazda Motor Corporation',  # capMarket in USD, currency JPY, same entity as 7261.T
    # '7211.T': 'Mitsubishi Motors Corporation',
    'MUFG': 'Mitsubishi UFJ Financial Group, Inc.',

    'TOASO.IS': 'Tofaş Türk Otomobil Fabrikası',  # currency: TRY, No US exchange
    'PII': 'Polaris',
    'PSNY': 'Polestar',
    'LOT': 'Lotus Technology',  
    '2201.TW': 'Yulon Motor Company',  # currency: TWD, No US exchange
    'AML.L': 'Aston Martin',  # currency: GBP, No US exchange
    'FORCEMOT.NS': 'Force Motors',  # currency: INR, No US exchange
    '003620.KS': 'KG Mobility (SsangYong Motor)', # currency: KRW, No US exchange
    'NWTN': 'NWTN Inc.',
    'REE': 'REE Automotive',
    'KNDI': 'Kandi Technologies Group',
    'NKLA': 'Nikola',
    'FFIE': 'Faraday Future',
    'CENN': 'Cenntro Electric Group',
    'PEV': 'Phoenix Motor',
    'MULN': 'Mullen Automotive',
    'GOEV': 'Canoo',
    'FUVV': 'Arcimoto'
}

"""


Sign in
Today
You said
Microsoft Copilot
Copilot said
Hello! I am Microsoft Copilot, your AI companion created to assist you in numerous ways. Whether you need help with productivity tasks, brainstorming ideas, learning new facts, or just having a friendly conversation, I'm here for you. What can I help you with today?




You said
What is the difference between Suzuku tickers SZKMY and 7269.T or between  Subaru tickers FUJHY and 7270.T? Both in each of the two examples have the same name and business summary but differ in the currency - it is USD in the former and JPY in the latter ticker with the '.T' suffix.
Copilot said
Great question! The difference between the tickers SZKMY and 7269.T for Suzuki, and FUJHY and 7270.T for Subaru, primarily lies in their listing and currency:

Suzuki Tickers:

SZKMY: This is an American Depositary Receipt (ADR) that represents Suzuki Motor Corporation's shares traded on the U.S. stock market. ADRs are denominated in U.S. dollars (USD) and allow U.S. investors to invest in foreign companies without dealing with foreign exchanges1
.

7269.T: This ticker represents Suzuki Motor Corporation's shares traded on the Tokyo Stock Exchange (TSE) and is denominated in Japanese yen (JPY)2
3
.

Subaru Tickers:

FUJHY: Similar to SZKMY, this is an ADR representing Subaru Corporation's shares traded on the U.S. stock market and is denominated in USD4
.

7270.T: This ticker represents Subaru Corporation's shares traded on the Tokyo Stock Exchange and is denominated in JPY5
.

In summary, the key differences are the stock exchange where they are listed and the currency in which they are traded. ADRs (SZKMY and FUJHY) are traded in the U.S. and denominated in USD, while the tickers with the '.T' suffix (7269.T and 7270.T) are traded on the Tokyo Stock Exchange and denominated in JPY.

I hope this helps clarify the differences! If you have any more questions, feel free to ask.


1
www.streetinsider.com

2
ca.finance.yahoo.com

3
finance.yahoo.com

4
tickeron.com

5
finance.yahoo.com



You said
Oh yes, now I recall the ADR... A couple of questions more: 1) Would the ADR quote history be the same or potentially shorter than that of the original exchange-traded equities ? 2) I see on YFinance website a note that SZKMY and FUJHY quotes are delayed - is that typical of ADRs?
Copilot said
ADR Quote History: The quote history for ADRs can be shorter than that of the original exchange-traded equities. This is because ADRs are created at a specific point in time when a U.S. depositary bank decides to issue them. Therefore, the historical data for ADRs will only go back as far as the ADR itself has existed, which might be shorter than the history of the original foreign shares1
2
.

Delayed Quotes: Yes, it is common for ADR quotes to be delayed. This is because ADRs are traded on U.S. exchanges, and the prices are updated based on the trading activity in the U.S. market. However, the underlying foreign shares might be trading in a different time zone, leading to delays in reflecting the most current prices3
4
.

I hope this helps! If you have any more questions, feel free to ask.


1
www.investopedia.com

2
www.nasdaq.com

3
international.schwab.com

4
csimarket.com



You said
Thanks, this is very helpful. I'm working on a technical analysis app where I want to offer the user a selection of YFinance tickers to compare the historical data in different categories - in this case car companies. So I'm guessing the exchange-traded equities would be more relevant in this context, despite the fact that the FX rate factor might complicate direct comparisons. Also I think I shouldn't mix equities with ADRs on the same list. Could you comment on this?
Copilot said
You're absolutely on the right track with your thinking!

Exchange-Traded Equities: For a technical analysis app, using exchange-traded equities would indeed be more relevant. These equities offer a longer and more consistent price history, which is vital for accurate technical analysis. Moreover, they reflect the actual trading activity and sentiment in the native market, providing more authentic data.

Currency Factor: You're correct that the exchange rate can complicate direct comparisons. However, this can be managed by either normalizing the data to a common currency or by providing tools within your app that allow users to account for these differences.

Mixing Equities and ADRs: It's a good idea to keep equities and ADRs separate on your list. Mixing them could introduce confusion, as ADRs reflect not only the underlying company's performance but also the exchange rate and the ADR market's trading behavior. Keeping them separate ensures clearer and more straightforward comparisons.

To summarize:

Focus on exchange-traded equities for a longer, more accurate historical data.

Be mindful of the currency factor and consider tools for normalization.

Separate equities and ADRs to maintain clarity.

Your approach sounds well thought out and should make for a robust technical analysis app. If you have more questions or need further assistance, feel free to ask!




You said
Great points, thanks for your help!
Copilot said
You're very welcome! I'm glad I could help. It sounds like your technical analysis app is shaping up to be a fantastic tool for users. If you have any more questions or need further assistance in the future, don't hesitate to reach out. Best of luck with your project! 🚀





What additional features could enhance my app?

Are there similar tools I should consider exploring?

Can you provide examples of implementing the features discussed?


"""