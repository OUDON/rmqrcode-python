from rmqrcode import rMQR
from rmqrcode import ErrorCorrectionLevel
from rmqrcode import QRImage
from rmqrcode import FitStrategy
from rmqrcode import encoder

import logging


try:
    import numpy
    import cv2
    USE_NUMPY = True
except ImportError:
    USE_NUMPY = False


def main():
    data = "https://github.com/OUDON/rmqrcode-python"
    error_correction_level = ErrorCorrectionLevel.M
    fit_strategy = FitStrategy.BALANCED

    # Determine rMQR version automatically
    qr = rMQR.fit(data, ecc=error_correction_level, fit_strategy=fit_strategy)
    print(qr)

    # Determine rMQR version manually
    # version = 'R7x43'
    # qr = rMQR(version, error_correction_level)
    # qr.add_segment("123", encoder_class=encoder.NumericEncoder)
    # qr.add_segment("Abc", encoder_class=encoder.ByteEncoder)
    # qr.make()
    # print(qr)

    # Save as png
    image = QRImage(qr, module_size=8)
    image.show()
    image.save("my_qr.png")

    # Convert to numpy array
    if USE_NUMPY:
        img = image.get_ndarray()
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


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
