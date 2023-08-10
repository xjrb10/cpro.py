from cpro.models.rest.request import EncodedPayload


def test_hmac():
    payload = EncodedPayload(
        raw_params={
            "symbol": "ETHBTC",
            "side": "BUY",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": 1,
            "price": 0.1,
            "recvWindow": 5000,
            "timestamp": 1538323200000,
        }
    )
    signed = payload.sign(
        api_key="tAQfOrPIZAhym0qHISRt8EFvxPemdBm5j5WMlkm3Ke9aFp0EGWC2CGM8GHV4kCYW",
        api_secret="lH3ELTNiFxCQTmi9pPcWWikhsjO04Yoqw3euoHUuOLC3GYBW64ZqzQsiOEHXQS76",
    )
    assert "signature" in signed.params
    assert signed.raw_params["signature"].lower() == "5f2750ad7589d1d40757a55342e621a44037dad23b5128cc70e18ec1d1c3f4c6"
