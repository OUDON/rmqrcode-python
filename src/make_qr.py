from enums.color import Color
from rmqr import rMQR, ErrorCollectionLevel
from encoder.byte_encoder import ByteEncoder
from qr_image import QRImage


def main():
    data = "ABCdef123漢字あいうえお"
    error_collection_level = ErrorCollectionLevel.M
    qr = rMQR.fit(data, error_collection_level)
    qr.dump()

    image = QRImage(qr)
    image.show()
    image.save("output/my_qr.png")


if __name__ == '__main__':
    main()
