import json
import os

from cpro.client.rest import APIRequests, BlockingHTTPClient
from cpro.models.rest.request import APICredentials, CoinsInformationRequest, DepositAddressRequest, DepositHistoryRequest, \
    WithdrawHistoryRequest

client = BlockingHTTPClient(APICredentials(
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
))


def test_get_all_coins():
    print(APIRequests.GET_ALL_USER_COINS.execute(client, CoinsInformationRequest()))


def test_get_eth_address():
    print(json.dumps(APIRequests.GET_DEPOSIT_ADDRESS.execute(client, DepositAddressRequest(
        coin="ETH",
        network="ETH"
    )).to_dict(), indent=2))


def test_get_deposit_history():
    print(json.dumps(
        APIRequests.GET_DEPOSIT_HISTORY.execute(client, DepositHistoryRequest(coin="ETH")).to_dict(),
        indent=2
    ))


def test_get_withdraw_history():
    print(json.dumps(
        APIRequests.GET_WITHDRAW_HISTORY.execute(client, WithdrawHistoryRequest(coin="ETH")).to_dict(),
        indent=2
    ))
