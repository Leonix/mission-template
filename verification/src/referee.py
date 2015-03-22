from checkio_referee import RefereeBase
from checkio_referee.handlers.common import CheckHandler
from checkio_referee.handlers.common import RunHandler
from checkio_referee.handlers.common import RunInConsoleHandler

import settings_env
from tests import TESTS

CheckHandler.TESTS = TESTS


class Referee(RefereeBase):
    ENVIRONMENTS = settings_env.ENVIRONMENTS

Referee.set_handler(Referee.HANDLER_ACTION_CHECK, CheckHandler)
Referee.set_handler(Referee.HANDLER_ACTION_RUN, RunHandler)
Referee.set_handler(Referee.HANDLER_ACTION_RUN_IN_CONSOLE, RunInConsoleHandler)
# TODO: Referee.set_handler(Referee.HANDLER_ACTION_TRY_IT, ...)
