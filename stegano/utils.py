"""
工具函式: 操作 RGB 通道的最低位與次低位
"""

def set_lsb(value: int, bit: int) -> int:
    return (value & ~1) | (bit & 1)

def get_lsb(value: int) -> int:
    return value & 1

def set_lsb2(value: int, bit: int) -> int:
    return (value & ~2) | ((bit & 1) << 1)

def get_lsb2(value: int) -> int:
    return (value >> 1) & 1