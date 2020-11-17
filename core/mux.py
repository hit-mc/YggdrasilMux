from core.concrete_server import ConcreteYggdrasilSessionServer
from core.yggdrasil import YggdrasilSessionServer
from logging import getLogger


class MuxServer(YggdrasilSessionServer):
    """
    Yggdrasil mux server
    """

    __servers = []
    __logger = getLogger(__name__)

    def __init__(self, server_urls):
        """
        Construct a mux server from several concrete yggdrasil servers.
        :param server_urls: concrete yggdrasil servers.
        """
        self.__servers = [ConcreteYggdrasilSessionServer(url) for url in server_urls]

    def hasJoined(self, form) -> (str, int):
        for server in self.__servers:
            assert isinstance(server, YggdrasilSessionServer)
            retry_counter = 5
            while retry_counter:
                retry_counter -= 1
                try:
                    response, code = server.hasJoined(form)
                    if code == 200 and response:
                        self.__logger.debug(f'Relay response {response} with code 200 from server {server}.')
                        return code, response  # User has joined in this server.
                    elif code == 204:
                        break  # Valid response. User has not joined in this server. Try next server.
                    else:
                        self.__logger.warning(f'Server {server} sent an '
                                              f'invalid response with payload {form}: '
                                              f'code={code}, response={response}. Retry.')
                    # Otherwise the request has failed. Try again.
                except Exception as e:
                    self.__logger.warning(f'An exception occurred while querying server {server}: {e}.')
                    # Request to this has failed. Try again.
            if not retry_counter:
                # Max retry times reached. Skip this server.
                self.__logger.error(f'Request to server {server} '
                                    f'failed too many times. Skip this server.')
        self.__logger.debug(f'Mux make empty response with code 204 to the client.')
        # Default response: have not joined in any server.
        return '', 204
