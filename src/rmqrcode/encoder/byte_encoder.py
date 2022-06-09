class ByteEncoder:
    MODE_INDICATOR = "011"

    @staticmethod
    def _encoded_bits(s):
        res = ""
        encoded = s.encode('utf-8')
        for byte in encoded:
            res += bin(byte)[2:].zfill(8)
        return res


    @staticmethod
    def encode(data, character_count_length):
        res = ByteEncoder.MODE_INDICATOR
        res += bin(len(data))[2:].zfill(character_count_length)
        res += ByteEncoder._encoded_bits(data)
        return res


    @staticmethod
    def length(data):
        return len(data.encode('utf-8'))
