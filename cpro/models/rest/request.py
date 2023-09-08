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

import hashlib
import hmac
import json
import typing
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from time import time
from urllib.parse import quote, urlencode, unquote
from decimal import *

from dataclasses_json import DataClassJsonMixin, config

from cpro.models.rest.enums import DepositStatus, ChartIntervals, OrderSides, OrderTypes, TimeInForce, \
    OrderResponseTypes, AntiSelfTradingBehaviours, ExchangeOrderStatus, PaymentOptions, DeliveryStatus
from cpro.models.rest.response import TResponsePayload, CoinsInformationResponse, DepositAddressResponse, \
    WithdrawHistoryResponse, OrderBookResponse, RecentTradesResponse, GraphDataResponse, DailyTickerResponse, \
    SymbolPriceTickerResponse, SymbolOrderBookTickerResponse, CryptoAssetCurrentPriceAverageResponse, \
    NewOrderResponse, NewOrderACKResponse, NewOrderRESULTResponse, NewOrderFULLResponse, QueryOrderResponse, \
    CancelOrderResponse, CancelledOrdersList, CurrentOpenOrdersResponse, OrderHistoryResponse, \
    AccountInformationResponse, AccountTradeListResponse, CoinsPHWithdrawResponse, CoinsPHDepositResponse, \
    DepositOrderHistoryResponse, PaymentRequestPayload, InvoiceRequestPayload, WithdrawOrderHistoryResponse, \
    TradeFeeResponse, FetchQuoteResponse, SupportedFiatChannelResponse, QuoteAcceptanceResponse, CashOutResponse, \
    FiatOrderDetailResponse, WithdrawRequestResponse


