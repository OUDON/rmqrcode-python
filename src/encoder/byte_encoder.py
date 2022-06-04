class ByteEncoder:
    MODE_INDICATOR = "011"

    def _convert_to_byte(self, s):
        if 'A' <= s and s <= 'Z':
            return ord(s) - ord('A') + 0x41;
        elif 'a' <= s and s <= 'z':
            return ord(s) - ord('a') + 0x61;
        elif '0' <= s and s <= '9':
            return ord(s) - ord('0') + 0x30;

        character_code = {
            ' ': 0x20,
            ',': 0x2C,
            '.': 0x2E
        }

        if s in character_code:
            return character_code[s]

        raise Exception()

    def encode(self, data, character_count_length):
        res = ByteEncoder.MODE_INDICATOR
        res += bin(len(data))[2:].zfill(character_count_length)
        for s in data:
            res += bin(self._convert_to_byte(s))[2:].zfill(8)
        return res