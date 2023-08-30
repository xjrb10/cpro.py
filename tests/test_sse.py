import os

import pytest

from cpro.client.sse import AsyncSSEClient


@pytest.mark.asyncio
async def test_user_data_stream():
    async with AsyncSSEClient(api_key=os.getenv("API_KEY")) as client:
        async for payload in client.listen():
            print(payload)
