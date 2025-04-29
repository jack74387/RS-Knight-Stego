from PIL import Image
from .rs_coder import RSCoder
from .knight import KnightTour
from .utils import set_lsb, set_lsb2

class StegoEncoder:
    """
    將 4 bytes 資料 + 1-bit 結束標誌，與 3 bytes parity 分別隱藏於
    12 個 pixels 中：
      - 前 11 pixels 的 RGB LSB (3 bits/pixel) 放 4 bytes data + 1-bit end_flag
      - 前 8 pixels 的 RGB LSB2 (3 bits/pixel) 放 3 bytes parity
      - 第 12 pixel 不動
    """
    def __init__(self, seed: int = 0):
        self.seed = seed
        self.rs = RSCoder()

    def encode_image(self, input_path: str, output_path: str, data: bytes):
        img = Image.open(input_path).convert('RGB')
        pixels = img.load()
        w,h = img.size
        knight = KnightTour(w, h, seed=self.seed)

        # 分組：每組 4 bytes
        groups = [data[i:i+4] for i in range(0, len(data), 4)]
        # 最後一組後加一個結束空組
        groups.append(b'\x00\x00\x00\x00')

        start = (0,0)
        for idx, block in enumerate(groups):
            is_last = (idx == len(groups)-1)
            # RS 編碼
            encoded = self.rs.encode(block)
            # 資料 bits: 前4 bytes = 32 bits
            data_bits = ''.join(f"{b:08b}" for b in encoded[:4])
            data_bits += '1' if is_last else '0'
            # parity bits: 3 bytes = 24 bits
            parity_bits = ''.join(f"{b:08b}" for b in encoded[4:])

            # 選12個pixels
            path = knight.generate_path(start[0], start[1], 12)
            # embed data
            for i, (x,y) in enumerate(path[:11]):
                r,g,b = pixels[x,y]
                # 分3 channel 嵌入 data_bits
                for ch, bit in enumerate(data_bits[i*3:(i+1)*3]):
                    if ch==0:
                        r = set_lsb(r, int(bit))
                    elif ch==1:
                        g = set_lsb(g, int(bit))
                    else:
                        b = set_lsb(b, int(bit))
                pixels[x,y] = (r,g,b)
            # embed parity
            for i, (x,y) in enumerate(path[:8]):
                r,g,b = pixels[x,y]
                for ch, bit in enumerate(parity_bits[i*3:(i+1)*3]):
                    if ch==0:
                        r = set_lsb2(r, int(bit))
                    elif ch==1:
                        g = set_lsb2(g, int(bit))
                    else:
                        b = set_lsb2(b, int(bit))
                pixels[x,y] = (r,g,b)
            # 下一起點
            start = path[-1]

        img.save(output_path)
        print(f"Encoded and saved to {output_path}")