from stegano.encoder import StegoEncoder
from stegano.decoder import StegoDecoder

if __name__ == '__main__':
    message = b"hello this is a test message" * 10
    encoder = StegoEncoder(seed=123)
    encoder.encode_image("examples/4.1.01.tiff", "output/test.tiff", message)

    decoder = StegoDecoder(seed=123)
    recovered = decoder.decode_image("output/test.tiff")
    print("Recovered message:", recovered)