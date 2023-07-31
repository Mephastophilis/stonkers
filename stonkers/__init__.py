import yaml
from collections import Counter
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
from stonkers.data_models import Portfolio, PortfolioHolding


class stock_portfolio:
    """Stock Portfolio Class"""

    def __init__(self, portfolio_model: Portfolio = None):
        if portfolio_model:
            self.portfolio = portfolio_model
            self.pull_stock_prices()
            self.calculate_portfolio_stats()
        else:
            self.portfolio = None

    def display_df(self):
        display(pd.DataFrame(self.portfolio.dict()['holdings']))

    def check_percent_holdings(self, autobalance=False):
        total = sum([holding.target_percentage for holding in self.portfolio.holdings])
        if np.isclose(total, 1):
            print("Balanced")
        if total > 1:
            raise ValueError("Target percetnages sum to greater than one")
        if total < 1:
            raise ValueError("Target percentages sum is less than one")

        if auto_balance:
            print("AutoBalancing")
            for holding in self.portfolio.holdings:
                holding.target_percentage = holding.target_percentage / total

    def add_or_modify_holding(self, ticker, target_percentage, shares):
        new_holding = PortfolioHolding(
            ticker=ticker, target_percentage=target_percentage, shares=shares
        )
        self.portfolio.holdings[ticker] = new_holding

    def add_one_share(self, ticker):
        self.portfolio.holdings[ticker].shares += 1

    def pull_stock_prices(self):
        for ticker_, holding in self.portfolio.holdings.items():
            stock_price = si.get_live_price(ticker_)
            self.portfolio.holdings[ticker_].price = stock_price

    def calculate_portfolio_stats(self):
        if None in [
            holding_.price for ticker_, holding_ in self.portfolio.holdings.items()
        ]:
            self.pull_stock_prices()
        total_portfolio_value_ = sum(
            [
                holding.shares * holding.price
                for _, holding in self.portfolio.holdings.items()
            ]
        )
        self.total_portfolio_value = total_portfolio_value_
        for ticker_, holding in self.portfolio.holdings.items():
            equity_ = holding.price * holding.shares
            target_percentage_ = holding.target_percentage
            equity_target_difference_ = (
                total_portfolio_value_ * target_percentage_ - equity_
            )
            price_ = holding.price
            target_percentage_ = holding.target_percentage

            self.portfolio.holdings[ticker_].equity = equity_
            self.portfolio.holdings[ticker_].portfolio_percentage = (
                equity_ / total_portfolio_value_
            )
            self.portfolio.holdings[
                ticker_
            ].equity_target_difference = equity_target_difference_
            self.portfolio.holdings[ticker_].number_of_shares_off_target = (
                equity_target_difference_ / price_
            )
            self.portfolio.holdings[ticker_].equity_target_difference_scaled = (
                equity_target_difference_ / target_percentage_
            )

    def stock_buy_advisor(self, investment_dollars):
        """Tells you which stocks to buy bash on available cash and the
        current balance of your porttfolio.
        """
        self.calculate_portfolio_stats()
        print(f"Attempting to buy stocks with ${investment_dollars}")

        allocating_investments = True
        self.buy_counter = Counter()

        while allocating_investments:

            next_stonk_to_buy_ = max(
                [
                    (holding.equity_target_difference_scaled, holding.ticker)
                    for holding in self.portfolio.holdings.values()
                ]
            )[1]
            price_of_stonk_ = self.portfolio.holdings[next_stonk_to_buy_].price

            if investment_dollars < price_of_stonk_:
                allocating_investments = False
            else:
                investment_dollars -= price_of_stonk_
                self.buy_counter[next_stonk_to_buy_] += 1
                self.add_one_share(next_stonk_to_buy_)
                self.calculate_portfolio_stats()

        print("Leftover cash:", investment_dollars)
        print(self.buy_counter)


