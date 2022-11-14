import logging

import hotdogbot
from hotdogbot.client import Client
from hotdogbot.config import config, configure_logging
from hotdogbot.db import db

configure_logging()
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, config.log_level))


def main():
    logger.info("version: %s", hotdogbot.__version__)
    db.migrate()
    client = Client()

    client.run(config.bot_token, log_handler=None)


if __name__ == "__main__":
    main()
