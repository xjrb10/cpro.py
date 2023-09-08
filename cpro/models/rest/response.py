import json
import re
import typing
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar
from urllib.parse import unquote, quote
from decimal import *

from dataclasses_json import dataclass_json, config, Undefined, DataClassJsonMixin

from cpro.models.rest.enums import OrderStatus, TimeInForce, OrderTypes, OrderSides, AccountTransactionStatus, \
    PaymentOptions, DeliveryStatus, SymbolStatus, OrderType, DepositStatus, WithdrawStatus
from cpro.models.rest.filter import FilterOption, create_filter
from cpro.models.rest.market import MarketOrder, TradeInfo, MarketDatapoint, TickerStatistics, \
    SymbolPriceTickerStatistics, SymbolOrderBookTickerStatistics, CryptoAssetTradingPair


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
    # https://coins-docs.github.io/rest-api/#test-connectivity
    pass


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class ServerTimeResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#check-server-time
    serverTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))


@dataclass_json
@dataclass(frozen=True)
class SymbolInfo:
    # https://coins-docs.github.io/rest-api/#exchange-information
    symbol: str
    status: SymbolStatus = field(metadata=config(
        encoder=lambda _: _.lower(),
        decoder=lambda _: _.upper()
    ))
    baseAsset: str
    baseAssetPrecision: int
    quoteAsset: str
    quoteAssetPrecision: int
    orderTypes: list[OrderType]
    filters: list[FilterOption] = field(metadata=config(
        encoder=lambda _: [__.to_dict() for __ in _],
        decoder=lambda _: [create_filter(__) for __ in _]
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class ExchangeInformationResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#exchange-information
    timezone: str  # default: UTC - todo: currently this is ignored by the lib
    serverTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)  # todo: auto convert to timezone maybe-?
    ))
    exchangeFilters: list  # empty -- Reason: https://coins-docs.github.io/rest-api/#exchange-filters
    symbols: list[SymbolInfo]


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class NetworkPayload:
    # https://coins-docs.github.io/rest-api/#all-coins-information-user_data
    addressRegex: re = field(
        metadata=config(
            encoder=lambda _: _.pattern,
            decoder=lambda _: re.compile(_)
        )
    )
    memoRegex: re = field(
        metadata=config(
            encoder=lambda _: _.pattern,
            decoder=lambda _: re.compile(_)
        )
    )
    network: str
    name: str
    depositEnable: bool
    minConfirm: int
    unLockConfirm: int
    withdrawDesc: str
    withdrawEnable: bool
    withdrawFee: Decimal
    withdrawIntegerMultiple: Decimal
    withdrawMax: Decimal
    withdrawMin: Decimal
    sameAddress: bool


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class CoinPayload:
    # https://coins-docs.github.io/rest-api/#all-coins-information-user_data
    coin: str
    name: str
    depositAllEnable: bool
    withdrawAllEnable: bool
    free: Decimal
    locked: Decimal
    networkList: list[NetworkPayload]
    legalMoney: bool


