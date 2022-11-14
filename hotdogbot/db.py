import logging
import sqlite3
from pathlib import Path

from hotdogbot.config import config

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, config.log_level))


class Row(sqlite3.Row):
    def __repr__(self):
        return f"Row<{repr(dict(self))}>"


class Connection(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_factory = Row
        self.executescript(
            """
            PRAGMA foreign_keys = ON;
            PRAGMA journal_mode = WAL;
        """
        )

    @property
    def user_version(self):
        cur = self.execute("PRAGMA user_version")
        return cur.fetchone()[0]

    @user_version.setter
    def user_version(self, val):
        self.execute("PRAGMA user_version = %d" % (val,))
        return val

    def migrate(self):
        orig_version = self.user_version
        logger.info("DB user_version = %d", orig_version)
        import importlib.resources

        for path in sorted(
            importlib.resources.files("hotdogbot").joinpath("migrations").iterdir()
        ):
            if path.is_file() and path.match("[0-9]*.sql"):
                logger.debug("Trying file %s", path)
                try:
                    num = int(path.stem.partition("-")[0])
                except Exception as e:
                    logger.exception(e)
                    continue
                if num > self.user_version:
                    logger.info("Applying migration %s", path.name)
                    self.executescript(path.read_text())
                    if self.user_version != num:
                        raise RuntimeError(
                            f"Migration {path.name} did not change user_version"
                        )
        if (new_version := self.user_version) != orig_version:
            logger.info("DB migrated to user_version = %d", new_version)
            try:
                with open(
                    Path(__file__).parent / "migrations" / "schema.sql", "w"
                ) as f:
                    f.write("-- This file is auto-generated. DO NOT EDIT.\n")
                    f.write(f"-- PRAGMA user_version = {new_version};\n")
                    for line in self.iterdump():
                        f.write("%s\n" % line)
            except Exception as e:
                logger.exception(e)


db = sqlite3.connect(config.db_path, factory=Connection)
