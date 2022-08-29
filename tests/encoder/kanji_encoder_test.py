from rmqrcode.encoder import KanjiEncoder, IllegalCharacterError

import pytest


class TestKanjiEncoder:
    def test_encode(self):
        encoded = KanjiEncoder.encode("点茗", 5)
        assert encoded == "1000001001101100111111101010101010"

    def test_encode_raises_invalid_character_error(self):
        with pytest.raises(IllegalCharacterError) as e:
            KanjiEncoder.encode("abc123", 5)

    def test_length(self):
        encoded_length = KanjiEncoder.length("点茗", 5)
        assert encoded_length is 34

    def test_is_valid_characters(self):
        assert KanjiEncoder.is_valid_characters("点茗") is True
        assert KanjiEncoder.is_valid_characters("abc") is False
        assert KanjiEncoder.is_valid_characters("📌") is False
