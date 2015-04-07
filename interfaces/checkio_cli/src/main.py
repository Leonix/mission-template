import logging
import sys

from tornado.ioloop import IOLoop
from interface import ServerController


if __name__ == "__main__":
    (_, slug, action, env_name, code_path, port, log_level) = sys.argv

    logging.getLogger().setLevel(int(log_level))
    io_loop = IOLoop.instance()
    server = ServerController(io_loop=io_loop, user_data={
        'action': action,
        'code': open(code_path).read(),
        'env_name': env_name
    })
    server.listen(port)
    logging.info('Start interface')
    io_loop.start()
