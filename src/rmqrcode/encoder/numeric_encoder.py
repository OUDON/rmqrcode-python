from .encoder_base import EncoderBase


class NumericEncoder(EncoderBase):
    @classmethod
    def mode_indicator(cls):
        return "001"

    @classmethod
    def _encoded_bits(cls, s):
        raise NotImplementedError()

    @classmethod
    def encode(cls, data, character_count_indicator_length):
        raise NotImplementedError()

    @classmethod
    def length(cls, data, character_count_indicator_length):
        raise NotImplementedError()
