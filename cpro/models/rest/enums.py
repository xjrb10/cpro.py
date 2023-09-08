from enum import Enum, auto


class AutoStrEnum(str, Enum):
    def _generate_next_value_(self, start, count, last_values):
        if self.startswith("_"):
            return self[1:]
        return self


class AutoLowercaseStrEnum(str, Enum):
    def _generate_next_value_(self, start, count, last_values):
        if self.startswith("_"):
            return self[1:].lower()
        return self.lower()


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
    # Endpoint requires sending a valid Merchant API Key and Merchant signature.
    # todo: SEPARATE THIS, THIS DOES NOT EXIST IN THE API
    MERCHANT = auto()

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


class ExecutionTypes(AutoStrEnum):
    NEW = auto()
    CANCELED = auto()
    REJECTED = auto()
    TRADE = auto()
    EXPIRED = auto()


class OrderSides(AutoStrEnum):
    BUY = auto()
    SELL = auto()


class WSStreamDataEventTypes(Enum):
    AGGREGATE_TRADE = "aggTrade"
    TRADE = "trade"
    KLINE = "kline"
    _24H_MINI_TICKER = "24hrMiniTicker"
    _24H_TICKER = "24hrTicker"
    PARTIAL_BOOK_DEPTH = "depth"
    DIFF_DEPTH = "depthUpdate"


class WSStreamProcedures(AutoStrEnum):
    SUBSCRIBE = auto()
    UNSUBSCRIBE = auto()
    LIST_SUBSCRIPTIONS = auto()


class OrderTypes(AutoStrEnum):
    LIMIT = auto()  # Add: quantity, price

    # MARKET orders using quantity field specifies the amount of the base asset the user wants to buy/sell,
    # E.g. MARKET order on BCHUSDT will specify how much BCH the user is buying/selling.
    # MARKET orders using quoteOrderQty field specifies the amount of the quote asset the user wants to buy/sell,
    # E.g. MARKET order on BCHUSDT will specify how much USDT the user is buying/selling.
    MARKET = auto()  # Add: quantity or quoteOrderQty

    # This will execute a MARKET order when stopPrice is met. Use quantity for selling, quoteOrderQty for buying.
    STOP_LOSS = auto()  # Add: quantity or quoteOrderQty, stopPrice

    # This will execute a LIMIT order when stopPrice is met.
    STOP_LOSS_LIMIT = auto()  # Add: quantity, price, stopPrice

    # This will execute a MARKET order when stopPrice is met. Use quantity for selling, quoteOrderQty for buying.
    TAKE_PROFIT = auto()  # Add: quantity or quoteOrderQty, stopPrice

    # This will execute a LIMIT order when stopPrice is met.
    TAKE_PROFIT_LIMIT = auto()  # Add: quantity, price, stopPrice

    # This is a LIMIT order that will be rejected if the order immediately matches and trades as a taker.
    LIMIT_MAKER = auto()  # Add: quantity, price


class TimeInForce(Enum):
    GOOD_TIL_CANCELLED = "GTC"
    IMMEDIATE_OR_CANCEL = "IOC"
    FILL_OR_KILL = "FOK"


class OrderResponseTypes(AutoStrEnum):
    ACK = auto()
    RESULT = auto()
    FULL = auto()


class AntiSelfTradingBehaviours(Enum):
    # Both orders will be cancelled by match engine
    CANCEL_BOTH = "CB"
    # The new order will be cancelled by match engine
    CANCEL_NEW = "CN"
    # The old order will be cancelled by match engine
    CANCEL_OLD = "CO"


class OrderStatus(AutoStrEnum):
    # The order has been accepted by the engine.
    NEW = auto()

    # A part of the order has been filled.
    PARTIALLY_FILLED = auto()

    # The order has been completed.
    FILLED = auto()

    # A part of the order has been cancelled with self trade.
    PARTIALLY_CANCELED = auto()

    # The order has been canceled by user
    CANCELED = auto()

    # The order has been cancelled by matching-engine: LIMIT FOK order not filled, limit order not fully filled etc
    EXPIRED = auto()


class ExchangeOrderStatus(Enum):
    INIT = 0
    CANCELLED = auto()
    AWAITING_APPROVAL = auto()
    REJECTED = auto()
    PROCESSING = auto()
    FAILURE = auto()
    COMPLETED = auto()


class AccountTransactionStatus(Enum):
    PENDING = auto()
    SUCCESS = auto()
    FAILED = auto()


class PaymentOptions(AutoLowercaseStrEnum):
    COINS_PESO_WALLET = auto()


class DeliveryStatus(AutoStrEnum):
    TODO = auto()
    SUCCESS = auto()
    FAILED = auto()
    PROCESSING = auto()