@dataclass
class EncodedPayload(DataClassJsonMixin):
    data: str = ""
    raw_params: dict = field(default_factory=dict)
    json: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)

    @property
    def params(self) -> str:
        return "&".join(f"{k}={v}" for k, v in self.raw_params.items())

    def with_key(self, api_key: str) -> "EncodedPayload":
        authenticated = copy(self)
        authenticated.headers["X-COINS-APIKEY"] = api_key
        return authenticated

    def sign(self, api_key: str, api_secret: str) -> "EncodedPayload":
        signed = copy(self)
        signed.raw_params["signature"] = hmac.new(
            api_secret.encode(),
            msg=signed.params.encode() + signed.data.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        return signed.with_key(api_key)

    def sign_merchant(self, api_key: str, api_secret: str, merchant_key: str, request_url: str) -> "EncodedPayload":
        # todo: TEST IF CORRECT
        signed = copy(self)
        signed.headers["X-Timestamp"] = t = int(time())
        signed.headers["X-Merchant-Key"] = merchant_key
        signed.headers["X-Merchant-Sign"] = hmac.new(
            api_secret.encode(),
            f"{t}{request_url}{signed.data}".encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        return signed.with_key(api_key)

    def put_urlencoded_data(self, data: dict) -> "EncodedPayload":
        with_data = copy(self)
        with_data.data = urlencode(data)
        return with_data


class RequestPayload(DataClassJsonMixin):
    def to_encoded(self) -> EncodedPayload:
        return EncodedPayload(raw_params={k: v for k, v in self.to_dict().items() if v and v != 'null'})

    def expected_response(self) -> typing.Type[TResponsePayload]:
        raise NotImplementedError


TRequestPayload = typing.TypeVar("TRequestPayload", bound=RequestPayload)


@dataclass(frozen=True)
class _OptionallyBatchedTickerRequest(RequestPayload):
    symbol: typing.Optional[str] = None
    symbols: typing.Optional[typing.List[str]] = field(
        default=None,
        metadata=config(
            encoder=lambda _: quote(json.dumps(_, separators=(',', ':')), safe='"\','),
            decoder=lambda _: json.loads(unquote(_))
        )
    )

    def to_encoded(self) -> EncodedPayload:
        if self.symbol and self.symbols:
            raise ValueError("Only one of `symbol` or `symbols` can be filled, not both.")
        return super().to_encoded()


@dataclass(frozen=True)
class ExchangeInformationTickerRequest(_OptionallyBatchedTickerRequest):
    pass


@dataclass(frozen=True)
class CoinsInformationRequest(RequestPayload, DataClassJsonMixin):
    recvWindow: typing.Optional[int] = None
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[CoinsInformationResponse]:
        return CoinsInformationResponse


@dataclass(frozen=True)
class DepositAddressRequest(RequestPayload):
    coin: str
    network: str
    recvWindow: int = 5000
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[DepositAddressResponse]:
        return DepositAddressResponse


@dataclass(frozen=True)
class WithdrawRequest(RequestPayload):
    coin: str
    network: str
    addressTag: str
    amount: Decimal
    withdrawOrderId: str
    recvWindow: int = 5000
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[WithdrawRequestResponse]:
        return WithdrawRequestResponse


@dataclass(frozen=True)
class TransactionHistoryRequest(RequestPayload):
    coin: typing.Optional[str] = None
    status: typing.Optional[DepositStatus] = None
    startTime: datetime = field(
        default_factory=lambda: datetime.now() - timedelta(days=90),
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    offset: int = 0
    limit: int = 1000
    recvWindow: int = 5000
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )


@dataclass(frozen=True)
class DepositHistoryRequest(TransactionHistoryRequest):
    txId: typing.Optional[str] = None

    def expected_response(self) -> typing.Type[DepositAddressResponse]:
        return DepositAddressResponse


@dataclass(frozen=True)
class WithdrawHistoryRequest(TransactionHistoryRequest):
    withdrawOrderId: typing.Optional[str] = None

    def expected_response(self) -> typing.Type[WithdrawHistoryResponse]:
        return WithdrawHistoryResponse


@dataclass(frozen=True)
class OrderBookRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#order-book
    symbol: str = None
    limit: int = 100

    def expected_response(self) -> typing.Type[OrderBookResponse]:
        return OrderBookResponse


@dataclass(frozen=True)
class RecentTradesRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#recent-trades-list
    symbol: str
    interval: int = 500

    def expected_response(self) -> typing.Type[RecentTradesResponse]:
        return RecentTradesResponse


@dataclass(frozen=True)
class GraphDataRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#klinecandlestick-data
    symbol: str
    interval: ChartIntervals
    startTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    limit: int = 500

    def expected_response(self) -> typing.Type[GraphDataResponse]:
        return GraphDataResponse


@dataclass(frozen=True)
class DailyTickerTickerRequest(_OptionallyBatchedTickerRequest):
    # https://coins-docs.github.io/rest-api/#24hr-ticker-price-change-statistics

    def expected_response(self) -> typing.Type[DailyTickerResponse]:
        return DailyTickerResponse


@dataclass(frozen=True)
class SymbolPriceTickerTickerRequest(_OptionallyBatchedTickerRequest):
    # https://coins-docs.github.io/rest-api/#symbol-price-ticker

    def expected_response(self) -> typing.Type[SymbolPriceTickerResponse]:
        return SymbolPriceTickerResponse


@dataclass(frozen=True)
class SymbolOrderBookTickerTickerRequest(_OptionallyBatchedTickerRequest):
    # https://coins-docs.github.io/rest-api/#symbol-order-book-ticker

    def expected_response(self) -> typing.Type[SymbolOrderBookTickerResponse]:
        return SymbolOrderBookTickerResponse


@dataclass(frozen=True)
class CryptoAssetCurrentPriceAverageRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#current-average-price
    symbol: str

    def expected_response(self) -> typing.Type[CryptoAssetCurrentPriceAverageResponse]:
        return CryptoAssetCurrentPriceAverageResponse


@dataclass()
class NewOrderRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#new-order--trade
    symbol: str
    side: OrderSides
    type: OrderTypes
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    timeInForce: typing.Optional[TimeInForce] = None
    quantity: typing.Optional[Decimal] = None
    quoteOrderQty: typing.Optional[Decimal] = None
    price: typing.Optional[Decimal] = None

    # A unique id among open orders. Automatically generated if not sent.
    # Orders with the same newClientOrderID can be accepted only when the previous one is filled,
    # otherwise the order will be rejected.
    newClientOrderId: typing.Optional[str] = None

    # Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
    stopPrice: typing.Optional[Decimal] = None

    # Set the response JSON. ACK, RESULT, or FULL;
    # MARKET and LIMIT order types default to FULL, all other orders default to ACK.
    newOrderRespType: typing.Optional[OrderResponseTypes] = None

    # The anti self-trading behaviour, Default anti self-dealing behaviour is CB
    stpFlag: typing.Optional[AntiSelfTradingBehaviours] = None

    # The value cannot be greater than 60000
    recvWindow: typing.Optional[int] = None

    def __post_init__(self):
        if not self.newOrderRespType:
            self.newOrderRespType = OrderResponseTypes.FULL \
                if self.type in (OrderTypes.MARKET, OrderTypes.LIMIT) \
                else OrderResponseTypes.ACK

    def expected_response(self) -> typing.Type[NewOrderResponse]:
        match self.newOrderRespType:
            case OrderResponseTypes.ACK:
                return NewOrderACKResponse
            case OrderResponseTypes.RESULT:
                return NewOrderRESULTResponse
            case OrderResponseTypes.FULL:
                return NewOrderFULLResponse
        raise ValueError(f"Unhandled New Order Response Type `{self.newOrderRespType}`")


@dataclass(frozen=True)
class _SingleOrderRequest(RequestPayload):
    orderId: typing.Optional[int] = None
    origClientOrderId: typing.Optional[str] = None
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )


@dataclass(frozen=True)
class QuerySingleOrderRequest(_SingleOrderRequest):
    # https://coins-docs.github.io/rest-api/#query-order-user_data
    def expected_response(self) -> typing.Type[TResponsePayload]:
        return QueryOrderResponse


@dataclass(frozen=True)
class CancelSingleOrderRequest(_SingleOrderRequest):
    # https://coins-docs.github.io/rest-api/#cancel-order-trade
    def expected_response(self) -> typing.Type[TResponsePayload]:
        return CancelOrderResponse


@dataclass(frozen=True)
class _AllOrdersRequest(RequestPayload):
    symbol: str
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )


