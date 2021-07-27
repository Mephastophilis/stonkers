import yaml
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si


class stock_portfolio:
    """Stock Portfolio Class
    """

    def __init__(self, portfolio_filename=None):
        if portfolio_filename:
            with open(portfolio_filename) as f:
                yaml_objects = yaml.safe_load(f)
                self.holding_percentage = yaml_objects["port_goals"]
                self.holdings = yaml_objects["port_holds"]
        else:
            self.holding_percentage = {}
            self.holdings = {}
        self.cols = [
            "ticker",
            "goal_percentage",
            "holding_percentage",
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

    def add_percent_holding(self, ticker, percentage):
        assert (type(ticker)) == str
        self.holding_percentage[ticker] = percentage

    def create_dataframe(self):
        self.dataframe = pd.DataFrame(
            data={
                "ticker": self.holding_percentage.keys(),
                "goal_percentage": self.holding_percentage.values(),
                "holdings": self.holdings.values(),
            }
        )
        self.dataframe["stock_price"] = round(
            self.dataframe.apply(lambda x: si.get_live_price(x.ticker), axis=1), 2
        )
        self.dataframe["holdings_value"] = round(
            self.dataframe.stock_price * self.dataframe.holdings, 2
        )
        self.dataframe["goal_holding_value"] = round(
            self.dataframe.goal_percentage * self.dataframe.holdings_value.sum(), 2
        )
        self.dataframe["holding_value_diff"] = (
            self.dataframe.goal_holding_value - self.dataframe.holdings_value
        )
        self.dataframe["holding_percentage"] = (
            self.dataframe.holdings_value / self.dataframe.holdings_value.sum()
        )

    def balance_buy_sell(self):
        if not hasattr(self, "dataframe"):
            self.create_dataframe()
        self.dataframe["need_to_buy_or_sell"] = round(
            self.dataframe.holding_value_diff / self.dataframe.stock_price, 4
        )

    def balance_only_buy(self):
        if not hasattr(self, "dataframe"):
            self.create_dataframe()

        ticker_min = self.dataframe[
            self.dataframe.need_to_buy == self.dataframe.need_to_buy.min()
        ].ticker.values
        min_buy_val = self.dataframe.need_to_buy.min()
        df_ = self.dataframe[self.dataframe.ticker == ticker_min[0]]
        goal_portfolio_value = (df_.holdings_value / df_.goal_percentage).values[0]
        print(goal_portfolio_value, self.dataframe.holdings_value.sum())
        self.dataframe["need_to_buy"] = round(
            (
                goal_portfolio_value * self.dataframe.goal_percentage
                - self.dataframe.holdings_value
            )
            / self.dataframe.stock_price,
            4,
        )

    def display_df(self):
        self.balance_buy_sell()
        df_ = self.dataframe
        df_["goal_percentage"] = df_.goal_percentage.apply(
            lambda x: "{:.4}%".format(str(x * 100))
        )
        df_["holding_percentage"] = df_.holding_percentage.apply(
            lambda x: "{:.4}%".format(str(x * 100))
        )

        print(df_[self.cols + ["need_to_buy_or_sell"]].to_markdown())
