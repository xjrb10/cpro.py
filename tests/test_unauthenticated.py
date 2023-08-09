import logging

import pytest

from client.rest import BlockingHTTPClient, AsyncIOHTTPClient, APIRequests
from models.rest.request import ExchangeInformationRequest
from models.rest.response import ExchangeInformationResponse, PingResponse, ServerTimeResponse

blocking_client = BlockingHTTPClient()
async_client = AsyncIOHTTPClient()

logger = logging.getLogger(__name__)


def test_ping_blocking():
    response = APIRequests.GET_PING.execute(blocking_client)
    assert isinstance(response, PingResponse)


def test_time_blocking():
    response: ServerTimeResponse = APIRequests.GET_SERVER_TIME.execute(blocking_client)
    assert response.serverTime.timestamp() > 0


def test_exchange_info_blocking():
    response: ExchangeInformationResponse = APIRequests.GET_EXCHANGE_INFO.execute(blocking_client)
    assert len(response.symbols) > 0
    response: ExchangeInformationResponse = APIRequests.GET_EXCHANGE_INFO.execute(
        blocking_client,
        ExchangeInformationRequest(symbol="ETHPHP")
    )
    assert len(response.symbols) == 1
    response: ExchangeInformationResponse = APIRequests.GET_EXCHANGE_INFO.execute(
        blocking_client,
        ExchangeInformationRequest(symbols=["ETHPHP"])
    )
    assert len(response.symbols) == 1
    response: ExchangeInformationResponse = APIRequests.GET_EXCHANGE_INFO.execute(
        blocking_client,
        ExchangeInformationRequest(symbols=["ETHUSDT"])
    )
    assert len(response.symbols) == 1
    response: ExchangeInformationResponse = APIRequests.GET_EXCHANGE_INFO.execute(
        blocking_client,
        ExchangeInformationRequest(symbols=["ETHPHP", "ETHUSDT"])
    )
    assert len(response.symbols) == 2


@pytest.mark.asyncio
async def test_exchange_info_async():
    response: ExchangeInformationResponse = await APIRequests.GET_EXCHANGE_INFO.execute_async(async_client)
    assert len(response.symbols) > 0
