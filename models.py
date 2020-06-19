import hashlib
from typing import *
from datetime import datetime
from dataclasses import dataclass


@dataclass
class NameMixin:
    first_name: str
    second_name: str
    patronymic: Optional[str]


@dataclass
class BirthdayMixin:
    birthday: datetime


@dataclass
class PasswordMixin:
    password: str

    def __post_init__(self):
        self.password = (
            hashlib.md5(self.password.encode(errors="replace"))
            .digest()
            .decode(errors="replace")
        )


@dataclass
class User(NameMixin, BirthdayMixin, PasswordMixin):
    ...


if __name__ == "__main__":
    print(
        User(
            first_name="Svyatoslav",
            second_name="Krivulya",
            birthday=datetime.now(),
            patronymic=None,
            password="Hello, world!",
        )
    )
