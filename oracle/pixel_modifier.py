# oracle/pixel_modifier.py
import random
import numpy as np
from PIL import Image

class PixelModifier:
    """
    提供在保持 RS 统计特征平衡的前提下对 LSB 进行翻转的工具。
    """
    def __init__(self, max_iter: int = 1000):
        self.max_iter = max_iter

    @staticmethod
    def knight_tour_pixels(width: int, height: int) -> list:
        # 简化版：按行扫描打乱后返回所有像素索引
        idxs = [(x, y) for y in range(height) for x in range(width)]
        random.shuffle(idxs)
        return idxs

    def embed_bits(self, img: Image.Image, bitstream: list) -> Image.Image:
        arr = np.array(img)
        h, w, _ = arr.shape
        pixels = self.knight_tour_pixels(w, h)
        bit_iter = iter(bitstream)
        for (x, y) in pixels:
            try:
                b = next(bit_iter)
            except StopIteration:
                break
            for c in range(3):
                arr[y, x, c] = (arr[y, x, c] & ~1) | b
        return Image.fromarray(arr)

    def perturb_until_clean(self, 
                            original: Image.Image, 
                            stego: Image.Image, 
                            detector, 
                            data_bits: list) -> Image.Image:
        """
        在检测器仍能识别时，反复打乱嵌入顺序并重嵌入，最多 self.max_iter 次。
        """
        for i in range(self.max_iter):
            if not detector.detect(stego):
                print(f"[PixelModifier] 迭代 {i} 次后通过检测")
                return stego
            # 重新嵌入：打乱顺序，或稍微增加噪声
            stego = self.embed_bits(original, data_bits)
        raise RuntimeError("无法在 max_iter 迭代内避开检测")
