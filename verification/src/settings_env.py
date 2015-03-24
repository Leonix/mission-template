import os


def get_environments():
    return {env: os.path.join(ENVS_PATH, env, ENV_FILE_RUNNER) for env in os.listdir(ENVS_PATH)}


SRC_PATH = os.path.realpath(os.path.dirname(__file__))
ENVS_PATH = os.path.join(SRC_PATH, '..', 'envs')

ENV_FILE_RUNNER = 'run.sh'

ENVIRONMENTS = get_environments()
