import sys
import logging

from tornado.tcpserver import TCPServer

from packet import InPacket, OutPacket, PacketStructureError


class TCPConsoleServer(TCPServer):
    cls_handler = None

    def __init__(self, *args, **kwargs):
        self.handler = self.cls_handler(kwargs.pop('user_data'), self)
        super().__init__(*args, **kwargs)

    def handle_stream(self, stream, address):
        StreamReader(stream, address, self)

    def dispatch(self, stream_r, method, data, request_id):
        self.handler.route(stream_r, method, data, request_id)


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
