from .encoder_base import EncoderBase, IllegalCharacterError


class NumericEncoder(EncoderBase):
    @classmethod
    def mode_indicator(cls):
        return "001"

    @classmethod
    def encode(cls, data, character_count_indicator_length):
        if not cls.is_valid_characters(data):
            raise IllegalCharacterError

        res = cls.mode_indicator()
        res += bin(len(data))[2:].zfill(character_count_indicator_length)
        res += cls._encoded_bits(data)
        return res

    @classmethod
    def _encoded_bits(cls, data):
        res = ""
        data_grouped = cls._group_by_3characters(data)
        for num in data_grouped:
            if len(num) == 3:
                res += bin(int(num))[2:].zfill(10)
            elif len(num) == 2:
                res += bin(int(num))[2:].zfill(7)
            elif len(num) == 1:
                res += bin(int(num))[2:].zfill(4)
        return res

    @classmethod
    def _group_by_3characters(cls, data):
        res = []
        while data != "":
            res.append(data[:3])
            data = data[3:]
        return res

    @classmethod
    def length(cls, data, character_count_indicator_length):
        if len(data) % 3 == 0:
            r = 0
        elif len(data) % 3 == 1:
            r = 4
        elif len(data) % 3 == 2:
            r = 7
        return len(cls.mode_indicator()) + character_count_indicator_length + 10 * (len(data) // 3) + r

    @classmethod
    def is_valid_characters(cls, data):
        for c in data:
            if ord(c) < ord("0") or ord(c) > ord("9"):
                return False
        return True
