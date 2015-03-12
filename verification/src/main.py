import coloredlogs
import logging
import signal
import sys

from tornado.ioloop import IOLoop

from referee import Referee


if __name__ == "__main__":
    logging.info("Start referee in docker")

    def handle_signal(sig, frame):
        IOLoop.instance().add_callback(IOLoop.instance().stop)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    coloredlogs.install()

    io_loop = IOLoop.instance()

    host = sys.argv[1]
    port = int(sys.argv[2])
    user_connection_id = sys.argv[3]
    docker_id = sys.argv[4]
    referee = Referee(host, port, user_connection_id=user_connection_id, docker_id=docker_id,
                      io_loop=io_loop)
    referee.start()
    io_loop.start()
