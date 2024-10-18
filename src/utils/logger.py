import logging
from functools import lru_cache
from configs.env import get_environment_variables

env = get_environment_variables()


@lru_cache
def get_logger():
    logging.basicConfig(
        format=env.LOG_FORMAT,
        datefmt=env.LOG_DATE_FORMAT,
        filename=env.LOG_FILE_NAME,
        filemode=env.LOG_FILE_MODE,
    )
    logger = logging.getLogger()
    logger.setLevel(env.LOG_LEVEL or logging.INFO)

    logger.info(f"Logger initialized with level {logging.getLevelName(logger.level)}.")
    return logger