@dataclass(frozen=True)
class CancelAllOpenOrdersRequest(_AllOrdersRequest):
    # https://coins-docs.github.io/rest-api/#cancel-all-open-orders-on-a-symbol-trade
    def expected_response(self) -> typing.Type[TResponsePayload]:
        return CancelledOrdersList


@dataclass(frozen=True)
class CurrentOpenOrdersRequest(_AllOrdersRequest):
    # https://coins-docs.github.io/rest-api/#current-open-orders-user_data
    def expected_response(self) -> typing.Type[TResponsePayload]:
        return CurrentOpenOrdersResponse


@dataclass(frozen=True)
class OrderHistoryRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#history-orders-user_data
    symbol: str
    orderId: typing.Optional[int] = None
    startTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    limit: typing.Optional[int] = None
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return OrderHistoryResponse


@dataclass(frozen=True)
class AccountInformationRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#account-information-user_data
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return AccountInformationResponse


@dataclass(frozen=True)
class AccountTradesRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#account-trade-list-user_data
    symbol: str
    orderId: typing.Optional[int] = None
    startTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    fromId: typing.Optional[int] = None
    limit: typing.Optional[int] = None
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return AccountTradeListResponse


@dataclass(frozen=True)
class CoinsPHWithdrawRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#withdraw-to-coins_ph-account-user_data
    coin: str
    amount: Decimal
    withdrawOrderId: str
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return CoinsPHWithdrawResponse


@dataclass(frozen=True)
class CoinsPHDepositRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#deposit-to-exchange-account-user_data
    coin: str
    amount: Decimal
    depositOrderId: str
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return CoinsPHDepositResponse


@dataclass(frozen=True)
class DepositOrderHistoryRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#deposit-order-historydeposit-order-which-deposit-from-coins_ph-to-exchange-user_data
    coin: str
    depositOrderId: str
    status: ExchangeOrderStatus
    offset: int
    limit: int
    startTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return DepositOrderHistoryResponse


@dataclass(frozen=True)
class WithdrawOrderHistoryRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#withdraw-order-history-withdrawal-order-which-withdraw-from-exchange-to-coins_ph-user_data
    coin: str
    withdrawOrderId: str
    status: ExchangeOrderStatus
    offset: int
    limit: int
    startTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return WithdrawOrderHistoryResponse


@dataclass(frozen=True)
class TradeFeeRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#trade-fee-user_data
    symbol: str
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return TradeFeeResponse


@dataclass(frozen=True)
class CreatePaymentRequestRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#payment-request-user_data

    # The contact information, typically an email address, to which the payment request should be sent.
    payer_contact_info: str

    # Balance ID of the user making the transfer.
    receiving_account: int

    # The requested amount to be transferred to the requestor’s receiving_account.
    amount: Decimal

    # An arbitrary message that will be attached to the payment request.
    message: str

    # Methods of payment that are available to a user when they view a payment request (e.g., ["coins_peso_wallet"])
    supported_payment_collectors: typing.Optional[typing.List[PaymentOptions]] = field(
        default=None,
        metadata=config(
            encoder=lambda _: quote(json.dumps(_, separators=(',', ':')), safe='"\','),
            decoder=lambda _: json.loads(unquote(_))
        )
    )

    # The expiration date of the payment request.
    # Expected to be in ISO 8601 datetime format (e.g., 2016-10-20T13:00:00.000000Z)
    # or a time delta from the current time (e.g., 1w 3d 2h 32m 5s).
    # The default expiration period is set to 7 days.
    expires_at: str = None

    # The value cannot be greater than 60000
    recvWindow: typing.Optional[int] = None
    timestamp: typing.Optional[datetime] = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return PaymentRequestPayload


