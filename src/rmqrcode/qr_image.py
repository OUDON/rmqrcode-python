from .enums.color import Color

from PIL import Image


class QRImage:
    def __init__(self, qr):
        self._img = Image.new('RGB', (qr.width() + 4, qr.height() + 4), (255, 255, 255))
        self._make_image(qr)


    def show(self):
        self._img.show()
        pass


    def save(self, name):
        self._img.save(name)


    def _make_image(self, qr):
        for y in range(qr.height()):
            for x in range(qr.width()):
                r, g, b = 125, 125, 125
                if qr.value_at(x, y) == Color.BLACK:
                    r, g, b = 0, 0, 0
                elif qr.value_at(x, y) == Color.WHITE:
                    r, g, b, = 255, 255, 255
                self._img.putpixel((x+2, y+2), (r, g, b))