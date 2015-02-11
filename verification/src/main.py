import argparse
import coloredlogs
import logging
import signal
import sys

from tornado.ioloop import IOLoop

from referee import Referee

import sys
# print(sys.argv)
#
# parser = argparse.ArgumentParser(description='Command line interface for CheckiO referee')
# parser.add_argument('-h', '--data_server_host', help='Host of data server', required=True)
# parser.add_argument('-p', '--data_server_port', help='Port of data server', required=True)
# options = parser.parse_args()


if __name__ == "__main__":
    def handle_signal(sig, frame):
        IOLoop.instance().add_callback(IOLoop.instance().stop)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    coloredlogs.install()

    # if not options:
    #     logging.error('No input options')
    #     sys.exit(0)
    #
    io_loop = IOLoop.instance()
    #
    # host = options.data_server_host
    # port = options.data_server_host

    host = sys.argv[1]
    port = int(sys.argv[2])
    referee = Referee(host, port, io_loop=io_loop)
    referee.start()
    io_loop.start()
