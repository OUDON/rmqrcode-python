from enums.color import Color
from enums.alignment_pattern_coordinates import AlignmentPatternCoordinates
from enums.error_collection_level import ErrorCollectionLevel
from rmqr import rMQR


def make_qr(data, height, width, error_collection_level):
    qr = rMQR(height, width, error_collection_level)
    qr.make(data)
    return qr


def main():
    height, width = 15, 139
    data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    qr = make_qr(data, height, width, ErrorCollectionLevel.M)
    qr.dump()

    # 画像へ変換
    # from PIL import Image
    # qr_img = Image.new('RGB', (width+4, height+4), (255, 255, 255))
    # for y in range(height):
    #     for x in range(width):
    #         r, g, b = 125, 125, 125
    #         if qr[y][x] == Color.BLACK:
    #             r, g, b = 0, 0, 0
    #         elif qr[y][x] == Color.WHITE:
    #             r, g, b, = 255, 255, 255
    #         qr_img.putpixel((x+2, y+2), (r, g, b))
    # qr_img.show()
    # qr_img.save("output/my_qr.png")


if __name__ == '__main__':
    main()
