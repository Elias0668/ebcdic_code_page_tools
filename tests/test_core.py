"""Tests for ebcdic_code_page_tools.core.

Run with:  PYTHONPATH=src python -m unittest discover -s tests
"""

import unittest

from ebcdic_code_page_tools.core import decode, encode


class TestDecode(unittest.TestCase):
    def test_ascii_letters_round_trip_to_lowercase_ebcdic(self):
        # In CP037 lowercase 'a' is byte 0x81.
        self.assertEqual(decode(b"\x81"), "a")
        self.assertEqual(decode(b"\x89"), "i")

    def test_uppercase_letters(self):
        # Uppercase 'A' is 0xC1 in CP037.
        self.assertEqual(decode(b"\xc1"), "A")
        self.assertEqual(decode(b"\xe9"), "Z")

    def test_digits(self):
        # '0' is 0xF0 in CP037.
        self.assertEqual(decode(b"\xf0"), "0")
        self.assertEqual(decode(b"\xf9"), "9")

    def test_space_is_0x40(self):
        self.assertEqual(decode(b"\x40"), " ")

    def test_undefined_byte_becomes_replacement_character(self):
        # 0x00 is a control; 0xFF has no assignment at all.
        self.assertEqual(decode(b"\xff"), "\ufffd")

    def test_control_chars_decode_literally(self):
        # NUL, LF, CR pass through as their ASCII control equivalents.
        self.assertEqual(decode(b"\x00"), "\x00")
        self.assertEqual(decode(b"\x0d"), "\x0d")

    def test_mixed_string(self):
        # "ABC" in CP037.
        self.assertEqual(decode(b"\xc1\xc2\xc3"), "ABC")

    def test_bytearray_accepted(self):
        self.assertEqual(decode(bytearray(b"\xc1\xc2\xc3")), "ABC")

    def test_empty_input(self):
        self.assertEqual(decode(b""), "")

    def test_type_error_on_non_bytes(self):
        with self.assertRaises(TypeError):
            decode("not bytes")


class TestEncode(unittest.TestCase):
    def test_ascii_letters(self):
        self.assertEqual(encode("a"), b"\x81")
        self.assertEqual(encode("Z"), b"\xe9")

    def test_digits(self):
        self.assertEqual(encode("0"), b"\xf0")
        self.assertEqual(encode("9"), b"\xf9")

    def test_space(self):
        self.assertEqual(encode(" "), b"\x40")

    def test_empty_string(self):
        self.assertEqual(encode(""), b"")

    def test_type_error_on_non_str(self):
        with self.assertRaises(TypeError):
            encode(b"not a str")

    def test_replacement_character_not_encodable(self):
        # U+FFFD never round-trips because it stands for undefined data.
        with self.assertRaises(KeyError):
            encode("\ufffd")


class TestRoundTrip(unittest.TestCase):
    def test_printable_ascii_round_trips(self):
        sample = "ABCDEFGHIJ0123456789 .+-/*"
        self.assertEqual(decode(encode(sample)), sample)

    def test_undefined_byte_does_not_round_trip(self):
        # 0xFF decodes to U+FFFD which cannot be encoded back.
        self.assertEqual(decode(b"\xff"), "\ufffd")
        with self.assertRaises(KeyError):
            encode(decode(b"\xff"))


if __name__ == "__main__":
    unittest.main()
