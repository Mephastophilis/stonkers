"""empty_portfolio_demo.py
This demo assumes you are starting from scratch with $3000 to invest in
a new portfolio that will align with the goal percentages in
demo_portfolio.yml. It will print out what stocks to buy in order to get
this new portfolio started.
"""

from stonkers import stock_portfolio

portfolio = stock_portfolio(portfolio_filename="demo_portfolio.yml")

for ticker in portfolio.goal_percentage.keys():
    portfolio.add_holding(ticker, 0)

portfolio.stock_buy_advisor(3000)
portfolio.display_df(to_markdown=True)

print("Demo done!")
