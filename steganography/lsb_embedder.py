# steganography/lsb_embedder.py
from PIL import Image

def gen_data(data: str) -> list:
    """
    將文字轉為 8-bit 二進位串列
    """
    return [format(ord(ch), '08b') for ch in data]


def embed(image: Image.Image, file_name: str) -> Image.Image:
    """
    在 image 中嵌入 message 字串至 RGB LSB
    返回新的 PIL Image
    """
    pixels = list(image.getdata())
    
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("The specified file does not exist.")

    if (len(data) == 0):
        raise ValueError('Data file is empty')
    print(f"Data length: {len(data)}")

    bins = gen_data(data)
    total_bits = len(bins) * 8
    if total_bits > len(pixels) * 3:
        raise ValueError("訊息過長，無法嵌入此圖片。")

    new_pixels = []
    bit_iter = iter(''.join(bins))
    for pix in pixels:
        r, g, b = pix[:3]
        try:
            r = (r & ~1) | int(next(bit_iter))
            g = (g & ~1) | int(next(bit_iter))
            b = (b & ~1) | int(next(bit_iter))
        except StopIteration:
            pass
        new_pixels.append((r, g, b) + pix[3:])

    stego = Image.new(image.mode, image.size)
    stego.putdata(new_pixels)
    return stego