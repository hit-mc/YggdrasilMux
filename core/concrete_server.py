from core.yggdrasil import YggdrasilSessionServer
import requests
import json
import logging


class ConcreteYggdrasilSessionServer(YggdrasilSessionServer):

    def __init__(self, server_url: str):
        if not server_url.endswith('/'):
            server_url += '/'
        self._server_url = server_url
        self._logger.setLevel(logging.DEBUG)

    def __str__(self):
        return self.get_server_url()

    def join(self, form) -> (str, int):
        return self._form_request(self._url_join(), form)

    def hasJoined(self, form) -> (str, int):
        return self._form_request(self._url_has_joined(), form)

    def profile(self, form) -> (str, int):
        return self._form_request(self._url_profile(), form)

    def get_server_url(self) -> str:
        return self._server_url

    def _url_has_joined(self):
        return self._server_url + 'session/minecraft/hasJoined'

    def _url_join(self):
        return self._server_url + 'session/minecraft/join'

    def _url_profile(self):
        return self._server_url + 'session/minecraft/profile'

    def _form_request(self, url, form, method='GET') -> (str, int):

        method = method.upper()
        self._logger.debug(f'Make request with form {json.dumps(form)}')
        if method == 'GET':
            r = requests.get(url, params=form)
        elif method == 'POST':
            r = requests.post(url, data=json.dumps(form), headers={'Content-Type': 'application/json'})
        else:
            raise ValueError(f'Unsupported method {method}')
        self._logger.debug(f'Form request returns ({r.text}, {r.status_code})')
        return r.text, r.status_code
