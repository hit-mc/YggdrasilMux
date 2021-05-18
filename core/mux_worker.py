import logging
import time
from queue import Queue
from threading import Thread

from core.yggdrasil import YggdrasilSessionServer


class MuxWorker(Thread):

    def __init__(self, queue: Queue, server, form, max_retry_times=3):
        super().__init__()
        self.__queue = queue
        self.__run = True
        self.__max_retry = max_retry_times
        self.__server = server
        self.__form = form
        if self.__max_retry <= 0:
            raise ValueError('Invalid max retry times')

    def cancel(self):
        self.__run = False

    def reset(self):
        self.__run = True

    def run(self) -> None:
        counter = self.__max_retry
        server = self.__server
        form = self.__form
        assert isinstance(server, YggdrasilSessionServer)

        while self.__run and counter:
            counter -= 1
            try:
                logging.debug(f'Invoke hasJoined of server {server}.')
                start_time = time.time()
                response, code = server.hasJoined(form)
                end_time = time.time()
                if end_time - start_time >= 1:
                    logging.warning(f'Request hasJoined to server {server} took {round((end_time - start_time) * 1000, 2)}ms!')
                if code == 200 and response:
                    if self.__run:  # success
                        logging.info(f'Server {server} returned a valid response: {response}.')
                        self.__queue.put((response, code))  # User has joined in this server.
                    return
                elif code == 204:
                    logging.info(f'Server {server} returned 204, user has not joined in.')
                    return  # Valid response. User has not joined in this server. Try next server.
                else:
                    logging.warning(f'Server {server} sent an '
                                         f'invalid response with payload {form}: '
                                         f'code={code}, response={response}. Retry.')
                # Otherwise the request has failed. Try again.
            except IOError as e:
                logging.warning(f'An exception occurred while querying server {server}: {e}.')
                # Request to this has failed. Try again.
            time.sleep(1)  # cool down
        # Max retry times reached. Skip this server.
        logging.error(f'Request to server {server} '
                           f'failed too many times. Skip this server.')


class MuxJoinThread(Thread):

    def __init__(self, queue: Queue, servers: list, default_response):
        super().__init__()
        self.__queue = queue
        self.__servers = servers
        self.__default = default_response

    def run(self) -> None:
        for server in self.__servers:
            try:
                if isinstance(server, Thread):
                    server.join()
            except Exception:
                pass
        self.__queue.put(self.__default)
