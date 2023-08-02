import yaml
from stonkers import stock_portfolio

portfolio_filename = "portfolios/stonkers_advisor_port.yaml"

portfolio = stock_portfolio(portfolio_filename=portfolio_filename)

portfolio.check_percent_holdings()

print("Current Portfolio")
portfolio.display_df(to_markdown=True)
print()



print("How much money are you going to invest?")
investment_amount = float(input())
print(f"Calculating stocks to but with {investment_amount}")

portfolio.stock_buy_advisor(investment_amount)

print("\nNew portfolio after buying")
portfolio.display_df(to_markdown=True)

print("Are you going to buy these stocks? Enter 1 to update porfolio holdings.")

decision = input()
if decision=='1':
    output_dict = {'port_goals': portfolio.goal_percentage, 'port_holds': portfolio.holdings}
    with open(portfolio_filename, 'w') as f:
        yaml.dump(output_dict, f)
    print("Portfolio holdings yaml file updated.")

print("Thank you for using stonkers. We hope your stonkers go up!")
