import logging

from packet import InPacket


class BaseHandler(object):
    ROUTING = {
        InPacket.METHOD_SELECT: 'handler_select',
        InPacket.METHOD_STDOUT: 'handler_stdout',
        InPacket.METHOD_STDERR: 'handler_stderr',
        InPacket.METHOD_RESULT: 'handler_result',
        InPacket.METHOD_ERROR: 'handler_error',
        InPacket.METHOD_STATUS: 'handler_status',
        InPacket.METHOD_SET: 'handler_set',
        InPacket.METHOD_PRE_TEST: 'handler_pre_test'
    }

    def __init__(self, user_data, server):
        self.server = server
        self.user_data = user_data
        self.user_data['code'] = self.get_code(user_data['code_path'])

    def get_code(self, code_path):
        code = open(code_path).read()
        if code[0:2] == '#!':
            lines = code.split('\n')
            code = '\n'.join([''] + lines[1:])
        return code

    def route(self, stream_r, method, data, request_id):
        if method not in self.ROUTING:
            return
        handler = getattr(self, self.ROUTING[method])
        handler(data, request_id, stream_r)

    def handler_select(self, data, request_id, stream_r):
        result = {}
        for item in data:
            if item not in self.user_data.keys():
                continue
            result[item] = self.user_data[item]
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
        return ''
