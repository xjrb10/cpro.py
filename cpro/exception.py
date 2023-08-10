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
