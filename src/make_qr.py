from enums.color import Color
from enums.error_collection_level import ErrorCollectionLevel
from enums.generator_polynomials import GeneratorPolynomials
from enums.alignment_pattern_coordinates import AlignmentPatternCoordinates
from qr_versions import qr_versions
from math import compute_bch, compute_reed_solomon
from encoder.byte_encoder import ByteEncoder

def print_qr(qr):
    h = len(qr)
    w = len(qr[0])

    show = {}
    show[Color.WHITE] = "_"
    show[Color.BLACK] = "X"
    show[Color.UNDEFINED] = "?"
    print(f"QRコード R{h}x{w}:")
    for i in range(h):
        for j in range(w):
            if qr[i][j] in show:
                print(show[qr[i][j]], end="")
            else:
                print(qr[i][j], end="")
        print("")


def version_name(height, width):
    return f"R{height}x{width}"


def compute_version_info(height, width, error_collection_level):
    version_information_data = qr_versions[version_name(height, width)]['version_indicator']
    if error_collection_level == ErrorCollectionLevel.H:
        version_information_data |= 1<<6
    reminder_polynomial = compute_bch(version_information_data)
    version_information_data = version_information_data<<12 | reminder_polynomial
    return version_information_data


def put_finder_pattern(qr, height, width):
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


def put_corner_finder_pattern(qr, height, width):
    # Corner finder pattern
    # 左下
    qr[height-1][0] = Color.BLACK
    qr[height-1][1] = Color.BLACK
    qr[height-1][2] = Color.BLACK

    if height >= 11:
        qr[height-2][0] = Color.BLACK
        qr[height-2][1] = Color.WHITE

    # 右上
    qr[0][width-1] = Color.BLACK
    qr[0][width-2] = Color.BLACK
    qr[1][width-1] = Color.BLACK
    qr[1][width-2] = Color.WHITE


def put_alignment_pattern(qr, height, width):
    # Alignment pattern
    center_xs = AlignmentPatternCoordinates[width]
    for center_x in center_xs:
        for i in range(3):
            for j in range(3):
                color = Color.BLACK if i == 0 or i == 2 or j == 0 or j == 2 else Color.WHITE
                # 上側
                qr[i][center_x + j - 1] = color
                # 下側
                qr[height-1-i][center_x + j - 1] = color


def put_timing_pattern(qr, height, width):
    # Timing pattern
    # 横
    for j in range(width):
        color = Color.BLACK if (j + 1) % 2 else Color.WHITE
        for i in [0, height - 1]:
            if qr[i][j] == Color.UNDEFINED:
                qr[i][j] = color

    # 縦
    center_xs = [0, width - 1]
    center_xs.extend(AlignmentPatternCoordinates[width])
    for i in range(height):
        color = Color.BLACK if (i + 1) % 2 else Color.WHITE
        for j in center_xs:
            if qr[i][j] == Color.UNDEFINED:
                qr[i][j] = color


def put_version_information(qr, height, width, error_collection_level):
    version_information = compute_version_info(height, width, error_collection_level)
    put_version_information_finder_pattern_side(qr, version_information)
    put_version_information_finder_sub_pattern_side(qr, height, width, version_information)


def put_version_information_finder_pattern_side(qr, data):
    mask = 0b011111101010110010
    data ^= mask

    si, sj = 1, 8
    for n in range(18):
        di = n % 5
        dj = n // 5
        qr[si+di][sj+dj] = Color.BLACK if data>>n & 1 else Color.WHITE


def put_version_information_finder_sub_pattern_side(qr, height, width, data):
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


def convert_to_bites_data(data, character_count_length, codewords_total):
    encoded_data = ByteEncoder().encode(data, character_count_length)

    # 付加できるなら終端文字を付け加える
    if len(encoded_data) + 3 <= codewords_total * 8:
        encoded_data += "000"

    return encoded_data


def split_into_8bits(data):
    codewords = []
    while (len(data) >= 8):
        codewords.append(data[:8])
        data = data[8:]
    if data != "":
        codewords.append(data.ljust(8, '0'))
    return codewords


