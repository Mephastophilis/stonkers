from pydantic import BaseModel, confloat

from typing import List, Dict


class PortfolioHolding(BaseModel):
    ticker: str
    target_percentage: confloat(ge=0, le=1)
    shares: confloat(ge=0)
    price: confloat(ge=0) = None
    equity: confloat(ge=0) = None
    portfolio_percentage: float = None
    equity_target_difference: float = None
    number_of_shares_off_target: float = None
    equity_target_difference_scaled: float = None


class Portfolio(BaseModel):
    holdings: Dict[str, PortfolioHolding] = None
