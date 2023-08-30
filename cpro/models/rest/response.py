import json
import typing
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar
from urllib.parse import unquote, quote
from decimal import *

from dataclasses_json import dataclass_json, config, Undefined, DataClassJsonMixin

from cpro.models.rest.enums import OrderStatus, TimeInForceEnum, OrderTypes, OrderSides, AccountTransactionStatus, \
    PaymentOptions
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
class EmptyResponse(ResponsePayload):
    pass


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class PingResponse(EmptyResponse):
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
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)  # todo: auto convert maybe-?
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


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class WithdrawRequestResponse(ResponsePayload):
    id: int


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


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class NewOrderResponse(ResponsePayload, ABC):
    pass


TNewOrderResponse = TypeVar("TNewOrderResponse", bound=NewOrderResponse)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class NewOrderACKResponse(NewOrderResponse):
    symbol: str
    orderId: int
    clientOrderId: str
    transactTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class NewOrderRESULTResponse(NewOrderACKResponse):
    price: Decimal
    origQty: Decimal
    executedQty: Decimal
    status: OrderStatus
    timeInForce: TimeInForceEnum
    type: OrderTypes
    side: OrderSides
    stopPrice: Decimal
    origQuoteOrderQty: Decimal


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class OrderFill:
    price: Decimal
    qty: Decimal
    commission: Decimal
    commissionAsset: str
    tradeId: str


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class NewOrderFULLResponse(NewOrderRESULTResponse):
    fills: list[OrderFill]


class _APIOrderResponse(ResponsePayload):
    symbol: str
    orderId: int
    clientOrderId: str
    time: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    updateTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    price: Decimal
    origQty: Decimal
    executedQty: Decimal
    cummulativeQuoteQty: Decimal
    status: OrderStatus
    timeInForce: TimeInForceEnum
    type: OrderTypes
    side: OrderSides
    stopPrice: Decimal
    origQuoteOrderQty: Decimal


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class QueryOrderResponse(_APIOrderResponse):
    isWorking: bool


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class CancelOrderResponse(_APIOrderResponse):
    pass


