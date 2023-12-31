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

import re
import typing
from dataclasses import dataclass
from decimal import *

from dataclasses_json import dataclass_json

from cpro.models.rest.enums import _FilterType

P_INFINITY = 99999999999.00000000
N_INFINITY = -99999999999.00000000


@dataclass_json
@dataclass(frozen=True)
class FilterOption:
    # https://coins-docs.github.io/rest-api/#symbol-filters
    filterType: _FilterType


TFilterOption = typing.TypeVar('TFilterOption', bound=FilterOption)


@dataclass_json
@dataclass(frozen=True)
class PriceFilter(FilterOption):
    """
    In order to pass the price filter, the following must be true for price/stopPrice:

    price >= minPrice
    price <= maxPrice
    (price-minPrice) % tickSize == 0

    LINK: https://coins-docs.github.io/rest-api/#price_filter
    """
    minPrice: Decimal
    maxPrice: Decimal
    tickSize: Decimal

    @classmethod
    def create(cls, min_price: Decimal, max_price: Decimal, tick_size: Decimal) -> 'PriceFilter':
        return cls(filterType=_FilterType.PRICE_FILTER, minPrice=min_price, maxPrice=max_price, tickSize=tick_size)


@dataclass_json
@dataclass(frozen=True)
class PercentPriceFilter(FilterOption):
    """
    The PERCENT_PRICE filter defines valid range for a price based on the weighted average of the previous trades.
    avgPriceMins is the number of minutes the weighted average price is calculated over.

    In order to pass the percent price, the following must be true for price:

    price <= weightedAveragePrice * multiplierUp
    price >= weightedAveragePrice * multiplierDown

    LINK: https://coins-docs.github.io/rest-api/#percent_price
    """
    multiplierUp: Decimal
    multiplierDown: Decimal
    avgPriceMins: Decimal

    @staticmethod
    def create(multiplier_up: Decimal, multiplier_down: Decimal, avg_price_mins: Decimal) -> 'PercentPriceFilter':
        return PercentPriceFilter(
            filterType=_FilterType.PERCENT_PRICE,
            multiplierUp=multiplier_up,
            multiplierDown=multiplier_down,
            avgPriceMins=avg_price_mins
        )


@dataclass_json
@dataclass(frozen=True)
class PercentPriceSAFilter(FilterOption):
    """
    The PERCENT_PRICE_SA filter defines valid range for a price based on the simple average of the previous trades.
    avgPriceMins is the number of minutes the simple average price is calculated over.

    In order to pass the percent_price_sa, the following must be true for price:

    price <= simpleAveragePrice * multiplierUp
    price >= simpleAveragePrice * multiplierDown

    LINK: https://coins-docs.github.io/rest-api/#percent_price
    """
    multiplierUp: Decimal
    multiplierDown: Decimal
    avgPriceMins: Decimal

    @classmethod
    def create(
            cls,
            multiplier_up: Decimal, multiplier_down: Decimal,
            avg_price_mins: Decimal
    ) -> 'PercentPriceSAFilter':
        return cls(
            filterType=_FilterType.PERCENT_PRICE_SA,
            multiplierUp=multiplier_up,
            multiplierDown=multiplier_down,
            avgPriceMins=avg_price_mins
        )


@dataclass_json
@dataclass(frozen=True)
class PercentPriceBySideFilter(FilterOption):
    """
    The PERCENT_PRICE_BY_SIDE filter defines the valid range for the price based on the last price of the symbol.
    There is a different range depending on whether the order is placed on the BUY side or the SELL side.

    Buy orders will succeed on this filter if:

    Order price <= bidMultiplierUp * lastPrice
    Order price >= bidMultiplierDown * lastPrice

    Sell orders will succeed on this filter if:

    Order Price <= askMultiplierUp * lastPrice
    Order Price >= askMultiplierDown * lastPrice

    LINK: https://coins-docs.github.io/rest-api/#percent_price_by_side
    """
    bidMultiplierUp: Decimal
    bidMultiplierDown: Decimal
    askMultiplierUp: Decimal
    askMultiplierDown: Decimal

    @classmethod
    def create(
            cls,
            bid_multiplier_up: Decimal, bid_multiplier_down: Decimal,
            ask_multiplier_up: Decimal, ask_multiplier_down: Decimal
    ) -> 'PercentPriceBySideFilter':
        return cls(
            filterType=_FilterType.PERCENT_PRICE_BY_SIDE,
            bidMultiplierUp=bid_multiplier_up,
            bidMultiplierDown=bid_multiplier_down,
            askMultiplierUp=ask_multiplier_up,
            askMultiplierDown=ask_multiplier_down
        )


