class DataTooLongError(ValueError):
    "A class represents an error raised when the given data is too long."
    pass


class IllegalVersionError(ValueError):
    "A class represents an error raised when the given version name is illegal."
    pass


class NoSegmentError(ValueError):
    "A class represents an error raised when no segments are add"
    pass
