#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图床总览生成器
自动扫描项目中的图片文件并生成markdown格式的总览文件
支持从任何位置运行，自动识别项目根目录
"""

import os
from pathlib import Path

# 支持的图片格式
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp', '.ico'}

# GitHub仓库信息
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Xuperbad/PicGoBed/master"

def find_project_root():
    """查找项目根目录（包含图床总览.md的目录）"""
    current_path = Path.cwd()

    # 首先检查当前目录
    if (current_path / "图床总览.md").exists():
        return current_path

    # 向上查找父目录
    for parent in current_path.parents:
        if (parent / "图床总览.md").exists():
            return parent

    # 如果没找到，返回当前目录
    return current_path

def is_image_file(filename):
    """判断文件是否为图片文件"""
    return Path(filename).suffix.lower() in IMAGE_EXTENSIONS

def get_image_name_without_extension(filename):
    """获取不带扩展名的图片名称"""
    return Path(filename).stem

def scan_directory(root_path):
    """扫描目录结构，返回按文件夹组织的图片列表"""
    structure = {}

    for root, dirs, files in os.walk(root_path):
        # 跳过隐藏文件夹和特殊文件夹
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        # 获取相对路径
        rel_path = os.path.relpath(root, root_path)
        if rel_path == '.':
            continue

        # 过滤出图片文件
        image_files = [f for f in files if is_image_file(f)]

        if image_files:
            # 按文件名排序
            image_files.sort()
            structure[rel_path] = image_files

    return structure

def generate_markdown_content(structure):
    """生成markdown内容（不包含标题）"""
    content = []

    # 按文件夹名称排序
    sorted_folders = sorted(structure.keys())

    for folder_path in sorted_folders:
        images = structure[folder_path]

        # 处理文件夹层级
        path_parts = folder_path.split(os.sep)

        if len(path_parts) == 1:
            # 一级文件夹
            content.append(f"# {path_parts[0]}\n")
        elif len(path_parts) == 2:
            # 二级文件夹
            content.append(f"## {path_parts[1]}\n")
        else:
            # 更深层级的文件夹，使用更多#号
            level = min(len(path_parts), 6)  # markdown最多支持6级标题
            content.append(f"{'#' * level} {'/'.join(path_parts)}\n")

        # 生成图片链接
        for image in images:
            image_name = get_image_name_without_extension(image)
            # 将Windows路径分隔符转换为URL路径分隔符
            url_path = folder_path.replace(os.sep, '/')
            image_url = f"{GITHUB_BASE_URL}/{url_path}/{image}"
            content.append(f"![{image_name}]({image_url})\n")

        content.append("\n")  # 添加空行分隔

    return "".join(content)

def read_existing_overview(file_path):
    """读取现有的图床总览文件，返回分隔符前的内容"""
    if not file_path.exists():
        return "# 图床总览\n\n---\n\n"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 查找 --- 分隔符
        if '---' in content:
            parts = content.split('---', 1)
            return parts[0] + '---\n\n'
        else:
            # 如果没有分隔符，添加一个
            return content.rstrip() + '\n\n---\n\n'

    except Exception as e:
        print(f"⚠️ 读取现有文件时出错: {e}")
        return "# 图床总览\n\n---\n\n"

def main():
    """主函数"""
    # 查找项目根目录
    project_root = find_project_root()

    print(f"项目根目录: {project_root}")
    print(f"正在扫描图片文件...")

    # 扫描目录结构
    structure = scan_directory(project_root)

    if not structure:
        print("未找到任何图片文件")
        return

    # 读取现有的总览文件内容（分隔符前的部分）
    output_file = project_root / "图床总览.md"
    header_content = read_existing_overview(output_file)

    # 生成新的图片内容
    images_content = generate_markdown_content(structure)

    # 合并内容
    final_content = header_content + images_content

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"✅ 图床总览已更新: {output_file}")

        # 统计信息
        total_images = sum(len(images) for images in structure.values())
        total_folders = len(structure)
        print(f"📊 统计信息: {total_folders} 个文件夹，{total_images} 张图片")

    except Exception as e:
        print(f"❌ 写入文件时出错: {e}")

if __name__ == "__main__":
    main()
