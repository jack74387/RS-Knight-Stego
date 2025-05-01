from PIL import Image
import random

def damage_image(input_path: str, output_path: str, num_bits: int = 100):
    img = Image.open(input_path).convert('RGB')
    pixels = img.load()
    w, h = img.size

    for _ in range(num_bits):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        channel = random.choice([0, 1, 2])  # R, G, or B
        bit_type = random.choice(["lsb", "lsb2"])

        rgb = list(pixels[x, y])
        if bit_type == "lsb":
            rgb[channel] ^= 1  # 翻轉 LSB
        else:
            rgb[channel] ^= 2  # 翻轉 LSB2
        pixels[x, y] = tuple(rgb)

    img.save(output_path)
    print(f"Damaged image saved to {output_path}")

if __name__ == "__main__":
    damage_image("output/test.tiff", "output/damaged.tiff", num_bits=50)
