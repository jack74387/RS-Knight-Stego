from PIL import Image
from .rs_coder import RSCoder
from .knight import KnightTour
from .utils import set_lsb, set_lsb2

class StegoEncoder:
    def __init__(self, seed: int = 0):
        self.seed = seed
        self.rs = RSCoder()

    def encode_image(self, input_path: str, output_path: str, data: bytes):
        img = Image.open(input_path).convert('RGB')
        pixels = img.load()
        w, h = img.size
        knight = KnightTour(w, h, seed=self.seed)

        # 分組：每組 4 bytes，並補至 4 bytes
        groups = []
        for i in range(0, len(data), 4):
            block = data[i:i+4]
            if len(block) < 4:
                block = block + b'\x00' * (4 - len(block))
            groups.append(block)
        # 最後一組之後標記結束
        groups.append(b'\x00\x00\x00\x00')

        used = set()
        start = (0, 0)
        for idx, block in enumerate(groups):
            is_last = (idx == len(groups) - 1)
            encoded = self.rs.encode(block)

            data_bits = ''.join(f"{b:08b}" for b in encoded[:4])
            data_bits += '1' if is_last else '0'
            parity_bits = ''.join(f"{b:08b}" for b in encoded[4:])

            # 使用不重複的 path
            path = knight.generate_path(start[0], start[1], 12, used=used)
            used.update(path)


            # 嵌入 data bits 到前 11 pixels 的 RGB LSB
            for i, (x, y) in enumerate(path[:11]):
                r, g, b = pixels[x, y]
                for ch, bit in enumerate(data_bits[i*3:(i+1)*3]):
                    if ch == 0:
                        r = set_lsb(r, int(bit))
                    elif ch == 1:
                        g = set_lsb(g, int(bit))
                    else:
                        b = set_lsb(b, int(bit))
                pixels[x, y] = (r, g, b)

            # 嵌入 parity bits 到前 8 pixels 的 RGB LSB2
            for i, (x, y) in enumerate(path[:8]):
                r, g, b = pixels[x, y]
                for ch, bit in enumerate(parity_bits[i*3:(i+1)*3]):
                    if ch == 0:
                        r = set_lsb2(r, int(bit))
                    elif ch == 1:
                        g = set_lsb2(g, int(bit))
                    else:
                        b = set_lsb2(b, int(bit))
                pixels[x, y] = (r, g, b)

            # 更新起點
            start = path[-1]

        img.save(output_path)
        print(f"Encoded and saved to {output_path}")