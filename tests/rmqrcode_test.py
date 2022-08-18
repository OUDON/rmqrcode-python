from rmqrcode import rMQR
from rmqrcode import ErrorCorrectionLevel
from rmqrcode import DataTooLongError
from rmqrcode import IllegalVersionError
from rmqrcode import NoSegmentError

import pytest


class TestRMQR:
    def test_fit(self):
        qr = rMQR.fit("abc")

    def test_make(self):
        qr = rMQR("R13x99", ErrorCorrectionLevel.M)
        qr.add_segment("abc")
        qr.make()

        assert len(qr.to_list(with_quiet_zone=True)) is 17
        assert len(qr.to_list(with_quiet_zone=True)[0]) is 103

        assert len(qr.to_list(with_quiet_zone=False)) is 13
        assert len(qr.to_list(with_quiet_zone=False)[0]) is 99

    def test_raise_no_segment_error(self):
        with pytest.raises(NoSegmentError) as e:
            qr = rMQR("R13x99", ErrorCorrectionLevel.M)
            qr.make()

    def test_raise_too_long_error(self):
        with pytest.raises(DataTooLongError) as e:
            s = "a".ljust(200, "a")
            rMQR.fit(s)

    def test_raise_invalid_version_error(self):
        with pytest.raises(IllegalVersionError) as e:
            qr = rMQR("not exists", ErrorCorrectionLevel.M)