@dataclass(frozen=True)
class GetPaymentRequestRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#get-payment-request
    id: int = None
    start_time: int = None
    end_time: int = None
    limit: int = None

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return PaymentRequestPayload


@dataclass(frozen=True)
class CancelPaymentRequestRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#cancel-payment-request
    id: int

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return PaymentRequestPayload


@dataclass(frozen=True)
class SendPaymentRequestReminderRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#send-reminder-for-payment-request
    id: int

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return PaymentRequestPayload


@dataclass(frozen=True)
class CreateInvoiceRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#creating-invoices

    # The amount expected from the customer.
    amount: Decimal

    # Currency of transaction.
    currency: str

    # Methods of payment that are available to a user when they view a payment request, e.g., [“coins_peso_wallet”]
    supported_payment_collectors: typing.Optional[typing.List[PaymentOptions]] = field(
        metadata=config(
            encoder=lambda _: quote(json.dumps(_, separators=(',', ':')), safe='"\','),
            decoder=lambda _: json.loads(unquote(_))
        )
    )

    # To maintain transactional integrity, each transaction_id must be unique.
    external_transaction_id: str

    # The expiration date of the payment request.
    # Expected to be in ISO 8601 datetime format (e.g., 2016-10-20T13:00:00.000000Z)
    # or a time delta from the current time (e.g., 1w 3d 2h 32m 5s).
    # The default expiration period is set to 7 days.
    expires_at: str = None

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return InvoiceRequestPayload


@dataclass(frozen=True)
class GetInvoicesRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#retrieving-invoices
    invoice_id: str = None
    start_time: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    end_time: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    limit: int = None

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return InvoiceRequestPayload


@dataclass(frozen=True)
class CancelInvoiceRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#canceling-invoices
    invoice_id: str

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return InvoiceRequestPayload


@dataclass(frozen=True)
class QuoteFetchRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#fetch-a-quote
    sourceCurrency: str
    targetCurrency: str
    sourceAmount: str

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return FetchQuoteResponse


@dataclass(frozen=True)
class QuoteAcceptRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#accept-the-quote
    quoteId: str

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return QuoteAcceptanceResponse


@dataclass(frozen=True)
class SupportedFiatPaymentChannelsRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#get-supported-fiat-channels

    # Set this parameter to -1 to indicate a cash-out transaction. At present, only cash-out transactions are supported.
    transactionType: str

    # The parameter represents the currency used in the transaction and should be set to PHP as it is the
    # only currency currently supported.
    currency: str
    transactionChannel: str = None
    transactionSubject: str = None

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return SupportedFiatChannelResponse


@dataclass(frozen=True)
class RetrieveOrderHistoryRequest(RequestPayload):
    # https://coins-docs.github.io/rest-api/#retrieve-order-history
    startTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda _: _ and int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    status: typing.Optional[DeliveryStatus] = None
    page: typing.Optional[int] = None
    size: typing.Optional[int] = None

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return RetrieveOrderHistoryResponse


@dataclass(frozen=True)
class CashOutRequestExtendInfo:
    recipientName: str
    recipientAccountNumber: str
    recipientAddress: str
    remarks: str


@dataclass(frozen=True)
class CashOutRequest(RequestPayload):
    internalOrderId: str
    currency: str
    amount: str
    channelName: str
    channelSubject: str
    extendInfo: typing.Optional[CashOutRequestExtendInfo] = None

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return CashOutResponse


@dataclass(frozen=True)
class FiatOrderDetailRequest(RequestPayload):
    internalOrderId: str

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return FiatOrderDetailResponse


@dataclass(frozen=True)
class FiatOrderHistoryRequest(RequestPayload):
    pageNum: str = None
    pageSize: str = None
    internalOrderId: str = None
    transactionType: str = None
    transactionChannel: str = None
    transactionSubject: str = None
    status: str = None
    fiatCurrency: str = None
    startDate: str = None
    endDate: str = None

    def expected_response(self) -> typing.Type[TResponsePayload]:
        return FiatOrderHistoryResponse
