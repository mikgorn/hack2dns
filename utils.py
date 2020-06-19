import socket
from typing import *
from logging import getLogger
from contextlib import suppress

import idna  # type: ignore


_logger = getLogger(__file__)


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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
