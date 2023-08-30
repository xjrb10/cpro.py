import asyncio
import typing
from abc import abstractmethod, ABC
from datetime import datetime
from time import time

from websockets.exceptions import ConnectionClosedOK
from websockets.sync import client as sync_client
from websockets import client as async_client

from cpro.models.ws_stream import WSFrame, PingRequestFrame, unmarshal_frame, PingResponseFrame, TRPCRequestFrame, \
    TRPCResponseFrame


class WSClient(ABC):
    BASE_URL = "wss://wsapi.pro.coins.ph/openapi/quote/ws/v3/"

    def __init__(self, stream: str):
        self.stream = stream
        self._websocket = None
        self._awaiting_resolution: typing.Dict[int, typing.Tuple[
            typing.Type[TRPCResponseFrame], typing.Callable[[TRPCResponseFrame], None]
        ]] = dict()
        self._last_request_id = 0
        self._last_ping = time()

    @abstractmethod
    def listen(self):
        ...

    def _get_rpc_callbacks(self, json_data: str) -> typing.Generator[typing.Callable, WSFrame, None]:
        resolved_keys = []
        for request_id, (response_type, callback) in self._awaiting_resolution.items():
            try:
                parsed = unmarshal_frame(json_data, response_type, request_id)
                yield callback, parsed
            except (KeyError, RuntimeError, ValueError):
                continue
            resolved_keys.append(request_id)

        for key in resolved_keys:
            self._awaiting_resolution.pop(key)


PING_TIME = 5 * 60


class BlockingWSClient(WSClient):
    def __enter__(self):
        self._websocket = sync_client.connect(f"{self.BASE_URL}{self.stream}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        while len(self._awaiting_resolution) > 0:
            data = self._websocket.recv(PING_TIME)  # ensure ping every 5 minutes
            self._handle_rpc_response(data)
            self._ensure_ping()
        self._websocket.close()

    def _send_payload(self, frame: WSFrame) -> None:
        self._websocket.send(frame.to_json())

    def _recv_payload(self, timeout: float) -> WSFrame:
        return unmarshal_frame(self._websocket.recv(timeout))

    def _ping_roundtrip(self) -> typing.Tuple[datetime, float]:
        """
        :return: A tuple of the server's time and the latency (in seconds)
        """
        self._send_payload(request := PingRequestFrame())
        while True:
            data = self._websocket.recv(PING_TIME)
            try:
                response = unmarshal_frame(data)
            except (KeyError, RuntimeError, ValueError):
                continue
            if not self._handle_rpc_response(data) and not isinstance(response, PingResponseFrame):
                continue
            return response.pong, response.pong.timestamp() - request.ping.timestamp()

    def _handle_rpc_response(self, json_data: str) -> bool:
        handled = False
        for callback, parsed in self._get_rpc_callbacks(json_data):
            callback(parsed)
            handled = True
        return handled

    def rpc_request(
            self,
            request: TRPCRequestFrame,
            callback: typing.Callable[[TRPCResponseFrame], None]
    ) -> None:
        if not request.id:
            self._last_request_id += 1
            request.id = self._last_request_id
        self._awaiting_resolution[request.id] = request.expected_response(), callback
        self._websocket.send(request.to_json())

    def _ensure_ping(self):
        if (time() - self._last_ping) <= PING_TIME:
            return
        attempts = 3
        while attempts:
            try:
                server_time, latency = self._ping_roundtrip()
                self._last_ping = server_time.timestamp()
                break
            except TimeoutError as e:
                attempts -= 1
                if attempts < 0:
                    self._websocket.close()
                    raise e

    def listen(self) -> typing.Generator[str, None, None]:
        try:
            while True:
                data = self._websocket.recv(PING_TIME)  # ensure ping every 5 minutes

                # unhandled responses go back to the listener
                if not self._handle_rpc_response(data):
                    yield unmarshal_frame(data)

                self._ensure_ping()
        except ConnectionClosedOK:
            return


class AsyncIOWSClient(WSClient):
    async def __aenter__(self):
        self._websocket = await async_client.connect(f"{self.BASE_URL}{self.stream}")
        return self

    async def _handle_rpc_response(self, json_data: str) -> bool:
        handled = False
        for callback, parsed in self._get_rpc_callbacks(json_data):
            if asyncio.iscoroutinefunction(callback):
                await callback(parsed)
            else:
                callback(parsed)
            handled = True
        return handled

    async def _ensure_ping(self):
        if (time() - self._last_ping) <= PING_TIME:
            return
        attempts = 3
        while attempts:
            try:
                server_time, latency = await self._ping_roundtrip()
                self._last_ping = server_time.timestamp()
                break
            except TimeoutError as e:
                attempts -= 1
                if attempts < 0:
                    await self._websocket.close()
                    raise e

    async def _ping_roundtrip(self) -> typing.Tuple[datetime, float]:
        """
        :return: A tuple of the server's time and the latency (in seconds)
        """
        await self._send_payload(request := PingRequestFrame())
        while True:
            data = await asyncio.wait_for(self._websocket.recv(), timeout=PING_TIME)  # ensure ping every 5 minutes
            try:
                response = unmarshal_frame(data)
            except (KeyError, RuntimeError, ValueError):
                continue
            if not await self._handle_rpc_response(data) and not isinstance(response, PingResponseFrame):
                continue
            return response.pong, response.pong.timestamp() - request.ping.timestamp()

    async def _send_payload(self, frame: WSFrame) -> None:
        await self._websocket.send(frame.to_json())

    async def _recv_payload(self, timeout: float) -> WSFrame:
        return unmarshal_frame(await asyncio.wait_for(self._websocket.recv(), timeout=timeout))

    async def rpc_request(
            self,
            request: TRPCRequestFrame,
            callback: typing.Callable[[TRPCResponseFrame], None]  # todo: support asyncio "Futures"
    ) -> None:
        if not request.id:
            self._last_request_id += 1
            request.id = self._last_request_id
        self._awaiting_resolution[request.id] = request.expected_response(), callback
        await self._websocket.send(request.to_json())

    async def __aexit__(self, exc_type, exc_value, traceback):
        while len(self._awaiting_resolution) > 0:
            data = await asyncio.wait_for(self._websocket.recv(), timeout=PING_TIME)
            await self._handle_rpc_response(data)
            await self._ensure_ping()
        await self._websocket.close()

    async def listen(self) -> typing.AsyncGenerator[str, None]:
        try:
            while True:
                data = await asyncio.wait_for(self._websocket.recv(), timeout=PING_TIME)  # ensure ping every 5 minutes

                # unhandled responses go back to the listener
                if not await self._handle_rpc_response(data):
                    yield unmarshal_frame(data)

                await self._ensure_ping()
        except ConnectionClosedOK:
            return
