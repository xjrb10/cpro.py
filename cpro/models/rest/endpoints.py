import typing
from enum import Enum

from cpro.client.rest import APIEndpoint, HTTPClient
from cpro.models.rest.enums import SecurityType
from cpro.models.rest.request import CoinsInformationRequest, DepositAddressRequest, DepositHistoryRequest, \
    WithdrawHistoryRequest, RequestPayload, OrderBookRequest, RecentTradesRequest, GraphDataRequest, \
    DailyTickerRequest, SymbolPriceTickerRequest, SymbolOrderBookTickerRequest, CryptoAssetCurrentPriceAverageRequest, \
    NewOrderRequest, QueryOrderRequest, CancelOrderRequest, CancelAllOpenOrdersRequest, CurrentOpenOrdersRequest, \
    OrderHistoryRequest, AccountInformationRequest, AccountTradesRequest, CoinsPHWithdrawRequest, CoinsPHDepositRequest, \
    DepositOrderHistoryRequest, WithdrawOrderHistoryRequest, TradeFeeRequest, CreatePaymentRequestRequest, \
    GetPaymentRequestRequest, CancelPaymentRequestRequest, SendPaymentRequestReminderRequest, CreateInvoiceRequest, \
    GetInvoicesRequest, CancelInvoiceRequest, QuoteFetchRequest, QuoteAcceptRequest, \
    SupportedFiatPaymentChannelsRequest, CashOutRequest, FiatOrderDetailRequest, FiatOrderHistoryRequest, \
    WithdrawRequest
from cpro.models.rest.response import PingResponse, ExchangeInformationResponse, ServerTimeResponse, TResponsePayload, \
    CryptoAssetTradingPairListResponse, EmptyResponse, QuoteAcceptanceResponse


