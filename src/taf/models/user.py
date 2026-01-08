from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    password: str
