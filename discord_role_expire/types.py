from datetime import datetime
from typing import TypedDict


class Expiry(TypedDict):
    member_id: int
    guild_id: int
    role_id: int
    expires_at: datetime
