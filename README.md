# STONKERS!!!!!

Welcome to stonkers. A python library that builds stock portfolio classes to help with portfolio management. Stonkers creates a stock_portfolio Class which can read in stock tickers holdings and portfolio percentage goals. It will then pull in the latest stock prices to calculate how balanced your portfolio is and how you need to buy/sell of your stocks in order to rebalance the portfolio.



# Demo:

Run the demo


|    | ticker   | goal_percentage   | holding_percentage   |   holdings |   stock_price |   holdings_value |   goal_holding_value |   holding_value_diff |   need_to_buy_or_sell |
|---:|:---------|:------------------|:---------------------|-----------:|--------------:|-----------------:|---------------------:|---------------------:|----------------------:|
|  0 | VTI      | 40.0%             | 37.9%                |         21 |        227.92 |          4786.32 |              5047.2  |               260.88 |                1.1446 |
|  1 | VGT      | 10.0%             | 13.1%                |          4 |        414.83 |          1659.32 |              1261.8  |              -397.52 |               -0.9583 |
|  2 | VEA      | 10.0%             | 9.42%                |         23 |         51.69 |          1188.87 |              1261.8  |                72.93 |                1.4109 |
|  3 | VWO      | 10.0%             | 9.29%                |         23 |         50.97 |          1172.31 |              1261.8  |                89.49 |                1.7557 |
|  4 | BND      | 5.0%              | 4.11%                |          6 |         86.48 |           518.88 |               630.9  |               112.02 |                1.2953 |
|  5 | MUB      | 10.0%             | 7.47%                |          8 |        117.83 |           942.64 |              1261.8  |               319.16 |                2.7086 |
|  6 | LQD      | 2.5%              | 2.14%                |          2 |        135.47 |           270.94 |               315.45 |                44.51 |                0.3286 |
|  7 | BNDX     | 2.5%              | 2.28%                |          5 |         57.76 |           288.8  |               315.45 |                26.65 |                0.4614 |
|  8 | XLE      | 5.0%              | 14.1%                |         36 |         49.72 |          1789.92 |               630.9  |             -1159.02 |              -23.3109 |
|  9 | GLD      | 5.0%              | 0.0%                 |          0 |        168.16 |             0    |               630.9  |               630.9  |                3.7518 |