@dataclass(frozen=True)
class CoinsInformationResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#all-coins-information-user_data
    coins: list[CoinPayload]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CoinsInformationResponse":
        if isinstance(kvs, list):
            return super().from_dict({"coins": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class DepositAddressResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#deposit-address-user_data
    coin: str
    address: str
    addressTag: str


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class WithdrawRequestResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#withdrawuser_data
    id: int


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class _TransactionInfo:
    id: str
    amount: Decimal
    coin: str
    network: str
    address: str
    addressTag: str
    txId: str
    confirmNo: int


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class DepositTransactionInfo(_TransactionInfo):
    status: DepositStatus
    insertTime: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )


@dataclass(frozen=True)
class DepositHistoryResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#deposit-history-user_data
    transactions: list[DepositTransactionInfo]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "DepositHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"transactions": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class WithdrawTransactionInfo(_TransactionInfo):
    status: WithdrawStatus
    applyTime: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    transactionFee: Decimal
    withdrawOrderId: str
    info: str


@dataclass(frozen=True)
class WithdrawHistoryResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#withdraw-history-user_data
    transactions: list[WithdrawTransactionInfo]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "WithdrawHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"transactions": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class OrderBookResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#order-book
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
    # https://coins-docs.github.io/rest-api/#recent-trades-list
    trades: list[TradeInfo]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "RecentTradesResponse":
        if isinstance(kvs, list):
            return super().from_dict({"trades": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass(frozen=True)
class GraphDataResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#klinecandlestick-data
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
    # https://coins-docs.github.io/rest-api/#24hr-ticker-price-change-statistics
    tickers: list[TickerStatistics]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "DailyTickerResponse":
        if isinstance(kvs, list):
            return super().from_dict({"tickers": kvs}, infer_missing=infer_missing)
        return super().from_dict({"tickers": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class SymbolPriceTickerResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#symbol-price-ticker
    tickers: list[SymbolPriceTickerStatistics]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "SymbolPriceTickerResponse":
        if isinstance(kvs, list):
            return super().from_dict({"tickers": kvs}, infer_missing=infer_missing)
        return super().from_dict({"tickers": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class SymbolOrderBookTickerResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#symbol-order-book-ticker
    tickers: list[SymbolOrderBookTickerStatistics]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "SymbolOrderBookTickerResponse":
        if isinstance(kvs, list):
            return super().from_dict({"tickers": kvs}, infer_missing=infer_missing)
        return super().from_dict({"tickers": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class CryptoAssetTradingPairListResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#cryptoasset-trading-pairs
    pairs: list[CryptoAssetTradingPair]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CryptoAssetTradingPairListResponse":
        if isinstance(kvs, list):
            return super().from_dict({"pairs": kvs}, infer_missing=infer_missing)
        return super().from_dict({"pairs": [kvs]}, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class CryptoAssetCurrentPriceAverageResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#current-average-price
    mins: int
    price: Decimal


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class NewOrderResponse(ResponsePayload, ABC):
    # https://coins-docs.github.io/rest-api/#new-order--trade
    pass


TNewOrderResponse = TypeVar("TNewOrderResponse", bound=NewOrderResponse)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class NewOrderACKResponse(NewOrderResponse):
    # https://coins-docs.github.io/rest-api/#new-order--trade
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
    # https://coins-docs.github.io/rest-api/#new-order--trade
    price: Decimal
    origQty: Decimal
    executedQty: Decimal
    status: OrderStatus
    timeInForce: TimeInForce
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
    # https://coins-docs.github.io/rest-api/#new-order--trade
    fills: list[OrderFill]


class _APIOrderResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#query-order-user_data
    # https://coins-docs.github.io/rest-api/#cancel-all-open-orders-on-a-symbol-trade
    # https://coins-docs.github.io/rest-api/#current-open-orders-user_data
    # https://coins-docs.github.io/rest-api/#history-orders-user_data
    # https://coins-docs.github.io/rest-api/#cancel-order-trade
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
    timeInForce: TimeInForce
    type: OrderTypes
    side: OrderSides
    stopPrice: Decimal
    origQuoteOrderQty: Decimal


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class QueryOrderResponse(_APIOrderResponse):
    # https://coins-docs.github.io/rest-api/#query-order-user_data
    isWorking: bool
    # all else inherited


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class CancelOrderResponse(_APIOrderResponse):
    # https://coins-docs.github.io/rest-api/#cancel-order-trade
    pass  # all inherited


@dataclass(frozen=True)
class CancelledOrdersList(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#cancel-all-open-orders-on-a-symbol-trade
    orders: list[_APIOrderResponse]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CancelledOrdersList":
        if isinstance(kvs, list):
            return super().from_dict({"orders": kvs}, infer_missing=infer_missing)
        return super().from_dict({"orders": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class CurrentOpenOrdersResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#current-open-orders-user_data
    orders: list[QueryOrderResponse]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CurrentOpenOrdersResponse":
        if isinstance(kvs, list):
            return super().from_dict({"orders": kvs}, infer_missing=infer_missing)
        return super().from_dict({"orders": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class OrderHistoryResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#history-orders-user_data
    orders: list[_APIOrderResponse]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "OrderHistoryResponse":
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
    # https://coins-docs.github.io/rest-api/#account-information-user_data
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
class AccountTrade(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#account-trade-list-user_data
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


@dataclass(frozen=True)
class CoinsPHWithdrawResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#withdraw-to-coins_ph-account-user_data
    id: int


@dataclass(frozen=True)
class CoinsPHDepositResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#deposit-to-exchange-account-user_data
    id: int


@dataclass(frozen=True)
class DepositOrderHistoryPayload(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#deposit-order-historydeposit-order-which-deposit-from-coins_ph-to-exchange-user_data
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
    # https://coins-docs.github.io/rest-api/#withdraw-order-history-withdrawal-order-which-withdraw-from-exchange-to-coins_ph-user_data
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
class TradeFeePayload:
    # https://coins-docs.github.io/rest-api/#trade-fee-user_data
    symbol: str
    makerCommission: Decimal
    takerCommission: Decimal


@dataclass(frozen=True)
class TradeFeeResponse(ResponsePayload, DataClassJsonMixin):
    fees: list[TradeFeePayload]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "TradeFeeResponse":
        if isinstance(kvs, list):
            return super().from_dict({"fees": kvs}, infer_missing=infer_missing)
        return super().from_dict({"fees": [kvs]}, infer_missing=infer_missing)


@dataclass(frozen=True)
class PaymentRequestPayload(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#payment-request-user_data
    # https://coins-docs.github.io/rest-api/#get-payment-request
    # https://coins-docs.github.io/rest-api/#cancel-payment-request
    # https://coins-docs.github.io/rest-api/#send-reminder-for-payment-request
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
    # https://coins-docs.github.io/rest-api/#creating-invoices
    # https://coins-docs.github.io/rest-api/#retrieving-invoices
    # https://coins-docs.github.io/rest-api/#canceling-invoices
    id: str
    amount: Decimal
    amount_due: Decimal  # todo: verify, no type on docs
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


@dataclass(frozen=True)
class StatusedAPIResponse(ResponsePayload, DataClassJsonMixin):
    status: str  # no docs, unknown enum values EX: "Success"
    error: str  # no docs, unknown enum values EX: "OK"
    params: None  # TODO: NO DOCS Ex: null


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class TradingPairPayload:
    # https://coins-docs.github.io/rest-api/#get-supported-trading-pairs
    sourceCurrency: str
    targetCurrency: str
    minSourceAmount: Decimal
    maxSourceAmount: Decimal
    precision: Decimal


@dataclass(frozen=True)
class SupportedTradingPairsResponse(StatusedAPIResponse):
    data: list[TradingPairPayload]


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class QuotePayload:
    # https://coins-docs.github.io/rest-api/#fetch-a-quote
    quoteId: str
    sourceCurrency: str
    targetCurrency: str
    sourceAmount: Decimal
    price: Decimal
    targetAmount: Decimal
    expiry: int


@dataclass(frozen=True)
class FetchQuoteResponse(StatusedAPIResponse):
    data: QuotePayload


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class QuoteAcceptancePayload:
    # https://coins-docs.github.io/rest-api/#accept-the-quote
    orderId: str
    status: str  # enum with unknown values, ex: "SUCCESS"


@dataclass(frozen=True)
class QuoteAcceptanceResponse(StatusedAPIResponse):
    data: QuoteAcceptancePayload


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class RetrieveOrderHistoryPayload:
    # https://coins-docs.github.io/rest-api/#retrieve-order-history
    id: str
    orderId: str
    quoteId: str
    userId: str
    sourceCurrency: str
    sourceCurrencyIcon: str
    targetCurrency: str
    targetCurrencyIcon: str
    sourceAmount: Decimal
    targetAmount: Decimal
    price: Decimal
    status: DeliveryStatus
    createdAt: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    errorCode: str
    errorMessage: str


@dataclass(frozen=True)
class RetrieveOrderHistoryResponse(StatusedAPIResponse):
    data: list[RetrieveOrderHistoryPayload]


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class SupportedFiatChannelPayload:
    # https://coins-docs.github.io/rest-api/#get-supported-fiat-channels
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
class CashOutPayload(StatusedAPIResponse):
    # https://coins-docs.github.io/rest-api/#cash-out
    externalOrderId: int
    internalOrderId: int


@dataclass(frozen=True)
class CashOutResponse(StatusedAPIResponse):
    data: CashOutPayload


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class FiatOrderDetailPayload:
    # https://coins-docs.github.io/rest-api/#fiat-order-detail
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
    # https://coins-docs.github.io/rest-api/#fiat-order-detail
    data: FiatOrderDetailPayload
    dealCancel: bool


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class FiatOrderHistoryPayload:
    # https://coins-docs.github.io/rest-api/#fiat-order-history
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
    # https://coins-docs.github.io/rest-api/#fiat-order-history
    data: list[FiatOrderHistoryPayload]
    total: int
