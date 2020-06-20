import hashlib
from typing import *
from datetime import datetime
from dataclasses import dataclass

import utils


@dataclass
class NameMixin:
    first_name: str
    second_name: str
    patronymic: str


@dataclass
class BirthdayMixin:
    birthday: datetime


@dataclass
class ContactsMixin:
    email: str
    address: str

    def __post_init__(self):
        self.email = utils.convert_email_from_punycode_to_utf(
            self.email.lower()
        )


@dataclass
class PasswordMixin:
    password: str

    def __post_init__(self):
        self.password = utils.get_password_hash(self.password)


@dataclass
class RetireeMixin:
    retiree: Union[bool, Any]

    def __post_init__(self):
        self.retiree = bool(self.retiree)


@dataclass
class DisabledMixin:
    disabled: Union[bool, Any]

    def __post_init__(self):
        self.disabled = bool(self.disabled)


@dataclass
class User(
    NameMixin,
    BirthdayMixin,
    PasswordMixin,
    RetireeMixin,
    DisabledMixin,
    ContactsMixin,
):
    def __post_init__(self):
        for base in self.__class__.__bases__:
            if hasattr(base, "__post_init__"):
                base.__post_init__(self)

    @classmethod
    def create_from_registration_form(
        cls, raw_data: Union[Dict[str, Any], MutableMapping[str, Any]]
    ) -> "User":
        defaults_values = {
            "disabled": False,
            "retiree": False,
            "patronymic": str,
        }
        other_fields = {"confirmpassword"}
        data = {k: v for k, v in raw_data.items()}
        for k, v in defaults_values.items():
            if k not in data:
                data[k] = v
        data["birthday"] = datetime(
            int(data.pop("bdyear")),
            int(data.pop("bdmonth")),
            int(data.pop("bdday")),
        )
        for k in other_fields:
            data.pop(k)
        return cls(**data)

    @classmethod
    def create_user_from_sqlite_db(
        cls, values: Tuple, fields: Tuple
    ) -> "User":
        data = {}
        for i in range(len(fields)):
            data[fields[i]] = values[i]
        data["birthday"] = datetime.strptime(
            data["birthday"], "%Y-%m-%d %H:%M:%S"
        )
        return cls(**data)


if __name__ == "__main__":
    from time import time

    u = User(
        first_name="slava",
        second_name="Кривуя",
        patronymic="",
        birthday=datetime.fromtimestamp(int(time())),
        password="ficus",
        email="ficus@bk.рф",
        disabled=False,
        retiree=True,
        address="Ficus",
    )
