import logging
from queue import Queue
import requests

from core.mux_worker import MuxWorker, MuxJoinThread
from core.yggdrasil import YggdrasilSessionServer, YggdrasilServerBuilder


class MuxServer(YggdrasilSessionServer):
    """
    Yggdrasil mux server
    """

    __logger = logging.getLogger()
    __servers = []

    def __init__(self, server_urls):
        """
        Construct a mux server from several concrete yggdrasil servers.
        :param server_urls: concrete yggdrasil servers.
        """
        self.__servers = [YggdrasilServerBuilder.from_root_url(url) for url in server_urls]
        unofficial_servers = filter(
            lambda url: not url.startswith('http://sessionserver.mojang.com')
                        and not url.startswith('https://sessionserver.mojang.com')
            , server_urls)
        try:
            self.__root_request_target_server = unofficial_servers.__next__()
            self.__root_response_cache = None
        except StopIteration:
            self.__root_request_target_server = None
            self.__logger.warning('No applicable authserver to offer root response. '
                                  'Any request to root will get 404 response.')
            self.__root_response_cache = 404

    def hasJoined(self, form) -> (str, int):

        # For all sub servers, we create request threads for every one of them,
        # in order to eliminate unnecessary wait, and finally speed up the joining progress.
        queue = Queue()
        workers = [MuxWorker(queue, server, form) for server in self.__servers]
        for worker in workers:
            worker.start()
        join_thread = MuxJoinThread(queue, workers, default_response=('', 204))
        join_thread.start()
        response, code = queue.get(block=True)
        for worker in workers:
            worker.cancel()
        # self.__logger.info(f'Mux make response {response} with code {code} to client.')
        return response, code
        # self.__logger.info(f'Mux make empty response with code 204 to the client.')
        # # Default response: have not joined in any server.
        # return '', 204

    def get_root(self) -> (str, int):
        """
        Perform GET request on root.
        :return:
        """
        if self.__root_response_cache == 404:
            return '', 404
        elif self.__root_response_cache:
            return self.__root_response_cache, 200
        # make request
        req = requests.get(self.__root_request_target_server)
        # update cache
        if req.status_code == 200:
            self.__root_response_cache = req.text
        return req.text, req.status_code
