import asyncio
import zlib
import re
import time

from project_path import PROJECT_PATH
import sys

sys.path.insert(0, PROJECT_PATH)

from server.utils.utils import convert
from server.utils.common import *
from server.base.descriptors import ServerVerifier

from server.manager import manager as server_manager

import logging
from server.log.log_decor import log
from server.log.log_config import logger_name

logger = logging.getLogger(logger_name)


class Server(metaclass=ServerVerifier):
    clients = dict()
    requests = dict()

    def __init__(self, host=HOST, port=PORT, que=QUE):
        self.host = host
        self.port = port
        self.que = que

        self.loop = asyncio.get_event_loop()
        self.server = asyncio.start_server(self.client_connected,
                                           host=self.host,
                                           port=self.port,
                                           loop=self.loop,
                                           limit=self.que)

    @log(logger)
    async def client_connected(self, client_reader, client_writer):
        client_sock = client_writer.get_extra_info('socket')
        print('=================>\nconnected-->', client_sock.getpeername())
        while True:
            z_bytes = await client_reader.read(SIZE)
            byte_request = zlib.decompress(z_bytes)
            print('from {}: {}'.format(client_sock.getpeername(), convert(byte_request)))
            name = self.make_clients(client_sock, byte_request)
            if name:
                print('connected user\'s name:', name)
                logger.info('Client {} connected, address {}'.format(name, client_sock.getpeername()))
            # making self.requests dict
            self.get_requests(client_sock, byte_request)
            print('requests-->', self.requests)
            print('clients-->', self.clients)
            try:
                requests = self.requests.get(client_sock)
                for byte_request in requests:
                    logger.info('request from {}: {}'.format(client_sock.getpeername(), convert(byte_request)))
                    list_responses = server_manager(byte_request)
                    if list_responses:
                        for response in list_responses:
                            print('response-->', response)
                            byte_response = convert(response)
                            z_bytes = zlib.compress(byte_response)
                            if 'message' in response:
                                if response.get('to').startswith('#'):
                                    for client in self.clients.values():
                                        try:
                                            print('common sending to-->', client.getpeername())
                                            client.send(z_bytes)
                                        except OSError:
                                            pass
                                else:
                                    try:
                                        self.clients.get(response.get('account_name')).send(z_bytes)
                                        print('private sending to-->',
                                              self.clients.get(response.get('to')).getpeername())
                                        self.clients.get(response.get('to')).send(z_bytes)
                                    except (OSError, AttributeError):
                                        print(response.get('to'), 'offline')
                                        logger.info(
                                            'Client {} offline, message {} not delivered'.format(response.get('to'),
                                                                                                 response.get(
                                                                                                     'message')))
                                        pass
                            else:
                                print('sending to-->', client_sock.getpeername(), end=': ')
                                asyncio.sleep(0.01)
                                client_writer.write(z_bytes)
                                print(convert(zlib.decompress(z_bytes)))
            except KeyError:
                pass
            # except ConnectionResetError:
            #     continue

    def make_clients(self, client_sock, byte_request):
        user = convert(byte_request).get('user')
        try:
            name = user.get('account_name')
            if name:
                self.clients.update({name: client_sock})
                return name
        except AttributeError:
            pass

    def get_requests(self, client_sock, byte_request):
        re_request = re.findall(PATTERN, byte_request.decode(CODING))
        self.requests[client_sock] = [req.encode(CODING) for req in [r[0] for r in re_request]]

    def mainloop(self):
        print('server starts at', self.host, self.port)
        self.server = self.loop.run_until_complete(self.server)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()


if __name__ == '__main__':
    server = Server().mainloop()
