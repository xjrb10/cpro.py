import logging

import pytest

from cpro.client.rest import BlockingHTTPClient, AsyncIOHTTPClient, APIRequests, HTTPClient
from cpro.models.rest.request import ExchangeInformationRequest
from cpro.models.rest.response import PingResponse, ExchangeInformationResponse
from tests.utils import _test_endpoint

blocking_client = BlockingHTTPClient()
async_client = AsyncIOHTTPClient()

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_ping(client: HTTPClient):
    response = await _test_endpoint(client, APIRequests.GET_PING)

    assert isinstance(response, PingResponse)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_time(client: HTTPClient):
    response = await _test_endpoint(client, APIRequests.GET_SERVER_TIME)

    assert response.serverTime.timestamp() > 0


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_exchange_info(client: HTTPClient):
    response: ExchangeInformationResponse = await _test_endpoint(client, APIRequests.GET_EXCHANGE_INFO)
    assert len(response.symbols) > 0

    response: ExchangeInformationResponse = await _test_endpoint(
        client, APIRequests.GET_EXCHANGE_INFO,
        ExchangeInformationRequest(
            symbol="ETHPHP"
        )
    )
    assert len(response.symbols) == 1

    response: ExchangeInformationResponse = await _test_endpoint(
        client, APIRequests.GET_EXCHANGE_INFO,
        ExchangeInformationRequest(
            symbols=["ETHPHP"]
        )
    )
    assert len(response.symbols) == 1

    response: ExchangeInformationResponse = await _test_endpoint(
        client, APIRequests.GET_EXCHANGE_INFO,
        ExchangeInformationRequest(
            symbols=["ETHUSDT"]
        )
    )
    assert len(response.symbols) == 1

    response: ExchangeInformationResponse = await _test_endpoint(
        client, APIRequests.GET_EXCHANGE_INFO,
        ExchangeInformationRequest(
            symbols=["ETHPHP", "ETHUSDT"]
        )
    )
    assert len(response.symbols) == 2
