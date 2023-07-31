from PIL import Image as _pilimg
import math as _mh
import random as _rd

class UserIcon():
    def __init__(self, imageBytes):
        dim = int(_mh.sqrt(len(imageBytes) / 3))
        if len(imageBytes) == dim ** 2 * 3:
            imageBytes = _pilimg.frombytes(_pilimg.RGB, (dim, dim), imageBytes).resize((1200, 1200)).tobytes()
        else:
            raise ValueError("the image isn't a square")
        self._image = imageBytes

    def bytes(self):
        return self._imagebytes
    
    def __bytes__(self):
        return self.bytes()

    def createNew():
        b = ""
        l = [[[0] * 3 for _ in range(5)] for _ in range(5)]
        color = _rd.choice([(85 * (i % 4), 85 * (i//2 % 4), 85 * (i//4 % 4)) for i in range(1, 63)])
        backcolor = _rd.choice(((0, 0, 0), (255, 255, 255)))
        for y in range(5):
            line = ""
            for x in range(5):
                n = _rd.randrange(2)
                part = ""
                for k in range(3):
                    if x <= 2:
                        if n:
                            intens = color [k]
                            intens = color [k]
                        else:
                            intens = backcolor [k]
                            intens = backcolor [k]
                    else:
                        intens = l[4 - x][y][k]
                    l[x][y][k] = intens
                    part += chr(intens)
                line += part * 240
            b += line * 240
        b = b.encode("latin1")
        return UserIcon(b)

