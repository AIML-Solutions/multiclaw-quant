from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class MarketBarIn(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    ts: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal = Decimal("0")
    source: str = Field(min_length=1, max_length=32)


class GreeksIn(BaseModel):
    underlying: str = Field(min_length=1, max_length=32)
    option_symbol: str = Field(min_length=1, max_length=96)
    ts: datetime
    price: Decimal
    iv: Decimal | None = None
    delta: Decimal | None = None
    gamma: Decimal | None = None
    vega: Decimal | None = None
    theta: Decimal | None = None
    rho: Decimal | None = None
    model: str = Field(default="unspecified", max_length=32)
