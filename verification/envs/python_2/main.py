import sys
from checkio_executor_python.client import ClientLoop

ClientLoop(int(sys.argv[1]), sys.argv[2]).start()
