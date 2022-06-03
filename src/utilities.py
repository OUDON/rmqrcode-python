def msb(n):
    return len(bin(n)) - 2


def to_binary(data, len):
    return bin(data)[2:].zfill(len)