"""ebcdic_code_page_tools: encode and decode IBM EBCDIC code page 037.

This package exposes two functions, ``decode`` and ``encode``, that convert
between Python ``str`` and EBCDIC CP037 byte sequences.  CP037 is the
North American English variant used in IBM mainframe data interchange.

Only the public functions below are part of the supported API.
"""

from .core import decode, encode

__all__ = ["decode", "encode"]
