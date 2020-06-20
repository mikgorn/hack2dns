from typing import *
from pathlib import Path

from utils import convert_punycode_to_utf


_tlds: Set[str] = set()


def _read_tld_file(tld_file_path: Path) -> Generator[str, None, None]:
    with open(str(tld_file_path)) as file:
        for line in file:
            if line.startswith("#"):
                continue
            yield line


def initialize_tld(tld_file_path: Path) -> None:
    for tld in _read_tld_file(tld_file_path):
        _tlds.add(convert_punycode_to_utf(tld.strip()))


def is_correct_tld(tld: str) -> bool:
    """
    >>> is_correct_tld("рф")
    True
    """
    return tld.lower() in _tlds


def is_correct_email_tld(email: str) -> bool:
    """
    >>> is_correct_email_tld("petrsergeev02@тестовая-зона.рф")
    True
    >>> is_correct_email_tld("andreyivanov01@тестовая-зона.нерф")
    False
    """
    return is_correct_tld(email.split(".")[-1])


if __name__ == "__main__":
    import doctest

    tld_file_path = Path("./tlds-alpha-by-domain.txt")
    initialize_tld(tld_file_path=tld_file_path)
    doctest.testmod()
