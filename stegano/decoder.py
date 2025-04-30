from PIL import Image
from .rs_coder import RSCoder
from .knight import KnightTour
from .utils import get_lsb, get_lsb2

class StegoDecoder:
    """
    反向解碼並 RS 修正，依據資料頭 4-byte 長度終止
    """
    def __init__(self, seed: int = 0):
        self.seed = seed
        self.rs = RSCoder()

    def decode_image(self, stego_path: str) -> bytes:
        img = Image.open(stego_path).convert('RGB')
        pixels = img.load()
        w, h = img.size
        knight = KnightTour(w, h, seed=self.seed)

        used = set()
        start = (0, 0)
        result = bytearray()
        total_len = None

        while True:
            path = knight.generate_path(start[0], start[1], 12, used)
            used.update(path)

            # extract data bits
            data_bits = ''
            for (x, y) in path[:11]:
                r, g, b = pixels[x, y]
                data_bits += str(get_lsb(r)) + str(get_lsb(g)) + str(get_lsb(b))
            block_bits = data_bits[:32]
            data_bytes = bytes(int(block_bits[i:i+8], 2) for i in range(0, 32, 8))

            # extract parity bits
            parity_bits = ''
            for (x, y) in path[:8]:
                r, g, b = pixels[x, y]
                parity_bits += str(get_lsb2(r)) + str(get_lsb2(g)) + str(get_lsb2(b))
            parity_bytes = bytes(int(parity_bits[i:i+8], 2) for i in range(0, 24, 8))

            encoded = data_bytes + parity_bytes
            try:
                decoded = self.rs.decode(encoded)
                result.extend(decoded)
            except Exception:
                print("Too many errors to correct. Decoding stopped.")
                break

            # parse length header
            if total_len is None and len(result) >= 4:
                total_len = int.from_bytes(result[:4], 'big')

            if total_len is not None and len(result) >= total_len + 4:
                break

            start = path[-1]

        # remove header and padding
        return bytes(result[4:4+total_len])