@dataclass(frozen=True)
class CancelledOrdersList(ResponsePayload, DataClassJsonMixin):
    orders: list[_APIOrderResponse]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CancelledOrdersList":
        if isinstance(kvs, list):
            return super().from_dict({"orders": kvs}, infer_missing=infer_missing)
        return super().from_dict({"orders": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class CurrentOpenOrdersResponse(ResponsePayload, DataClassJsonMixin):
    orders: list[QueryOrderResponse]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CurrentOpenOrdersResponse":
        if isinstance(kvs, list):
            return super().from_dict({"orders": kvs}, infer_missing=infer_missing)
        return super().from_dict({"orders": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class OrderHistoryResponse(ResponsePayload, DataClassJsonMixin):
    orders: list[_APIOrderResponse]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "OrderHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"orders": kvs}, infer_missing=infer_missing)
        return super().from_dict({"orders": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class AccountTrade(ResponsePayload, DataClassJsonMixin):
    symbol: str
    id: int
    orderId: int
    price: Decimal
    qty: Decimal
    quoteQty: Decimal
    commission: Decimal
    commissionAsset: str
    time: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    isBuyer: bool
    isMaker: bool
    isBestMatch: bool


@dataclass(frozen=True)
class AccountTradeListResponse(ResponsePayload, DataClassJsonMixin):
    orders: list[AccountTrade]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "AccountTradeListResponse":
        if isinstance(kvs, list):
            return super().from_dict({"orders": kvs}, infer_missing=infer_missing)
        return super().from_dict({"orders": [kvs]}, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class CoinBalance:
    asset: str
    free: Decimal
    locked: Decimal


@dataclass(frozen=True)
class AccountInformationResponse(ResponsePayload, DataClassJsonMixin):
    canTrade: bool
    canWithdraw: bool
    canDeposit: bool
    accountType: str
    updateTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    balances: list[CoinBalance]


@dataclass(frozen=True)
class CoinsPHWithdrawResponse(ResponsePayload, DataClassJsonMixin):
    id: int


@dataclass(frozen=True)
class CoinsPHDepositResponse(ResponsePayload, DataClassJsonMixin):
    id: int


@dataclass(frozen=True)
class DepositOrderHistoryPayload(ResponsePayload, DataClassJsonMixin):
    coin: str
    address: str
    addressTag: str
    amount: Decimal
    id: int
    network: str
    transferType: str
    transferType: str
    status: int
    confirmTimes: str
    unlockConfirm: str
    unlockConfirm: str
    insertTime: str
    depositOrderId: str


@dataclass(frozen=True)
class DepositOrderHistoryResponse(ResponsePayload, DataClassJsonMixin):
    orders: list[DepositOrderHistoryPayload]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "DepositOrderHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"orders": kvs}, infer_missing=infer_missing)
        return super().from_dict({"orders": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class WithdrawOrderHistoryPayload(ResponsePayload, DataClassJsonMixin):
    coin: str
    address: str
    amount: Decimal
    id: int
    network: str
    withdrawOrderId: str
    transferType: str
    status: int
    transactionFee: Decimal
    confirmNo: int
    info: str
    txId: str
    applyTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))


@dataclass(frozen=True)
class WithdrawOrderHistoryResponse(ResponsePayload, DataClassJsonMixin):
    orders: list[WithdrawOrderHistoryPayload]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "WithdrawOrderHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"orders": kvs}, infer_missing=infer_missing)
        return super().from_dict({"orders": [kvs]}, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class TradeFee:
    symbol: str
    makerCommission: Decimal
    takerCommission: Decimal


@dataclass(frozen=True)
class TradeFeeResponse(ResponsePayload, DataClassJsonMixin):
    fees: list[TradeFee]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "TradeFeeResponse":
        if isinstance(kvs, list):
            return super().from_dict({"fees": kvs}, infer_missing=infer_missing)
        return super().from_dict({"fees": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class PaymentRequestPayload(ResponsePayload, DataClassJsonMixin):
    message: str
    id: int
    invoice: int
    amount: Decimal
    currency: str
    status: AccountTransactionStatus
    created_at: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    updated_at: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    expires_at: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    supported_payment_collectors: typing.List[PaymentOptions] = field(
        metadata=config(
            encoder=lambda _: quote(json.dumps(_, separators=(',', ':')), safe='"\','),
            decoder=lambda _: json.loads(unquote(_))
        )
    )
    payment_url: str
    payer_contact_info: str

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "PaymentRequestPayload":
        if isinstance(kvs, dict) and "payment-request" in kvs:
            return super().from_dict(kvs["payment-request"], infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass(frozen=True)
class InvoiceRequestPayload(ResponsePayload, DataClassJsonMixin):
    id: str
    amount: Decimal
    amount_due: str  # todo: verify, no type on docs
    currency: str
    status: AccountTransactionStatus  # todo: verify, no type on docs
    external_transaction_id: str
    created_at: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    updated_at: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    expires_at: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    supported_payment_collectors: typing.List[PaymentOptions] = field(
        metadata=config(
            encoder=lambda _: quote(json.dumps(_, separators=(',', ':')), safe='"\','),
            decoder=lambda _: json.loads(unquote(_))
        )
    )
    payment_url: str
    expires_in_seconds: int
    incoming_address: str

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "InvoiceRequestPayload":
        if isinstance(kvs, dict) and "invoice" in kvs:
            return super().from_dict(kvs["invoice"], infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class TradingPairPayload:
    sourceCurrency: str
    targetCurrency: str
    minSourceAmount: Decimal
    maxSourceAmount: Decimal
    precision: Decimal


@dataclass(frozen=True)
class StatusedAPIResponse(ResponsePayload, DataClassJsonMixin):
    status: str  # no docs, unknown enum values
    error: str  # no docs, unknown enum values
    params: None  # NO DOCS


@dataclass(frozen=True)
class SupportedTradingPairsResponse(StatusedAPIResponse):
    data: list[TradingPairPayload]


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class QuotePayload:
    quoteId: str
    sourceCurrency: str
    targetCurrency: str
    sourceAmount: Decimal
    price: Decimal
    targetAmount: Decimal
    expiry: int


@dataclass(frozen=True)
class FetchQuoteResponse(StatusedAPIResponse):
    data: list[QuotePayload]


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class QuoteAcceptancePayload:
    orderId: str
    status: str  # enum with unknown values, ex: "SUCCESS"


@dataclass(frozen=True)
class QuoteAcceptanceResponse(StatusedAPIResponse):
    data: list[QuoteAcceptancePayload]


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class SupportedFiatChannelPayload:
    id: int
    transactionChannel: str
    transactionChannelName: str
    transactionSubject: str
    transactionSubjectType: str
    transactionSubjectTypeLabel: str
    transactionSubjectName: str
    transactionType: str
    paymentMethod: str
    channelIcon: str
    subjectIcon: str
    maximum: Decimal
    minimum: Decimal
    dailyLimit: Decimal
    monthlyLimit: Decimal
    annualLimit: Decimal
    remainingDailyLimit: Decimal
    remainingMonthlyLimit: Decimal
    remainingAnnualLimit: Decimal
    precision: int
    fee: int
    feeType: int
    maxWithdrawBalance: Decimal


@dataclass(frozen=True)
class SupportedFiatChannelResponse(StatusedAPIResponse):
    data: list[SupportedFiatChannelPayload]


@dataclass(frozen=True)
class CashOutResponse(StatusedAPIResponse):
    externalOrderId: int
    internalOrderId: int


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class FiatOrderDetailPayload:
    id: int
    orderId: int
    paymentOrderId: int
    fiatCurrency: str
    fiatAmount: Decimal
    transactionType: int
    transactionChannel: str
    transactionSubject: str
    transactionSubjectType: str
    transactionChannelName: str
    transactionSubjectName: str
    feeCurrency: str
    channelFee: Decimal
    platformFee: Decimal
    status: str
    errorCode: str
    errorMessage: str
    completedTime: str  # "2023-03-31T07:44:42.000+00:00",
    source: str
    createdAt: str  # "2023-03-31T07:43:37.000+00:00",
    orderExtendedMap: dict


@dataclass(frozen=True)
class FiatOrderDetailResponse(StatusedAPIResponse):
    data: FiatOrderDetailPayload
    dealCancel: bool


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class FiatOrderHistoryPayload:
    externalOrderId: int
    internalOrderId: int
    paymentOrderId: int
    fiatCurrency: str
    fiatAmount: Decimal
    transactionType: int
    transactionChannel: str
    transactionSubject: str
    transactionSubjectType: str
    transactionChannelName: str
    transactionSubjectName: str
    feeCurrency: str
    channelFee: Decimal
    platformFee: Decimal
    status: str
    errorCode: str
    errorMessage: str
    completedTime: str  # "2023-03-31T07:44:42.000+00:00",
    source: str
    createdAt: str  # "2023-03-31T07:43:37.000+00:00",
    orderExtendedMap: dict
    dealCancel: bool


@dataclass(frozen=True)
class FiatOrderHistoryResponse(StatusedAPIResponse):
    data: list[FiatOrderHistoryPayload]
    total: int
