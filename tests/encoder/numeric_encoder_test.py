from rmqrcode.encoder import NumericEncoder, IllegalCharacterError

import pytest


class TestNumericEncoder:
    def test_encode(self):
        encoded = NumericEncoder.encode("0123456789012345", 5)
        assert encoded == "00110000000000110001010110011010100110111000010100111010100101"

    def test_encode_raises_invalid_character_error(self):
        with pytest.raises(IllegalCharacterError) as e:
            NumericEncoder.encode("ABC123", 5)

    def test_length(self):
        encoded_length = NumericEncoder.length("0123456789012345", 5)
        assert encoded_length is 62

    def test_is_valid_characters(self):
        assert NumericEncoder.is_valid_characters("0123456789") is True
        assert NumericEncoder.is_valid_characters("A1234!678@") is False
