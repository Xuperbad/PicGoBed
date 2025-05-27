#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重命名工具
可以对指定文件夹内的所有文件进行批量重命名，重命名的首个部分由用户指定
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime, timedelta


class BatchRenamer:
    def __init__(self):
        self.rename_log = []
        self.log_file = "rename_log.json"

    def get_files_in_directory(self, directory: str, include_subdirs: bool = False) -> List[Path]:
        """获取目录中的所有文件"""
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")

        if not directory_path.is_dir():
            raise NotADirectoryError(f"路径不是目录: {directory}")

        files = []
        if include_subdirs:
            # 递归获取所有文件
            for file_path in directory_path.rglob("*"):
                if file_path.is_file():
                    files.append(file_path)
        else:
            # 只获取当前目录的文件
            for file_path in directory_path.iterdir():
                if file_path.is_file():
                    files.append(file_path)

        # 按文件名排序
        files.sort(key=lambda x: x.name.lower())
        return files

    def generate_new_names(self, files: List[Path], prefix: str, use_timestamp: bool = True, start_number: int = 1) -> List[Tuple[Path, str]]:
        """生成新的文件名"""
        rename_pairs = []

        if use_timestamp:
            # 使用时间戳格式: 年月日时分 (例如: 2505261507)
            base_time = datetime.now()
            for i, file_path in enumerate(files):
                # 获取文件扩展名
                extension = file_path.suffix
                # 每个文件时间递增1分钟，避免重名
                # 使用timedelta来正确处理时间增加
                current_time = base_time + timedelta(minutes=i)
                timestamp = current_time.strftime("%y%m%d%H%M")
                # 生成新文件名
                new_name = f"{prefix}_{timestamp}{extension}"
                rename_pairs.append((file_path, new_name))
        else:
            # 使用序号格式
            for i, file_path in enumerate(files):
                # 获取文件扩展名
                extension = file_path.suffix
                # 生成新文件名
                new_name = f"{prefix}_{start_number + i:03d}{extension}"
                rename_pairs.append((file_path, new_name))

        return rename_pairs

    def preview_rename(self, rename_pairs: List[Tuple[Path, str]]) -> None:
        """预览重命名操作"""
        print("\n" + "="*80)
        print("重命名预览:")
        print("="*80)
        print(f"{'原文件名':<40} -> {'新文件名':<40}")
        print("-"*80)

        for old_path, new_name in rename_pairs:
            print(f"{old_path.name:<40} -> {new_name:<40}")

        print("-"*80)
        print(f"总共 {len(rename_pairs)} 个文件将被重命名")
        print("="*80)

    def execute_rename(self, rename_pairs: List[Tuple[Path, str]], directory: str) -> bool:
        """执行重命名操作"""
        directory_path = Path(directory)
        success_count = 0
        failed_operations = []

        # 清空之前的日志
        self.rename_log = []

        for old_path, new_name in rename_pairs:
            try:
                new_path = directory_path / new_name

                # 检查新文件名是否已存在
                if new_path.exists():
                    print(f"警告: 文件 {new_name} 已存在，跳过重命名 {old_path.name}")
                    failed_operations.append((old_path.name, new_name, "文件已存在"))
                    continue

                # 执行重命名
                old_path.rename(new_path)

                # 记录操作日志
                log_entry = {
                    "old_name": old_path.name,
                    "new_name": new_name,
                    "old_path": str(old_path),
                    "new_path": str(new_path)
                }
                self.rename_log.append(log_entry)
                success_count += 1

                print(f"✓ {old_path.name} -> {new_name}")

            except Exception as e:
                print(f"✗ 重命名失败: {old_path.name} -> {new_name}, 错误: {str(e)}")
                failed_operations.append((old_path.name, new_name, str(e)))

        # 保存操作日志
        if self.rename_log:
            self.save_log()

        print(f"\n重命名完成! 成功: {success_count}, 失败: {len(failed_operations)}")

        if failed_operations:
            print("\n失败的操作:")
            for old_name, new_name, error in failed_operations:
                print(f"  {old_name} -> {new_name}: {error}")

        return len(failed_operations) == 0

    def save_log(self) -> None:
        """保存操作日志"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.rename_log, f, ensure_ascii=False, indent=2)
            print(f"\n操作日志已保存到: {self.log_file}")
        except Exception as e:
            print(f"保存日志失败: {str(e)}")

    def undo_rename(self) -> bool:
        """撤销上次重命名操作"""
        if not os.path.exists(self.log_file):
            print("没有找到操作日志文件，无法撤销")
            return False

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

            if not log_data:
                print("日志文件为空，没有可撤销的操作")
                return False

            print(f"\n找到 {len(log_data)} 个重命名操作，开始撤销...")

            success_count = 0
            failed_count = 0

            # 逆序撤销操作
            for entry in reversed(log_data):
                try:
                    new_path = Path(entry["new_path"])
                    old_path = Path(entry["old_path"])

                    if new_path.exists():
                        new_path.rename(old_path)
                        print(f"✓ 撤销: {entry['new_name']} -> {entry['old_name']}")
                        success_count += 1
                    else:
                        print(f"✗ 文件不存在，无法撤销: {entry['new_name']}")
                        failed_count += 1

                except Exception as e:
                    print(f"✗ 撤销失败: {entry['new_name']} -> {entry['old_name']}, 错误: {str(e)}")
                    failed_count += 1

            print(f"\n撤销完成! 成功: {success_count}, 失败: {failed_count}")

            # 删除日志文件
            if failed_count == 0:
                os.remove(self.log_file)
                print("操作日志文件已删除")

            return failed_count == 0

        except Exception as e:
            print(f"读取日志文件失败: {str(e)}")
            return False


def main():
    renamer = BatchRenamer()

    print("批量重命名工具")
    print("="*50)

    while True:
        print("\n请选择操作:")
        print("1. 批量重命名文件")
        print("2. 撤销上次重命名")
        print("3. 退出")

        choice = input("\n请输入选项 (1-3): ").strip()

        if choice == "1":
            # 获取目录路径
            directory = input("\n请输入目标文件夹路径 (直接回车使用当前目录): ").strip()
            if not directory:
                directory = "."

            try:
                # 询问是否包含子目录
                include_subdirs = input("是否包含子目录中的文件? (y/N): ").strip().lower() == 'y'

                # 获取文件列表
                files = renamer.get_files_in_directory(directory, include_subdirs)

                if not files:
                    print("目录中没有找到文件")
                    continue

                print(f"\n找到 {len(files)} 个文件")

                # 获取新文件名前缀
                prefix = input("请输入新文件名的前缀: ").strip()
                if not prefix:
                    print("前缀不能为空")
                    continue

                # 选择命名方式
                naming_choice = input("选择命名方式:\n1. 时间戳格式 (推荐，如: prefix_2505261507)\n2. 序号格式 (如: prefix_001)\n请选择 (1/2，默认为1): ").strip()
                use_timestamp = naming_choice != "2"

                start_number = 1
                if not use_timestamp:
                    # 只有在使用序号格式时才询问起始编号
                    start_num_input = input("请输入起始编号 (默认为1): ").strip()
                    if start_num_input:
                        try:
                            start_number = int(start_num_input)
                        except ValueError:
                            print("起始编号必须是数字，使用默认值1")

                # 生成新文件名
                rename_pairs = renamer.generate_new_names(files, prefix, use_timestamp, start_number)

                # 预览重命名
                renamer.preview_rename(rename_pairs)

                # 确认执行
                confirm = input("\n确认执行重命名操作? (y/N): ").strip().lower()
                if confirm == 'y':
                    renamer.execute_rename(rename_pairs, directory)
                else:
                    print("操作已取消")

            except Exception as e:
                print(f"错误: {str(e)}")

        elif choice == "2":
            renamer.undo_rename()

        elif choice == "3":
            print("再见!")
            break

        else:
            print("无效选项，请重新选择")


if __name__ == "__main__":
    main()
