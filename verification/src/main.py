import coloredlogs
import signal
import sys

from tornado.ioloop import IOLoop

from referee import Referee


if __name__ == "__main__":
    def handle_signal(sig, frame):
        IOLoop.instance().add_callback(IOLoop.instance().stop)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    coloredlogs.install()

    io_loop = IOLoop.instance()

    host = sys.argv[1]
    port = int(sys.argv[2])
    referee = Referee(host, port, io_loop=io_loop)
    referee.start()
    io_loop.start()
