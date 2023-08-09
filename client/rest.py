import typing
from abc import ABC, abstractmethod
from enum import Enum
from http.client import HTTPResponse
from json import dumps
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import aiohttp

from models.rest.enums import SecurityType
from models.rest.request import RequestPayload, APICredentials, TRequestPayload, CoinsInformationRequest, \
    DepositAddressRequest, DepositHistoryRequest, WithdrawHistoryRequest
from models.rest.response import ExchangeInformationResponse, TResponsePayload, ServerTimeResponse, PingResponse, \
    CoinsInformationResponse, DepositAddressResponse, DepositHistoryResponse, WithdrawHistoryResponse


class HTTPException(Exception):
    def __init__(self, body: str, headers: dict, status: int):
        self.body = body
        self.headers = headers
        self.status = status
        super().__init__(f"Received code {status}: {body}\n\nResponse Headers: {dumps(headers, indent=2)}")


API_BASE_URL = "https://api.pro.coins.ph"  # https://coins-docs.github.io/rest-api/#general-api-information


class _APIRequest:
    def __init__(
            self,
            endpoint: str,
            response_cls: typing.Type[TResponsePayload],
            required_payload_cls: typing.Type[TRequestPayload] = None,
            security: SecurityType = SecurityType.NONE
    ):
        self.method, self.endpoint = endpoint.split(" ")
        self.response_cls = response_cls
        self.required_payload_cls = required_payload_cls
        self.security = security


class HTTPClient(ABC):
    def __init__(self, credentials: APICredentials = None):
        self.credentials = credentials

    @abstractmethod
    def do_request(
            self,
            request: _APIRequest,
            request_payload: typing.Optional[RequestPayload] = None
    ) -> TResponsePayload:
        ...

    def payload_to_tuple(self, request: _APIRequest, payload: typing.Optional[RequestPayload] = None) -> tuple:
        json = {}
        data = ""
        params = ""
        headers = {"Accept": "application/json"}

        if not isinstance(payload, request.required_payload_cls):
            raise ValueError(f"Payload must be of {request.required_payload_cls}, {type(payload)} given.")

        if not payload and request.security != SecurityType.NONE:
            raise ValueError(f"Credentials are required to access {request.endpoint}!")

        if payload:
            encoded_payload = payload.to_encoded()
            if request.security != SecurityType.NONE:
                if self.credentials is None:
                    raise ValueError(f"Credentials are required to access {request.endpoint}!")
                if request.security.is_signed():
                    if self.credentials.api_secret is None:
                        raise ValueError(f"API Secret required to access {request.endpoint}!")
                    encoded_payload = encoded_payload.sign(self.credentials.api_key, self.credentials.api_secret)
                else:
                    encoded_payload = encoded_payload.with_key(self.credentials.api_key)
            data = encoded_payload.data
            json.update(encoded_payload.json)
            params = encoded_payload.params
            headers.update(encoded_payload.headers)

        return json, data, params, headers


class APIRequests(Enum):
    GET_PING = _APIRequest("GET /openapi/v1/ping", PingResponse)
    GET_SERVER_TIME = _APIRequest("GET /openapi/v1/time", ServerTimeResponse)
    GET_EXCHANGE_INFO = _APIRequest("GET /openapi/v1/exchangeInfo", ExchangeInformationResponse)

    GET_ALL_USER_COINS = _APIRequest(
        "GET /openapi/wallet/v1/config/getall", CoinsInformationResponse,
        CoinsInformationRequest, SecurityType.USER_DATA
    )
    GET_DEPOSIT_ADDRESS = _APIRequest(
        "GET /openapi/wallet/v1/deposit/address", DepositAddressResponse,
        DepositAddressRequest, SecurityType.USER_DATA
    )
    # todo: https://coins-docs.github.io/rest-api/#withdrawuser_data
    GET_DEPOSIT_HISTORY = _APIRequest(
        "GET /openapi/wallet/v1/deposit/history", DepositHistoryResponse,
        DepositHistoryRequest, SecurityType.USER_DATA
    )
    GET_WITHDRAW_HISTORY = _APIRequest(
        "GET /openapi/wallet/v1/withdraw/history", WithdrawHistoryResponse,
        WithdrawHistoryRequest, SecurityType.USER_DATA
    )

    def execute(self, client: HTTPClient, payload: typing.Optional[RequestPayload] = None) -> TResponsePayload:
        return client.do_request(self.value, payload)

    async def execute_async(
            self, client: HTTPClient, payload: typing.Optional[RequestPayload] = None
    ) -> TResponsePayload:
        return await client.do_request(self.value, payload)


class BlockingHTTPClient(HTTPClient):
    def do_request(
            self,
            request: _APIRequest,
            request_payload: typing.Optional[RequestPayload] = None
    ) -> TResponsePayload:
        json, data, params, headers = self.payload_to_tuple(request, request_payload)
        headers.update({"User-Agent": "urllib/cpro.py v0.0.1"})

        url = request.endpoint
        if params:
            url += f"?{params}"

        if json and data:
            raise ValueError("Only one of `json` or `data` can be passed.")

        if json:
            request_data = dumps(data)
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = data

        print(API_BASE_URL + url, request_data.encode(), headers, request.method.upper())
        try:
            with urlopen(Request(
                    API_BASE_URL + url, data=request_data.encode(), headers=headers, method=request.method.upper()
            )) as response:  # type: HTTPResponse
                return request.response_cls.from_json(response.read().decode(
                    response.headers.get_content_charset("utf-8")
                ))
        except HTTPError as e:
            raise HTTPException(
                body=str(e.reason),
                headers={key.lower(): value for key, value in e.headers.items()},
                status=e.code
            )


class AsyncIOHTTPClient(HTTPClient):
    async def do_request(
            self,
            request: _APIRequest,
            request_payload: typing.Optional[RequestPayload] = None
    ) -> TResponsePayload:
        json, data, params, headers = self.payload_to_tuple(request, request_payload)
        headers.update({"User-Agent": "aiohttp/cpro.py v0.0.1"})

        url = request.endpoint
        if params:
            url += f"?{params}"

        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.request(
                        request.method.upper(), API_BASE_URL + request.endpoint,
                        data=data, json=json, headers=headers
                ) as response:
                    return request.response_cls.from_json(await response.text())
        except HTTPError as e:
            raise HTTPException(
                body=str(e.reason),
                headers={key.lower(): value for key, value in e.headers.items()},
                status=e.code
            )