class APIEndpoints(Enum):
    GET_PING = APIEndpoint("GET /openapi/v1/ping", response_cls=PingResponse)
    GET_SERVER_TIME = APIEndpoint("GET /openapi/v1/time", response_cls=ServerTimeResponse)
    GET_EXCHANGE_INFO = APIEndpoint("GET /openapi/v1/exchangeInfo", response_cls=ExchangeInformationResponse)

    GET_ALL_USER_COINS = APIEndpoint(
        "GET /openapi/wallet/v1/config/getall",
        CoinsInformationRequest, SecurityType.USER_DATA
    )
    GET_DEPOSIT_ADDRESS = APIEndpoint(
        "GET /openapi/wallet/v1/deposit/address",
        DepositAddressRequest, SecurityType.USER_DATA
    )
    REQUEST_WITHDRAWAL = APIEndpoint(
        "POST /openapi/wallet/v1/withdraw/apply",
        WithdrawRequest, SecurityType.USER_DATA
    )
    GET_DEPOSIT_HISTORY = APIEndpoint(
        "GET /openapi/wallet/v1/deposit/history",
        DepositHistoryRequest, SecurityType.USER_DATA
    )
    GET_WITHDRAW_HISTORY = APIEndpoint(
        "GET /openapi/wallet/v1/withdraw/history",
        WithdrawHistoryRequest, SecurityType.USER_DATA
    )
    GET_ORDER_BOOK = APIEndpoint(
        "GET /openapi/quote/v1/depth",
        OrderBookRequest
    )
    GET_RECENT_TRADES = APIEndpoint(
        "GET /openapi/quote/v1/trades",
        RecentTradesRequest
    )
    GET_GRAPH_DATA = APIEndpoint(
        "GET /openapi/quote/v1/klines",
        GraphDataRequest
    )
    GET_DAILY_TICKER = APIEndpoint(
        "GET /openapi/quote/v1/ticker/24hr",
        DailyTickerRequest
    )
    GET_SYMBOL_PRICE_TICKER = APIEndpoint(
        "GET /openapi/quote/v1/ticker/price",
        SymbolPriceTickerRequest
    )
    GET_SYMBOL_ORDER_BOOK_TICKER = APIEndpoint(
        "GET /openapi/quote/v1/ticker/bookTicker",
        SymbolOrderBookTickerRequest
    )
    GET_CRYPTO_ASSET_CURRENT_PRICE_AVERAGE = APIEndpoint(
        "GET /openapi/quote/v1/avgPrice",
        CryptoAssetCurrentPriceAverageRequest
    )
    GET_CRYPTO_ASSET_TRADING_PAIRS = APIEndpoint(
        "GET /openapi/v1/pairs",
        response_cls=CryptoAssetTradingPairListResponse
    )
    TEST_NEW_ORDER = APIEndpoint(
        "POST /openapi/v1/order/test",
        NewOrderRequest, SecurityType.TRADE,
        response_cls=EmptyResponse
    )
    NEW_ORDER = APIEndpoint(
        "POST /openapi/v1/order",
        NewOrderRequest, SecurityType.TRADE
    )
    QUERY_ORDER = APIEndpoint(
        "GET /openapi/v1/order",
        QueryOrderRequest, SecurityType.USER_DATA
    )
    CANCEL_ORDER = APIEndpoint(
        "DELETE /openapi/v1/order",
        CancelOrderRequest, SecurityType.TRADE
    )
    CANCEL_OPEN_ORDERS = APIEndpoint(
        "DELETE /openapi/v1/openOrders",
        CancelAllOpenOrdersRequest, SecurityType.TRADE
    )
    CURRENT_OPEN_ORDERS = APIEndpoint(
        "GET /openapi/v1/openOrders",
        CurrentOpenOrdersRequest, SecurityType.USER_DATA
    )
    GET_ORDER_HISTORY = APIEndpoint(
        "GET /openapi/v1/historyOrders",
        OrderHistoryRequest, SecurityType.USER_DATA
    )
    GET_ACCOUNT_INFORMATION = APIEndpoint(
        "GET /openapi/v1/account",
        AccountInformationRequest, SecurityType.USER_DATA
    )
    GET_ACCOUNT_TRADE_LIST = APIEndpoint(
        "GET /openapi/v1/myTrades",
        AccountTradesRequest, SecurityType.USER_DATA
    )
    CREATE_WITHDRAW_ORDER_TO_COINSPH = APIEndpoint(
        "POST /openapi/v1/capital/withdraw/apply",
        CoinsPHWithdrawRequest, SecurityType.USER_DATA
    )
    CREATE_DEPOSIT_ORDER_TO_EXCHANGE = APIEndpoint(
        "POST /openapi/v1/capital/deposit/apply",
        CoinsPHDepositRequest, SecurityType.USER_DATA
    )
    GET_DEPOSIT_ORDER_HISTORY = APIEndpoint(
        "GET /openapi/v1/capital/deposit/history",
        DepositOrderHistoryRequest, SecurityType.USER_DATA
    )
    GET_WITHDRAW_ORDER_HISTORY = APIEndpoint(
        "GET /openapi/v1/capital/withdraw/history",
        WithdrawOrderHistoryRequest, SecurityType.USER_DATA
    )
    GET_TRADE_FEE = APIEndpoint(
        "GET /openapi/v1/asset/tradeFee",
        TradeFeeRequest, SecurityType.USER_DATA
    )
    CREATE_PAYMENT_REQUEST = APIEndpoint(
        "POST /openapi/v3/payment-request/payment-requests",
        CreatePaymentRequestRequest, SecurityType.USER_DATA
    )
    GET_PAYMENT_REQUEST = APIEndpoint(
        "GET /openapi/v3/payment-request/get-payment-request",
        GetPaymentRequestRequest, SecurityType.USER_DATA
    )
    CANCEL_PAYMENT_REQUEST = APIEndpoint(
        "POST /openapi/v3/payment-request/delete-payment-request",
        CancelPaymentRequestRequest, SecurityType.USER_DATA
    )
    SEND_PAYMENT_REQUEST_REMINDER = APIEndpoint(
        "POST /openapi/v3/payment-request/payment-request-reminder",
        SendPaymentRequestReminderRequest, SecurityType.USER_DATA
    )
    # todo: separate the merchant API into its own part of the library, with callback support (NO DOCS)
    CREATE_INVOICE = APIEndpoint(
        "POST /merchant-api/v1/invoices",
        CreateInvoiceRequest, SecurityType.MERCHANT
    )
    GET_INVOICE = APIEndpoint(
        "GET /merchant-api/v1/get-invoices",
        GetInvoicesRequest, SecurityType.MERCHANT
    )
    CANCEL_INVOICE = APIEndpoint(
        "POST /merchant-api/v1/invoices-cancel",
        CancelInvoiceRequest, SecurityType.MERCHANT
    )
    CONVERSION_GET_SUPPORTED_TRADING_PAIRS = APIEndpoint(
        "POST /openapi/convert/v1/get-supported-trading-pairs"
    )
    CONVERSION_GET_QUOTE = APIEndpoint(
        "POST /openapi/convert/v1/get-quote",
        QuoteFetchRequest
    )
    CONVERSION_ACCEPT_QUOTE = APIEndpoint(
        "POST /openapi/convert/v1/accept-quote",
        QuoteAcceptRequest
    )
    FIAT_GET_SUPPORTED_PAYMENT_CHANNELS = APIEndpoint(
        "POST /openapi/fiat/v1/support-channel",
        SupportedFiatPaymentChannelsRequest
    )
    FIAT_REQUEST_CASH_OUT = APIEndpoint(
        "POST /openapi/fiat/v1/cash-out",
        CashOutRequest
    )
    FIAT_GET_ORDER_DETAILS = APIEndpoint(
        "GET /openapi/fiat/v1/details",
        FiatOrderDetailRequest
    )
    FIAT_GET_ORDER_HISTORY = APIEndpoint(
        "POST /openapi/fiat/v1/history",
        FiatOrderHistoryRequest
    )

    def execute(self, client: HTTPClient, payload: typing.Optional[RequestPayload] = None) -> TResponsePayload:
        return client.do_request(self.value, payload)

    async def execute_async(
            self, client: HTTPClient, payload: typing.Optional[RequestPayload] = None
    ) -> TResponsePayload:
        return await client.do_request(self.value, payload)
