from checkio_referee import RefereeBase

import settings_env
from tests import TESTS


class Referee(RefereeBase):
    ENVIRONMENTS = settings_env.ENVIRONMENTS
    TESTS = TESTS
