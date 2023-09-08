# cpro.py 🐍

Clear and concise CoinsPro API library written in Python for coins.ph

### Features / TO-DO:

- [X] Blocking / synchronous & AsyncIO Compatible
- [X] Full HMAC Authentication
- [X] Full implementation of API data models & enums
- [X] Type-hinted
- [X] Minimal Third-party Dependencies ( `dataclasses-json`, `aiohttp` )
- [X] **REST Endpoints:**
    - [X] Un-authenticated:
        - [X] General:
            - [X] [Ping](https://coins-docs.github.io/rest-api/#test-connectivity)
            - [X] [Get Server Time](https://coins-docs.github.io/rest-api/#check-server-time)
            - [X] [Get Exchange Information](https://coins-docs.github.io/rest-api/#exchange-information)
        - [X] Market Info:
            - [X] [Get Order Book](https://coins-docs.github.io/rest-api/#order-book)
            - [X] [Get Recent Trades](https://coins-docs.github.io/rest-api/#recent-trades-list)
            - [X] [Get Kline/Candlestick Data](https://coins-docs.github.io/rest-api/#klinecandlestick-data)
            - [X] [Get 24hr Ticker Price Change Statistics](https://coins-docs.github.io/rest-api/#24hr-ticker-price-change-statistics)
            - [X] [Get Symbol Price Ticker](https://coins-docs.github.io/rest-api/#symbol-order-book-ticker)
            - [X] [Get Symbol Order Book Ticker](https://coins-docs.github.io/rest-api/#symbol-order-book-ticker)
            - [X] [Get Current Average Price](https://coins-docs.github.io/rest-api/#current-average-price)
            - [X] [Get CryptoAsset Trading Pairs](https://coins-docs.github.io/rest-api/#cryptoasset-trading-pairs)
    - [X] HMAC Authenticated:
        - [X] Wallet Endpoints:
            - [X] [Get All Coins' Information](https://coins-docs.github.io/rest-api/#all-coins-information-user_data)
            - [X] [Get Deposit Address](https://coins-docs.github.io/rest-api/#deposit-address-user_data)
            - [X] [Initiate Withdrawal](https://coins-docs.github.io/rest-api/#withdrawuser_data)
            - [X] [Get Deposit History](https://coins-docs.github.io/rest-api/#deposit-history-user_data)
            - [X] [Get Withdraw History](https://coins-docs.github.io/rest-api/#withdraw-history-user_data)
        - [X] Account endpoints:
            - [X] [Test New Order](https://coins-docs.github.io/rest-api/#test-new-order-trade)
            - [X] [New Order](https://coins-docs.github.io/rest-api/#new-order--trade)
            - [X] [Query Order](https://coins-docs.github.io/rest-api/#query-order-user_data)
            - [X] [Cancel Order](https://coins-docs.github.io/rest-api/#cancel-order-trade)
            - [X] [Cancel All Open Orders on a Symbol](https://coins-docs.github.io/rest-api/#cancel-all-open-orders-on-a-symbol-trade)
            - [X] [Get Current Open Orders](https://coins-docs.github.io/rest-api/#current-open-orders-user_data)
            - [X] [Get Order History](https://coins-docs.github.io/rest-api/#history-orders-user_data)
            - [X] [Get Account Information](https://coins-docs.github.io/rest-api/#account-information-user_data)
            - [X] [Get Account Trade List](https://coins-docs.github.io/rest-api/#account-trade-list-user_data)
            - [X] [Withdraw (To Coins.ph Account)](https://coins-docs.github.io/rest-api/#withdraw-to-coins_ph-account-user_data)
            - [X] [Get Deposit order history(deposit order which deposit from coins_ph to exchange)](https://coins-docs.github.io/rest-api/#deposit-order-historydeposit-order-which-deposit-from-coins_ph-to-exchange-user_data)
            - [X] [Get Withdraw Order History (withdrawal order which withdraw from exchange to coins_ph)](https://coins-docs.github.io/rest-api/#withdraw-order-history-withdrawal-order-which-withdraw-from-exchange-to-coins_ph-user_data)
            - [X] [Get Trade Fee](https://coins-docs.github.io/rest-api/#trade-fee-user_data)
            - [X] [Request a Payment](https://coins-docs.github.io/rest-api/#payment-request-user_data)
            - [X] [Get Payment Request](https://coins-docs.github.io/rest-api/#get-payment-request)
            - [X] [Cancel payment request](https://coins-docs.github.io/rest-api/#cancel-payment-request)
            - [X] [Send reminder for payment request](https://coins-docs.github.io/rest-api/#send-reminder-for-payment-request)
    - [X] API Key Authenticated:
        - [X] [User Data Event Stream](https://coins-docs.github.io/user-data-stream/):
            - [X] [Start Streaming](https://coins-docs.github.io/rest-api/#start-user-data-stream-user_stream)
            - [X] [Stream KeepAlive](https://coins-docs.github.io/rest-api/#keepalive-user-data-stream-user_stream)
            - [X] [Close Stream](https://coins-docs.github.io/rest-api/#close-user-data-stream-user_stream)
        - [X] [Merchant Endpoints](https://coins-docs.github.io/rest-api/#merchant-endpoints)
          - [X] [Creating Invoices](https://coins-docs.github.io/rest-api/#creating-invoices)
          - [X] [Retrieving Invoices](https://coins-docs.github.io/rest-api/#retrieving-invoices)
          - [X] [Canceling Invoices](https://coins-docs.github.io/rest-api/#canceling-invoices)
        - [X] [Convert endpoints](https://coins-docs.github.io/rest-api/#convert-endpoints)
          - [X] [Get supported trading pairs](https://coins-docs.github.io/rest-api/#get-supported-trading-pairs)
          - [X] [Fetch a quote](https://coins-docs.github.io/rest-api/#fetch-a-quote)
          - [X] [Accept the quote](https://coins-docs.github.io/rest-api/#accept-the-quote)
        - [X] [Fiat endpoints](https://coins-docs.github.io/rest-api/#fiat-endpoints)
          - [X] [Get supported fiat channels](https://coins-docs.github.io/rest-api/#get-supported-fiat-channels)
          - [X] [Cash out](https://coins-docs.github.io/rest-api/#cash-out)
          - [X] [Fiat order detail](https://coins-docs.github.io/rest-api/#fiat-order-detail)
          - [X] [Fiat order history](https://coins-docs.github.io/rest-api/#fiat-order-history)
- [X] **WebSocket Stream:**
    - [X] Client
    - [X] Data Models:
      - [X] [Aggregate Trade Streams](https://coins-docs.github.io/web-socket-streams/#aggregate-trade-streams)
      - [X] [Trade Streams](https://coins-docs.github.io/web-socket-streams/#trade-streams)
      - [X] [Kline/Candlestick Streams](https://coins-docs.github.io/web-socket-streams/#klinecandlestick-streams)
      - [X] [Individual Symbol Mini Ticker Stream](https://coins-docs.github.io/web-socket-streams/#individual-symbol-mini-ticker-stream)
      - [X] [Individual Symbol Ticker Streams](https://coins-docs.github.io/web-socket-streams/#individual-symbol-ticker-streams)
      - [X] [Individual Symbol Book Ticker Streams](https://coins-docs.github.io/web-socket-streams/#individual-symbol-book-ticker-streams)
      - [X] [Partial Book Depth Streams](https://coins-docs.github.io/web-socket-streams/#partial-book-depth-streams)
      - [X] [Diff. Depth Stream](https://coins-docs.github.io/web-socket-streams/#diff-depth-stream)
- [X] **User Data Event Stream:**
    - [X] Asyncio Client
    - [X] Blocking Client
    - [X] Data Models:
      - [X] [Account Update](https://coins-docs.github.io/user-data-stream/#account-update)
      - [X] [Balance Update](https://coins-docs.github.io/user-data-stream/#balance-update)
      - [X] [Order Update](https://coins-docs.github.io/user-data-stream/#order-update)

### Quirks:

For precision purposes, we store decimals as python standard `Decimal` objects, this is to prevent any inherent
rounding errors. These `Decimal` objects should then be cast into a `float` or an `int` in order to do arithmetic 
operations.

### Not Implemented:

- Rate limit management
- Enums for symbols (would require frequent updates)

## Example Usage:

```py
import os

from cpro.client.rest import BlockingHTTPClient, AsyncIOHTTPClient, APICredentials
from cpro.models.rest.request import CoinsInformationRequest
from cpro.models.rest.response import CoinsInformationResponse
from cpro.models.rest.endpoints import APIEndpoints

credentials = APICredentials(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# blocking/non-async example:
client = BlockingHTTPClient(credentials)
response: CoinsInformationResponse = APIEndpoints.GET_ALL_USER_COINS.execute(
    client,
    CoinsInformationRequest()
)

# non-blocking/async example:
async_client = AsyncIOHTTPClient(credentials)
response: CoinsInformationResponse = await APIEndpoints.GET_ALL_USER_COINS.execute_async(
# diff:                              ^^^^^                                        ^^^^^^
    client,
    CoinsInformationRequest()
)

# >>> response: CoinsInformationResponse(coins=[Coin(coin='PHP', name='PHP', ... )])
```

### Development

NOTE: Guide assumes you have the repository locally cloned.

**Running tests:**

1. **Install required test dependencies:**
   > `pip install -e "cpro.py[test]"`
2. **Create a `./tests/.env` file with your API key and secret, example in [`./tests/.env.example`](/tests/.env.example)
   **
3. **Run unit tests**
   > `python -m pytest`

---

Made as a submission for **[Coins.ph Hackathon 2023](https://coins.ph/blog/join-the-coins-ph-hackathon/)** ❤️

**Project start:** August 9, 2023