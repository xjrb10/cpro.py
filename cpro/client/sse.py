"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2023-present xjrb10

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import json
import threading
import typing
from abc import ABC

import aiohttp
import requests
from websockets import client as async_client
from websockets.sync import client as sync_client

from cpro.exception import CoinsAPIException
from cpro.models.ud_stream import UserStreamData, unmarshal_stream_data

BASE_URL = "https://api.pro.coins.ph"
BASE_WS_URL = "wss://wsapi.pro.coins.ph"


class SSEClient(ABC):
    def __init__(self, *, api_key: str, keepalive_interval: int = 30 * 60):
        self.api_key = api_key
        self.keepalive_interval = keepalive_interval

    def _make_headers(self):
        return {
            "X-COINS-APIKEY": self.api_key
        }


class KeepAliveThread(threading.Thread):
    def __init__(self, *args, client_session: requests.Session, interval: int, listen_key: str, **kwargs):
        self.client_session = client_session
        self.interval = interval
        self.listen_key = listen_key
        self.sleeper = threading.Event()
        self.finished = False
        super().__init__(*args, **kwargs)

    def run(self) -> None:
        while True:
            self.sleeper.wait(timeout=self.interval)

            if self.finished:
                break  # don't send a keepalive after killing to keep it clean

            self.client_session.put(f"{BASE_URL}/openapi/v1/userDataStream", params={
                "listenKey": self.listen_key
            })

    def stop(self) -> None:
        self.finished = True
        self.sleeper.set()


class BlockingSSEClient(SSEClient):
    def __init__(self, *, api_key: str, keepalive_interval: int = 30 * 60):
        super().__init__(api_key=api_key, keepalive_interval=keepalive_interval)
        self.keepalive_task: typing.Optional[KeepAliveThread] = None

    def send_keepalive(self, interval: int, sleeper: threading.Event):
        while True:
            sleeper.wait(timeout=interval)
            self.client_session.put(f"{BASE_URL}/openapi/v1/userDataStream", params={
                "listenKey": self.listen_key
            })

    def __enter__(self):
        self.client_session = requests.Session()
        self.client_session.headers = self._make_headers()

        r = self.client_session.post(f"{BASE_URL}/openapi/v1/userDataStream")
        data = r.json()
        if data and "code" in data and "msg" in data:
            raise CoinsAPIException(data["code"], data["msg"])
        self.listen_key = data["listenKey"]
        self.keepalive_task = KeepAliveThread(
            client_session=self.client_session,
            interval=self.keepalive_interval,
            listen_key=self.listen_key
        )
        self.keepalive_task.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.keepalive_task.stop()
        self.keepalive_task.join()
        self.client_session.delete(f"{BASE_URL}/openapi/v1/userDataStream", params={
            "listenKey": self.listen_key
        })

        self.client_session.close()

    def __iter__(self) -> typing.Iterator[UserStreamData]:
        with sync_client.connect(f"{BASE_WS_URL}/openapi/ws/{self.listen_key}") as c:
            for line in c:
                yield unmarshal_stream_data(json.loads(line))


class AsyncSSEClient(SSEClient):
    def __init__(self, *, api_key: str, keepalive_interval: int = 30 * 60):
        super().__init__(api_key=api_key, keepalive_interval=keepalive_interval)
        self.keepalive_task: typing.Optional[asyncio.Task] = None

    async def send_keepalive(self, interval):
        while True:
            await asyncio.sleep(interval)
            await self.client_session.put(f"{BASE_URL}/openapi/v1/userDataStream", params={
                "listenKey": self.listen_key
            })

    async def __aenter__(self):
        self.client_session = aiohttp.ClientSession(headers=self._make_headers())

        async with self.client_session.post(f"{BASE_URL}/openapi/v1/userDataStream") as r:
            data = await r.json()
            if data and "code" in data and "msg" in data:
                raise CoinsAPIException(data["code"], data["msg"])
            self.listen_key = data["listenKey"]
        self.keepalive_task = asyncio.create_task(self.send_keepalive(self.keepalive_interval))

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.keepalive_task.cancel()
        await self.client_session.delete(f"{BASE_URL}/openapi/v1/userDataStream", params={
            "listenKey": self.listen_key
        })

        await self.client_session.close()

    async def __aiter__(self) -> typing.AsyncIterator[UserStreamData]:
        async with async_client.connect(f"{BASE_WS_URL}/openapi/ws/{self.listen_key}") as c:
            async for line in c:
                yield unmarshal_stream_data(json.loads(line))
