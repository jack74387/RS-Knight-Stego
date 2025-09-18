# oracle/attack_strategy.py
from PIL import Image
from .oracle_detector import RSOracleDetector
from .pixel_modifier import PixelModifier

class OracleAttack:
    """
    利用 detector 提供的“是否检测到”反馈来微调嵌入，从而实现抗检测。
    """
    def __init__(self, threshold: float = 0.05, max_iter: int = 500):
        self.detector = RSOracleDetector(threshold=threshold)
        self.modifier = PixelModifier(max_iter=max_iter)

    @staticmethod
    def data_to_bits(data: bytes) -> list:
        bits = []
        for byte in data:
            for i in range(8)[::-1]:
                bits.append((byte >> i) & 1)
        return bits

    def hide_data(self, cover_image: Image.Image, secret: bytes) -> Image.Image:
        """
        对给定 cover_image 嵌入 secret，并调用 modifier 保证通过 detector。
        """
        bits = self.data_to_bits(secret)
        # 初次嵌入
        stego = self.modifier.embed_bits(cover_image, bits)
        # 反复扰动，直到检测器认为干净
        final = self.modifier.perturb_until_clean(cover_image, stego, self.detector, bits)
        return final
