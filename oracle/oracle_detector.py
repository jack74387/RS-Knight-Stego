# oracle/oracle_detector.py
import numpy as np
from PIL import Image

class RSOracleDetector:
    """
    RS 检测器封装。detect 返回 True 表示检测到隐藏信息。
    """
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold

    def detect(self, img: Image.Image) -> bool:
        arr = np.array(img)
        # 对每个通道分别计算 R/S 变异差值
        diffs = []
        for c in range(3):
            channel = arr[..., c]
            flipped = np.bitwise_xor(channel, 1)  # 翻转 LSB
            diffs.append(np.mean(np.abs(channel.astype(int) - flipped.astype(int))))
        avg_diff = float(np.mean(diffs))
        # 差异太大则认为有隐藏
        return avg_diff > self.threshold
