import os
import logging
import sqlite3
from typing import Iterator
from datetime import datetime

from discord_role_expire.types import Expiry

log = logging.getLogger(__name__)

TABLE_NAME = "expiry"

connection = sqlite3.connect(os.getenv("DB"))
cursor = connection.cursor()


def init() -> None:
    log.info("Initializing DB...")
    with connection:
        cursor.execute(
            (
                f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} "
                "(member_id INTEGER, guild_id INTEGER, "
                "role_id INTEGER, expires_at TEXT)"
            )
        )


def de_init() -> None:
    log.info("Deinitializing DB...")
    cursor.close()
    connection.close()


async def insert(expiry: Expiry) -> None:
    with connection:
        cursor.execute(
            (
                f"INSERT INTO {TABLE_NAME} VALUES "
                f"({expiry['member_id']}, {expiry['guild_id']}, {expiry['role_id']}, "
                f"'{expiry['expires_at'].isoformat()}')"
            )
        )
        log.info("Expiry inserted into db:", f"{expiry=}")


async def remove(expiry: Expiry) -> None:
    with connection:
        cursor.execute(
            (
                f"DELETE FROM {TABLE_NAME} WHERE member_id = ? "
                "AND guild_id = ? AND role_id = ?"
            ),
            (expiry["member_id"], expiry["guild_id"], expiry["role_id"]),
        )
        log.info("Expiry removed from db:", f"{expiry=}")


def list_expiries() -> Iterator[Expiry]:
    with connection:
        log.info("Getting expiries...")
        rows = cursor.execute(
            f"SELECT member_id, guild_id, role_id, expires_at FROM {TABLE_NAME}"
        ).fetchall()
        for row in rows:
            member_id, guild_id, role_id, expires_at = row
            yield Expiry(
                dict(
                    member_id=member_id,
                    guild_id=guild_id,
                    role_id=role_id,
                    expires_at=datetime.fromisoformat(expires_at),
                )
            )
