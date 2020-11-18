from queue import Queue

from core.concrete_server import ConcreteYggdrasilSessionServer
from core.mux_worker import MuxWorker, MuxJoinThread
from core.yggdrasil import YggdrasilSessionServer


class MuxServer(YggdrasilSessionServer):
    """
    Yggdrasil mux server
    """

    __servers = []

    def __init__(self, server_urls):
        """
        Construct a mux server from several concrete yggdrasil servers.
        :param server_urls: concrete yggdrasil servers.
        """
        self.__servers = [ConcreteYggdrasilSessionServer(url) for url in server_urls]

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

