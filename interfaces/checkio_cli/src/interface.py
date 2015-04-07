from handlers.simple_output import SimplePrintHandler
from server import TCPConsoleServer


class ServerController(TCPConsoleServer):
    cls_handler = SimplePrintHandler
