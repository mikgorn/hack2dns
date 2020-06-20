import re
import socket
import hashlib
from typing import *
from logging import getLogger
from contextlib import suppress

import idna  # type: ignore


_logger = getLogger(__file__)
_email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")


def convert_punycode_to_utf(punycode: str) -> str:
    return idna.decode(punycode)


def is_hostname_exist(hostname: str) -> bool:
    """
    >>> is_hostname_exist("google.com")
    True
    >>> is_hostname_exist("minus_plus_del.abcd")
    False
    """
    with suppress(Exception):
        socket.gethostbyname(hostname)
        return True
    return False


def get_password_hash(password: str) -> str:
    return (
        hashlib.md5(password.encode(errors="replace"))
        .digest()
        .decode(errors="replace")
    )


def convert_email_from_punycode_to_utf(email: str) -> str:
    """
    >>> convert_email_from_punycode_to_utf("fsafasfa@xn---11-5cdbjut8cfe4alc2r")
    'fsafasfa@тестовая-зона11'
    """
    parts = email.split("@")
    return "@".join([parts[0], convert_punycode_to_utf(parts[1])])


def is_correct_email(email: str) -> bool:
    """
    >>> is_correct_email("andreyivanov01@тестовая-зона.рф")
    True
    >>> is_correct_email("andreyivanov01@тестовая-зонарф")
    False
    """
    return bool(re.search(_email_pattern, email))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
