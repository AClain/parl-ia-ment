import os
from functools import lru_cache
from pydantic import BaseModel
import logging
from pathlib import Path


@lru_cache
def get_env_filename() -> str:
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


def get_src_path(current_path: Path):
    if "src" not in str(current_path):
        return "src"

    if str(current_path.parent).endswith("src"):
        return current_path.parent
    else:
        return get_src_path(current_path.parent)


class Settings(BaseModel):
    LOG_FILE_NAME: str = str(get_src_path(Path(os.getcwd()))) + "/logs/app.log"
    LOG_FILE_MODE: str = "a"
    LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_LEVEL: str = logging.INFO

    class Config:
        env_file = get_env_filename()


@lru_cache
def get_environment_variables() -> Settings:
    return Settings()
