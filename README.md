# cpro.py 🐍

Clear and concise CoinsPro API library written in Python for coins.ph

### Features / TO-DO:

- [X] Blocking / synchronous & AsyncIO Compatible
- [X] Full HMAC Authentication
- [X] Full implementation of API data models & enums
- [X] Type-hinted
- [X] Minimal Third-party Dependencies ( `dataclasses-json`, `aiohttp` (optional) )
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
        - [ ] Wallet Endpoints:
            - [X] [Get All Coins' Information](https://coins-docs.github.io/rest-api/#all-coins-information-user_data)
            - [X] [Get Deposit Address](https://coins-docs.github.io/rest-api/#deposit-address-user_data)
            - [ ] [Initiate Withdrawal](https://coins-docs.github.io/rest-api/#withdrawuser_data) (TODO)
            - [X] [Get Deposit History](https://coins-docs.github.io/rest-api/#deposit-history-user_data)
            - [X] [Get Withdraw History](https://coins-docs.github.io/rest-api/#withdraw-history-user_data)
        - [ ] Account endpoints:
            - [ ] [Test New Order](https://coins-docs.github.io/rest-api/#test-new-order-trade) (TODO)
            - [ ] [New Order](https://coins-docs.github.io/rest-api/#new-order--trade) (TODO)
            - [ ] [Query Order](https://coins-docs.github.io/rest-api/#query-order-user_data) (TODO)
            - [ ] [Cancel Order](https://coins-docs.github.io/rest-api/#cancel-order-trade) (TODO)
            - [ ] [Cancel All Open Orders on a Symbol](https://coins-docs.github.io/rest-api/#cancel-all-open-orders-on-a-symbol-trade) (
              TODO)
            - [ ] [Get Current Open Orders](https://coins-docs.github.io/rest-api/#current-open-orders-user_data) (TODO)
            - [ ] [Get Order History](https://coins-docs.github.io/rest-api/#history-orders-user_data) (TODO)
            - [ ] [Get Account Information](https://coins-docs.github.io/rest-api/#account-information-user_data) (TODO)
            - [ ] [Get Account Trade List](https://coins-docs.github.io/rest-api/#account-trade-list-user_data) (TODO)
            - [ ] [Withdraw (To Coins.ph Account)](https://coins-docs.github.io/rest-api/#withdraw-to-coins_ph-account-user_data) (
              TODO)
            - [ ] Deposit (to xyz account) (does not exist)
            - [ ] [Get Withdraw Order History (withdrawal order which withdraw from exchange to coins_ph)](https://coins-docs.github.io/rest-api/#withdraw-order-history-withdrawal-order-which-withdraw-from-exchange-to-coins_ph-user_data) (
              TODO: explain yourself 😃)
            - [ ] [Get Deposit order history(deposit order which deposit from coins_ph to exchange)](https://coins-docs.github.io/rest-api/#deposit-order-historydeposit-order-which-deposit-from-coins_ph-to-exchange-user_data) (
              TODO: explain yourself 😃)
            - [ ] [Get Trade Fee](https://coins-docs.github.io/rest-api/#trade-fee-user_data) (TODO)
            - [ ] [Request a Payment](https://coins-docs.github.io/rest-api/#payment-request-user_data) (TODO)
    - [X] API Key Authenticated:
        - [ ] [User Data Event Stream](https://coins-docs.github.io/user-data-stream/):
            - [ ] [Start Streaming](https://coins-docs.github.io/rest-api/#start-user-data-stream-user_stream) (TODO)
            - [ ] [Stream KeepAlive](https://coins-docs.github.io/rest-api/#keepalive-user-data-stream-user_stream) (
              TODO)
            - [ ] [Close Stream](https://coins-docs.github.io/rest-api/#close-user-data-stream-user_stream) (TODO)
            - [ ] [Payloads](https://coins-docs.github.io/user-data-stream/#web-socket-payloads):
                - [ ] [Account Update Payload](https://coins-docs.github.io/user-data-stream/#account-update) (TODO)
                - [ ] [Balance Update Payload](https://coins-docs.github.io/user-data-stream/#balance-update) (TODO)
                - [ ] [Order Update Payload](https://coins-docs.github.io/user-data-stream/#order-update) (TODO)
- [ ] **WebSocket Listener:**
    - [ ] not even going to list for now 🤦‍♂️ (TODO: lol)

### Quirks:

For precision purposes, we store decimals as `marshmallow.fields.Decimal` objects, this is to prevent any inherent
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
from cpro.models.rest.endpoints import APIEndpoints

credentials = APICredentials(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# blocking/non-async example:
client = BlockingHTTPClient(credentials)
response = APIEndpoints.GET_ALL_USER_COINS.execute(client, CoinsInformationRequest())

# non-blocking/async example:
async_client = AsyncIOHTTPClient(credentials)
response = await APIEndpoints.GET_ALL_USER_COINS.execute_async(client, CoinsInformationRequest())
# diff:    ^^^^^                                        ^^^^^^

# >>> response: CoinsInformationResponse(coins=[Coin(coin='PHP', name='PHP', ... )])
```

### Development

NOTE: Guide assumes you have the repository locally cloned.

**Running tests:**

1. **Install required test dependencies:**
   > `pip install -e ".[test]"`
2. **Create a `./tests/.env` file with your API key and secret, example in [`./tests/.env.example`](/tests/.env.example)
   **
3. **Run unit tests**
   > `python -m pytest`

---

Made as a submission for **[Coins.ph Hackathon 2023](https://coins.ph/blog/join-the-coins-ph-hackathon/)** ❤️

**Project start:** August 9, 2023