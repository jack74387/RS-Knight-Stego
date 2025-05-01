# steganography/lsb_extractor.py
from PIL import Image

def extract(image: Image.Image, length: int) -> str:
    """
    從 image 提取 length 字元的隱藏訊息
    """
    pixels = list(image.getdata())
    bits = []
    for pix in pixels:
        bits.append(str(pix[0] & 1))
        bits.append(str(pix[1] & 1))
        bits.append(str(pix[2] & 1))
        if len(bits) >= length * 8:
            break

    message = ''
    for i in range(length):
        byte = bits[i*8:(i+1)*8]
        message += chr(int(''.join(byte), 2))
    return message