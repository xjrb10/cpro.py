import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from http.client import HTTPResponse
from json import dumps, loads
from urllib.error import HTTPError
from urllib.request import Request, urlopen, HTTPErrorProcessor, build_opener

import aiohttp

from cpro.exception import HTTPException, CoinsAPIException
from cpro.models.rest.enums import SecurityType
from cpro.models.rest.request import RequestPayload, TRequestPayload
from cpro.models.rest.response import TResponsePayload


@dataclass(frozen=True)
class APICredentials:
    api_key: str
    api_secret: str = None


class APIEndpoint:
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
    API_BASE_URL = "https://api.pro.coins.ph"  # https://coins-docs.github.io/rest-api/#general-api-information

    def __init__(self, credentials: APICredentials = None):
        self.credentials = credentials

    @abstractmethod
    def do_request(
            self,
            request: APIEndpoint,
            request_payload: typing.Optional[RequestPayload] = None
    ) -> TResponsePayload:
        ...

    def payload_to_tuple(self, request: APIEndpoint, payload: typing.Optional[RequestPayload] = None) -> tuple:
        json = {}
        data = ""
        params = ""
        headers = {"Accept": "application/json"}

        if request.required_payload_cls and not isinstance(payload, request.required_payload_cls):
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


class _NonRaisingHTTPErrorProcessor(HTTPErrorProcessor):
    def http_response(self, _, response):
        return response

    def https_response(self, _, response):
        return response


class BlockingHTTPClient(HTTPClient):
    def do_request(
            self,
            request: APIEndpoint,
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

        with build_opener(_NonRaisingHTTPErrorProcessor).open(Request(
                self.API_BASE_URL + url, data=request_data.encode(), headers=headers, method=request.method.upper()
        )) as response:  # type: HTTPResponse
            text_content = response.read().decode(
                response.headers.get_content_charset("utf-8")
            )
            response_data = loads(text_content)
            if response_data and "code" in response_data and "msg" in response_data:
                raise CoinsAPIException(response_data["code"], response_data["msg"])
            if response.status >= 400:
                raise HTTPException(
                    body=text_content,
                    headers={key.lower(): value for key, value in response.headers.items()},
                    status=response.status
                )
            return request.response_cls.from_dict(response_data)


class AsyncIOHTTPClient(HTTPClient):
    async def do_request(
            self,
            request: APIEndpoint,
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
                        request.method.upper(), self.API_BASE_URL + url,
                        data=data or None, json=json or None, headers=headers
                ) as response:
                    response_data = await response.json()
                    if response_data and "code" in response_data and "msg" in response_data:
                        raise CoinsAPIException(response_data["code"], response_data["msg"])
                    response.raise_for_status()
                    return request.response_cls.from_dict(response_data)
        except HTTPError as e:
            raise HTTPException(
                body=str(e.reason),
                headers={key.lower(): value for key, value in e.headers.items()},
                status=e.code
            )
