from PIL import Image
import numpy as np

# Chi-square 計算
def chi_square_attack(channel_data):
    counts = [0] * 256
    for value in channel_data.flatten():
        counts[value] += 1

    chi = 0
    for i in range(0, 256, 2):
        o1 = counts[i]
        o2 = counts[i + 1]
        e = (o1 + o2) / 2
        if e > 0:
            chi += ((o1 - e) ** 2 + (o2 - e) ** 2) / e
    return chi

# 根據 chi-square 值判斷是否藏資料
def is_likely_stego(chi_value, threshold=500):
    return chi_value < threshold

# 主流程
def analyze_image(path):
    img = Image.open(path).convert('RGB')
    r, g, b = img.split()

    r_data = np.array(r)
    g_data = np.array(g)
    b_data = np.array(b)

    r_chi = chi_square_attack(r_data)
    g_chi = chi_square_attack(g_data)
    b_chi = chi_square_attack(b_data)

    print("Chi-square statistic per channel:")
    print(f"  R: {r_chi:.2f} {'<<可能有藏資料>>' if is_likely_stego(r_chi) else ''}")
    print(f"  G: {g_chi:.2f} {'<<可能有藏資料>>' if is_likely_stego(g_chi) else ''}")
    print(f"  B: {b_chi:.2f} {'<<可能有藏資料>>' if is_likely_stego(b_chi) else ''}")

if __name__ == '__main__':
    image_path = input("請輸入圖片檔名: ")  # 輸入你的圖片檔名
    analyze_image(image_path)  # 改成你的圖片檔名
