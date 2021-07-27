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
Stonkers has an internal dataframe that keeps track of your portfolio the calculated values used to determine which stocks to buy and how much. You can always call the current state of your portfolio's dataframe as an attribute.
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
| VTI      | 40.0%             | 40.0%                |         23 |        226.69 |          5213.87 |              5206.23 |                -7.64 |               -0.0337 |
| VGT      | 10.0%             | 12.6%                |          4 |        410.31 |          1641.24 |              1301.56 |              -339.68 |               -0.8279 |
| VEA      | 10.0%             | 9.89%                |         25 |         51.5  |          1287.5  |              1301.56 |                14.06 |                0.273  |
| VWO      | 10.0%             | 8.81%                |         23 |         49.87 |          1147.01 |              1301.56 |               154.55 |                3.0991 |
| BND      | 5.0%              | 5.32%                |          8 |         86.7  |           693.6  |               650.78 |               -42.82 |               -0.4939 |
| MUB      | 10.0%             | 9.05%                |         10 |        117.8  |          1178    |              1301.56 |               123.56 |                1.0489 |
| LQD      | 2.5%              | 2.09%                |          2 |        136.05 |           272.1  |               325.39 |                53.29 |                0.3917 |
| BNDX     | 2.5%              | 2.22%                |          5 |         57.84 |           289.2  |               325.39 |                36.19 |                0.6257 |
| XLE      | 5.0%              | 6.05%                |         16 |         49.23 |           787.68 |               650.78 |              -136.9  |               -2.7808 |
| GLD      | 5.0%              | 3.88%                |          3 |        168.46 |           505.38 |               650.78 |               145.4  |                0.8631 | 

Demo done!

## Future Work:
- Add historical strategy calculations: e.g. How much money would your strategy yield over the last year if you were investing $1000 and rebalancing the portfolio once a month.
- Add plotting functionality:
	- Pie charts that show goal percentages of a portfolio and actual holding percentages.
	- Line graphs that can show outcomes for historical strategies for backtesting.
	- Lines graphs can plot the outcomes of multiple strategies so you can compare the effectiveness of different portfolio strategies.
- Let's say you only have $1000 to invest and you only want to buy stocks and not sell. $1000 might not be enough to rebalance the portfolio, but how should you buy stocks to get it as close as possible to rebalanced. Have an option for buying whole stocks or for buying fractional shares.