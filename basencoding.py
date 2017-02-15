# basencoding - convert byte sequence to integer in multiple bases
# Copyright (C) 2017 Raphael McSinyx
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Convert byte sequence to integer in multiple bases.

Basically, this encoding treats each byte sequence as a base-256 number
and convert it to another base between 2 and 36.
"""

from math import gcd
from random import randint

DIGITS = [b'0123456789abcdefghijklmnopqrstuvwxyz',
          b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ']
POW2 = (1, 2, 4, 8, 16, 32)

__all__ = ['encode', 'decode']


def _encode_others(data, base, case):
    """Basencode bytes object data to base numeral system.

    Returning letters will be in lowercase if case is 0, uppercase if
    case is 1, otherwise picked randomly.
    """
    a, n = [], sum(c * 256**i for i, c in enumerate(reversed(data)))
    if case == -1:
        while n:
            n, mod = divmod(n, base)
            a.append(DIGITS[randint(0, 1)][mod])
    else:
        while n:
            n, mod = divmod(n, base)
            a.append(DIGITS[case][mod])
    a.reverse()
    return bytes(a)


def _encode_pow2(data, base, case):
    """Basencode bytes object data to base numeral system in the case
    in the case that base is power of 2.

    Returning letters will be in lowercase if case is 0, uppercase if
    case is 1, otherwise picked randomly.
    """
    p = POW2.index(base)
    bufsiz = p // gcd(p, 8)
    start = len(data) % bufsiz
    return (_encode_others(data[:start], base, case) +
            b''.join(_encode_others(data[i:i+bufsiz], base, case).zfill(bufsiz*8//p)
                     for i in range(start, len(data), bufsiz)))


def encode(data, base=None):
    """Basencode bytes object data to base numeral system.

    base is a bytes represents base between 2 and 36 that data will be
    basencoded to. If base is in base 10, the cases of returned digits
    will be chosen randomly, else base would be in base 36 and the
    cases will be the same as the case of base (special: lowercase 36 is
    0 and uppercase is 1). If base is None, it will be picked randomly
    between 2 and 36.

    A newline character will be added to the end of the returning bytes.
    """
    if base is None: base = str(randint(2, 36)).encode()
    if len(base) == 1:
        case = 0 if base.islower() or base == b'0' else 1
        base = 36 if base in b'01' else max(i.find(base) for i in DIGITS)
    elif base.isdigit():
        case = -1
        base = int(base)
    if not isinstance(base, int) or base < 2 or base > 36:
        raise ValueError("base doesn't represent a number between 2 and 36")
    if base in POW2:
        return _encode_pow2(data, base, case) + b'\n'
    return _encode_others(data, base, case) + b'\n'


def _decode_others(data, base):
    """Decoded bytes object data basencoded to base numeral system."""
    if not data:
        return data
    data, a = int(data, base), []
    while data:
        data, mod = divmod(data, 256)
        a.append(mod)
    a.reverse()
    return bytes(a)


def _decode_pow2(data, base):
    """Decoded bytes object data basencoded to base numeral system
    in the case that base is power of 2.
    """
    bufsiz = 8 // gcd(POW2.index(base), 8)
    start = len(data) % bufsiz
    return (_decode_others(data[:start], base) +
            b''.join(_decode_others(data[i:i+bufsiz], base)
                     for i in range(start, len(data), bufsiz))


def decode(data, base=None, encoding='utf-8'):
    """Return decoded bytes object data basencoded to base numeral
    system.

    base is a bytes represents a base between 2 and 36 that data has
    been basencoded to, rather in base 10 or base + 1. If base is None,
    this function will find the base that decoded data can be decoded to
    encoding.
    """
    data = data.rstrip()
    if set(data) - set(DIGITS[0] + DIGITS[1]):
        raise ValueError("data hasn't been encoded using basencoding")
    if base is None:
        base, d = range(DIGITS[0].find(max(data.lower())) + 1, 37), {}
        for i in base:
            try:
                if i in POW2: d[i] = _decode_pow2(data, i).decode(encoding)
                else: d[i] = _decode_others(data, i).decode(encoding)
            except:
                pass
        if not d:
            raise ValueError("data hasn't been encoded using basencoding")
        elif len(d) > 1:
            d = ', '.join(str(i) for i in sorted(d.keys()))
            raise RuntimeError("data could be decodable by base {}".format(d))
        return list(d.values())[0].encode(encoding)
    else:
        if len(base) == 1: base = max(i.find(base) for i in DIGITS)
        elif base.isdigit(): base = int(base)
        if not isinstance(base, int) or base < 2 or base > 36:
            raise ValueError("base doesn't represent a number between 2 and 36")
        return (_decode_pow2 if base in POW2 else _decode_others)(data, base)
