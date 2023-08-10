import typing
from enum import Enum

from cpro.client.rest import APIEndpoint, HTTPClient
from cpro.models.rest.enums import SecurityType
from cpro.models.rest.request import CoinsInformationRequest, DepositAddressRequest, DepositHistoryRequest, \
    WithdrawHistoryRequest, RequestPayload, OrderBookRequest, RecentTradesRequest, GraphDataRequest, DailyTickerRequest, \
    SymbolPriceTickerRequest, SymbolOrderBookTickerRequest, CryptoAssetCurrentPriceAverageRequest
from cpro.models.rest.response import PingResponse, ExchangeInformationResponse, ServerTimeResponse, \
    CoinsInformationResponse, DepositHistoryResponse, DepositAddressResponse, WithdrawHistoryResponse, TResponsePayload, \
    OrderBookResponse, RecentTradesResponse, GraphDataResponse, DailyTickerResponse, SymbolPriceTickerResponse, \
    SymbolOrderBookTickerResponse, CryptoAssetTradingPairListResponse, CryptoAssetCurrentPriceAverageResponse


class APIEndpoints(Enum):
    GET_PING = APIEndpoint("GET /openapi/v1/ping", PingResponse)
    GET_SERVER_TIME = APIEndpoint("GET /openapi/v1/time", ServerTimeResponse)
    GET_EXCHANGE_INFO = APIEndpoint("GET /openapi/v1/exchangeInfo", ExchangeInformationResponse)

    GET_ALL_USER_COINS = APIEndpoint(
        "GET /openapi/wallet/v1/config/getall", CoinsInformationResponse,
        CoinsInformationRequest, SecurityType.USER_DATA
    )
    GET_DEPOSIT_ADDRESS = APIEndpoint(
        "GET /openapi/wallet/v1/deposit/address", DepositAddressResponse,
        DepositAddressRequest, SecurityType.USER_DATA
    )
    # todo: https://coins-docs.github.io/rest-api/#withdrawuser_data
    GET_DEPOSIT_HISTORY = APIEndpoint(
        "GET /openapi/wallet/v1/deposit/history", DepositHistoryResponse,
        DepositHistoryRequest, SecurityType.USER_DATA
    )
    GET_WITHDRAW_HISTORY = APIEndpoint(
        "GET /openapi/wallet/v1/withdraw/history", WithdrawHistoryResponse,
        WithdrawHistoryRequest, SecurityType.USER_DATA
    )
    GET_ORDER_BOOK = APIEndpoint(
        "GET /openapi/quote/v1/depth", OrderBookResponse,
        OrderBookRequest
    )
    GET_RECENT_TRADES = APIEndpoint(
        "GET /openapi/quote/v1/trades", RecentTradesResponse,
        RecentTradesRequest
    )
    GET_GRAPH_DATA = APIEndpoint(
        "GET /openapi/quote/v1/klines", GraphDataResponse,
        GraphDataRequest
    )
    GET_DAILY_TICKER = APIEndpoint(
        "GET /openapi/quote/v1/ticker/24hr", DailyTickerResponse,
        DailyTickerRequest
    )
    GET_SYMBOL_PRICE_TICKER = APIEndpoint(
        "GET /openapi/quote/v1/ticker/price", SymbolPriceTickerResponse,
        SymbolPriceTickerRequest
    )
    GET_SYMBOL_ORDER_BOOK_TICKER = APIEndpoint(
        "GET /openapi/quote/v1/ticker/bookTicker", SymbolOrderBookTickerResponse,
        SymbolOrderBookTickerRequest
    )
    GET_CRYPTO_ASSET_CURRENT_PRICE_AVERAGE = APIEndpoint(
        "GET /openapi/quote/v1/avgPrice", CryptoAssetCurrentPriceAverageResponse,
        CryptoAssetCurrentPriceAverageRequest
    )
    GET_CRYPTO_ASSET_TRADING_PAIRS = APIEndpoint(
        "GET /openapi/v1/pairs", CryptoAssetTradingPairListResponse
    )

    def execute(self, client: HTTPClient, payload: typing.Optional[RequestPayload] = None) -> TResponsePayload:
        return client.do_request(self.value, payload)

    async def execute_async(
            self, client: HTTPClient, payload: typing.Optional[RequestPayload] = None
    ) -> TResponsePayload:
        return await client.do_request(self.value, payload)
