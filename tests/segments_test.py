from rmqrcode.segments import SegmentOptimizer, compute_length
from rmqrcode import encoder, ErrorCorrectionLevel, DataTooLongError
import pytest


class TestSegments:
    def test_can_optimize_segments_numeric_and_byte(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("123Abc", "R7x43", ErrorCorrectionLevel.M)
        assert segments == [
            {"data": "123", "encoder_class": encoder.NumericEncoder},
            {"data": "Abc", "encoder_class": encoder.ByteEncoder},
        ]

    def test_can_optimize_segments_alphanumeric_and_kanji(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("17:30集合", "R7x59", ErrorCorrectionLevel.M)
        assert segments == [
            {"data": "17:30", "encoder_class": encoder.AlphanumericEncoder},
            {"data": "集合", "encoder_class": encoder.KanjiEncoder},
        ]

    def test_can_optimize_segments_numeric_only(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("123456", "R7x59", ErrorCorrectionLevel.M)
        assert segments == [
            {"data": "123456", "encoder_class": encoder.NumericEncoder},
        ]

    def test_can_optimize_segments_alphanumeric_only(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("HTTPS://", "R7x59", ErrorCorrectionLevel.M)
        assert segments == [
            {"data": "HTTPS://", "encoder_class": encoder.AlphanumericEncoder},
        ]

    def test_can_optimize_segments_byte_only(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("1+zY!a:K", "R7x59", ErrorCorrectionLevel.M)
        assert segments == [
            {"data": "1+zY!a:K", "encoder_class": encoder.ByteEncoder},
        ]

    def test_can_optimize_segments_kanji_only(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("漢字", "R7x59", ErrorCorrectionLevel.M)
        assert segments == [
            {"data": "漢字", "encoder_class": encoder.KanjiEncoder},
        ]

    def test_optimize_segments_raises_data_too_long_error(self):
        optimizer = SegmentOptimizer()
        with pytest.raises(DataTooLongError) as e:
            segments = optimizer.compute("a" * 12, "R7x59", ErrorCorrectionLevel.M)

    def test_compute_length(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("123Abc", "R7x43", ErrorCorrectionLevel.M)
        assert compute_length(segments, "R7x43") is 47
