from cpro.client.rest import HTTPClient, APIRequests, AsyncIOHTTPClient
from cpro.models.rest.response import TResponsePayload


async def _test_endpoint(client: HTTPClient, endpoint: APIRequests, *args, **kwargs) -> TResponsePayload:
    return await endpoint.execute_async(client, *args, **kwargs) \
        if isinstance(client, AsyncIOHTTPClient) else \
        endpoint.execute(client, *args, **kwargs)
