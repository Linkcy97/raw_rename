# -*- coding: utf-8 -*-   
# Author       : Chongyang Li
# Email        : lichongyang2016@163.com
# Date         : 2025-05-06 08:17:44
# LastEditors  : Chongyang Li
# LastEditTime : 2026-05-25 19:50:06
# FilePath     : \raw_rename\Raw_rename.py

import shutil
from pathlib import Path
import re 

def extract_data_from_folder_name(folder_name):
    # 使用正则表达式提取数字部分
    match = re.search(r'\d+', folder_name)
    if match:
        return match.group()  # 返回匹配到的数字部分
    return None

def move_and_rename_files(folder_path):
    folder = Path(folder_path)

    # 检查输入路径是否存在且是目录
    if not folder.exists() or not folder.is_dir():
        print(f"路径无效: {folder}")
        return

    # 收集 JPG、RAW（NEF）和 MOV 文件
    jpg_files = sorted(folder.glob("*.JPG"), key=lambda x: x.stat().st_mtime)
    raw_files = sorted(folder.glob("*.NEF"), key=lambda x: x.stat().st_mtime)
    mov_files = sorted(folder.glob("*.MOV"), key=lambda x: x.stat().st_mtime)

    if not jpg_files and not raw_files and not mov_files:
        print("该文件夹下没有找到 .JPG, .NEF 或 .MOV 文件。")
        return

    # 根据文件名(不含后缀)对文件进行分组
    files_by_stem = {}
    for f in jpg_files:
        files_by_stem.setdefault(f.stem, {})['JPG'] = f
    for f in raw_files:
        files_by_stem.setdefault(f.stem, {})['NEF'] = f
    for f in mov_files:
        files_by_stem.setdefault(f.stem, {})['MOV'] = f

    # 获取每组的修改时间用于排序
    def get_mtime(stem):
        group = files_by_stem[stem]
        if 'JPG' in group:
            return group['JPG'].stat().st_mtime
        elif 'NEF' in group:
            return group['NEF'].stat().st_mtime
        else:
            return group['MOV'].stat().st_mtime

    # 按照修改时间排序
    sorted_stems = sorted(files_by_stem.keys(), key=get_mtime)

    auto_prefix = extract_data_from_folder_name(folder.name)            
    prefix = input("请输入重命名前缀，否则以默认形式%s:\n" % auto_prefix)
    if not prefix:
        prefix = auto_prefix
    # 动态生成目标文件夹名称：原文件夹名称加下划线加 raw
    raw_folder_name = f"{folder.name}_raw"
    raw_folder = folder / raw_folder_name
    
    # 只有当存在 RAW 文件时才创建 raw_folder
    if raw_files:
        raw_folder.mkdir(exist_ok=True)

    # 重命名并移动文件
    index = 1
    for stem in sorted_stems:
        group = files_by_stem[stem]
        new_name = f"{prefix}_{index:03d}"

        if 'JPG' in group:
            jpg_file = group['JPG']
            new_jpg_name = folder / f"{new_name}.JPG"
            jpg_file.rename(new_jpg_name)
            print(f"已重命名: {jpg_file.name} → {new_jpg_name.name}")

        if 'MOV' in group:
            mov_file = group['MOV']
            new_mov_name = folder / f"{new_name}.MOV"
            mov_file.rename(new_mov_name)
            print(f"已重命名: {mov_file.name} → {new_mov_name.name}")

        if 'NEF' in group:
            raw_file = group['NEF']
            new_raw_name = raw_folder / f"{new_name}.NEF"
            shutil.move(str(raw_file), new_raw_name)
            print(f"已重命名并移动: {raw_file.name} → {new_raw_name.name}")

        index += 1

    print(f"共处理 {index - 1} 组文件")

if __name__ == "__main__":
    user_input = input("请输入文件夹路径:\n")
    move_and_rename_files(user_input)
    input("处理完成。按回车键退出...")
