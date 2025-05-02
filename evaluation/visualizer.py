import numpy as np

def add_salt_pepper_noise(image, amount=0.01):
    """
    對輸入影像加入 salt and pepper noise。
    
    :param image: numpy array (H, W, 3)
    :param amount: 噪聲比例（0~1）
    :return: 加噪後圖像
    """
    noisy = np.copy(image)
    h, w, c = image.shape
    num_salt = np.ceil(amount * h * w * 0.5)
    num_pepper = np.ceil(amount * h * w * 0.5)

    # 加 salt (白點)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape[:2]]
    noisy[coords[0], coords[1], :] = 255

    # 加 pepper (黑點)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape[:2]]
    noisy[coords[0], coords[1], :] = 0

    return noisy.astype(np.uint8)
