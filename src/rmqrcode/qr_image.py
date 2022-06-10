from .enums.color import Color

from PIL import Image
from PIL import ImageDraw


class QRImage:
    def __init__(self, qr, module_size=10):
        self._module_size = module_size
        self._img = Image.new(
            'RGB',
            ((qr.width() + 4) * module_size, (qr.height() + 4) * module_size),
            (255, 255, 255)
        )
        self._make_image(qr)


    def show(self):
        self._img.show()
        pass


    def save(self, name):
        self._img.save(name)


    def _make_image(self, qr):
        draw = ImageDraw.Draw(self._img)
        for y in range(qr.height()):
            for x in range(qr.width()):
                r, g, b = 125, 125, 125
                if qr.value_at(x, y) == Color.BLACK:
                    r, g, b = 0, 0, 0
                elif qr.value_at(x, y) == Color.WHITE:
                    r, g, b, = 255, 255, 255
                draw.rectangle(
                    xy=((x + 2) * self._module_size, (y + 2) * self._module_size, (x + 1 + 2) * self._module_size, (y + 1 + 2) * self._module_size),
                    fill=(r, g, b)
                )