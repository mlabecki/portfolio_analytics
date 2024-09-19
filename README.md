# portfolio_analytics
The main purpose of this project was to create an interactive dashboard offering the user the opportunity to perform technical analysis on a portfolio of custom selected assets. These historical insights would then serve the broader goal of being able to build an optimal portfolio that is expected to perform successfully based on the desired investment objectives.

The **portfolio_analytics** repository contains the Python code designed to perform four major groups of tasks:

**1. Download data**
> - web scrape comprehensive lists of top assets in various categories
> - download ticker information from Yahoo!Finance
> - download historical ticker data from Yahoo!Finance

**2. Analyze prices**
> - statistical summary at the portfolio level
> - drawdown analysis with tabular summaries and an interactive plot of top drawdowns for each ticker
> - interactive line graphs and candlestick plots with traditional and hollow candles
> - moving average convergence-divergence (MACD) plot with signal overlay and an optional price overlay for each ticker
> - relative strength index (RSI) plot with overlays
> - up to six custom selected moving average overlays on top of an existing graph
> - up to three pairs of customized Bollinger band overlays on top of an existing graph
> - up to three pairs of customized moving average envelope overlays on top of an existing graph
> - price differential plot for two custom selected moving averages with an optional signal line

**3. Analyze returns**
> - summary of statistical properties of asset return distributions
> - heat map plots of various asset correlation metrics
> - principal component analysis with scatter plots for top components and eigenvector overlays

**4. Analyze performance**
> - summaries of a variety of performance metrics both for each asset and for the portfolio with selected weights:
>   - Sharpe ratio
>   - Sortino ratio
>   - probabilistic Sharpe ratio
>   - Sharpe ratio
>   - Treynor's ratio
>   - Jensen's alpha
>   - information ratio
>   - omega ratio
>   - up and down market capture ratios
>   - Amihud liquidity measure
>   - Calmar ratio
>   - Sterling ratio
>   - Martin ratio