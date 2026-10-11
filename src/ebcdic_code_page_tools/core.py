"""Core encoding/decoding tables and functions for EBCDIC code page 037.

CP037 is a single-byte EBCDIC variant used on IBM mainframes in North America.
We hard-code two tables of exactly 256 entries rather than parsing a code-page
file at runtime so that the library has no external data dependency.

An important design decision: several EBCDIC byte values have no defined
graphic character in CP037 (IBM labels them as control positions).  We map
those bytes to U+FFFD REPLACEMENT CHARACTER on decode, and we raise
``KeyError`` if the caller tries to *encode* a replacement character back to
bytes.  This makes round-tripping lossy for undefined bytes, which is the
correct behaviour: there is no glyph to preserve, so the data is already lost.
"""

from __future__ import annotations

# Ordered by byte value 0x00-0xFF.
#
# U+FFFD marks byte positions that have no assigned graphic character in
# CP037.  The official IBM code-page table leaves these blank; we cannot
# invent a mapping, so we surface them as the Unicode replacement character.
_DECODING_TABLE: tuple[str, ...] = (
    "\x00", "\x01", "\x02", "\x03", "\ufffd", "\x09", "\ufffd", "\x7f",
    "\ufffd", "\ufffd", "\ufffd", "\x0b", "\x0c", "\x0d", "\x0e", "\x0f",
    "\x10", "\x11", "\x12", "\x13", "\ufffd", "\ufffd", "\x08", "\ufffd",
    "\x18", "\x19", "\ufffd", "\ufffd", "\x1c", "\x1d", "\x1e", "\x1f",
    "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\x0a", "\x17", "\x1b",
    "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\x05", "\x06", "\x07",
    "\ufffd", "\ufffd", "\x16", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\x04",
    "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\x14", "\x15", "\ufffd", "\x1a",
    " ", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\ufffd", "\ufffd", "\xa2", ".", "<", "(", "+", "|",
    "&", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\ufffd", "\ufffd", "!", "$", "*", ")", ";", "\ufffd",
    "-", "/", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\ufffd", "\ufffd", "\xa6", ",", "%", "_", ">", "?",
    "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\ufffd", "`", ":", "#", "@", "'", "=", '"',
    "\ufffd", "a", "b", "c", "d", "e", "f", "g",
    "h", "i", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\ufffd", "j", "k", "l", "m", "n", "o", "p",
    "q", "r", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\ufffd", "~", "s", "t", "u", "v", "w", "x",
    "y", "z", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "{", "A", "B", "C", "D", "E", "F", "G",
    "H", "I", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "}", "J", "K", "L", "M", "N", "O", "P",
    "Q", "R", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "\\", "\ufffd", "S", "T", "U", "V", "W", "X",
    "Y", "Z", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
    "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd", "\ufffd",
)

# Inverse of the decoding table.  Control characters that appear only once
# in the decoding table are included; characters that appear more than once
# (we use the lowest byte value for the inverse so the result is stable) are
# resolved deterministically.  U+FFFD is deliberately absent so that
# encode() raises KeyError rather than silently producing a byte.
_ENCODING_TABLE: dict[str, int] = {}
for _i, _ch in enumerate(_DECODING_TABLE):
    if _ch == "\ufffd":
        continue
    # Keep the first (lowest) byte value for a given character so encoding
    # is a stable, well-defined function.
    _ENCODING_TABLE.setdefault(_ch, _i)
del _i, _ch


def decode(data: bytes) -> str:
    """Decode EBCDIC CP037 ``data`` into a Python ``str``.

    Bytes with no assigned CP037 graphic character become U+FFFD.
    Accepts ``bytes`` or ``bytearray``.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("decode expects bytes or bytearray, got " + type(data).__name__)
    return "".join(_DECODING_TABLE[b] for b in data)


def encode(text: str) -> bytes:
    """Encode ``text`` (str) into EBCDIC CP037 ``bytes``.

    Raises ``KeyError`` for any character that has no CP037 byte, including
    U+FFFD.  This is intentional: if the caller asks for a byte that does not
    exist, we surface the problem rather than emit undefined output.
    """
    if not isinstance(text, str):
        raise TypeError("encode expects str, got " + type(text).__name__)
    out = bytearray()
    for ch in text:
        out.append(_ENCODING_TABLE[ch])
    return bytes(out)
