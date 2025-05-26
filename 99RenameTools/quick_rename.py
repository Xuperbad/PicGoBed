#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速批量重命名工具 - 命令行版本
用法: python quick_rename.py <目录路径> <新前缀> [--sequence] [起始编号]
默认使用时间戳格式，添加 --sequence 参数使用序号格式
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def quick_rename(directory: str, prefix: str, use_timestamp: bool = True, start_number: int = 1):
    """快速重命名指定目录中的所有文件"""

    # 检查目录是否存在
    directory_path = Path(directory)
    if not directory_path.exists():
        print(f"错误: 目录不存在 - {directory}")
        return False

    if not directory_path.is_dir():
        print(f"错误: 路径不是目录 - {directory}")
        return False

    # 获取所有文件
    files = []
    for file_path in directory_path.iterdir():
        if file_path.is_file():
            files.append(file_path)

    if not files:
        print(f"目录中没有找到文件: {directory}")
        return False

    # 按文件名排序
    files.sort(key=lambda x: x.name.lower())

    print(f"找到 {len(files)} 个文件")
    print(f"将使用前缀: {prefix}")

    if use_timestamp:
        print("命名格式: 时间戳 (年月日时分)")
    else:
        print(f"命名格式: 序号 (起始编号: {start_number})")

    print("-" * 50)

    # 生成重命名预览
    rename_pairs = []

    if use_timestamp:
        # 使用时间戳格式
        base_time = datetime.now()
        for i, file_path in enumerate(files):
            extension = file_path.suffix
            # 每个文件时间递增1分钟，避免重名
            # 使用timedelta来正确处理时间增加
            from datetime import timedelta
            current_time = base_time + timedelta(minutes=i)
            timestamp = current_time.strftime("%y%m%d%H%M")
            new_name = f"{prefix}_{timestamp}{extension}"
            rename_pairs.append((file_path, new_name))
            print(f"{file_path.name} -> {new_name}")
    else:
        # 使用序号格式
        for i, file_path in enumerate(files):
            extension = file_path.suffix
            new_name = f"{prefix}_{start_number + i:03d}{extension}"
            rename_pairs.append((file_path, new_name))
            print(f"{file_path.name} -> {new_name}")

    print("-" * 50)

    # 确认执行
    confirm = input(f"确认重命名这 {len(files)} 个文件? (y/N): ").strip().lower()
    if confirm != 'y':
        print("操作已取消")
        return False

    # 执行重命名
    success_count = 0
    for old_path, new_name in rename_pairs:
        try:
            new_path = directory_path / new_name

            # 检查新文件名是否已存在
            if new_path.exists():
                print(f"跳过 (文件已存在): {old_path.name} -> {new_name}")
                continue

            # 执行重命名
            old_path.rename(new_path)
            print(f"✓ {old_path.name} -> {new_name}")
            success_count += 1

        except Exception as e:
            print(f"✗ 重命名失败: {old_path.name} -> {new_name}, 错误: {str(e)}")

    print(f"\n重命名完成! 成功处理 {success_count} 个文件")
    return True


def main():
    if len(sys.argv) < 3:
        print("批量重命名工具 - 快速版")
        print("="*50)
        print("用法: python quick_rename.py <目录路径> <新前缀> [选项] [起始编号]")
        print("\n选项:")
        print("  --sequence    使用序号格式 (默认使用时间戳格式)")
        print("\n示例:")
        print("  python quick_rename.py ./像素 pixel_art")
        print("  python quick_rename.py ./卡通 cartoon --sequence 1")
        print("\n时间戳格式示例: pixel_art_2505261507.png")
        print("序号格式示例: cartoon_001.png")
        sys.exit(1)

    directory = sys.argv[1]
    prefix = sys.argv[2]
    use_timestamp = True
    start_number = 1

    # 解析参数
    args = sys.argv[3:]
    if "--sequence" in args:
        use_timestamp = False
        args.remove("--sequence")

    # 如果还有参数，尝试解析为起始编号
    if args and not use_timestamp:
        try:
            start_number = int(args[0])
        except ValueError:
            print("错误: 起始编号必须是数字")
            sys.exit(1)

    quick_rename(directory, prefix, use_timestamp, start_number)


if __name__ == "__main__":
    main()
