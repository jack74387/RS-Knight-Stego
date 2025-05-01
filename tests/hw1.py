import reedsolo
import random

# 初始化 RS 編碼器，增加 3 個 parity bytes
rs = reedsolo.RSCodec(3)

message = "Hello, this is a test message!"
message_bytes = message.encode('utf-8')
print("原始訊息：", message_bytes)

# 將資料分成每 4 個 bytes 一組
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
for i, encoded in enumerate(encoded_chunks):
    data_part = encoded[:4]   # 前4個是data
    parity_part = encoded[4:] # 後3個是parity
    print(f"Chunk {i}: data: {list(data_part)}, parity: {list(parity_part)}")

# 模擬破壞（例如：破壞第0組的第1個byte）
print("\n模擬破壞：")
damaged_chunks = []
for i, encoded in enumerate(encoded_chunks):
    damaged = bytearray(encoded)
    if i == 0:
        print(" - 原始第0組：", list(damaged))
        damaged[1] ^= 0xFF  # 改變第2個byte的值
        damaged[2] ^= 0xFF  # 改變第3個byte的值
        damaged[3] ^= 0xFF
        damaged[4] ^= 0xFF
        damaged[5] ^= 0xFF
        print(" - 破壞後第0組：", list(damaged))
    damaged_chunks.append(bytes(damaged))

# 解碼（含錯誤處理）
decoded_bytes = bytearray()
print("\n解碼過程：")
for i, encoded in enumerate(damaged_chunks):
    try:
        decoded, _, _ = rs.decode(encoded)
        print(f"Chunk {i} 解碼成功：{list(decoded)}")
        decoded_bytes.extend(decoded)
    except reedsolo.ReedSolomonError as e:
        print(f"Chunk {i} 解碼失敗！錯誤：{e}")
        # 根據情況可補上空白或 0 作為 fallback
        decoded_bytes.extend(b'????')

# 截斷補0的部分，還原原始長度
decoded_bytes = decoded_bytes[:len(message_bytes)]

decoded_message = decoded_bytes.decode('utf-8', errors='replace')

print("\n最終解碼後訊息：", decoded_message)
