# ebcdic_code_page_tools

A single-purpose library that decodes and encodes IBM EBCDIC code page 037, the North American English variant used for mainframe data interchange.

```python
from ebcdic_code_page_tools import decode, encode

text = decode(b"\xc1\xc2\xc3")   # "ABC"
bytes_out = encode("Hello")       # b'\xc8\x85\x93\x93\x96'
```

## Why this exists

Mainframe flat files and record-oriented data often arrive as raw EBCDIC bytes. When you need to inspect or transform that data from a Python toolchain you need a small, dependency-free translator rather than a full DB2 connectivity layer. This library covers exactly CP037 and nothing else, so the table is hard-coded and the surface area is two functions.

## The awkward edge

Several EBCDIC byte positions have no assigned graphic character in CP037. On `decode`, those bytes become `U+FFFD` (the Unicode replacement character). On `encode`, `U+FFFD` raises `KeyError` rather than silently emitting a byte. This means undefined bytes are lossy: you can see that they were undefined, but you cannot round-trip them. That is deliberate — there is no correct byte to produce.
