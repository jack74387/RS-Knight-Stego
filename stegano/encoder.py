from PIL import Image
from .rs_coder import RSCoder
from .knight import KnightTour
from .utils import set_lsb, set_lsb2

class StegoEncoder:
    """
    隱寫 4-byte data + 4-byte length 頭 → RS(7,4) → 藏於 12 pixels 中:
      - 前 11 pixels RGB LSB (3 bits/pixel) 放 32 data bits
      - 前 8 pixels RGB LSB2 (3 bits/pixel) 放 24 parity bits
    """
    def __init__(self, seed: int = 0):
        self.seed = seed
        self.rs = RSCoder()

    def encode_image(self, input_path: str, output_path: str, data: bytes):
        img = Image.open(input_path).convert('RGB')
        pixels = img.load()
        w, h = img.size
        knight = KnightTour(w, h, seed=self.seed)

        # 在資料頭加入 4-byte 長度
        length_bytes = len(data).to_bytes(4, 'big')
        data = length_bytes + data

        # 分組 4-byte
        groups = []
        for i in range(0, len(data), 4):
            block = data[i:i+4]
            if len(block) < 4:
                block += b'\x00' * (4 - len(block))
            groups.append(block)

        used = set()
        start = (0, 0)

        for block in groups:
            encoded = self.rs.encode(block)  # 7 bytes
            # 資料 bits
            data_bits = ''.join(f"{b:08b}" for b in encoded[:4])
            # parity bits
            parity_bits = ''.join(f"{b:08b}" for b in encoded[4:])

            # 取不重複的 12 pixels
            path = knight.generate_path(start[0], start[1], 12, used)
            used.update(path)

            # embed data
            for i, (x, y) in enumerate(path[:11]):
                r, g, b = pixels[x, y]
                bits = data_bits[i*3:(i+1)*3]
                for ch, bit in enumerate(bits):
                    if ch == 0: r = set_lsb(r, int(bit))
                    if ch == 1: g = set_lsb(g, int(bit))
                    if ch == 2: b = set_lsb(b, int(bit))
                pixels[x, y] = (r, g, b)

            # embed parity
            for i, (x, y) in enumerate(path[:8]):
                r, g, b = pixels[x, y]
                bits = parity_bits[i*3:(i+1)*3]
                for ch, bit in enumerate(bits):
                    if ch == 0: r = set_lsb2(r, int(bit))
                    if ch == 1: g = set_lsb2(g, int(bit))
                    if ch == 2: b = set_lsb2(b, int(bit))
                pixels[x, y] = (r, g, b)

            start = path[-1]

        img.save(output_path)
        print(f"Encoded and saved to {output_path}")