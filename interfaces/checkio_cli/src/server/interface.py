import os
import sys
import logging

from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop

from .packet import InPacket, OutPacket, PacketStructureError


class TCPConsoleInterfaceServer(TCPServer):

    USER_DATA = None
    ROUTING = {
        InPacket.METHOD_SELECT: 'handler_select',
        InPacket.METHOD_STDOUT: 'handler_stdout',
        InPacket.METHOD_STDERR: 'handler_stderr',
        InPacket.METHOD_RESULT: 'handler_result',
        InPacket.METHOD_ERROR: 'handler_error',
        InPacket.METHOD_STATUS: 'handler_status',
        InPacket.METHOD_SET: 'handler_set',
        'pre_test': 'handler_pre_test'
    }

    def __init__(self, *args, **kwargs):
        self.USER_DATA = kwargs.pop('user_data')
        super().__init__(*args, **kwargs)

    def handle_stream(self, stream, address):
        StreamReader(stream, address, self)

    def dispatch(self, stream_r, method, data, request_id):
        if method not in self.ROUTING:
            return
        handler = getattr(self, self.ROUTING[method])
        handler(data, request_id, stream_r)

    def handler_select(self, data, request_id, stream_r):
        result = {}
        for item in data:
            if item not in self.USER_DATA.keys():
                continue
            result[item] = self.USER_DATA[item]
        stream_r.write_select_result(result, request_id)

    def handler_pre_test(self, data, request_id, stream_r):
        logging.debug("checkio-cli server:: pre_test: {}".format(data))

    def handler_stdout(self, line, request_id, stream_r):
        logging.debug("checkio-cli server:: stdout: {}".format(line))

    def handler_stderr(self, line, request_id, stream_r):
        logging.debug("checkio-cli server:: stderr: {}".format(line))

    def handler_result(self, data, request_id, stream_r):
        logging.debug("checkio-cli server:: result: {}".format(data))

    def handler_error(self, data, request_id, stream_r):
        logging.debug("checkio-cli server:: error: {}".format(data))

    def handler_status(self, data, request_id, stream_r):
        logging.debug("checkio-cli server:: status: {}".format(data))


    def handler_set(self, data, request_id, stream_r):
        logging.debug("checkio-cli server:: set: {}".format(data))


class StreamReader(object):

    terminator = b'\n'

    def __init__(self, stream, address, server):
        self.stream = stream
        self.address = address
        self.server = server
        self.stream.set_close_callback(self._on_client_connection_close)
        self._read_data()

    def _on_client_connection_close(self):
        sys.exit(0)

    def _read_data(self):
        self.stream.read_until(self.terminator, self._on_data)

    def _on_data(self, data):
        data = data.decode('utf-8')
        logging.debug("checkio-cli server:: received: {}".format(data))
        if data is None:
            logging.error("Client sent an empty data: {}".format(self.address), exc_info=True)
        else:
            try:
                packet = InPacket.decode(data)
            except PacketStructureError as e:
                logging.error(e, exc_info=True)
            else:
                self.server.dispatch(self, **packet.get_all_data())
        self._read_data()

    def write(self, method, data=None, request_id=None, callback=None):
        if self.stream.closed():
            raise Exception('Connection is closed')

        message = OutPacket(method, data, request_id).encode()
        try:
            self.stream.write(message.encode('utf-8') + self.terminator, callback=callback)
            logging.debug("checkio-cli server:: write {}".format(message))
        except Exception as e:
            logging.error(e, exc_info=True)

    def write_select_result(self, result, request_id):
        self.write(OutPacket.METHOD_SELECT_RESULT, result, request_id=request_id)

def sys_start(csl_server=TCPConsoleInterfaceServer):
    (_, slug, action, env_name, code_path, port, log_level) = sys.argv
    logging.getLogger().setLevel(int(log_level))
    io_loop = IOLoop.instance()
    server = csl_server(io_loop=io_loop, user_data={
        'action': action,
        'code': open(code_path).read(),
        'env_name': env_name
    })
    server.listen(port)
    logging.info('START INTERFACE')
    io_loop.start()
