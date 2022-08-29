from .encoder_base import EncoderBase, IllegalCharacterError


class KanjiEncoder(EncoderBase):
    @classmethod
    def mode_indicator(cls):
        return "100"

    @classmethod
    def _encoded_bits(cls, data):
        res = ""
        for c in data:
            shift_jis = c.encode("shift-jis")
            hex_value = shift_jis[0] * 256 + shift_jis[1]

            if hex_value >= 0x8140 and hex_value <= 0x9FFC:
                sub = 0x8140
            elif hex_value >= 0xE040 and hex_value <= 0xEBBF:
                sub = 0xC140
            else:
                raise IllegalCharacterError()

            msb = (hex_value - sub) >> 8
            lsb = (hex_value - sub) & 255
            encoded_value = msb * 0xC0 + lsb
            res += bin(encoded_value)[2:].zfill(13)
        return res

    @classmethod
    def length(cls, data, character_count_indicator_length):
        return len(cls.mode_indicator()) + character_count_indicator_length + 13 * len(data)

    @classmethod
    def characters_num(cls, data):
        return len(data.encode("shift_jis")) // 2

    @classmethod
    def is_valid_characters(cls, data):
        for c in data:
            try:
                shift_jis = c.encode("shift_jis")
            except UnicodeEncodeError:
                return False
            if len(shift_jis) < 2:
                return False
            hex_value = shift_jis[0] * 256 + shift_jis[1]
            if (0x8140 > hex_value and 0x9FFC < hex_value) or (0xE040 > hex_value and 0xEBBF < hex_value):
                return False
        return True
