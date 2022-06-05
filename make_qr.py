from rmqr import rMQR
from rmqr import ErrorCollectionLevel
from rmqr import QRImage


def main():
    data = "ABCdef123漢字あいうえお"
    error_collection_level = ErrorCollectionLevel.M
    qr = rMQR.fit(data, error_collection_level)
    qr.dump()
    print(qr.to_list())

    image = QRImage(qr)
    image.show()
    image.save("output/my_qr.png")


if __name__ == '__main__':
    main()
