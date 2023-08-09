import typing
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar

from dataclasses_json import dataclass_json, config, Undefined, DataClassJsonMixin

from models.rest.symbol import SymbolInfo
from models.rest.wallet import Coin, DepositTransactionInfo, WithdrawTransactionInfo


@dataclass(frozen=True)
class ResponsePayload(DataClassJsonMixin):
    pass


TResponsePayload = TypeVar("TResponsePayload", bound=ResponsePayload)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class PingResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#test-connectivity
    pass


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class ServerTimeResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#check-server-time
    serverTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class ExchangeInformationResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#exchange-information
    timezone: str  # default: UTC - todo: currently this is ignored by the lib
    serverTime: datetime = field(metadata=config(
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)  # todo: perhaps base timezone from given timezone field?
    ))
    exchangeFilters: list  # empty -- Reason: https://coins-docs.github.io/rest-api/#exchange-filters
    symbols: list[SymbolInfo]


@dataclass(frozen=True)
class CoinsInformationResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#all-coins-information-user_data
    coins: list[Coin]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "CoinsInformationResponse":
        if isinstance(kvs, list):
            return super().from_dict({"coins": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class DepositAddressResponse(ResponsePayload):
    # https://coins-docs.github.io/rest-api/#deposit-address-user_data
    coin: str
    address: str
    addressTag: str


@dataclass(frozen=True)
class DepositHistoryResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#deposit-address-user_data
    transactions: list[DepositTransactionInfo]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "DepositHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"transactions": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)


@dataclass(frozen=True)
class WithdrawHistoryResponse(ResponsePayload, DataClassJsonMixin):
    # https://coins-docs.github.io/rest-api/#withdraw-history-user_data
    transactions: list[WithdrawTransactionInfo]

    @classmethod
    def from_dict(cls, kvs, *, infer_missing=False) -> "WithdrawHistoryResponse":
        if isinstance(kvs, list):
            return super().from_dict({"transactions": kvs}, infer_missing=infer_missing)
        return super().from_dict(kvs, infer_missing=infer_missing)
