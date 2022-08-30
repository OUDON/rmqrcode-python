from rmqrcode.segments import SegmentOptimizer, compute_length
from rmqrcode import encoder
import pytest


class TestSegments:
    def test_can_optimize_segments(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("123Abc", "R7x43")
        assert segments == [
            {"data": "123", "encoder_class": encoder.NumericEncoder},
            {"data": "Abc", "encoder_class": encoder.ByteEncoder},
        ]

    def test_compute_length(self):
        optimizer = SegmentOptimizer()
        segments = optimizer.compute("123Abc", "R7x43")
        assert compute_length(segments, "R7x43") is 47
