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

import typing
from dataclasses import dataclass, field
from datetime import datetime
from decimal import *
from enum import Enum

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin, config

from cpro.models.rest.enums import ExecutionTypes, OrderSides, TimeInForce, OrderType, OrderStatus


class UserDataStreamEventTypes(Enum):
    ACCOUNT_UPDATE = "outboundAccountPosition"
    BALANCE_UPDATE = "balanceUpdate"
    ORDER_UPDATE = "executionReport"


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class UserStreamData(DataClassJsonMixin):
    pass


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class AccountBalanceUpdateData:
    asset: str = field(metadata=config(
        field_name="a"
    ))
    free: Decimal = field(metadata=config(
        field_name="f"
    ))
    locked: Decimal = field(metadata=config(
        field_name="l"
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class AccountUpdateData(UserStreamData):
    eventType: UserDataStreamEventTypes = field(metadata=config(
        field_name="e"  # outboundAccountPosition
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    asset: str = field(metadata=config(
        field_name="a"
    ))
    delta: Decimal = field(metadata=config(
        field_name="d"
    ))
    clearTime: datetime = field(metadata=config(
        field_name="T",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class BalanceUpdateData(UserStreamData):
    eventType: UserDataStreamEventTypes = field(metadata=config(
        field_name="e"  # balanceUpdate
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    lastAccountUpdatetime: datetime = field(metadata=config(
        field_name="u",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    balanceUpdates: list[AccountBalanceUpdateData] = field(metadata=config(
        field_name="B",
    ))


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class OrderUpdateData(UserStreamData):
    eventType: UserDataStreamEventTypes = field(metadata=config(
        field_name="e"  # executionReport
    ))
    eventTime: datetime = field(metadata=config(
        field_name="E",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    symbol: str = field(metadata=config(
        field_name="s"
    ))
    clientOrderID: str = field(metadata=config(
        field_name="c"
    ))
    side: OrderSides = field(metadata=config(
        field_name="S"
    ))
    orderType: OrderType = field(metadata=config(
        field_name="o"
    ))
    timeInForce: TimeInForce = field(metadata=config(
        field_name="f"
    ))
    orderQuantity: Decimal = field(metadata=config(
        field_name="q"
    ))
    orderPrice: Decimal = field(metadata=config(
        field_name="p"
    ))
    stopPrice: Decimal = field(metadata=config(
        field_name="P"
    ))
    currentExecutionType: ExecutionTypes = field(metadata=config(
        field_name="x"
    ))
    currentOrderStatus: OrderStatus = field(metadata=config(
        field_name="X"
    ))
    orderRejectReason: str = field(metadata=config(
        field_name="r"  # todo: make this an enum? undocumented (EX: NONE)
    ))
    orderID: int = field(metadata=config(
        field_name="i"
    ))
    lastExecutedQuantity: Decimal = field(metadata=config(
        field_name="l"
    ))
    cumulativeFilledQuantity: Decimal = field(metadata=config(
        field_name="z"
    ))
    lastExecutedPrice: Decimal = field(metadata=config(
        field_name="L"
    ))
    commissionAmount: Decimal = field(metadata=config(
        field_name="n"
    ))
    tradeID: int = field(metadata=config(
        field_name="t"
    ))
    isOrderOnBook: bool = field(metadata=config(
        field_name="w"
    ))
    isTradeMakerSide: bool = field(metadata=config(
        field_name="m"
    ))
    orderCreationTime: datetime = field(metadata=config(
        field_name="O",
        encoder=lambda _: int(_.timestamp() * 1000),
        decoder=lambda _: datetime.fromtimestamp(_ / 1000.0)
    ))
    cumulativeQuoteAssetTransactedQuantity: Decimal = field(metadata=config(
        field_name="Z"
    ))
    lastQuoteAssetTransactedQuantity: Decimal = field(metadata=config(
        field_name="Y"
    ))
    quoteOrderQuantity: Decimal = field(metadata=config(
        field_name="Q"
    ))
    commissionAsset: typing.Optional[str] = field(
        default=None,
        metadata=config(field_name="N")
    )
    transactionTime: typing.Optional[datetime] = field(
        default=None,
        metadata=config(
            field_name="T",
            encoder=lambda _: int(_.timestamp() * 1000) if _ is not None else None,
            decoder=lambda _: datetime.fromtimestamp(_ / 1000.0) if _ > 0 else None
        )
    )


def unmarshal_stream_data(data: dict) -> UserStreamData:
    match data['e']:
        case UserDataStreamEventTypes.ACCOUNT_UPDATE:
            return AccountUpdateData.from_dict(data)
        case UserDataStreamEventTypes.BALANCE_UPDATE:
            return BalanceUpdateData.from_dict(data)
        case UserDataStreamEventTypes.ORDER_UPDATE:
            return OrderUpdateData.from_dict(data)
    raise ValueError(f"Unhandled event: {data['e']}")
