from time import time

import pytest

from cpro.client.wss import BlockingWSClient, AsyncIOWSClient
from cpro.models.ws_stream import SubscriptionListRequest, StreamUnsubscribeRequest


def test_ws_client():
    end_time = 10 * 60 + time()
    with BlockingWSClient("btcusdt@depth@100ms") as client:
        for line in client.listen():
            if end_time < time():
                break
            print(line)


@pytest.mark.asyncio
async def test_ws_client_ping_async():
    async with AsyncIOWSClient("btcusdt@depth@100ms") as client:
        await client.rpc_request(SubscriptionListRequest(), lambda _: print(_))
        await client._ping_roundtrip()
        await client.rpc_request(SubscriptionListRequest(), lambda _: print(_))


def test_ws_client_ping():
    with BlockingWSClient("btcusdt@depth@100ms") as client:
        client.rpc_request(SubscriptionListRequest(), lambda _: print(_))
        client._ping_roundtrip()
        client.rpc_request(SubscriptionListRequest(), lambda _: print(_))


@pytest.mark.asyncio
async def test_ws_client2():
    limit = 100
    async with AsyncIOWSClient("btcusdt@depth@100ms") as client:
        async for line in client.listen():
            if limit < 0:
                break
            limit -= 1
            print(line)
