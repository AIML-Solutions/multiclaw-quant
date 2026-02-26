from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class MarketBar(BaseModel):
    symbol: str = Field(min_length=1)
    ts: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal = Decimal("0")
    source: str = "lean"


class GreeksSnapshot(BaseModel):
    underlying: str
    option_symbol: str
    ts: datetime
    price: Decimal
    iv: Decimal | None = None
    delta: Decimal | None = None
    gamma: Decimal | None = None
    vega: Decimal | None = None
    theta: Decimal | None = None
    rho: Decimal | None = None
    model: str = "unspecified"
