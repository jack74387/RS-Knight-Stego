# steganography/metrics.py
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def compute_psnr(orig: np.ndarray, mod: np.ndarray) -> float:
    """計算 PSNR 值"""
    return peak_signal_noise_ratio(orig, mod)


def compute_ssim(orig: np.ndarray, mod: np.ndarray) -> float:
    """計算 SSIM 值"""
    # 使用新版 channel_axis，避免 multichannel 被棄用
    # 自動縮小 win_size 以適應小圖
    min_dim = min(orig.shape[0], orig.shape[1])
    win_size = min(7, min_dim // 2 * 2 + 1)  # 最接近且小於 min_dim 的奇數
    return structural_similarity(orig, mod, channel_axis=-1, win_size=win_size)


def compute_metrics(orig: np.ndarray, mod: np.ndarray) -> dict:
    """回傳 PSNR 與 SSIM"""
    return {
        'psnr': compute_psnr(orig, mod),
        'ssim': compute_ssim(orig, mod)
    }
