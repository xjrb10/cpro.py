from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar

from dataclasses_json import dataclass_json, config, Undefined, DataClassJsonMixin
from marshmallow.fields import Decimal

from cpro.models.rest.market import MarketOrder, TradeInfo, MarketDatapoint, TickerStatistics, \
    SymbolPriceTickerStatistics, SymbolOrderBookTickerStatistics, CryptoAssetTradingPair
from cpro.models.rest.symbol import SymbolInfo
from cpro.models.rest.wallet import Coin, DepositTransactionInfo, WithdrawTransactionInfo


@dataclass(frozen=True)
class ResponsePayload(DataClassJsonMixin):
    pass


TResponsePayload = TypeVar("TResponsePayload", bound=ResponsePayload)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class PingResponse(ResponsePayload):
    pass


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class ServerTimeResponse(ResponsePayload):
    serverTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class ExchangeInformationResponse(ResponsePayload):
    timezone: str  # default: UTC - todo: currently this is ignored by the lib
    serverTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)  # todo: perhaps base timezone from given timezone field?
    ))
    exchangeFilters: list  # empty -- Reason: https://coins-docs.github.io/rest-api/#exchange-filters
    symbols: list[SymbolInfo]


@dataclass(frozen=True)
class CoinsInformationResponse(ResponsePayload, DataClassJsonMixin):
    coins: list[Coin]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CoinsInformationResponse":
        if isinstance(kvs, list):
            return super().from_dict({"coins": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class DepositAddressResponse(ResponsePayload):
    coin: str
    address: str
    addressTag: str


@dataclass(frozen=True)
class DepositHistoryResponse(ResponsePayload, DataClassJsonMixin):
    transactions: list[DepositTransactionInfo]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "DepositHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"transactions": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass(frozen=True)
class WithdrawHistoryResponse(ResponsePayload, DataClassJsonMixin):
    transactions: list[WithdrawTransactionInfo]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "WithdrawHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"transactions": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class OrderBookResponse(ResponsePayload):
    lastUpdateId: int
    bids: list[MarketOrder] = field(
        metadata=config(
            encoder=lambda _: [(__.price, __.qty) for __ in _],
            decoder=lambda _: [MarketOrder(*__) for __ in _]
        )
    )
    asks: list[MarketOrder] = field(
        metadata=config(
            encoder=lambda _: [(__.price, __.qty) for __ in _],
            decoder=lambda _: [MarketOrder(*__) for __ in _]
        )
    )


@dataclass(frozen=True)
class RecentTradesResponse(ResponsePayload, DataClassJsonMixin):
    trades: list[TradeInfo]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "RecentTradesResponse":
        if isinstance(kvs, list):
            return super().from_dict({"trades": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass(frozen=True)
class GraphDataResponse(ResponsePayload, DataClassJsonMixin):
    datapoints: list[MarketDatapoint] = field(
        metadata=config(
            decoder=lambda _: [MarketDatapoint.from_dict({
                # map into dict for typed parsing
                "openTime": __[0],
                "open": __[1],
                "high": __[2],
                "low": __[3],
                "close": __[4],
                "volume": __[5],
                "closeTime": __[6],
                "quoteAssetVolume": __[7],
                "trades": __[8],
                "takerBuyBaseAssetVolume": __[9],
                "takerBuyQuoteAssetVolume": __[10],
            }) for __ in _]
        )
    )

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "GraphDataResponse":
        if isinstance(kvs, list):
            return super().from_dict({"datapoints": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass(frozen=True)
class DailyTickerResponse(ResponsePayload, DataClassJsonMixin):
    tickers: list[TickerStatistics]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "DailyTickerResponse":
        if isinstance(kvs, list):
            return super().from_dict({"tickers": kvs}, infer_missing=infer_missing)
        return super().from_dict({"tickers": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class SymbolPriceTickerResponse(ResponsePayload, DataClassJsonMixin):
    tickers: list[SymbolPriceTickerStatistics]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "SymbolPriceTickerResponse":
        if isinstance(kvs, list):
            return super().from_dict({"tickers": kvs}, infer_missing=infer_missing)
        return super().from_dict({"tickers": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class SymbolOrderBookTickerResponse(ResponsePayload, DataClassJsonMixin):
    tickers: list[SymbolOrderBookTickerStatistics]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "SymbolOrderBookTickerResponse":
        if isinstance(kvs, list):
            return super().from_dict({"tickers": kvs}, infer_missing=infer_missing)
        return super().from_dict({"tickers": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class CryptoAssetTradingPairListResponse(ResponsePayload, DataClassJsonMixin):
    pairs: list[CryptoAssetTradingPair]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CryptoAssetTradingPairListResponse":
        if isinstance(kvs, list):
            return super().from_dict({"pairs": kvs}, infer_missing=infer_missing)
        return super().from_dict({"pairs": [kvs]}, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class CryptoAssetCurrentPriceAverageResponse(ResponsePayload):
    mins: int
    price: Decimal
