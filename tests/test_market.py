import json

import pytest

from cpro.client.rest import BlockingHTTPClient, HTTPClient, AsyncIOHTTPClient
from cpro.models.rest.endpoints import APIEndpoints
from cpro.models.rest.enums import ChartIntervals
from cpro.models.rest.request import OrderBookRequest, RecentTradesRequest, GraphDataRequest, DailyTickerTickerRequest, \
    SymbolPriceTickerTickerRequest, SymbolOrderBookTickerTickerRequest, CryptoAssetCurrentPriceAverageRequest
from cpro.models.rest.response import OrderBookResponse, RecentTradesResponse, GraphDataResponse, DailyTickerResponse, \
    SymbolPriceTickerResponse, SymbolOrderBookTickerResponse, CryptoAssetCurrentPriceAverageResponse, \
    CryptoAssetTradingPairListResponse
from tests.utils import _test_endpoint

blocking_client = BlockingHTTPClient()
async_client = AsyncIOHTTPClient()


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_order_book(client: HTTPClient):
    response = await _test_endpoint(client, APIEndpoints.GET_ORDER_BOOK, OrderBookRequest(
        symbol="ETHPHP"
    ))

    assert isinstance(response, OrderBookResponse)
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_recent_trades(client: HTTPClient):
    response: RecentTradesResponse = await _test_endpoint(client, APIEndpoints.GET_RECENT_TRADES, RecentTradesRequest(
        symbol="ETHPHP"
    ))

    assert isinstance(response, RecentTradesResponse)
    assert len(response.trades) > 0
    assert float(response.trades[0].price) > 0
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_graph_data(client: HTTPClient):
    response: GraphDataResponse = await _test_endpoint(client, APIEndpoints.GET_GRAPH_DATA, GraphDataRequest(
        symbol="ETHPHP",
        interval=ChartIntervals._1h
    ))

    assert isinstance(response, GraphDataResponse)
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_daily_ticker(client: HTTPClient):
    response: DailyTickerResponse = await _test_endpoint(client, APIEndpoints.GET_DAILY_TICKER, DailyTickerTickerRequest())

    assert isinstance(response, DailyTickerResponse)
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_symbol_price_ticker(client: HTTPClient):
    response: SymbolPriceTickerResponse = await _test_endpoint(
        client, APIEndpoints.GET_SYMBOL_PRICE_TICKER,
        SymbolPriceTickerTickerRequest()
    )

    assert isinstance(response, SymbolPriceTickerResponse)
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_symbol_order_book_ticker(client: HTTPClient):
    response: SymbolOrderBookTickerResponse = await _test_endpoint(
        client, APIEndpoints.GET_SYMBOL_ORDER_BOOK_TICKER,
        SymbolOrderBookTickerTickerRequest()
    )

    assert isinstance(response, SymbolOrderBookTickerResponse)
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_average_price(client: HTTPClient):
    response: CryptoAssetCurrentPriceAverageResponse = await _test_endpoint(
        client, APIEndpoints.GET_CRYPTO_ASSET_CURRENT_PRICE_AVERAGE,
        CryptoAssetCurrentPriceAverageRequest(symbol="ETHUSDT")
    )

    assert isinstance(response, CryptoAssetCurrentPriceAverageResponse)
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_trading_pair_list(client: HTTPClient):
    response: CryptoAssetTradingPairListResponse = await _test_endpoint(
        client, APIEndpoints.GET_CRYPTO_ASSET_TRADING_PAIRS
    )

    assert isinstance(response, CryptoAssetTradingPairListResponse)
    assert isinstance(response.to_dict(), dict)
