"""
工具函式: 操作 RGB 通道的最低位與次低位
"""

def set_lsb(value: int, bit: int) -> int:
    """將 value 的最低位 (bit0) 設為 bit (0 or 1)"""
    return (value & ~1) | (bit & 1)


def get_lsb(value: int) -> int:
    """回傳 value 的最低位 (bit0)"""
    return value & 1


def set_lsb2(value: int, bit: int) -> int:
    """將 value 的次低位 (bit1) 設為 bit (0 or 1)"""
    return (value & ~2) | ((bit & 1) << 1)


def get_lsb2(value: int) -> int:
    """回傳 value 的次低位 (bit1)"""
    return (value >> 1) & 1