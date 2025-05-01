from stegano.encoder import StegoEncoder
from stegano.decoder import StegoDecoder
from examples.damage import damage_image

if __name__ == '__main__':
    message = b"hello this is a test !" * 7
    encoder = StegoEncoder(seed=123)
    encoder.encode_image("examples/4.1.01.tiff", "output/test.tiff", message)

    # 加入破壞
    damage_image("output/test.tiff", "output/damaged.tiff", num_bits=10)

    # 解碼破壞過的圖片
    decoder = StegoDecoder(seed=123)
    recovered = decoder.decode_image("output/damaged.tiff")
    print("Recovered message:", recovered)
