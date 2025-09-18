"""
基本的 RS-Knight 隱寫系統使用範例
演示如何嵌入和提取訊息
"""

from stegano.encoder import StegoEncoder
from stegano.decoder import StegoDecoder

def main():
    print("RS-Knight 隱寫系統 - 基本範例")
    print("=" * 40)
    
    # 要隱藏的訊息
    message = b"Hello, this is a test message for RS-Knight steganography system! " * 10
    print(f"原始訊息長度: {len(message)} bytes")
    print(f"訊息內容: {message[:50].decode('utf-8')}...")
    
    # 使用相同的 seed 確保編碼和解碼一致
    seed = 123
    
    # 初始化編碼器並嵌入訊息
    print("\n正在嵌入訊息...")
    encoder = StegoEncoder(seed=seed)
    encoder.encode_image(
        input_path="images/cover/4.1.01.tiff", 
        output_path="output/example_stego.tiff", 
        data=message
    )
    
    # 初始化解碼器並提取訊息
    print("正在提取訊息...")
    decoder = StegoDecoder(seed=seed)
    recovered_message = decoder.decode_image("output/example_stego.tiff")
    
    # 驗證結果
    print(f"\n提取的訊息長度: {len(recovered_message)} bytes")
    print(f"提取的訊息內容: {recovered_message[:50].decode('utf-8')}...")
    
    # 檢查完整性
    if message == recovered_message:
        print("\n✅ 訊息完整性驗證成功！")
        print("原始訊息與提取訊息完全一致")
    else:
        print("\n❌ 訊息完整性驗證失敗！")
        print("原始訊息與提取訊息不一致")
    
    print(f"\n隱寫圖片已保存至: output/example_stego.tiff")

if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError:
        print("❌ 錯誤: 找不到封面圖片檔案")
        print("請確保 images/cover/4.1.01.tiff 檔案存在")
    except Exception as e:
        print(f"❌ 執行錯誤: {e}")