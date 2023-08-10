import os

import pytest

from cpro.client.rest import BlockingHTTPClient, AsyncIOHTTPClient, HTTPClient, APICredentials
from cpro.models.rest.endpoints import APIEndpoints
from cpro.models.rest.request import CoinsInformationRequest, DepositAddressRequest, \
    DepositHistoryRequest, \
    WithdrawHistoryRequest
from cpro.models.rest.response import CoinsInformationResponse, DepositAddressResponse, DepositHistoryResponse, \
    WithdrawHistoryResponse
from tests.utils import _test_endpoint

credentials = APICredentials(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)
blocking_client = BlockingHTTPClient(credentials)
async_client = AsyncIOHTTPClient(credentials)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_all_coins(client: HTTPClient):
    response: CoinsInformationResponse = await _test_endpoint(
        client, APIEndpoints.GET_ALL_USER_COINS, CoinsInformationRequest()
    )

    assert len(response.coins) > 0
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_deposit_address(client: HTTPClient):
    response: DepositAddressResponse = await _test_endpoint(
        client, APIEndpoints.GET_DEPOSIT_ADDRESS,
        DepositAddressRequest(
            coin="ETH",
            network="ETH"
        )
    )

    assert len(response.address) > 0
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_deposit_history(client: HTTPClient):
    response: DepositHistoryResponse = await _test_endpoint(
        client, APIEndpoints.GET_DEPOSIT_HISTORY,
        DepositHistoryRequest(
            coin="ETH"
        )
    )

    assert isinstance(response, DepositHistoryResponse)
    assert isinstance(response.to_dict(), dict)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_get_withdraw_history(client: HTTPClient):
    response: WithdrawHistoryResponse = await _test_endpoint(
        client, APIEndpoints.GET_WITHDRAW_HISTORY,
        WithdrawHistoryRequest(
            coin="ETH"
        )
    )

    assert isinstance(response, WithdrawHistoryResponse)
    assert isinstance(response.to_dict(), dict)
