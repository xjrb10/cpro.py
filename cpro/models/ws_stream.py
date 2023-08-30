import json
import typing
from dataclasses import dataclass, field
from datetime import datetime
from decimal import *

from dataclasses_json import dataclass_json, Undefined, config, DataClassJsonMixin

from cpro.exception import CoinsAPIException
from cpro.models.rest.enums import ChartIntervals, WSStreamDataEventTypes, WSStreamProcedures
from cpro.models.rest.market import MarketOrder


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class WSFrame(DataClassJsonMixin):
    pass


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class StreamData(WSFrame):
    pass


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class AggregateTradeData(StreamData):
    eventType: WSStreamDataEventTypes = field(metadata=config(
        field_name="e"
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
    eventType: WSStreamDataEventTypes = field(metadata=config(
        field_name="e"
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
    eventType: WSStreamDataEventTypes = field(metadata=config(
        field_name="e"
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
    eventType: WSStreamDataEventTypes = field(metadata=config(
        field_name="e"
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
    eventType: WSStreamDataEventTypes = field(metadata=config(
        field_name="e"
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
    eventType: WSStreamDataEventTypes = field(metadata=config(
        field_name="e"
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
    eventType: WSStreamDataEventTypes = field(metadata=config(
        field_name="e"
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


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class RPCFrame(WSFrame):
    pass


TRPCFrame = typing.TypeVar("TRPCFrame", bound=RPCFrame)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class PingRequestFrame(RPCFrame):
    ping: datetime = field(
        default_factory=lambda: datetime.now(),
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class PingResponseFrame(RPCFrame):
    pong: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class RPCResponseFrame(RPCFrame):
    # id: int
    # result: typing.Any
    pass


TRPCResponseFrame = typing.TypeVar("TRPCResponseFrame", bound=RPCResponseFrame)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class RPCRequestFrame(RPCFrame):
    # method: WSStreamProcedures
    # params: typing.Optional[typing.Any] = None
    # id: typing.Optional[int] = None  # to be filled (if missing) by WSClient.rpc_request()

    @classmethod
    def expected_response(cls) -> typing.Type[TRPCResponseFrame]:
        raise NotImplementedError


TRPCRequestFrame = typing.TypeVar("TRPCRequestFrame", bound=RPCRequestFrame)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class StreamSubscribeResponse(RPCResponseFrame):
    id: int
    result: None


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class StreamSubscribeRequest(RPCRequestFrame):
    params: list[str]
    method: WSStreamProcedures = WSStreamProcedures.SUBSCRIBE
    id: typing.Optional[int] = None

    @classmethod
    def expected_response(cls) -> typing.Type[TRPCResponseFrame]:
        return StreamSubscribeResponse


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class StreamUnsubscribeResponse(RPCResponseFrame):
    id: int
    result: None


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class StreamUnsubscribeRequest(RPCRequestFrame):
    params: list[str]
    method: WSStreamProcedures = WSStreamProcedures.UNSUBSCRIBE
    id: typing.Optional[int] = None

    @classmethod
    def expected_response(cls) -> typing.Type[TRPCResponseFrame]:
        return StreamUnsubscribeResponse


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class SubscriptionListResponse(RPCResponseFrame):
    id: int
    result: list[str]


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class SubscriptionListRequest(RPCRequestFrame):
    method: WSStreamProcedures = WSStreamProcedures.LIST_SUBSCRIPTIONS
    id: typing.Optional[int] = None

    @classmethod
    def expected_response(cls) -> typing.Type[TRPCResponseFrame]:
        return SubscriptionListResponse


def unmarshal_frame(
        json_data: str,
        expected_response_type: typing.Optional[TRPCFrame] = None,
        expected_response_id: typing.Optional[int] = None
) -> WSFrame:
    print(json_data)
    received_object = json.loads(json_data)
    if (expected_response_type or expected_response_id) and not (expected_response_type and expected_response_id):
        # allow expected_response_type of PingResponseFrame without requiring ID, but resolve all ping requests with
        # the resulting latency, and the server time
        raise ValueError(
            "Both expected_response_type and expected_response_id must be set if one of the other is provided."
        )

    if "error" in received_object:
        raise CoinsAPIException(received_object["error"]["code"], received_object["error"]["msg"])

    # attempt to decode RPC calls
    if len(received_object) == 1:
        if "ping" in received_object:
            return PingRequestFrame.from_dict(received_object)
        if "pong" in received_object:
            return PingResponseFrame.from_dict(received_object)

    if "id" in received_object and int(received_object["id"]) == expected_response_id:
        return expected_response_type.from_dict(received_object)

    elif not (expected_response_type and expected_response_id):
        match WSStreamDataEventTypes(received_object["e"]):
            case WSStreamDataEventTypes.AGGREGATE_TRADE:
                return AggregateTradeData.from_dict(received_object)
            case WSStreamDataEventTypes.TRADE:
                return TradeData.from_dict(received_object)
            case WSStreamDataEventTypes.KLINE:
                return KlineCandlestickData.from_dict(received_object)
            case WSStreamDataEventTypes._24H_MINI_TICKER:
                return IndividualSymbolMiniTickerData.from_dict(received_object)
            case WSStreamDataEventTypes._24H_TICKER:
                return IndividualSymbolTickerData.from_dict(received_object)
            case WSStreamDataEventTypes.PARTIAL_BOOK_DEPTH:
                return PartialBookDepthData.from_dict(received_object)
            case WSStreamDataEventTypes.DIFF_DEPTH:
                return DiffDepthData.from_dict(received_object)

    raise ValueError(f"Unable to unmarshal received frame: {json_data}")
