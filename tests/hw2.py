import reedsolo

rs = reedsolo.RSCodec(3)  # RS(7,4): 4 data + 3 parity
data = b'abcd'            # 原始 4 bytes 資料

encoded = rs.encode(data)
print("原始資料:", data)
print("編碼後  :", list(encoded))

# 假設第 2 個 byte 被破壞了（改成錯誤值）
corrupted = bytearray(encoded)
corrupted[1] ^= 0xFF  # XOR 破壞數值
print("\n[1 錯誤] 損壞後：", list(corrupted))

decoded, _, _ = rs.decode(corrupted)
print("修正後：", decoded)  # ✅ 成功修正！

corrupted2 = bytearray(encoded)
corrupted2[0] ^= 0xFF
corrupted2[2] ^= 0xFF
print("\n[2 錯誤] 損壞後：", list(corrupted2))

try:
    decoded, _, _ = rs.decode(corrupted2)
    print("修正後：", decoded)
except reedsolo.ReedSolomonError as e:
    print("❌ 解碼失敗！錯誤訊息：", str(e))  # ❌ 偵測到錯但不能修

corrupted3 = bytearray(encoded)
corrupted3[0] ^= 0xFF
corrupted3[2] ^= 0xFF
corrupted3[4] ^= 0xFF  # 假設第 0, 2, 4 個 byte 被破壞
print("\n[3 錯誤] 損壞後：", list(corrupted3))

try:
    decoded, _, _ = rs.decode(corrupted3)
    print("修正後：", decoded)
except reedsolo.ReedSolomonError as e:
    print("❌ 解碼失敗！錯誤訊息：", str(e))  # ❌ 偵測到錯但不能修

# 使用 rs.decode(data, erase_pos=[pos1, pos2]) 來修復
erased = bytearray(encoded)
erased[0] ^= 0xFF
erased[2] ^= 0xFF
erased[4] ^= 0xFF  # 假設第 0, 2, 4 個 byte 被破壞
print("\n[3 erasures] 損壞後：", list(erased))

decoded, _, _ = rs.decode(erased, erase_pos=[0, 2, 4])
print("修正後：", decoded)  # ✅ 成功修復！
