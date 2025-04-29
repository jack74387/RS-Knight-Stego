from PIL import Image
from .rs_coder import RSCoder
from .knight import KnightTour
from .utils import get_lsb, get_lsb2

class StegoDecoder:
    """
    依照 Encode 規則反向讀取並 RS 解碼
    """
    def __init__(self, seed: int = 0):
        self.seed = seed
        self.rs = RSCoder()

    def decode_image(self, stego_path: str) -> bytes:
        img = Image.open(stego_path).convert('RGB')
        pixels = img.load()
        w,h = img.size
        knight = KnightTour(w, h, seed=self.seed)

        start = (0,0)
        result = bytearray()
        while True:
            path = knight.generate_path(start[0], start[1], 12)
            # 讀 data bits
            data_bits = ''
            for x,y in path[:11]:
                r,g,b = pixels[x,y]
                data_bits += str(get_lsb(r)) + str(get_lsb(g)) + str(get_lsb(b))
            # 32 bits data + 1bit end
            block_bits = data_bits[:32]
            end_flag = data_bits[32]
            data_bytes = bytes(int(block_bits[i:i+8],2) for i in range(0,32,8))
            # 讀 parity bits
            parity_bits = ''
            for x,y in path[:8]:
                r,g,b = pixels[x,y]
                parity_bits += str(get_lsb2(r)) + str(get_lsb2(g)) + str(get_lsb2(b))
            parity_bytes = bytes(int(parity_bits[i:i+8],2) for i in range(0,24,8))

            # RS 解碼
            encoded = data_bytes + parity_bytes
            try:
                decoded = self.rs.decode(encoded)
            except Exception as e:
                print("Too many errors, stop decoding.")
                break
            result.extend(decoded)

            if end_flag == '1':
                break
            start = path[-1]

        # 去掉 padding zero
        return bytes(result).rstrip(b'\x00')