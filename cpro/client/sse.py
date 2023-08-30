import asyncio
import json
import typing
from abc import ABC

import aiohttp
from websockets import client as async_client

from cpro.exception import CoinsAPIException
from cpro.models.ud_stream import UserStreamData, unmarshal_stream_data


class SSEClient(ABC):
    BASE_URL = "https://api.pro.coins.ph"
    BASE_WS_URL = "wss://wsapi.pro.coins.ph"


class AsyncSSEClient(SSEClient):
    def __init__(self, *, api_key: str):
        self.keepalive_task = None
        self.api_key = api_key

    async def send_keepalive(self, interval):
        while True:
            await asyncio.sleep(interval)
            await self.client_session.put(f"{self.BASE_URL}/openapi/v1/userDataStream", params={
                "listenKey": self.listen_key
            })

    async def listen(self) -> typing.Generator[UserStreamData, None, None]:
        self.keepalive_task = asyncio.create_task(self.send_keepalive(30 * 60))

        async with async_client.connect(f"{self.BASE_WS_URL}/openapi/ws/{self.listen_key}") as c:
            async for line in c:
                yield unmarshal_stream_data(json.loads(line))

    async def __aenter__(self):
        self.client_session = aiohttp.ClientSession(headers={
            "X-COINS-APIKEY": self.api_key
        })

        async with self.client_session.post(f"{self.BASE_URL}/openapi/v1/userDataStream") as r:
            data = await r.json()
            if data and "code" in data and "msg" in data:
                raise CoinsAPIException(data["code"], data["msg"])
            self.listen_key = data["listenKey"]

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.keepalive_task.cancel()
        await self.client_session.delete(f"{self.BASE_URL}/openapi/v1/userDataStream", params={
            "listenKey": self.listen_key
        })

        await self.client_session.close()
