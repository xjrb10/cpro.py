from enum import Enum, auto


class AutoStrEnum(str, Enum):
    def _generate_next_value_(self, start, count, last_values):
        if self.startswith("_"):
            return self[1:]
        return self


class SymbolStatus(AutoStrEnum):
    # https://coins-docs.github.io/rest-api/#enum-definitions
    TRADING = auto()
    BREAK = auto()
    CANCEL_ONLY = auto()


class OrderType(AutoStrEnum):
    # https://coins-docs.github.io/rest-api/#enum-definitions
    LIMIT = auto()
    MARKET = auto()
    LIMIT_MAKER = auto()
    STOP_LOSS_LIMIT = auto()
    STOP_LOSS = auto()
    TAKE_PROFIT_LIMIT = auto()
    TAKE_PROFIT = auto()


class _FilterType(AutoStrEnum):
    # https://coins-docs.github.io/rest-api/#symbol-filters
    PRICE_FILTER = auto()
    PERCENT_PRICE = auto()
    PERCENT_PRICE_SA = auto()
    PERCENT_PRICE_BY_SIDE = auto()
    PERCENT_PRICE_INDEX = auto()
    PERCENT_PRICE_ORDER_SIZE = auto()
    STATIC_PRICE_RANGE = auto()
    LOT_SIZE = auto()
    NOTIONAL = auto()
    MIN_NOTIONAL = auto()
    MAX_NUM_ORDERS = auto()
    MAX_NUM_ALGO_ORDERS = auto()


class SecurityType(AutoStrEnum):
    # https://coins-docs.github.io/rest-api/#endpoint-security-type

    # Endpoint can be accessed freely.
    NONE = auto()
    # Endpoint requires sending a valid API Key and signature.
    TRADE = auto()
    # Endpoint requires sending a valid API Key and signature.
    USER_DATA = auto()
    # Endpoint requires sending a valid API Key.
    USER_STREAM = auto()
    # Endpoint requires sending a valid API Key.
    MARKET_DATA = auto()

    def is_signed(self) -> bool:
        return self in (SecurityType.TRADE, SecurityType.USER_DATA)


class DepositStatus(Enum):
    PROCESSING = 0
    SUCCESS = auto()
    FAILED = auto()
    NEED_FILL_DATA = auto()


class WithdrawStatus(Enum):
    PROCESSING = 0
    SUCCESS = auto()
    FAILED = auto()


class ChartIntervals(AutoStrEnum):
    _1m = auto()
    _3m = auto()
    _5m = auto()
    _15m = auto()
    _30m = auto()
    _1h = auto()
    _2h = auto()
    _4h = auto()
    _6h = auto()
    _8h = auto()
    _12h = auto()
    _1d = auto()
    _3d = auto()
    _1w = auto()
    _1M = auto()
