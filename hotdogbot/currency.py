import json
import logging
from datetime import datetime

import aiohttp

from .config import config
from .db import Connection

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, config.log_level))


def convert_to_usd(db: Connection, amount: float, currency: str):
    cur = db.cursor()
    cur.execute(
        "SELECT value->'rates'->>currency FROM exchange_rates, (SELECT ? as currency) ORDER BY timestamp DESC LIMIT 1",
        (currency,),
    )
    if (row := cur.fetchone()) and row[0]:
        rate = row[0]
        return amount / rate
    else:
        raise ValueError(f"No rate found for {currency}")


async def update_exchange_rates(db: Connection):
    if not config.exchange_rates_api_token:
        raise RuntimeError("No API token for exchange rates API")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.apilayer.com/exchangerates_data/latest?base=USD",
            headers={"apikey": config.exchange_rates_api_token},
        ) as resp:
            value = await resp.json()
            logger.debug(f"status: {resp.status}")
            logger.debug(f"headers: {json.dumps(dict(resp.headers))}")
            logger.debug(f"value: {json.dumps(value)}")
            if resp.status >= 200 and resp.status < 300:
                with db:
                    db.execute(
                        "INSERT INTO exchange_rates (value, headers) VALUES (?, ?)",
                        (json.dumps(value), json.dumps(dict(resp.headers))),
                    )
            else:
                raise RuntimeError(f"HTTP error {resp.status}")


def get_last_rate_update(db: Connection) -> datetime:
    cur = db.execute(
        "SELECT timestamp FROM exchange_rates ORDER BY timestamp DESC LIMIT 1"
    )
    if row := cur.fetchone():
        return datetime.fromisoformat(row[0])
    else:
        return datetime.fromtimestamp(0)
