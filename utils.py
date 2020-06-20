import re
import socket
import hashlib
from typing import *
from logging import getLogger
from contextlib import suppress

import idna  # type: ignore
import dns.resolver


_logger = getLogger(__file__)
_email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")


def convert_punycode_to_utf(punycode: str) -> str:
    return idna.decode(punycode)


def is_domain_exist(hostname: str) -> bool:
    """
    >>> is_domain_exist("google.com")
    True
    >>> is_domain_exist("minus_plus_del.abcd")
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
    >>> is_correct_email("andreyivanov01@тестовая-зона.область.рф")
    True
    """
    return bool(re.search(_email_pattern, email))


def is_domain_has_mx(domain: str) -> bool:
    """
    >>> is_domain_has_mx("rtv.ru")
    True
    >>> is_domain_has_mx("vse.net.da")
    False
    >>> is_domain_has_mx("mail.ru")
    True
    """
    with suppress(dns.resolver.NoAnswer):
        try:
            return bool(dns.resolver.query(domain, "MX"))
        except dns.resolver.NXDOMAIN:
            return False
    return False


def is_domain_has_host_addresses(domain: str) -> bool:
    """
    >>> is_domain_has_host_addresses("rtv.ru")
    True
    >>> is_domain_has_host_addresses("vse.net.da")
    False
    """
    with suppress(dns.resolver.NoAnswer):
        try:
            return bool(dns.resolver.query(domain, "A"))
        except dns.resolver.NXDOMAIN:
            return False
    return False


def is_domain_has_host_ipv6_addresses(domain: str) -> bool:
    """
    >>> is_domain_has_host_ipv6_addresses("rtv.ru")
    False
    >>> is_domain_has_host_ipv6_addresses("vse.net.da")
    False
    """
    with suppress(dns.resolver.NoAnswer):
        try:
            return bool(dns.resolver.query(domain, "AAAA"))
        except dns.resolver.NXDOMAIN:
            return False
    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
