"""stonkers_demo.py
"""

from stonkers import stock_portfolio

portfolio = stock_portfolio(portfolio_filename="demo_portfolio.yml.yml")

portfolio.display_df()

print("Demo done!")