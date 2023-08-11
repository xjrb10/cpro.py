import typing
from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import dataclass_json, Undefined, config, DataClassJsonMixin
from marshmallow.fields import Decimal

from cpro.models.rest.enums import ChartIntervals
from cpro.models.rest.market import MarketOrder


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class StreamData(DataClassJsonMixin):
    pass


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class AggregateTradeData(StreamData):
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
        field_name="e"  # aggTrade
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    aggregateTradeID: int = field(metadata=config(
        field_name="a"
    ))
    price: Decimal = field(metadata=config(
        field_name="p",
    ))
    quantity: Decimal = field(metadata=config(
        field_name="q",
    ))
    firstTradeID: int = field(metadata=config(
        field_name="f"
    ))
    lastTradeID: int = field(metadata=config(
        field_name="l"
    ))
    tradeTime: datetime = field(metadata=config(
        field_name="T",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    isBuyerMarketMaker: bool = field(metadata=config(
        field_name="m"
    ))
    _ignored: typing.Optional[Decimal] = field(
        default=None,
        metadata=config(field_name="M")
    )


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class TradeData(StreamData):
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
        field_name="e"  # trade
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    tradeID: int = field(metadata=config(
        field_name="t",
    ))
    price: Decimal = field(metadata=config(
        field_name="p",
    ))
    quantity: Decimal = field(metadata=config(
        field_name="q",
    ))
    buyerOrderID: Decimal = field(metadata=config(
        field_name="b",
    ))
    sellerOrderID: Decimal = field(metadata=config(
        field_name="a",
    ))
    tradeTime: datetime = field(metadata=config(
        field_name="T",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    isBuyerMarketMaker: bool = field(metadata=config(
        field_name="m"
    ))
    _ignored: typing.Optional[Decimal] = field(
        default=None,
        metadata=config(field_name="M")
    )


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class GraphPointData:
    startTime: datetime = field(metadata=config(
        field_name="t",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    closeTime: datetime = field(metadata=config(
        field_name="T",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    interval: ChartIntervals = field(metadata=config(
        field_name="i"
    ))
    firstTradeID: int = field(metadata=config(
        field_name="f"
    ))
    lastTradeID: int = field(metadata=config(
        field_name="L"
    ))
    openPrice: Decimal = field(metadata=config(
        field_name="o"
    ))
    closePrice: Decimal = field(metadata=config(
        field_name="c"
    ))
    highPrice: Decimal = field(metadata=config(
        field_name="h"
    ))
    lowPrice: Decimal = field(metadata=config(
        field_name="l"
    ))
    baseAssetVolume: Decimal = field(metadata=config(
        field_name="v"
    ))
    totalTradeCount: int = field(metadata=config(
        field_name="n"
    ))
    isClosed: bool = field(metadata=config(
        field_name="x"
    ))
    quoteAssetVolume: Decimal = field(metadata=config(
        field_name="q"
    ))
    takerBuyBaseAssetVolume: Decimal = field(metadata=config(
        field_name="V"
    ))
    takerBuyQuoteAssetVolume: Decimal = field(metadata=config(
        field_name="Q"
    ))
    _ignored: typing.Optional[Decimal] = field(
        default=None,
        metadata=config(field_name="B")
    )


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class KlineCandlestickData(StreamData):
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
        field_name="e"  # kline
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    dataPoint: GraphPointData = field(metadata=config(
        field_name="k"
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class IndividualSymbolMiniTickerData(StreamData):
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
        field_name="e"  # 24hrMiniTicker
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    closePrice: Decimal = field(metadata=config(
        field_name="c"
    ))
    openPrice: Decimal = field(metadata=config(
        field_name="o"
    ))
    highPrice: Decimal = field(metadata=config(
        field_name="h"
    ))
    lowPrice: Decimal = field(metadata=config(
        field_name="l"
    ))
    totalTradedBaseAssetVolume: Decimal = field(metadata=config(
        field_name="v"
    ))
    totalTradedQuoteAssetVolume: Decimal = field(metadata=config(
        field_name="q"
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class IndividualSymbolTickerData(StreamData):
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
        field_name="e"  # 24hrTicker
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    priceChange: Decimal = field(metadata=config(
        field_name="p"
    ))
    priceChangePercent: Decimal = field(metadata=config(
        field_name="P"
    ))
    weightedAveragePrice: Decimal = field(metadata=config(
        field_name="w"
    ))
    firstTradePrice: Decimal = field(metadata=config(
        field_name="x"
    ))
    lastPrice: Decimal = field(metadata=config(
        field_name="c"
    ))
    lastQuantity: Decimal = field(metadata=config(
        field_name="Q"
    ))
    bestBidPrice: Decimal = field(metadata=config(
        field_name="b"
    ))
    bestBidQuantity: Decimal = field(metadata=config(
        field_name="B"
    ))
    bestAskPrice: Decimal = field(metadata=config(
        field_name="a"
    ))
    bestAskQuantity: Decimal = field(metadata=config(
        field_name="A"
    ))
    openPrice: Decimal = field(metadata=config(
        field_name="o"
    ))
    highPrice: Decimal = field(metadata=config(
        field_name="h"
    ))
    lowPrice: Decimal = field(metadata=config(
        field_name="l"
    ))
    totalTradedBaseAssetVolume: Decimal = field(metadata=config(
        field_name="v"
    ))
    totalTradedQuoteAssetVolume: Decimal = field(metadata=config(
        field_name="q"
    ))
    statisticsOpenTime: datetime = field(metadata=config(
        field_name="O",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    statisticsCloseTime: datetime = field(metadata=config(
        field_name="C",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    firstTradeID: int = field(metadata=config(
        field_name="F"
    ))
    lastTradeID: int = field(metadata=config(
        field_name="L"
    ))
    totalTradeCount: int = field(metadata=config(
        field_name="n"
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class IndividualSymbolBookTickerData(StreamData):
    orderBookUpdateID: int = field(metadata=config(
        field_name="u"
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    bestBidPrice: Decimal = field(metadata=config(
        field_name="b"
    ))
    bestBidQuantity: Decimal = field(metadata=config(
        field_name="B"
    ))
    bestAskPrice: Decimal = field(metadata=config(
        field_name="a"
    ))
    bestAskQuantity: Decimal = field(metadata=config(
        field_name="A"
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class PartialBookDepthData(StreamData):
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
        field_name="e"  # depth
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    lastUpdateID: int = field(metadata=config(
        field_name="lastUpdateId"
    ))
    bidsUpdated: list[MarketOrder] = field(metadata=config(
        field_name="b",
        encoder=lambda _: [(__.price, __.qty) for __ in _],
        decoder=lambda _: [MarketOrder(*__) for __ in _]
    ))
    asksUpdated: list[MarketOrder] = field(metadata=config(
        field_name="a",
        encoder=lambda _: [(__.price, __.qty) for __ in _],
        decoder=lambda _: [MarketOrder(*__) for __ in _]
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class DiffDepthData(StreamData):
    # https://coins-docs.github.io/web-socket-streams/#diff-depth-stream
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
        field_name="e"  # depthUpdate
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    firstUpdateID: int = field(metadata=config(
        field_name="U"
    ))
    lastUpdateID: int = field(metadata=config(
        field_name="u"
    ))
    bidsUpdated: list[MarketOrder] = field(metadata=config(
        field_name="b",
        encoder=lambda _: [(__.price, __.qty) for __ in _],
        decoder=lambda _: [MarketOrder(*__) for __ in _]
    ))
    asksUpdated: list[MarketOrder] = field(metadata=config(
        field_name="a",
        encoder=lambda _: [(__.price, __.qty) for __ in _],
        decoder=lambda _: [MarketOrder(*__) for __ in _]
    ))
