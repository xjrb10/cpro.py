from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import dataclass_json, Undefined, config, DataClassJsonMixin
from marshmallow.fields import Decimal


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
