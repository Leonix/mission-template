import os
import sys

PATH_CURRENT = os.path.realpath(os.path.dirname(__file__)) + os.sep
PATH_ENVS = os.path.join(PATH_CURRENT, '..')
sys.path.insert(0, PATH_ENVS)

from executor import client


if __name__ == "__main__":
    client.start()
