# STONKERS!!!!!

Welcome to stonkers. A python library that helps with stock portfolio management. Stonkers creates a stock_portfolio Class which can read in stock holdings and portfolio percentage goals from a .yaml file. These holdings and goal percentages can be manually added as well to a instance. Stonkers then has built in functionality to pull the latest stock prices for each ticker to calculate the current distribution of your portfolio. Finally it will calculate how much you need to buy/sell of your stocks in order to rebalance your portfolio.

The goal to provide a helpful tool that can enable your investment strategy. Stonkers can advise you which stocks to buy first when the money transfers to your investment account. A well balanced portfolio will keep the returns flowing in while managing your risk. The stock portfolio percentages in `stonkers.demo_portfolio.yml` are based on the modern portfolio theory outlined in Wealthfront's white paper. Read more about it here: https://research.wealthfront.com/whitepapers/investment-methodology/



## Demo:

Instantiate a new stock_portfolio that reads in a portfolio.yml config file:
```
portfolio = stock_portfolio(portfolio_filename="demo_portfolio.yml")
```
Or create a new stock_portfolio and manually add your stocks to it (holdings and goal percentages):
```
chadfolio = stock_portfolio()
chadfolio.add_holding("TQQQ", 50)
chadfolio.add_holding("LAND", 20)
chadfolio.add_holding("XLE", 50)
chadfolio.add_percent_holding("TQQQ", 0.6)
chadfolio.add_percent_holding("LAND", 0.2)
chadfolio.add_percent_holding("XLE", 0.2)
```
Maybe you are never selling(!) so you only want to buy more stocks in order to rebalance the portfolio. Use the `balance_only_buy` method.
```
chadfolio.balance_only_buy()
Current total portfolio value: 9376.4
Necessary Portfolio value to rebalance with only buying: 9944.0
Required Cash Money: 567.6
```
Stonkers has an internal dataframe that keeps track of your portfolio and the calculated values used to determine which stocks to buy and how much. You can always call the current state of your portfolio's dataframe as an attribute.
```
chadfolio.dataframe[['ticker', 'need_to_buy']]
```
| ticker   |   need_to_buy |
|:---------|--------------:|
| TQQQ     |        3.5091 |
| LAND     |        3.6333 |
| XLE      |        0      |

### stonkers_demo.py
Below is the command output from running `stonkers.stonkers_demo.py`. Note the final column `need_to_buy_or_sell`, which tells the user how much he needs to buy or sell of each stock so that the holding_percentages align with the goal_percentages.

| ticker   | goal_percentage   | holding_percentage   |   holdings |   stock_price |   holdings_value |   goal_holding_value |   holding_value_diff |   need_to_buy_or_sell |
|:---------|:------------------|:---------------------|-----------:|--------------:|-----------------:|---------------------:|---------------------:|----------------------:|
| VTI      | 40.0%             | 37.9%                |         21 |        227.92 |          4786.32 |              5047.2  |               260.88 |                1.1446 |
| VGT      | 10.0%             | 13.1%                |          4 |        414.83 |          1659.32 |              1261.8  |              -397.52 |               -0.9583 |
| VEA      | 10.0%             | 9.42%                |         23 |         51.69 |          1188.87 |              1261.8  |                72.93 |                1.4109 |
| VWO      | 10.0%             | 9.29%                |         23 |         50.97 |          1172.31 |              1261.8  |                89.49 |                1.7557 |
| BND      | 5.0%              | 4.11%                |          6 |         86.48 |           518.88 |               630.9  |               112.02 |                1.2953 |
| MUB      | 10.0%             | 7.47%                |          8 |        117.83 |           942.64 |              1261.8  |               319.16 |                2.7086 |
| LQD      | 2.5%              | 2.14%                |          2 |        135.47 |           270.94 |               315.45 |                44.51 |                0.3286 |
| BNDX     | 2.5%              | 2.28%                |          5 |         57.76 |           288.8  |               315.45 |                26.65 |                0.4614 |
| XLE      | 5.0%              | 14.1%                |         36 |         49.72 |          1789.92 |               630.9  |             -1159.02 |              -23.3109 |
| GLD      | 5.0%              | 0.0%                 |          0 |        168.16 |             0    |               630.9  |               630.9  |                3.7518 |  

Demo done!

## Future Work:
- Add historical strategy calculations: e.g. How much money would your strategy yield over the last year if you were investing $1000 and rebalancing the portfolio once a month.
- Add plotting functionality:
	- Pie charts that show goal percentages of a portfolio and actual holding percentages.
	- Line graphs that can show outcomes for historical strategies for backtesting.
	- Lines graphs can plot the outcomes of multiple strategies so you can compare the effectiveness of different portfolio strategies.
- Let's say you only have $1000 to invest and you only want to buy stocks and not sell. $1000 might not be enough to rebalance the portfolio, but how should you buy stocks to get it as close as possible to rebalanced. Have an option for buying whole stocks or for buying fractional shares.
