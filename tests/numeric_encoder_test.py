from rmqrcode.encoder import NumericEncoder

import pytest


class TestNumericEncoder:
    def test_encode(self):
        encoded = NumericEncoder.encode("0123456789012345", 5)
        assert encoded == "00110000000000110001010110011010100110111000010100111010100101"

    def test_length(self):
        encoded_length = NumericEncoder.length("0123456789012345", 5)
        assert encoded_length is 62