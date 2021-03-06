from rmqrcode import rMQR
from rmqrcode import ErrorCorrectionLevel
from rmqrcode import QRImage
from rmqrcode import FitStrategy

import logging


def main():
    data = "https://oudon.xyz"
    error_correction_level = ErrorCorrectionLevel.M
    fit_strategy = FitStrategy.BALANCED

    # Determine rMQR version automatically
    qr = rMQR.fit(data, ecc=error_correction_level, fit_strategy=fit_strategy)
    print(qr)

    # Determine rMQR version manually
    # version = 'R13x99'
    # qr = rMQR(version, error_correction_level)
    # qr.make(data)
    # print(qr)

    # Save as png
    image = QRImage(qr, module_size=8)
    image.show()
    image.save("my_qr.png")


def _init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    logger = _init_logger()
    main()
