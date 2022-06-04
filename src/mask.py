from enums.color import Color

def mask(x, y):
    return (y//2 + x//3) % 2 == 0

def apply_mask(qr, mask_area, height, width):
    for y in range(height):
        for x in range(width):
            if not mask_area[y][x]:
                continue
            if mask(x, y):
                if qr[y][x] == Color.BLACK:
                    qr[y][x] = Color.WHITE
                elif qr[y][x] == Color.WHITE:
                    qr[y][x] = Color.BLACK
            # qr[y][x] = 'B' if mask(x, y) else 'W'