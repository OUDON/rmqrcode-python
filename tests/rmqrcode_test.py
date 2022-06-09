from rmqrcode import rMQR
from rmqrcode import ErrorCorrectionLevel
from rmqrcode import DataTooLongError
from rmqrcode import IllegalVersionError

import pytest


class TestRMQR:
    def test_fit(self):
        qr = rMQR.fit("abc")

    def test_make(self):
        qr = rMQR('R13x99', ErrorCorrectionLevel.M)
        qr.make("abc")

    def test_raise_too_long_error(self):
        with pytest.raises(DataTooLongError) as e:
            s = "a".ljust(200, "a")
            rMQR.fit(s)

    def test_raise_invalid_version_error(self):
        with pytest.raises(IllegalVersionError) as e:
            qr = rMQR("not exists", ErrorCorrectionLevel.M)
