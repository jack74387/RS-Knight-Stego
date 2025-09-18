"""
完整示範 RS-Knight 隱寫系統的基本功能
包含嵌入、提取和錯誤恢復能力測試
"""

from stegano.encoder import StegoEncoder
from stegano.decoder import StegoDecoder
from evaluation.visualizer import add_salt_pepper_noise
from evaluation.metrics import compute_psnr, compute_ssim
from rs_analysis.rs_analyzer import RSAnalyzer
import numpy as np
from PIL import Image

def basic_steganography_demo():
    """基本隱寫演示：嵌入和提取訊息"""
    print("=" * 50)
    print("基本隱寫演示")
    print("=" * 50)
    
    # 準備要隱藏的訊息
    secret_message = b"Hello, this is a secret message embedded using RS-Knight steganography!"
    print(f"原始訊息: {secret_message.decode('utf-8')}")
    print(f"訊息長度: {len(secret_message)} bytes")
    
    # 初始化編碼器和解碼器（使用相同的 seed）
    seed = 12345
    encoder = StegoEncoder(seed=seed)
    decoder = StegoDecoder(seed=seed)
    
    # 嵌入訊息到圖片中
    cover_image_path = "images/cover/4.1.01.tiff"
    stego_image_path = "output/demo_stego.tiff"
    
    print(f"\n正在將訊息嵌入到 {cover_image_path}...")
    encoder.encode_image(cover_image_path, stego_image_path, secret_message)
    
    # 從隱寫圖片中提取訊息
    print(f"正在從 {stego_image_path} 提取訊息...")
    recovered_message = decoder.decode_image(stego_image_path)
    
    # 驗證結果
    print(f"\n提取的訊息: {recovered_message.decode('utf-8')}")
    print(f"訊息完整性: {'✅ 成功' if secret_message == recovered_message else '❌ 失敗'}")
    
    return cover_image_path, stego_image_path

def quality_assessment_demo(cover_path, stego_path):
    """圖片品質評估演示"""
    print("\n" + "=" * 50)
    print("圖片品質評估")
    print("=" * 50)
    
    # 載入圖片
    cover_img = np.array(Image.open(cover_path))
    stego_img = np.array(Image.open(stego_path))
    
    # 計算品質指標
    psnr = compute_psnr(cover_img, stego_img)
    ssim = compute_ssim(cover_img, stego_img)
    
    print(f"PSNR: {psnr:.2f} dB")
    print(f"SSIM: {ssim:.4f}")
    
    # 品質評估
    if psnr > 40:
        print("✅ 圖片品質優秀 (PSNR > 40 dB)")
    elif psnr > 30:
        print("⚠️  圖片品質良好 (PSNR > 30 dB)")
    else:
        print("❌ 圖片品質較差 (PSNR < 30 dB)")

def noise_resilience_demo(stego_path):
    """雜訊抗性測試演示"""
    print("\n" + "=" * 50)
    print("雜訊抗性測試")
    print("=" * 50)
    
    decoder = StegoDecoder(seed=12345)
    original_message = decoder.decode_image(stego_path)
    print(f"原始嵌入訊息: {original_message.decode('utf-8')}")
    
    # 測試不同程度的雜訊
    noise_levels = [0.001, 0.005, 0.01, 0.02, 0.05]
    
    for noise_level in noise_levels:
        print(f"\n測試雜訊程度: {noise_level*100:.1f}%")
        
        # 載入圖片並加入雜訊
        stego_img = np.array(Image.open(stego_path))
        noisy_img = add_salt_pepper_noise(stego_img, amount=noise_level)
        
        # 保存加雜訊的圖片
        noisy_path = f"output/noisy_{noise_level*100:.1f}percent.tiff"
        Image.fromarray(noisy_img).save(noisy_path)
        
        # 嘗試從加雜訊的圖片中提取訊息
        try:
            recovered = decoder.decode_image(noisy_path)
            if recovered == original_message:
                print(f"  ✅ 成功恢復訊息")
            else:
                print(f"  ❌ 訊息已損壞")
                print(f"  恢復內容: {recovered.decode('utf-8', errors='replace')[:50]}...")
        except Exception as e:
            print(f"  ❌ 提取失敗: {e}")

def steganalysis_demo(cover_path, stego_path):
    """隱寫分析演示"""
    print("\n" + "=" * 50)
    print("隱寫分析演示")
    print("=" * 50)
    
    analyzer = RSAnalyzer()
    
    # 分析原始圖片
    print("分析原始封面圖片:")
    cover_img = np.array(Image.open(cover_path))
    is_stego_cover = analyzer.is_stego(cover_img, debug=True)
    print(f"檢測結果: {'⚠️ 疑似包含隱寫內容' if is_stego_cover else '✅ 未檢測到隱寫內容'}")
    
    # 分析隱寫圖片
    print("\n分析隱寫圖片:")
    stego_img = np.array(Image.open(stego_path))
    is_stego_stego = analyzer.is_stego(stego_img, debug=True)
    print(f"檢測結果: {'⚠️ 疑似包含隱寫內容' if is_stego_stego else '✅ 未檢測到隱寫內容'}")

def capacity_analysis_demo():
    """容量分析演示"""
    print("\n" + "=" * 50)
    print("容量分析演示")
    print("=" * 50)
    
    # 計算理論容量
    test_image = Image.open("images/cover/4.1.01.tiff")
    width, height = test_image.size
    total_pixels = width * height
    
    # RS-Knight 系統參數
    # 每 4 bytes 原始資料需要 12 pixels (3 bits data + 3 bits parity per pixel)
    pixels_per_block = 12
    bytes_per_block = 4
    
    theoretical_capacity = (total_pixels // pixels_per_block) * bytes_per_block
    print(f"圖片尺寸: {width} × {height} = {total_pixels:,} pixels")
    print(f"理論最大容量: {theoretical_capacity:,} bytes ({theoretical_capacity/1024:.1f} KB)")
    print(f"嵌入效率: {theoretical_capacity/total_pixels*8:.3f} bits per pixel")

def main():
    """主要演示函數"""
    print("RS-Knight 隱寫系統功能演示")
    print("Author: RS-Knight-Stego Project")
    print("Version: 1.0.0\n")
    
    try:
        # 基本隱寫演示
        cover_path, stego_path = basic_steganography_demo()
        
        # 圖片品質評估
        quality_assessment_demo(cover_path, stego_path)
        
        # 容量分析
        capacity_analysis_demo()
        
        # 雜訊抗性測試
        noise_resilience_demo(stego_path)
        
        # 隱寫分析測試
        steganalysis_demo(cover_path, stego_path)
        
        print("\n" + "=" * 50)
        print("演示完成！")
        print("=" * 50)
        print("所有輸出檔案已保存到 output/ 目錄")
        
    except FileNotFoundError as e:
        print(f"❌ 檔案未找到: {e}")
        print("請確保 images/cover/ 目錄中有測試圖片")
    except Exception as e:
        print(f"❌ 執行錯誤: {e}")

if __name__ == "__main__":
    main()