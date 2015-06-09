import logging
import sys
import os

from tornado.ioloop import IOLoop
from interface import ServerController


if __name__ == "__main__":
    (_, slug, action, env_name, code_path, port, log_level, tmp_file_name) = sys.argv

    logging.getLogger().setLevel(int(log_level))
    io_loop = IOLoop.instance()
    server = ServerController(io_loop=io_loop, user_data={
        'action': action,
        'code_path': code_path,
        'env_name': env_name
    })
    server.listen(port)
    logging.info('Start interface')
    if tmp_file_name != '-':
        os.remove(tmp_file_name)
    io_loop.start()
