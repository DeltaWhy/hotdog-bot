import logging
import os
import sys
from dataclasses import dataclass

import dotenv
from rich.logging import RichHandler


@dataclass
class Config:
    bot_token: str
    log_level: str
    db_path: str
    exchange_rates_api_token: str


dotenv.load_dotenv()
config = Config(
    bot_token=os.environ["BOT_TOKEN"],
    log_level=os.environ.get("LOG_LEVEL", "INFO"),
    db_path=os.environ.get("DB_PATH", "hotdogbot.db"),
    exchange_rates_api_token=os.environ.get("EXCHANGE_RATES_API_TOKEN"),
)


def configure_logging():
    if sys.stdout.isatty():
        logging.basicConfig(
            encoding="utf-8",
            format="%(name)s\t| %(message)s",
            level=logging.INFO,
            handlers=[RichHandler(rich_tracebacks=True)],
        )
    else:
        logging.basicConfig(
            encoding="utf-8",
            format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s",
            level=logging.INFO,
        )
