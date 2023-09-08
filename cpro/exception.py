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

import json


class CProException(Exception):
    pass


class HTTPException(CProException):
    def __init__(self, body: str, headers: dict, status: int):
        self.body = body
        self.headers = headers
        self.status = status
        super().__init__(f"Received code {status}: {body}\n\nResponse Headers: {json.dumps(headers, indent=2)}")


class CoinsAPIException(CProException):
    def __init__(self, code: str, message: dict):
        self.code = code
        self.message = message
        super().__init__(f"Received code {code}: {message}")
