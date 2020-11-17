import uuid


def form_authenticate(username: str, password: str, clientToken: str = None, requestUser: bool = False) -> dict:
    if not clientToken:
        clientToken = uuid.uuid1().hex
    return {
        "username": username,
        "password": password,
        "clientToken": clientToken,
        "requestUser": requestUser,
        "agent": {
            "name": "Minecraft",
            "version": 1
        }
    }