def split_into_blocks(codewords, blocks_definition):
    data_idx, error_idx = 0, 0
    data_codewords_per_block = []
    rs_codewords_per_block = []
    for block_definition in blocks_definition:
        for i in range(block_definition['num']):
            data_codewords_num = block_definition['k']
            rs_codewords_num = block_definition['c'] - block_definition['k']
            g = GeneratorPolynomials[rs_codewords_num]

            # print('----------')
            # print(f"D{data_idx} to D{data_idx + data_codewords_num - 1}")
            # print(f"E{error_idx} to D{error_idx + rs_codewords_num - 1}")

            codewords_in_block = codewords[data_idx : data_idx + data_codewords_num]
            rs_codewords_in_block = compute_reed_solomon(codewords_in_block, g, rs_codewords_num)

            data_codewords_per_block.append(codewords_in_block)
            rs_codewords_per_block.append(rs_codewords_in_block)

            data_idx += data_codewords_num
            error_idx += rs_codewords_num

            # print(f"codewords in block = {codewords_in_block}, len = {len(codewords_in_block)}")
            # print(f"rs_codewords in block = {rs_codewords_in_block}, len = {len(rs_codewords_in_block)}")
    return data_codewords_per_block, rs_codewords_per_block


def put_data(qr, height, width, error_collection_level, data):
    qr_version = qr_versions[version_name(height, width)]

    character_count_length = qr_version['character_count_length']
    codewords_total = qr_version['codewords_total']
    encoded_data = convert_to_bites_data(data, character_count_length, codewords_total)
    codewords = split_into_8bits(encoded_data)

    # codeword数に満たない場合は規定の文字列を付与する
    while True:
        if len(codewords) >= codewords_total:
            break
        codewords.append("11101100")
        if len(codewords) >= codewords_total:
            break
        codewords.append("00010001")

    data_codewords_per_block, rs_codewords_per_block = split_into_blocks(
        codewords,
        qr_version['blocks'][error_collection_level]
    )
    # print("==============")
    # print(f"data_codewords_per_block = {data_codewords_per_block}")
    # print(f"rs_codewords_per_block = {rs_codewords_per_block}")

    # データの並び替え
    # Data codewords
    final_codewords = []
    for i in range(len(data_codewords_per_block[-1])):
        for data_codewords in data_codewords_per_block:
            if i >= len(data_codewords):
                continue
            final_codewords.append(data_codewords[i])
            print(f"Put QR data codeword {i} : {data_codewords[i]}")

    # RS Codewords
    for i in range(len(rs_codewords_per_block[-1])):
        for rs_codewords in rs_codewords_per_block:
            if i >= len(rs_codewords):
                continue
            final_codewords.append(rs_codewords[i])
            print(f"Put RS data codewords {i} : {rs_codewords[i]}")

    # 配置
    dy = -1 # 最初は上方向
    current_codeword_idx = 0
    current_bit_idx = 0
    cx, cy = width - 2, height - 6
    while True:
        for x in [cx, cx-1]:
            if qr[cy][x] == Color.UNDEFINED:
                qr[cy][x] = Color.BLACK if final_codewords[current_codeword_idx][current_bit_idx] == '1' else Color.WHITE
                # qr[cy][x] = chr(ord('A') + current_codeword_idx)
                current_bit_idx += 1
                if current_bit_idx == 8:
                    current_bit_idx = 0
                    current_codeword_idx += 1
                    if current_codeword_idx == len(final_codewords):
                        break
        if current_codeword_idx == len(final_codewords):
            break
        if dy < 0 and cy == 1:
            cx -= 2
            dy = 1
        elif dy > 0 and cy == height - 1 - 1:
            cx -= 2
            dy = -1
        else:
            cy += dy



def make_qr(height, width, error_collection_level):
    qr = [[Color.UNDEFINED for i in range(width)] for j in range(height)]
    put_finder_pattern(qr, height, width)
    put_corner_finder_pattern(qr, height, width)
    put_alignment_pattern(qr, height, width)
    put_timing_pattern(qr, height, width)
    put_version_information(qr, height, width, error_collection_level)
    put_data(qr, height, width, error_collection_level, "HelloWorld");
    return qr


def main():
    qr = make_qr(13, 99, ErrorCollectionLevel.H)
    print_qr(qr)
    qr = make_qr(7, 59, ErrorCollectionLevel.H)
    print_qr(qr)
    qr = make_qr(13, 59, ErrorCollectionLevel.H)
    print_qr(qr)


if __name__ == '__main__':
    main()
