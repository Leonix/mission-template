from .interface import TCPConsoleInterfaceServer

class SimplePrintInterface(TCPConsoleInterfaceServer):
    def handler_pre_test(self, data, request_id, stream_r):
        super().handler_pre_test(data, request_id, stream_r)
        print('TEST: {}'.format(data['representation']))

    def handler_result(self, data, request_id, stream_r):
        super().handler_result(data, request_id, stream_r)
        if data['success']:
            print('SUCCESS')
        else:
            print('INCOMPLETE')