@dataclass_json
@dataclass(frozen=True)
class PercentPriceIndexFilter(FilterOption):
    """
    The PERCENT_PRICE_INDEX filter defines valid range for a price based on the index price which is calculated based on
    several exhanges in the market by centain rule. (indexPrice wobsocket pushing will be available in future)

    In order to pass the percent_price_index, the following must be true for price:

    price <= indexPrice * multiplierUp
    price >= indexPrice * multiplierDown

    LINK: https://coins-docs.github.io/rest-api/#percent_price_index
    """
    multiplierUp: Decimal
    multiplierDown: Decimal

    @classmethod
    def create(
            cls,
            multiplier_up: Decimal, multiplier_down: Decimal
    ) -> 'PercentPriceIndexFilter':
        return cls(
            filterType=_FilterType.PERCENT_PRICE_INDEX,
            multiplierUp=multiplier_up,
            multiplierDown=multiplier_down,
        )


@dataclass_json
@dataclass(frozen=True)
class PercentPriceOrderSizeFilter(FilterOption):
    """
    The PERCENT_PRICE_ORDER_SIZE filter is used to determine whether the execution of an order would cause the market
    price to fluctuate beyond the limit price, and if so, the order will be rejected.

    In order to pass the percent_price_order_size, the following must be true:

    A buy order needs to meet: the market price after the order get filled <askPrice * multiplierUp
    A sell order needs to meet: the market price after the order get filled >bidPrice * multiplierDown

    LINK: https://coins-docs.github.io/rest-api/#percent_price_order_size
    """
    multiplierUp: Decimal
    multiplierDown: Decimal

    @classmethod
    def create(
            cls,
            multiplier_up: Decimal, multiplier_down: Decimal
    ) -> 'PercentPriceOrderSizeFilter':
        return cls(
            filterType=_FilterType.PERCENT_PRICE_ORDER_SIZE,
            multiplierUp=multiplier_up,
            multiplierDown=multiplier_down,
        )


@dataclass_json
@dataclass(frozen=True)
class StaticPriceRangeFilter(FilterOption):
    """
    The STATIC_PRICE_RANGE filter defines a static valid range for the price.

    In order to pass the static_price_range, the following must be true for price:

    price <= priceUp
    price >= priceDown

    LINK: https://coins-docs.github.io/rest-api/#static_price_range
    """
    priceUp: Decimal
    priceDown: Decimal

    @classmethod
    def create(
            cls,
            price_up: Decimal, price_down: Decimal
    ) -> 'StaticPriceRangeFilter':
        return cls(
            filterType=_FilterType.STATIC_PRICE_RANGE,
            priceUp=price_up,
            priceDown=price_down,
        )


@dataclass_json
@dataclass(frozen=True)
class LotSizeFilter(FilterOption):
    """
    The LOT_SIZE filter defines the quantity (aka “lots” in auction terms) rules for a symbol. There are 3 parts:

    minQty defines the minimum quantity allowed.
    maxQty defines the maximum quantity allowed.
    stepSize defines the intervals that a quantitycan be increased/decreased by.

    In order to pass the lot size, the following must be true for quantity:

    quantity >= minQty
    quantity <= maxQty
    (quantity-minQty) % stepSize == 0

    LINK: https://coins-docs.github.io/rest-api/#lot_size
    """
    minQty: Decimal
    maxQty: Decimal
    stepSize: Decimal

    @classmethod
    def create(
            cls,
            min_qty: Decimal, max_qty: Decimal, step_size: Decimal
    ) -> 'LotSizeFilter':
        return cls(
            filterType=_FilterType.LOT_SIZE,
            minQty=min_qty,
            maxQty=max_qty,
            stepSize=step_size,
        )


