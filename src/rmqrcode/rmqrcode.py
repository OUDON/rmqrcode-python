from .format.error_correction_level import ErrorCorrectionLevel
from .format.qr_versions import qr_versions
from .format.data_capacities import data_capacities
from .format.alignment_pattern_coordinates import AlignmentPatternCoordinates
from .format.generator_polynomials import GeneratorPolynomials
from .format.mask import mask

from .encoder.byte_encoder import ByteEncoder
from .util.error_correction import compute_bch, compute_reed_solomon
from .util.utilities import split_into_8bits
from .enums.color import Color
from .enums.fit_strategy import FitStrategy

import logging

class rMQR:
    @staticmethod
    def _init_logger():
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.NullHandler())
        logger.setLevel(logging.DEBUG)
        logger.propagate = True
        return logger


    @staticmethod
    def fit(data,ecc=ErrorCorrectionLevel.M, fit_strategy=FitStrategy.BALANCED):
        logger = rMQR._init_logger()

        data_length = ByteEncoder.length(data)
        ok_versions = []
        determined_width = set()
        determined_height = set()

        logger.debug("Select rMQR Code version")
        for version_name, qr_version in data_capacities.items():
            if data_length <= qr_version['capacity']['Byte'][ecc]:
                width, height = qr_version['width'], qr_version['height']
                if not width in determined_width and not height in determined_height:
                    determined_width.add(width)
                    determined_height.add(height)
                    ok_versions.append({
                        'version': version_name,
                        'width': width,
                        'height': height,
                    })
                    logger.debug(f"ok: {version_name}")

        if len(ok_versions) == 0:
            raise DataTooLongError("The data is too long.")

        if fit_strategy == FitStrategy.MINIMIZE_WIDTH:
            sort_key = lambda x: x['width']
        elif fit_strategy == FitStrategy.MINIMIZE_HEIGHT:
            sort_key = lambda x: x['height']
        elif fit_strategy == FitStrategy.BALANCED:
            sort_key = lambda x: x['height'] * 9 + x['width']
        selected = sorted(ok_versions, key=sort_key)[0]
        logger.debug(f"selected: {selected}")

        qr = rMQR(selected['version'], ecc)
        qr.make(data)
        return qr


    def __init__(self, version, ecc, logger=None):
        self._logger = logger or rMQR._init_logger()

        if not rMQR.validate_version(version):
            raise IllegalVersionError("The rMQR version is illegal.")

        qr_version = qr_versions[version]
        self._version = version
        self._height = qr_version['height']
        self._width = qr_version['width']
        self._error_correction_level = ecc
        self._qr = [[Color.UNDEFINED for x in range(self._width)] for y in range(self._height)]


    def make(self, data):
        self._put_finder_pattern()
        self._put_corner_finder_pattern()
        self._put_alignment_pattern()
        self._put_timing_pattern()
        self._put_version_information()
        mask_area = self._put_data(data);
        self._apply_mask(mask_area)


    def version_name(self):
        return f"R{self._height}x{self._width}"


    def size(self):
        return (self.width(), self.height())


    def height(self):
        return self._height


    def width(self):
        return self._width


    def value_at(self, x, y):
        return self._qr[y][x]


    def to_list(self):
        return [list(map(lambda x: 1 if x == Color.BLACK else 0, column)) for column in self._qr]


    def __str__(self):
        res = ""

        show = {}
        show[Color.WHITE] = "_"
        show[Color.BLACK] = "X"
        show[Color.UNDEFINED] = "?"
        show[True] = "X"
        show[False] = "_"

        res += f"rMQR Version R{self._height}x{self._width}:\n"
        for i in range(self._height):
            for j in range(self._width):
                if self._qr[i][j] in show:
                    res += show[self._qr[i][j]]
                else:
                    res += self._qr[i][j]
            res += "\n"
        return res


    def _put_finder_pattern(self):
        # Finder pattern
        # 周囲
        for i in range(7):
            for j in range(7):
                if i == 0 or i == 6 or j == 0 or j == 6:
                    self._qr[i][j] = Color.BLACK
                else:
                    self._qr[i][j] = Color.WHITE

        # 真ん中
        for i in range(3):
            for j in range(3):
                self._qr[2+i][2+j] = Color.BLACK

        # Separator
        for n in range(8):
            if n < self._height:
                self._qr[n][7] = Color.WHITE

            if self._height >= 9:
                self._qr[7][n] = Color.WHITE

        # Finder sub pattern
        # 周囲
        for i in range(5):
            for j in range(5):
                color = Color.BLACK if i == 0 or i == 4 or j == 0 or j == 4 else Color.WHITE
                self._qr[self._height-i-1][self._width-j-1] = color

        # 真ん中
        self._qr[self._height-1-2][self._width-1-2] = Color.BLACK


    def _put_corner_finder_pattern(self):
        # Corner finder pattern
        # 左下
        self._qr[self._height-1][0] = Color.BLACK
        self._qr[self._height-1][1] = Color.BLACK
        self._qr[self._height-1][2] = Color.BLACK

        if self._height >= 11:
            self._qr[self._height-2][0] = Color.BLACK
            self._qr[self._height-2][1] = Color.WHITE

        # 右上
        self._qr[0][self._width-1] = Color.BLACK
        self._qr[0][self._width-2] = Color.BLACK
        self._qr[1][self._width-1] = Color.BLACK
        self._qr[1][self._width-2] = Color.WHITE


    def _put_alignment_pattern(self):
        # Alignment pattern
        center_xs = AlignmentPatternCoordinates[self._width]
        for center_x in center_xs:
            for i in range(3):
                for j in range(3):
                    color = Color.BLACK if i == 0 or i == 2 or j == 0 or j == 2 else Color.WHITE
                    # 上側
                    self._qr[i][center_x + j - 1] = color
                    # 下側
                    self._qr[self._height-1-i][center_x + j - 1] = color


    def _put_timing_pattern(self):
        # Timing pattern
        # 横
        for j in range(self._width):
            color = Color.BLACK if (j + 1) % 2 else Color.WHITE
            for i in [0, self._height - 1]:
                if self._qr[i][j] == Color.UNDEFINED:
                    self._qr[i][j] = color

        # 縦
        center_xs = [0, self._width - 1]
        center_xs.extend(AlignmentPatternCoordinates[self._width])
        for i in range(self._height):
            color = Color.BLACK if (i + 1) % 2 else Color.WHITE
            for j in center_xs:
                if self._qr[i][j] == Color.UNDEFINED:
                    self._qr[i][j] = color


    def _put_version_information(self):
        version_information = self._compute_version_info()
        self._put_version_information_finder_pattern_side(version_information)
        self._put_version_information_finder_sub_pattern_side(version_information)


    def _put_version_information_finder_pattern_side(self, version_information):
        mask = 0b011111101010110010
        version_information ^= mask

        si, sj = 1, 8
        for n in range(18):
            di = n % 5
            dj = n // 5
            self._qr[si+di][sj+dj] = Color.BLACK if version_information>>n & 1 else Color.WHITE


    def _put_version_information_finder_sub_pattern_side(self, version_information):
        mask = 0b100000101001111011
        version_information ^= mask

        si, sj = self._height - 1 - 5, self._width - 1 - 7
        for n in range(15):
            di = n % 5
            dj = n // 5
            self._qr[si+di][sj+dj] = Color.BLACK if version_information>>n & 1 else Color.WHITE
        self._qr[self._height-1-5][self._width-1-4] = Color.BLACK if version_information>>15 & 1 else Color.WHITE
        self._qr[self._height-1-5][self._width-1-3] = Color.BLACK if version_information>>16 & 1 else Color.WHITE
        self._qr[self._height-1-5][self._width-1-2] = Color.BLACK if version_information>>17 & 1 else Color.WHITE


    def _compute_version_info(self):
        qr_version = qr_versions[self.version_name()]
        version_information_data = qr_version['version_indicator']
        if self._error_correction_level == ErrorCorrectionLevel.H:
            version_information_data |= 1<<6
        reminder_polynomial = compute_bch(version_information_data)
        version_information_data = version_information_data<<12 | reminder_polynomial
        return version_information_data


    def _put_data(self, data):
        qr_version = qr_versions[self.version_name()]

        character_count_length = qr_version['character_count_length']
        codewords_total = qr_version['codewords_total']
        encoded_data = self._convert_to_bites_data(data, character_count_length, codewords_total)
        codewords = split_into_8bits(encoded_data)

        # codeword数に満たない場合は規定の文字列を付与する
        while True:
            if len(codewords) >= codewords_total:
                break
            codewords.append("11101100")
            if len(codewords) >= codewords_total:
                break
            codewords.append("00010001")

        data_codewords_per_block, rs_codewords_per_block = self._split_into_blocks(
            codewords,
            qr_version['blocks'][self._error_correction_level]
        )

        # データの並び替え
        # Data codewords
        final_codewords = []
        for i in range(len(data_codewords_per_block[-1])):
            for data_codewords in data_codewords_per_block:
                if i >= len(data_codewords):
                    continue
                final_codewords.append(data_codewords[i])
                self._logger.debug(f"Put QR data codeword {i} : {data_codewords[i]}")

        # RS Codewords
        for i in range(len(rs_codewords_per_block[-1])):
            for rs_codewords in rs_codewords_per_block:
                if i >= len(rs_codewords):
                    continue
                final_codewords.append(rs_codewords[i])
                self._logger.debug(f"Put RS data codewords {i} : {rs_codewords[i]}")

        # 配置
        dy = -1 # 最初は上方向
        current_codeword_idx = 0
        current_bit_idx = 0
        cx, cy = self._width - 2, self._height - 6
        remainder_bits = qr_version['remainder_bits']
        mask_area = [[False for i in range(self._width)] for j in range(self._height)]

        while True:
            for x in [cx, cx-1]:
                if self._qr[cy][x] == Color.UNDEFINED:
                    # 空白のセルのみ処理する
                    if current_codeword_idx == len(final_codewords):
                        # codewordsを配置しきった場合はremainder_bitsがあれば配置する
                        self._qr[cy][x] = Color.WHITE
                        mask_area[cy][x] = True
                        remainder_bits -= 1
                    else:
                        # codewordsを配置する
                        self._qr[cy][x] = Color.BLACK if final_codewords[current_codeword_idx][current_bit_idx] == '1' else Color.WHITE
                        mask_area[cy][x] = True
                        current_bit_idx += 1
                        if current_bit_idx == 8:
                            current_bit_idx = 0
                            current_codeword_idx += 1

                    # codewordsの配置が終わりremainder_bitsも残っていなければ終了
                    if current_codeword_idx == len(final_codewords) and remainder_bits == 0:
                        break

            # codewordsの配置が終わりremainder_bitsも残っていなければ終了
            if current_codeword_idx == len(final_codewords) and remainder_bits == 0:
                break

            # 座標の更新
            if dy < 0 and cy == 1:
                cx -= 2
                dy = 1
            elif dy > 0 and cy == self._height - 1 - 1:
                cx -= 2
                dy = -1
            else:
                cy += dy

        return mask_area


    def _split_into_blocks(self, codewords, blocks_definition):
        data_idx, error_idx = 0, 0
        data_codewords_per_block = []
        rs_codewords_per_block = []
        for block_definition in blocks_definition:
            for i in range(block_definition['num']):
                data_codewords_num = block_definition['k']
                rs_codewords_num = block_definition['c'] - block_definition['k']
                g = GeneratorPolynomials[rs_codewords_num]

                codewords_in_block = codewords[data_idx : data_idx + data_codewords_num]
                rs_codewords_in_block = compute_reed_solomon(codewords_in_block, g, rs_codewords_num)

                data_codewords_per_block.append(codewords_in_block)
                rs_codewords_per_block.append(rs_codewords_in_block)

                data_idx += data_codewords_num
                error_idx += rs_codewords_num

        return data_codewords_per_block, rs_codewords_per_block


    def _convert_to_bites_data(self, data, character_count_length, codewords_total):
        encoded_data = ByteEncoder.encode(data, character_count_length)

        # 付加できるなら終端文字を付け加える
        if len(encoded_data) + 3 <= codewords_total * 8:
            encoded_data += "000"

        return encoded_data


    def _apply_mask(self, mask_area):
        for y in range(self._height):
            for x in range(self._width):
                if not mask_area[y][x]:
                    continue
                if mask(x, y):
                    if self._qr[y][x] == Color.BLACK:
                        self._qr[y][x] = Color.WHITE
                    elif self._qr[y][x] == Color.WHITE:
                        self._qr[y][x] = Color.BLACK


    @staticmethod
    def validate_version(version_name):
        return version_name in qr_versions


class DataTooLongError(ValueError):
    pass


class IllegalVersionError(ValueError):
    pass