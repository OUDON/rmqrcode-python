from rmqrcode import rMQR
from rmqrcode import ErrorCollectionLevel
from rmqrcode import QRImage


def main():
    data = "ABCdef123漢字あいうえお"
    error_collection_level = ErrorCollectionLevel.M

    # Determine rMQR version automatically
    qr = rMQR.fit(data, error_collection_level)
    qr.dump()

    # Determine rMQR version manually
    # version = 'R13x99'
    # qr = rMQR(version, error_collection_level)
    # qr.make(data)
    # qr.dump()

    # Save as png
    image = QRImage(qr)
    image.show()
    image.save("output/my_qr.png")


if __name__ == '__main__':
    main()