@dataclass_json
@dataclass(frozen=True)
class NotionalFilter(FilterOption):
    """
    The NOTIONAL filter defines the acceptable notional range allowed for an order on a symbol.

    In order to pass this filter, the notional (price * quantity) has to pass the following conditions:

    price * quantity <= maxNotional
    price * quantity >= minNotional

    LINK: https://coins-docs.github.io/rest-api/#notional
    """
    minNotional: Decimal
    maxNotional: Decimal

    @classmethod
    def create(
            cls,
            min_notional: Decimal, max_notional: Decimal = P_INFINITY
    ) -> 'NotionalFilter':
        return cls(
            filterType=_FilterType.NOTIONAL,
            minNotional=min_notional,
            maxNotional=max_notional,
        )


@dataclass_json
@dataclass(frozen=True)
class MinNotionalFilter(FilterOption):
    """
    !! NO DOCUMENTATION !!

    REFERENCE: https://coins-docs.github.io/rest-api/#exchange-information
    {
        "filterType": "MIN_NOTIONAL",
        "minNotional": "0.00100000"
    },
    """
    minNotional: Decimal

    @classmethod
    def create(
            cls,
            min_notional: Decimal
    ) -> 'MinNotionalFilter':
        return cls(
            filterType=_FilterType.MIN_NOTIONAL,
            minNotional=min_notional
        )


@dataclass_json
@dataclass(frozen=True)
class MaxNumOrdersFilter(FilterOption):
    """
    The MAX_NUM_ORDERS filter defines the maximum number of orders an account is allowed to have open on a symbol.
    Note that both triggered “algo” orders and normal orders are counted for this filter.

    LINK: https://coins-docs.github.io/rest-api/#max_num_orders
    """
    maxNumOrders: int

    @classmethod
    def create(
            cls,
            max_num_orders: int
    ) -> 'MaxNumOrdersFilter':
        return cls(
            filterType=_FilterType.MAX_NUM_ORDERS,
            maxNumOrders=max_num_orders
        )


@dataclass_json
@dataclass(frozen=True)
class MaxNumAlgoOrdersFilter(FilterOption):
    """
    The MAX_NUM_ORDERS filter defines the maximum number of orders an account is allowed to have open on a symbol.
    Note that both triggered “algo” orders and normal orders are counted for this filter.

    LINK: https://coins-docs.github.io/rest-api/#max_num_algo_orders
    """
    maxNumAlgoOrders: int

    @classmethod
    def create(
            cls,
            max_num_algo_orders: int
    ) -> 'MaxNumAlgoOrdersFilter':
        return cls(
            filterType=_FilterType.MAX_NUM_ALGO_ORDERS,
            maxNumAlgoOrders=max_num_algo_orders
        )


def camel_to_snake_case(string: str):
    return re.sub(r'([a-z0-9]|.)([A-Z])', r'\1_\2', string).lower()


def create_filter(data: dict) -> TFilterOption:
    filter_type = data.get("filterType", None)

    def __get_cls() -> typing.Type[TFilterOption]:
        match filter_type:
            case _FilterType.PRICE_FILTER:
                return PriceFilter
            case _FilterType.PERCENT_PRICE:
                return PercentPriceFilter
            case _FilterType.PERCENT_PRICE_SA:
                return PercentPriceSAFilter
            case _FilterType.PERCENT_PRICE_BY_SIDE:
                return PercentPriceBySideFilter
            case _FilterType.PERCENT_PRICE_INDEX:
                return PercentPriceIndexFilter
            case _FilterType.PERCENT_PRICE_ORDER_SIZE:
                return PercentPriceOrderSizeFilter
            case _FilterType.STATIC_PRICE_RANGE:
                return StaticPriceRangeFilter
            case _FilterType.LOT_SIZE:
                return LotSizeFilter
            case _FilterType.NOTIONAL:
                return NotionalFilter
            case _FilterType.MIN_NOTIONAL:
                return MinNotionalFilter
            case _FilterType.MAX_NUM_ORDERS:
                return MaxNumOrdersFilter
            case _FilterType.MAX_NUM_ALGO_ORDERS:
                return MaxNumAlgoOrdersFilter

        raise ValueError(f"Unsupported filter type: {filter_type or 'None'}")

    data.pop("filterType")
    return __get_cls().create(**{camel_to_snake_case(k): v for k, v in data.items()})
