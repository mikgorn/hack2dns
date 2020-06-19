from typing import *
from dataclasses import dataclass


@dataclass
class BasicUser:
    first_name: str
    second_name: str
    patronymic: Optional[str] = None