import re
from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import dataclass_json, Undefined, config
from marshmallow.fields import Decimal

from cpro.models.rest.enums import DepositStatus


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class Network:
    # https://coins-docs.github.io/rest-api/#all-coins-information-user_data
    addressRegex: re = field(
        metadata=config(
            encoder=lambda _: _.pattern,
            decoder=lambda _: re.compile(_)
        )
    )
    memoRegex: re = field(
        metadata=config(
            encoder=lambda _: _.pattern,
            decoder=lambda _: re.compile(_)
        )
    )
    network: str
    name: str
    depositEnable: bool
    minConfirm: int
    unLockConfirm: int
    withdrawDesc: str
    withdrawEnable: bool
    withdrawFee: Decimal
    withdrawIntegerMultiple: Decimal
    withdrawMax: Decimal
    withdrawMin: Decimal
    sameAddress: bool


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class Coin:
    # https://coins-docs.github.io/rest-api/#all-coins-information-user_data
    coin: str
    name: str
    depositAllEnable: bool
    withdrawAllEnable: bool
    free: Decimal
    locked: Decimal
    networkList: list[Network]
    legalMoney: bool


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class TransactionInfo:
    id: str
    amount: Decimal
    coin: str
    network: str
    status: DepositStatus
    address: str
    addressTag: str
    txId: str
    confirmNo: int


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class DepositTransactionInfo(TransactionInfo):
    insertTime: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )


@dataclass_json(undefined=Undefined.RAISE)
@dataclass(frozen=True)
class WithdrawTransactionInfo(TransactionInfo):
    applyTime: datetime = field(
        metadata=config(
            encoder=lambda _: int(_.timestamp() * 1000),
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
        )
    )
    transactionFee: Decimal
    withdrawOrderId: str
    info: str
