import reedsolo

# 初始化 RS 編碼器
rs = reedsolo.RSCodec(3)

message = "Hello, this is a test message!"
message_bytes = message.encode('utf-8')
print("原始訊息：", message_bytes)

# 分成每4個bytes一組
def chunk(lst, size):
    return [lst[i:i+size] for i in range(0, len(lst), size)]

chunks = chunk(message_bytes, 4)

# 編碼
encoded_chunks = []
for ch in chunks:
    if len(ch) < 4:
        ch += bytes(4 - len(ch))  # 補0，湊滿4個bytes
    encoded = rs.encode(ch)
    encoded_chunks.append(encoded)

print("\n編碼後：")
for encoded in encoded_chunks:
    data_part = encoded[:4]   # 前4個是data
    parity_part = encoded[4:] # 後3個是parity
    print(f"data: {list(data_part)}, parity: {list(parity_part)}")

# 解碼
decoded_bytes = bytearray()
for encoded in encoded_chunks:
    decoded, _, _ = rs.decode(encoded)
    decoded_bytes.extend(decoded)

# 只保留原來的長度
decoded_bytes = decoded_bytes[:len(message_bytes)]  # 截斷掉補的0

decoded_message = decoded_bytes.decode('utf-8')

print("\n解碼後訊息：", decoded_message)
