from rmqrcode import (
    rMQR,
    encoder,
    ErrorCorrectionLevel,
    DataTooLongError,
    IllegalVersionError,
    NoSegmentError,
)

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

    def test_can_make_max_length_numeric_encoder(self):
        s = "1" * 361
        qr = rMQR("R17x139", ErrorCorrectionLevel.M)
        qr.add_segment(s, encoder_class=encoder.NumericEncoder)
        qr.make()

    def test_raise_too_long_error_numeric_encoder(self):
        with pytest.raises(DataTooLongError) as e:
            s = "1" * 362
            qr = rMQR("R17x139", ErrorCorrectionLevel.M)
            qr.add_segment(s, encoder_class=encoder.NumericEncoder)
            qr.make()

    def test_can_make_max_length_alphanumeric_encoder(self):
        s = "A" * 219
        qr = rMQR("R17x139", ErrorCorrectionLevel.M)
        qr.add_segment(s, encoder_class=encoder.AlphanumericEncoder)
        qr.make()

    def test_raise_too_long_error_alphanumeric_encoder(self):
        with pytest.raises(DataTooLongError) as e:
            s = "A" * 220
            qr = rMQR("R17x139", ErrorCorrectionLevel.M)
            qr.add_segment(s, encoder_class=encoder.AlphanumericEncoder)
            qr.make()

    def test_can_make_max_length_byte_encoder(self):
        s = "a" * 150
        qr = rMQR("R17x139", ErrorCorrectionLevel.M)
        qr.add_segment(s, encoder_class=encoder.ByteEncoder)
        qr.make()

    def test_raise_too_long_error_byte_encoder(self):
        with pytest.raises(DataTooLongError) as e:
            s = "a" * 151
            qr = rMQR("R17x139", ErrorCorrectionLevel.M)
            qr.add_segment(s, encoder_class=encoder.ByteEncoder)
            qr.make()

    def test_can_make_max_length_kanji_encoder(self):
        s = "漢" * 92
        qr = rMQR("R17x139", ErrorCorrectionLevel.M)
        qr.add_segment(s, encoder_class=encoder.KanjiEncoder)
        qr.make()

    def test_raise_too_long_error_kanji_encoder(self):
        with pytest.raises(DataTooLongError) as e:
            s = "漢" * 93
            qr = rMQR("R17x139", ErrorCorrectionLevel.M)
            qr.add_segment(s, encoder_class=encoder.KanjiEncoder)
            qr.make()

    def test_raise_too_long_error_fit(self):
        with pytest.raises(DataTooLongError) as e:
            s = "a".ljust(200, "a")
            rMQR.fit(s)

    def test_raise_invalid_version_error(self):
        with pytest.raises(IllegalVersionError) as e:
            qr = rMQR("not exists", ErrorCorrectionLevel.M)
