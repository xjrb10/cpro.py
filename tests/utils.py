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

from cpro.client.rest import HTTPClient, AsyncIOHTTPClient
from cpro.models.rest.endpoints import APIEndpoints
from cpro.models.rest.response import TResponsePayload


async def _test_endpoint(client: HTTPClient, endpoint: APIEndpoints, *args, **kwargs) -> TResponsePayload:
    return await endpoint.execute_async(client, *args, **kwargs) \
        if isinstance(client, AsyncIOHTTPClient) else \
        endpoint.execute(client, *args, **kwargs)
