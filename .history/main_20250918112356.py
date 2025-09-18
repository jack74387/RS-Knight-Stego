"""
RS-Knight 隱寫系統主程式
提供 RS 分析和雜訊測試功能
"""

import sys
from pathlib import Path
import cv2
import numpy as np
from rs_analysis.rs_analyzer import RSAnalyzer
from stegano.decoder import StegoDecoder
from evaluation.visualizer import add_salt_pepper_noise

def analyze_image(image_path: str):
    """分析圖片是否包含隱寫內容"""
    print(f"正在分析圖片: {image_path}")
    
    # 讀取圖片並轉換為 RGB
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ 無法讀取圖片: {image_path}")
        return False
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 初始化 RS 分析器
    analyzer = RSAnalyzer()
    
    # 檢查是否為隱寫圖片
    is_stego = analyzer.is_stego(img_rgb, debug=True)
    
    if is_stego:
        print("⚠️  可能含有隱寫內容")
    else:
        print("✅ 看起來是原始圖片")
    
    return is_stego

def noise_test_demo():
    """雜訊測試演示"""
    print("\n" + "="*50)
    print("雜訊抗性測試演示")
    print("="*50)
    
    # 使用預設的隱寫圖片進行測試
    stego_path = "images/stego/4.1.01.tiff"
    
    if not Path(stego_path).exists():
        print(f"❌ 找不到測試圖片: {stego_path}")
        return
    
    # 初始化解碼器
    decoder = StegoDecoder(seed=123)  # 使用預設 seed
    
    try:
        # 解碼原始隱寫圖片
        print("正在解碼原始隱寫圖片...")
        original_data = decoder.decode_image(stego_path)
        print(f"📥 原始嵌入訊息長度: {len(original_data)} bytes")
        print(f"原始訊息前50字元: {original_data[:50]}")
        
        # 加入雜訊測試糾錯
        print("\n正在加入雜訊進行測試...")
        img = cv2.imread(stego_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # 加入 1% 的 salt-and-pepper 雜訊
        noisy_img = add_salt_pepper_noise(img_rgb, amount=0.01)
        
        # 保存雜訊圖片
        noisy_path = "output/noisy_test.tiff"
        cv2.imwrite(noisy_path, cv2.cvtColor(noisy_img, cv2.COLOR_RGB2BGR))
        
        # 從雜訊圖片解碼
        print("正在從雜訊圖片解碼...")
        noisy_data = decoder.decode_image(noisy_path)
        print(f"⚡ 加雜訊後解碼訊息長度: {len(noisy_data)} bytes")
        
        # 比較結果
        if original_data == noisy_data:
            print("✅ Reed-Solomon 成功還原訊息")
        else:
            print("❌ 還原失敗，可能需要增加冗餘度")
            print(f"差異位置: {len([i for i, (a, b) in enumerate(zip(original_data, noisy_data)) if a != b])}")
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")

def main():
    """主函數"""
    print("RS-Knight 隱寫系統分析工具")
    print("Version: 1.0.0")
    print("="*50)
    
    if len(sys.argv) > 1:
        # 命令列模式：分析指定的圖片
        image_path = sys.argv[1]
        if Path(image_path).exists():
            analyze_image(image_path)
        else:
            print(f"❌ 檔案不存在: {image_path}")
    else:
        # 互動模式：讓使用者選擇功能
        print("請選擇功能:")
        print("1. 分析圖片是否包含隱寫內容")
        print("2. 雜訊抗性測試演示")
        print("3. 退出")
        
        while True:
            try:
                choice = input("\n請輸入選項 (1-3): ").strip()
                
                if choice == "1":
                    image_path = input("請輸入圖片路徑: ").strip()
                    if Path(image_path).exists():
                        analyze_image(image_path)
                    else:
                        print(f"❌ 檔案不存在: {image_path}")
                        
                elif choice == "2":
                    noise_test_demo()
                    
                elif choice == "3":
                    print("程式結束")
                    break
                    
                else:
                    print("❌ 無效選項，請輸入 1-3")
                    
            except KeyboardInterrupt:
                print("\n程式被中斷")
                break
            except Exception as e:
                print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    main()
