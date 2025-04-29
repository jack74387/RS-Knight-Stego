from reedsolo import RSCodec

class RSCoder:
    """
    Reed–Solomon 編碼/解碼 (7,4)
    每 4 bytes 原始資料 -> 7 bytes (4 data + 3 parity)
    """
    def __init__(self, nsym: int = 3):
        self.rs = RSCodec(nsym)

    def encode(self, data: bytes) -> bytes:
        if len(data) != 4:
            raise ValueError("RSCoder.encode: input must be exactly 4 bytes")
        return self.rs.encode(data)

    def decode(self, encoded: bytes) -> bytes:
        # returns original 4 bytes, or raises ReedSolomonError
        decoded, _, _ = self.rs.decode(encoded)
        return decoded