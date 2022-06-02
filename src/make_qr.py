from enums.color import Color
from enums.error_collection_level import ErrorCollectionLevel
from qr_versions import qr_versions

def print_qr(qr):
    h = len(qr)
    w = len(qr[0])

    show = {}
    show[Color.WHITE] = "_"
    show[Color.BLACK] = "X"
    show[Color.UNDEFINED] = "?"
    print("QRコード:")
    for i in range(h):
        for j in range(w):
            print(show[qr[i][j]], end="")
        print("")


def version_name(height, width):
    return f"R{height}x{width}"


def msb(n):
    return len(bin(n)) - 2


def compute_bch(data):
    data <<= 12
    g = 1<<12 | 1<<11 | 1<<10 | 1<<9 | 1<<8 | 1<<5 | 1<<2 | 1<<0

    tmp_data = data
    while (msb(tmp_data) >= 13):
        multiple = msb(tmp_data) - 13
        tmp_g = g << multiple
        tmp_data ^= tmp_g
    return tmp_data


def compute_version_info(height, width, error_collection_level):
    version_information_data = qr_versions[version_name(height, width)]['version_indicator']
    if error_collection_level == ErrorCollectionLevel.H:
        version_information_data |= 1<<6
    reminder_polynomial = compute_bch(version_information_data)
    version_information_data = version_information_data<<12 | reminder_polynomial
    return version_information_data


def put_pattern_information_finder_pattern_side(qr, data):
    mask = 0b011111101010110010
    data ^= mask

    si, sj = 1, 8
    for n in range(18):
        di = n % 5
        dj = n // 5
        qr[si+di][sj+dj] = Color.BLACK if data>>n & 1 else Color.WHITE


def put_pattern_information_finder_sub_pattern_side(qr, height, width, data):
    mask = 0b100000101001111011
    data ^= mask

    si, sj = height - 1 - 5, width - 1 - 7
    for n in range(15):
        di = n % 5
        dj = n // 5
        qr[si+di][sj+dj] = Color.BLACK if data>>n & 1 else Color.WHITE
    qr[height-1-5][width-1-4] = Color.BLACK if data>>n & 15 else Color.WHITE
    qr[height-1-5][width-1-3] = Color.BLACK if data>>n & 16 else Color.WHITE
    qr[height-1-5][width-1-2] = Color.BLACK if data>>n & 17 else Color.WHITE



def put_pattern_information(qr, height, width, error_collection_level):
    version_information = compute_version_info(height, width, error_collection_level)
    put_pattern_information_finder_pattern_side(qr, version_information)
    put_pattern_information_finder_sub_pattern_side(qr, height, width, version_information)


def make_qr(height, width, error_collection_level):
    qr = [[Color.UNDEFINED for i in range(width)] for j in range(height)]

    # Finder pattern
    # 周囲
    for i in range(7):
        for j in range(7):
            if i == 0 or i == 6 or j == 0 or j == 6:
                qr[i][j] = Color.BLACK
            else:
                qr[i][j] = Color.WHITE

    # 真ん中
    for i in range(3):
        for j in range(3):
            qr[2+i][2+j] = Color.BLACK

    # Separator
    for n in range(8):
        if n < height:
            qr[n][7] = Color.WHITE

        if height >= 9:
            qr[7][n] = Color.WHITE

    # Finder sub pattern
    # 周囲
    for i in range(5):
        for j in range(5):
            color = Color.BLACK if i == 0 or i == 4 or j == 0 or j == 4 else Color.WHITE
            qr[height-i-1][width-j-1] = color

    # 真ん中
    qr[height-1-2][width-1-2] = Color.BLACK

    # Corner finder pattern
    # 左下
    qr[height-1][0] = Color.BLACK
    qr[height-1][1] = Color.BLACK
    qr[height-1][2] = Color.BLACK

    # 右上
    qr[0][width-1] = Color.BLACK
    qr[0][width-2] = Color.BLACK
    qr[1][width-1] = Color.BLACK
    qr[1][width-2] = Color.WHITE

    # Alignment pattern
    for i in range(3):
        for j in range(3):
            color = Color.BLACK if i == 0 or i == 2 or j == 0 or j == 2 else Color.WHITE
            qr[i][width//2+j] = color
            qr[height-1-i][width//2+j] = color

    # Timing pattern
    # 横
    for j in range(width):
        color = Color.BLACK if (j + 1) % 2 else Color.WHITE
        for i in [0, height - 1]:
            if qr[i][j] == Color.UNDEFINED:
                qr[i][j] = color

    # 縦
    for i in range(height):
        color = Color.BLACK if (i + 1) % 2 else Color.WHITE
        for j in [0, width//2+1, width-1]:
            if qr[i][j] == Color.UNDEFINED:
                qr[i][j] = color

    put_pattern_information(qr, height, width, error_collection_level)
    return qr


def main():
    qr = make_qr(17, 77, ErrorCollectionLevel.M)
    print_qr(qr)


if __name__ == '__main__':
    main()