class stock_portfolio_old:
    """Stock Portfolio Class"""

    def __init__(self, portfolio_filename=None):
        if portfolio_filename:
            with open(portfolio_filename) as f:
                yaml_objects = yaml.safe_load(f)
                self.goal_percentage = yaml_objects["port_goals"]
                self.holdings = yaml_objects["port_holds"]
        else:
            self.goal_percentage = {}
            self.holdings = {}
        self.cols = [
            "ticker",
            "goal_percentage",
            "holding_percentage",
            "holdings",
            "stock_price",
            "holding_value_diff",
            "need_to_buy_or_sell",
            "need_to_buy",
        ]

    def add_holding(self, ticker, amount):
        assert (type(ticker)) == str
        assert (type(amount)) == int
        self.holdings[ticker] = amount

    def add_goal_percent(self, ticker, percentage):
        assert (type(ticker)) == str
        self.goal_percentage[ticker] = percentage

    def check_percent_holdings(self, balance_percents=False):
        percentage_sum = sum(self.goal_percentage.values())
        if percentage_sum != 1:
            print("Portfolio percentages do not sum to 100%")
            if balance_percents:
                for ticker in self.goal_percentage.keys():
                    print("Rebalancing holding percentages to sum to 100%")
                    self.goal_percentage[ticker] = (
                        self.goal_percentage[ticker] / percentage_sum
                    )

    def pull_stock_prices(self):
        self.stock_price = {
            t: si.get_live_price(t) for t in self.goal_percentage.keys()
        }

    def calculate_portfolio_stats(self):
        if not hasattr(self, "holdings"):
            print("Please add hodlings before calculating stats")

        elif not hasattr(self, "goal_percentage"):
            print("Please add goal percentage before calculating stats")

        else:
            if not hasattr(self, "stock_price"):
                self.pull_stock_prices()

            self.holdings_value = {
                t: round(self.stock_price[t] * self.holdings[t], 2)
                for t in self.goal_percentage.keys()
            }
            self.total_portfolio_value = round(sum(self.holdings_value.values()), 2)

            self.goal_holding_value = {
                t: round(self.goal_percentage[t] * self.total_portfolio_value, 2,)
                for t in self.goal_percentage.keys()
            }
            self.holding_value_diff = {
                t: self.goal_holding_value[t] - self.holdings_value[t]
                for t in self.goal_percentage.keys()
            }
            self.holding_percentage = {
                t: self.holdings_value[t] / self.total_portfolio_value
                for t in self.goal_percentage.keys()
            }
            self.holding_value_diff_scaled = {
                t: self.holding_value_diff[t] / self.goal_percentage[t]
                for t in self.goal_percentage.keys()
            }

    def balance_portfolio(self, verbose=True):
        self.calculate_portfolio_stats()
        self.need_to_buy_or_sell = {}
        for ticker in self.goal_percentage.keys():
            self.need_to_buy_or_sell[ticker] = round(
                self.holding_value_diff[ticker] / self.stock_price[ticker], 2
            )

        ticker_min = min(
            self.holding_value_diff_scaled, key=self.holding_value_diff_scaled.get
        )
        self.goal_portfolio_value = round(
            self.holdings_value[ticker_min] / self.goal_percentage[ticker_min], 2
        )
        if verbose:
            print("Current total portfolio value:", self.total_portfolio_value)
            print(
                "Necessary Portfolio value to rebalance with only buying:",
                self.goal_portfolio_value,
            )
            print(
                "Required Cash Money:",
                round(self.goal_portfolio_value - self.total_portfolio_value, 2),
            )

        self.need_to_buy = {
            t: round(
                (
                    self.goal_portfolio_value * self.goal_percentage[t]
                    - self.holdings_value[t]
                )
                / self.stock_price[t],
                2,
            )
            for t in self.goal_percentage.keys()
        }

    def create_dataframe(self):
        if not hasattr(self, "need_to_buy_or_sell"):
            self.balance_portfolio()
        self.dataframe = pd.DataFrame(
            data={
                "ticker": self.goal_percentage.keys(),
                "goal_percentage": self.goal_percentage.values(),
                "holding_percentage": self.holding_percentage.values(),
                "holdings": self.holdings.values(),
                "stock_price": self.stock_price.values(),
                "holdings_value": self.holdings_value.values(),
                "goal_holding_value": self.goal_holding_value.values(),
                "holding_value_diff": self.holding_value_diff.values(),
                "holding_value_diff_scaled": self.holding_value_diff_scaled.values(),
                "need_to_buy_or_sell": self.need_to_buy_or_sell.values(),
                "need_to_buy": self.need_to_buy.values(),
            }
        )
        # convert percentage columns into readable strings
        self.dataframe["goal_percentage"] = self.dataframe.goal_percentage.apply(
            lambda x: "{:.4}%".format(str(x * 100))
        )
        self.dataframe["holding_percentage"] = self.dataframe.holding_percentage.apply(
            lambda x: "{:.4}%".format(str(x * 100))
        )

    def display_df(self, to_markdown=False):
        if not hasattr(self, "dataframe"):
            self.create_dataframe()
        if to_markdown:
            print(self.dataframe[self.cols].to_markdown(index=False))
        else:
            return self.dataframe[self.cols]

    def stock_buy_advisor(self, buying_cash: float):
        """Tells you which stocks to buy bash on available cash and the
        current balance of your porttfolio.
        """
        if not hasattr(self, "need_to_buy_or_sell"):
            self.balance_portfolio()
        print(f"Attempting to buy stocks with ${buying_cash}")
        allocating_invest_chunk = True
        self.buy_counter = Counter()

        while allocating_invest_chunk:
            next_stonk_buy = max(
                self.holding_value_diff_scaled, key=self.holding_value_diff_scaled.get
            )
            if buying_cash < self.stock_price[next_stonk_buy]:
                allocating_invest_chunk = False
                break
            else:
                buying_cash -= self.stock_price[next_stonk_buy]
                self.buy_counter[next_stonk_buy] += 1
                self.add_holding(next_stonk_buy, self.holdings[next_stonk_buy] + 1)
                self.balance_portfolio(verbose=False)
        self.create_dataframe()
        print("Leftover cash:", buying_cash)
        print(self.buy_counter)
