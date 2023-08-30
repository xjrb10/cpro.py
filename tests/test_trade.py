import os
from decimal import *

import pytest
from cpro.client.rest import BlockingHTTPClient, AsyncIOHTTPClient, HTTPClient, APICredentials
from cpro.models.rest.endpoints import APIEndpoints
from cpro.models.rest.enums import OrderSides, OrderTypes
from cpro.models.rest.request import NewOrderRequest
from cpro.models.rest.response import NewOrderResponse
from tests.utils import _test_endpoint

credentials = APICredentials(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)
blocking_client = BlockingHTTPClient(credentials)
async_client = AsyncIOHTTPClient(credentials)


@pytest.mark.asyncio
@pytest.mark.parametrize("client", [blocking_client, async_client])
async def test_new_order(client: HTTPClient):
    response: NewOrderResponse = await _test_endpoint(client, APIEndpoints.TEST_NEW_ORDER, NewOrderRequest(
        symbol="ETHUSDT",
        side=OrderSides.BUY,
        type=OrderTypes.MARKET,
        quantity=Decimal(0.1)
    ))
    print(response)
