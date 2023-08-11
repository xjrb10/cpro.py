import typing
from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin, config
from marshmallow.fields import Decimal

from cpro.models.rest.enums import ExecutionTypes, OrderSides


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
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
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
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
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
    eventType: str = field(metadata=config(
        # todo: maybe turn this into an enum
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
    orderType: str = field(metadata=config(
        field_name="o"  # todo: make this an enum? undocumented (EX: LIMIT)
    ))
    timeInForce: str = field(metadata=config(
        field_name="f"  # todo: make this an enum? undocumented (EX: GTC)
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
    currentOrderStatus: str = field(metadata=config(
        field_name="X"  # todo: make this an enum? undocumented (EX: NEW)
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
