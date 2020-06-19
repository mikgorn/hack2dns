from typing import *

import idna


def convert_punycode_to_utf(punycode: str) -> str:
    return idna.decode(punycode)
