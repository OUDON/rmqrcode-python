from rmqrcode.encoder import ByteEncoder, IllegalCharacterError

import pytest


class TestNumericEncoder:
    def test_encode(self):
        encoded = ByteEncoder.encode("📌", 5)
        assert encoded == "0110010011110000100111111001001110001100"

    def test_length(self):
        encoded_length = ByteEncoder.length("📌", 5)
        assert encoded_length is 40

    def test_is_valid_characters(self):
        assert ByteEncoder.is_valid_characters("0123456789") is True
        assert ByteEncoder.is_valid_characters("A1234!678@") is True
        assert ByteEncoder.is_valid_characters("📌") is True
