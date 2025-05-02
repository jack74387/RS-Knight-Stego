import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

def compute_psnr(original, distorted):
    """
    計算 PSNR（峰值訊噪比）
    """
    mse = np.mean((original - distorted) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))

def compute_ssim(original, distorted):
    """
    計算 SSIM（結構相似性指標）
    """
    ssim_total = 0
    for i in range(3):  # 對 RGB 三通道計算平均
        ssim_val = ssim(original[:, :, i], distorted[:, :, i], data_range=255)
        ssim_total += ssim_val
    return ssim_total / 3

def compute_qi(original, distorted):
    """
    計算 QI（品質指標，Q 指標）
    W. Wang, “A universal quality index,” IEEE Signal Processing Letters, 2002
    """
    original = original.astype(np.float64)
    distorted = distorted.astype(np.float64)
    mean_x = np.mean(original)
    mean_y = np.mean(distorted)
    var_x = np.var(original)
    var_y = np.var(distorted)
    cov_xy = np.mean((original - mean_x) * (distorted - mean_y))

    numerator = 4 * cov_xy * mean_x * mean_y
    denominator = (var_x + var_y) * (mean_x**2 + mean_y**2)

    if denominator == 0:
        return 1 if numerator == 0 else 0
    return numerator / denominator
