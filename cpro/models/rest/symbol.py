from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config

from cpro.models.rest.filter import FilterOption, create_filter
from cpro.models.rest.enums import OrderType, SymbolStatus


@dataclass_json
@dataclass(frozen=True)
class SymbolInfo:
    # https://coins-docs.github.io/rest-api/#exchange-information
    symbol: str
    status: SymbolStatus = field(metadata=config(
        encoder=lambda _: _.lower(),
        decoder=lambda _: _.upper()
    ))
    baseAsset: str
    baseAssetPrecision: int
    quoteAsset: str
    quoteAssetPrecision: int
    orderTypes: list[OrderType]
    filters: list[FilterOption] = field(metadata=config(
        encoder=lambda _: [__.to_dict() for __ in _],
        decoder=lambda _: [create_filter(__) for __ in _]
    ))
