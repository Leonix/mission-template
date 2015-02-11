from checkio_referee import RefereeBase

import settings
from tests import TESTS


class Referee(RefereeBase):
    TESTS = TESTS
    EXECUTABLE_PATH = settings.EXECUTABLE_PATH
