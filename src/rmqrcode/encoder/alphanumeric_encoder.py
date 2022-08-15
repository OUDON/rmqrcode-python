from .encoder_base import EncoderBase, IllegalCharacterError


class AlphanumericEncoder(EncoderBase):
    CHARACTER_MAP = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
        "G": 16,
        "H": 17,
        "I": 18,
        "J": 19,
        "K": 20,
        "L": 21,
        "M": 22,
        "N": 23,
        "O": 24,
        "P": 25,
        "Q": 26,
        "R": 27,
        "S": 28,
        "T": 29,
        "U": 30,
        "V": 31,
        "W": 32,
        "X": 33,
        "Y": 34,
        "Z": 35,
        " ": 36,
        "$": 37,
        "%": 38,
        "*": 39,
        "+": 40,
        "-": 41,
        ".": 42,
        "/": 43,
        ":": 44,
    }

    @classmethod
    def mode_indicator(cls):
        return "010"

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
        data_grouped = cls._group_by_2characters(data)
        for s in data_grouped:
            if len(s) == 2:
                value = cls.CHARACTER_MAP[s[0]] * 45 + cls.CHARACTER_MAP[s[1]]
                res += bin(value)[2:].zfill(11)
            elif len(s) == 1:
                value = cls.CHARACTER_MAP[s[0]]
                res += bin(value)[2:].zfill(6)
        return res

    @classmethod
    def _group_by_2characters(cls, data):
        res = []
        while data != "":
            res.append(data[:2])
            data = data[2:]
        return res

    @classmethod
    def length(cls, data, character_count_indicator_length):
        return (
            len(cls.mode_indicator()) + character_count_indicator_length + 11 * (len(data) // 2) + 6 * (len(data) % 2)
        )

    @classmethod
    def is_valid_characters(cls, data):
        for c in data:
            if c not in cls.CHARACTER_MAP:
                return False
        return True
