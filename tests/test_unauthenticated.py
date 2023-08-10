import pytest

from cpro.client.rest import BlockingHTTPClient, AsyncIOHTTPClient, HTTPClient
from cpro.models.rest.endpoints import APIEndpoints
from cpro.models.rest.request import ExchangeInformationRequest
from cpro.models.rest.response import PingResponse, ExchangeInformationResponse
from tests.utils import _test_endpoint

blocking_client = BlockingHTTPClient()
async_client = AsyncIOHTTPClient()


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_ping(client: HTTPClient):
    response = await _test_endpoint(client, APIEndpoints.GET_PING)

    assert isinstance(response, PingResponse)
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_time(client: HTTPClient):
    response = await _test_endpoint(client, APIEndpoints.GET_SERVER_TIME)

    assert response.serverTime.timestamp() > 0
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_exchange_info(client: HTTPClient):
    response: ExchangeInformationResponse = await _test_endpoint(client, APIEndpoints.GET_EXCHANGE_INFO)
    assert len(response.symbols) > 0

    response: ExchangeInformationResponse = await _test_endpoint(
        client, APIEndpoints.GET_EXCHANGE_INFO,
        ExchangeInformationRequest(
            symbol="ETHPHP"
        )
    )
    assert len(response.symbols) == 1
    assert isinstance(response.to_dict(), dict)

    response: ExchangeInformationResponse = await _test_endpoint(
        client, APIEndpoints.GET_EXCHANGE_INFO,
        ExchangeInformationRequest(
            symbols=["ETHPHP"]
        )
    )
    assert len(response.symbols) == 1
    assert isinstance(response.to_dict(), dict)

    response: ExchangeInformationResponse = await _test_endpoint(
        client, APIEndpoints.GET_EXCHANGE_INFO,
        ExchangeInformationRequest(
            symbols=["ETHUSDT"]
        )
    )
    assert len(response.symbols) == 1
    assert isinstance(response.to_dict(), dict)

    response: ExchangeInformationResponse = await _test_endpoint(
        client, APIEndpoints.GET_EXCHANGE_INFO,
        ExchangeInformationRequest(
            symbols=["ETHPHP", "ETHUSDT"]
        )
    )
    assert len(response.symbols) == 2
    assert isinstance(response.to_dict(), dict)
