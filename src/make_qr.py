from enums.color import Color
from enums.alignment_pattern_coordinates import AlignmentPatternCoordinates
from enums.error_collection_level import ErrorCollectionLevel
from rmqr import rMQR
from qr_image import QRImage


def make_qr(data, height, width, error_collection_level):
    qr = rMQR(height, width, error_collection_level)
    qr.make(data)
    return qr


def main():
    height, width = 15, 139
    data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    qr = make_qr(data, height, width, ErrorCollectionLevel.M)
    qr.dump()

    image = QRImage(qr)
    image.show()
    image.save("output/my_qr.png")


if __name__ == '__main__':
    main()
