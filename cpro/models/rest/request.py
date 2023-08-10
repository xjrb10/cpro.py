import hashlib
import hmac
import json
import typing
from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from urllib.parse import quote, urlencode

from dataclasses_json import DataClassJsonMixin, config

from cpro.models.rest.enums import DepositStatus, WithdrawStatus


@dataclass(frozen=True)
class APICredentials:
    api_key: str
    api_secret: str = None


@dataclass
class EncodedPayload(DataClassJsonMixin):
    data: str = ""
    raw_params: dict = field(default_factory=dict)
    json: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)

    @property
    def params(self) -> str:
        return "&".join(f"{k}={v}" for k, v in self.raw_params.items())

    def with_key(self, api_key: str) -> "EncodedPayload":
        authenticated = copy(self)
        authenticated.headers["X-COINS-APIKEY"] = api_key
        return authenticated

    def sign(self, api_key: str, api_secret: str) -> "EncodedPayload":
        signed = copy(self)
        signed.raw_params["signature"] = hmac.new(
            api_secret.encode(),
            msg=signed.params.encode() + signed.data.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        return signed.with_key(api_key)

    def put_urlencoded_data(self, data: dict) -> "EncodedPayload":
        with_data = copy(self)
        with_data.data = urlencode(data)
        return with_data


class RequestPayload(ABC):
    @abstractmethod
    def to_encoded(self) -> EncodedPayload:
        ...


TRequestPayload = typing.TypeVar("TRequestPayload", bound=RequestPayload)


@dataclass(frozen=True)
class ExchangeInformationRequest(RequestPayload):
    symbol: typing.Optional[str] = None
    symbols: typing.Optional[typing.List[str]] = None

    def to_encoded(self) -> EncodedPayload:
        if self.symbols:
            return EncodedPayload(raw_params={
                "symbols": quote(json.dumps(self.symbols, separators=(',', ':')), safe='"\',')
            })
        if self.symbol:
            return EncodedPayload(raw_params={
                "symbol": self.symbol
            })
        return EncodedPayload()


@dataclass(frozen=True)
class CoinsInformationRequest(RequestPayload, DataClassJsonMixin):
    recvWindow: typing.Optional[int] = None
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def to_encoded(self) -> EncodedPayload:
        data = self.to_dict()
        if not self.recvWindow:
            data.pop("recvWindow")
        return EncodedPayload(raw_params=data)


@dataclass(frozen=True)
class DepositAddressRequest(RequestPayload, DataClassJsonMixin):
    coin: str
    network: str
    recvWindow: int = 5000
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def to_encoded(self) -> EncodedPayload:
        return EncodedPayload(raw_params=self.to_dict())


@dataclass(frozen=True)
class DepositHistoryRequest(RequestPayload, DataClassJsonMixin):
    coin: typing.Optional[str] = None
    txId: typing.Optional[str] = None
    status: typing.Optional[DepositStatus] = None
    startTime: datetime = field(
        default_factory=lambda: datetime.now() - timedelta(days=90),
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    offset: int = 0
    limit: int = 1000
    recvWindow: int = 5000
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def to_encoded(self) -> EncodedPayload:
        return EncodedPayload(raw_params={k: v for k, v in self.to_dict().items() if v})


@dataclass(frozen=True)
class WithdrawHistoryRequest(RequestPayload, DataClassJsonMixin):
    coin: typing.Optional[str] = None
    withdrawOrderId: typing.Optional[str] = None
    status: typing.Optional[WithdrawStatus] = None
    startTime: datetime = field(
        default_factory=lambda: datetime.now() - timedelta(days=90),
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    endTime: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    offset: int = 0
    limit: int = 1000
    recvWindow: int = 5000
    timestamp: datetime = field(
        default_factory=datetime.now,
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )

    def to_encoded(self) -> EncodedPayload:
        return EncodedPayload(raw_params={k: v for k, v in self.to_dict().items() if v})
