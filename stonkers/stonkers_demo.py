"""stonkers_demo.py
"""

from stonkers import stock_portfolio

portfolio = stock_portfolio(portfolio_filename="demo_portfolio.yml")

portfolio.display_df(to_markdown=True)
portfolio.stock_buy_advisor(1000)

print("Demo done!")