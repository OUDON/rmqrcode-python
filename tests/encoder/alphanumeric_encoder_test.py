from rmqrcode.encoder import AlphanumericEncoder, IllegalCharacterError

import pytest


class TestAlphaNumericEncoder:
    def test_encode(self):
        encoded = AlphanumericEncoder.encode("AC-42", 5)
        assert encoded == "010001010011100111011100111001000010"

    def test_encode_raises_invalid_character_error(self):
        with pytest.raises(IllegalCharacterError) as e:
            AlphanumericEncoder.encode("abc123", 5)

    def test_length(self):
        encoded_length = AlphanumericEncoder.length("AC-42", 5)
        assert encoded_length is 36

    def test_is_valid_characters(self):
        assert AlphanumericEncoder.is_valid_characters("AC-42") is True
        assert AlphanumericEncoder.is_valid_characters("abc123") is False
        assert AlphanumericEncoder.is_valid_characters("📌") is False
