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
class ContactsMixin:
    email: str


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
    @classmethod
    def create_from_registration_form(
        cls, raw_data: Union[Dict[str, Any], MutableMapping[str, Any]]
    ) -> "User":
        defaults_values = {
            "disabled": False,
            "retiree": False,
            "patronymic": None,
        }
        other_fields = {"confirmpassword", "confirmemail"}
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
