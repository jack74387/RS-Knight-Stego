import numpy as np

def discrimination_function(window: np.ndarray) -> float:
    # zig-zag 掃描
    arr = np.concatenate([
        np.diagonal(window[::-1, :], k)[::(2*(k % 2)-1)]
        for k in range(1-window.shape[0], window.shape[0])
    ])
    return float(np.sum(np.abs(arr[:-1] - arr[1:])))

def flipping_operation(window: np.ndarray, mask: np.ndarray) -> np.ndarray:
    # 支援 f1, f0, f-1
    def f1(x): return (x + 1) if x % 2 == 0 else (x - 1)
    def f0(x): return x
    def f_1(x): return f1(x + 1) - 1

    ops = { 1: f1, 0: f0, -1: f_1 }
    vec = np.vectorize(lambda px, m: ops[m](px))
    return vec(window, mask)

def calculate_count_groups(channel: np.ndarray, mask: np.ndarray) -> tuple[float, float]:
    h, w = mask.shape
    reg = sing = unus = 0
    for i in range(0, channel.shape[0], h):
        for j in range(0, channel.shape[1], w):
            win = channel[i:i+h, j:j+w]
            flipped = flipping_operation(win, mask)
            d0 = discrimination_function(win)
            d1 = discrimination_function(flipped)
            if d1 > d0: reg += 1
            elif d1 < d0: sing += 1
            else: unus += 1
    total = reg + sing + unus
    return reg/total, sing/total

def rs_helper(channels: list[np.ndarray], mask: np.ndarray) -> np.ndarray:
    rm = sm = rneg = sneg = 0.0
    for ch in channels:
        r, s = calculate_count_groups(ch, mask)
        rn, sn = calculate_count_groups(ch, -mask)
        rm += r; sm += s; rneg += rn; sneg += sn
    # 平均到每個 channel
    return np.array([rm, sm, rneg, sneg]) / len(channels)

def detect_stego_image(rs_values: list[np.ndarray], threshold=0.1) -> bool:
    for rm, sm, rneg, sneg in rs_values:
        if abs(rm - rneg) > threshold or abs(sm - sneg) > threshold:
            return True
    return False
