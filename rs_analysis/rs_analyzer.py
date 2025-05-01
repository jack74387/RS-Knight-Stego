import cv2
import numpy as np
from .utils import rs_helper, detect_stego_image

class RSAnalyzer:
    def __init__(self, mask_size=(8, 8), threshold=0.1, seed=30):
        self.mask_size = mask_size
        self.threshold = threshold
        self.seed = seed

    def analyze(self, image, debug=False):
        """
        對輸入 RGB 影像做 RS 分析，回傳每個通道 (Rm, Sm, R-m, S-m)
        """
        # 建立 mask
        np.random.seed(self.seed)
        mask = np.random.randint(0, 2, size=self.mask_size)

        # 轉成 int16，並調整尺寸為 mask 的整數倍
        img = image.astype("int16")
        h, w = img.shape[:2]
        h += (self.mask_size[0] - h % self.mask_size[0]) % self.mask_size[0]
        w += (self.mask_size[1] - w % self.mask_size[1]) % self.mask_size[1]
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

        # 分離三個通道並計算 RS
        channels = [img[:, :, i] for i in range(3)]
        rs_vals = [rs_helper([ch], mask) for ch in channels]

        if debug:
            for i, (rm, sm, rneg, sneg) in enumerate(rs_vals):
                print(f"Channel {i}: Rm={rm:.4f}, R-m={rneg:.4f}, Sm={sm:.4f}, S-m={sneg:.4f}")

        return rs_vals

    def is_stego(self, image, debug=False):
        rs_vals = self.analyze(image, debug=debug)
        return detect_stego_image(rs_vals, threshold=self.threshold)


if __name__ == "__main__":
    import sys
    from pathlib import Path

    path = sys.argv[1] if len(sys.argv) > 1 else input("Image path: ")
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    analyzer = RSAnalyzer()
    if analyzer.is_stego(img, debug=True):
        print("⚠️ 可能含有隱寫")
    else:
        print("✅ 看起來是原始圖片")
