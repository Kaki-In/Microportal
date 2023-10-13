from PIL import Image as _pilimg
import math as _mh
import random as _rd
import base64 as _b64
import io as _io

def _pngToPillow(png):
    b = _io.BytesIO(png)

    image = _pilimg.open(b)
    return image.tobytes()

def _pillowToPng(pillow, dim):
    b = _io.BytesIO()

    image = _pilimg.frombytes("RGB", (dim, dim), pillow)
    image.save(b, "PNG")
    b.seek(0)
    return b.getvalue()

class UserIcon():
    def __init__(self, imageBytes):
        pill = _pngToPillow(imageBytes)
        dim = int(_mh.sqrt(len(pill) / 3))
        if len(pill) == dim ** 2 * 3:
            imageBytes = _pillowToPng(_pilimg.frombytes('RGB', (dim, dim), pill).resize((120, 120)).tobytes(), 120)
        else:
            raise ValueError("the image isn't a square")
        self._image = imageBytes

    def bytes(self):
        return self._image
    
    def __bytes__(self):
        return self.bytes()
    
    def createNew():
        b = ""
        colors = [(85 * (i % 4), 85 * (i//2 % 4), 85 * (i//4 % 4)) for i in range(64)]

        color = _rd.choice(colors)
        colors.remove(color)
        backcolor = _rd.choice(colors)
        l = [[[0] * 3 for _ in range(7)] for _ in range(7)]

        for y in range(7):
            line = ""
            for x in range(7):
                n = _rd.randrange(2)
                part = ""
                for k in range(3):
                    if x <= 3:
                        if 0 < x < 6 and 0 < y < 6:
                            if n:
                                intens = color [k]
                                intens = color [k]
                            else:
                                intens = backcolor [k]
                                intens = backcolor [k]
                        else:
                            intens = backcolor [k]
                    else:
                        intens = l[6 - x][y][k]
                    l[x][y][k] = intens
                    part += chr(intens)
                line += part * 50
            b += line * 50
        b = b.encode("latin1")
        return UserIcon(_pillowToPng(b, 350))

    def toJson(self):
        return _b64.b64encode(self._image).decode()
    
    def fromJson(json):
        return UserIcon(_b64.b64decode(json))
