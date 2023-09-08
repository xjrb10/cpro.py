import os

import pytest

from cpro.client.sse import AsyncSSEClient, BlockingSSEClient


@pytest.mark.asyncio
async def test_user_data_stream_async():
    async with AsyncSSEClient(api_key=os.getenv("API_KEY")) as client:
        async for payload in client:
            print(payload)


def test_user_data_stream_sync():
    with BlockingSSEClient(api_key=os.getenv("API_KEY")) as client:
        for payload in client:
            print(payload)
