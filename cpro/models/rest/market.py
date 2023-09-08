"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2023-present xjrb10

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import *

from dataclasses_json import dataclass_json, Undefined, config, DataClassJsonMixin


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class MarketOrder:
    price: Decimal
    qty: Decimal


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class TradeInfo:
    id: int
    price: Decimal
    qty: Decimal
    quoteQty: Decimal
    isBuyerMaker: bool
    isBestMatch: bool
    time: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )


@dataclass(frozen=True)
class MarketDatapoint(DataClassJsonMixin):
    openTime: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    closeTime: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    quoteAssetVolume: Decimal
    trades: int
    takerBuyBaseAssetVolume: Decimal
    takerBuyQuoteAssetVolume: Decimal


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class TickerStatistics:
    symbol: str
    priceChange: Decimal
    priceChangePercent: Decimal
    weightedAvgPrice: Decimal
    prevClosePrice: Decimal
    lastPrice: Decimal
    lastQty: Decimal
    bidPrice: Decimal
    bidQty: Decimal
    askPrice: Decimal
    askQty: Decimal
    openPrice: Decimal
    highPrice: Decimal
    lowPrice: Decimal
    volume: Decimal
    quoteVolume: Decimal
    openTime: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    closeTime: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    firstTradeId: int = field(
        metadata=config(
            field_name="firstId"
        )
    )
    lastTradeId: int = field(
        metadata=config(
            field_name="lastId"
        )
    )
    tradeCount: int = field(
        metadata=config(
            field_name="count"
        )
    )


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class SymbolPriceTickerStatistics:
    symbol: str
    price: Decimal


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class SymbolOrderBookTickerStatistics:
    symbol: str
    bidPrice: Decimal
    bidQty: Decimal
    askPrice: Decimal
    askQty: Decimal


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class CryptoAssetTradingPair:
    symbol: str
    quoteToken: str
    baseToken: str
