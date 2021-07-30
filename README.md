# STONKERS!!!!!

Welcome to stonkers. A python library that helps with stock portfolio management. Stonkers creates a stock_portfolio class which can read in stock holdings and portfolio percentage goals from a .yaml file. These holdings and goal percentages can be manually added as well to a instance. Stonkers then has built in functionality to pull the latest stock prices for each ticker to calculate the current distribution of your portfolio. Finally it will calculate how much you need to buy/sell of your stocks in order to rebalance your portfolio.

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
chadfolio.add_holding("LAND", 100)
chadfolio.add_holding("XLE", 50)
chadfolio.add_goal_percent("TQQQ", 0.6)
chadfolio.add_goal_percent("LAND", 0.2)
chadfolio.add_goal_percent("XLE", 0.2)
```
Maybe you are never selling(!) so you only want to buy more stocks in order to rebalance the portfolio. Use the `balance_only_buy` method.
```
chadfolio.balance_portfolio()
Current total portfolio value: 11438.0
Necessary Portfolio value to rebalance with only buying: 12345.0
Required Cash Money: 907.0
```
Stonkers keeps track of the portfolio calculated values with dictionaries as attributes. These dictionaries can be converted into an easy to read dataframe with the `create_dataframe` method.
```
chadfolio.create_dataframe()
```
 You can always call the current state of your portfolio's dataframe as an attribute.
```
chadfolio.dataframe[['ticker', 'need_to_buy']]
```
| ticker   |   need_to_buy |
|:---------|--------------:|
| TQQQ     |          5.8  |
| LAND     |          5.87 |
| XLE      |          0    |

Let's say you have $1000 to invest in your `chadfolio` portfolio. The `stock_buy_advisor` method will take an input chunk of money and return a Counter with all the stock tickers and amount to buy. The calculation looks at which stock has the greatest `holding_value_diff`, adds it to the holdings, subtracts the cost from the `buying_cash`, and then recalculates the portfolio distributions. It keeps doing this process until there is not enough money left to buy the stock with the greatest `holding_value_diff`.
```
chadfolio.stock_buy_advisor(1000)
Attempting to buy stocks with $1000
Leftover cash: 14.249969482421875
Counter({'TQQQ': 6, 'LAND': 6, 'XLE': 1})
```
The internal dataframe has been updated to reflect the new holdings in the portfolio.

```
chadfolio.dataframe[['ticker', 'holdings']]
```
| ticker   |   holdings |
|:---------|-----------:|
| TQQQ     |         56 |
| LAND     |        106 |
| XLE      |         51 |


### stonkers_demo.py
Below is the command output from running `stonkers.stonkers_demo.py`. Note the final column `need_to_buy_or_sell`, which tells the user how much he needs to buy or sell of each stock so that the holding_percentages align with the goal_percentages.
```
Current total portfolio value: 13065.27
Necessary Portfolio value to rebalance with only buying: 16488.4
Required Cash Money: 3423.13
| ticker   | goal_percentage   | holding_percentage   |   holdings |   stock_price |   holding_value_diff |   need_to_buy_or_sell |   need_to_buy |
|:---------|:------------------|:---------------------|-----------:|--------------:|---------------------:|----------------------:|--------------:|
| VTI      | 40.0%             | 39.9%                |         23 |        226.76 |                10.63 |                  0.05 |          6.09 |
| VGT      | 10.0%             | 12.6%                |          4 |        412.21 |              -342.31 |                 -0.83 |          0    |
| VEA      | 10.0%             | 9.90%                |         25 |         51.78 |                12.03 |                  0.23 |          6.84 |
| VWO      | 10.0%             | 8.99%                |         23 |         51.11 |               131    |                  2.56 |          9.26 |
| BND      | 5.0%              | 5.31%                |          8 |         86.76 |               -40.82 |                 -0.47 |          1.5  |
| MUB      | 10.0%             | 8.99%                |         10 |        117.56 |               130.93 |                  1.11 |          4.03 |
| LQD      | 2.5%              | 2.08%                |          2 |        136.01 |                54.61 |                  0.4  |          1.03 |
| BNDX     | 2.5%              | 2.21%                |          5 |         57.91 |                37.08 |                  0.64 |          2.12 |
| XLE      | 5.0%              | 6.04%                |         16 |         49.39 |              -136.98 |                 -2.77 |          0.69 |
| GLD      | 5.0%              | 3.89%                |          3 |        169.81 |               143.83 |                  0.85 |          1.85 |
Attempting to buy stocks with $1000
Leftover cash: 196.04001235961914
Counter({'VWO': 3, 'MUB': 2, 'GLD': 1, 'LQD': 1, 'BNDX': 1, 'VEA': 1})
Demo done!
```

## Future Work:
- Add historical strategy calculations: e.g. How much money would your strategy yield over the last year if you were investing $1000 and rebalancing the portfolio once a month.
- Add plotting functionality:
	- Pie charts that show goal percentages of a portfolio and actual holding percentages.
	- Line graphs that can show outcomes for historical strategies for backtesting.
	- Lines graphs can plot the outcomes of multiple strategies so you can compare the effectiveness of different portfolio strategies.
- Let's say you only have $1000 to invest and you only want to buy stocks and not sell. $1000 might not be enough to rebalance the portfolio, but how should you buy stocks to get it as close as possible to rebalanced. Have an option for buying whole stocks or for buying fractional shares.
- Function that will write your new portfolio to a yaml file after advising what stocks to buy.