import yaml
from collections import Counter
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si


class stock_portfolio:
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
            "holdings",
            "stock_price",
            "holdings_value",
            "goal_holding_value",
            "holding_value_diff",
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
        self.stock_price = {}
        for ticker in self.goal_percentage.keys():
            self.stock_price[ticker] = si.get_live_price(ticker)

    def calculate_portfolio_stats(self):
        if not hasattr(self, "holdings"):
            print("Please add hodlings before calculating stats")

        elif not hasattr(self, "goal_percentage"):
            print("Please add goal percentage before calculating stats")

        else:
            if not hasattr(self, "stock_price"):
                self.pull_stock_prices()

            self.holdings_value = {}
            self.goal_holding_value = {}
            self.holding_value_diff = {}
            self.holding_percentage = {}
            for ticker in self.goal_percentage.keys():
                self.holdings_value[ticker] = round(
                    self.stock_price[ticker] * self.holdings[ticker], 2
                )
            for ticker in self.goal_percentage.keys():
                self.goal_holding_value[ticker] = round(
                    self.goal_percentage[ticker] * (sum(self.holdings_value.values())),
                    2,
                )
                self.holding_value_diff[ticker] = (
                    self.goal_holding_value[ticker] - self.holdings_value[ticker]
                )
                self.holding_percentage[ticker] = self.holdings_value[ticker] / sum(
                    self.holdings_value.values()
                )

    def balance_portfolio(self, verbose=True):
        self.calculate_portfolio_stats()
        self.need_to_buy_or_sell = {}
        for ticker in self.goal_percentage.keys():
            self.need_to_buy_or_sell[ticker] = round(
                self.holding_value_diff[ticker] / self.stock_price[ticker], 4
            )

        self.need_to_buy = {}
        ticker_min = min(self.need_to_buy_or_sell, key=self.need_to_buy_or_sell.get)
        self.goal_portfolio_value = (
            self.holdings_value[ticker_min] / self.goal_percentage[ticker_min]
        )
        if verbose:
            print("Current total portfolio value:", sum(self.holdings_value.values()))
            print(
                "Necessary Portfolio value to rebalance with only buying:",
                self.goal_portfolio_value,
            )
            print(
                "Required Cash Money:",
                round(self.goal_portfolio_value - sum(self.holdings_value.values()), 2),
            )
        for ticker in self.goal_percentage.keys():
            self.need_to_buy[ticker] = round(
                (
                    self.goal_portfolio_value * self.goal_percentage[ticker]
                    - self.holdings_value[ticker]
                )
                / self.stock_price[ticker],
                4,
            )

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
            print(self.dataframe.to_markdown(index=False))
        else:
            return self.dataframe

    def stock_buy_advisor(self, buying_cash):
        """Tells you which stocks to buy bash on available cash and the
        current balance of your porttfolio.
        """
        if not hasattr(self, "need_to_buy_or_sell"):
            self.balance_portfolio()
        allocating_invest_chunk = True
        self.buy_counter = Counter()

        while allocating_invest_chunk:
            next_stonk_buy = max(
                self.holding_value_diff, key=self.holding_value_diff.get
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
