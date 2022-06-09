from rmqrcode import rMQR
from rmqrcode import ErrorCorrectionLevel
from rmqrcode import QRImage
from rmqrcode import FitStrategy


def main():
    data = "https://oudon.xyz"
    error_correction_level = ErrorCorrectionLevel.M
    fit_strategy = FitStrategy.BALANCED

    # Determine rMQR version automatically
    qr = rMQR.fit(data, error_correction_level, fit_strategy=fit_strategy)
    qr.dump()

    # Determine rMQR version manually
    # version = 'R13x99'
    # qr = rMQR(version, error_correction_level)
    # qr.make(data)
    # qr.dump()

    # Save as png
    image = QRImage(qr)
    image.show()
    image.save("my_qr.png")


if __name__ == '__main__':
    main()
