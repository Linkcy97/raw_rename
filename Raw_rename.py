# -*- coding: utf-8 -*-   
# Author       : Chongyang Li
# Email        : lichongyang2016@163.com
# Date         : 2025-05-06 08:17:44
# LastEditors  : Chongyang Li
# LastEditTime : 2025-05-09 22:09:59
# FilePath     : \raw_rename\Raw_rename.py

import shutil
from pathlib import Path

def move_and_rename_files(folder_path):
    folder = Path(folder_path)

    # 检查输入路径是否存在且是目录
    if not folder.exists() or not folder.is_dir():
        print(f"路径无效: {folder}")
        return

    # 收集 JPG 和 RAW（NEF） 文件
    jpg_files = sorted(folder.glob("*.JPG"), key=lambda x: x.stat().st_mtime)
    raw_files = sorted(folder.glob("*.NEF"), key=lambda x: x.stat().st_mtime)

    if not jpg_files and not raw_files:
        print("该文件夹下没有找到 .JPG 或 .NEF 文件。")
        return

    # 确保 JPG 和 RAW 数量一致
    # 检查文件数量是否匹配
    if len(jpg_files) != len(raw_files):
        print("JPG 和 RAW 文件数量不一致。")
        # 查找不匹配的文件
        jpg_names = {file.stem for file in jpg_files}
        raw_names = {file.stem for file in raw_files}

        unmatched_jpgs = [file.name for file in jpg_files if file.stem not in raw_names]
        unmatched_raws = [file.name for file in raw_files if file.stem not in jpg_names]

        if unmatched_jpgs:
            print("未匹配的 JPG 文件:")
            for name in unmatched_jpgs:
                print(name)

        if unmatched_raws:
            print("未匹配的 RAW 文件:")
            for name in unmatched_raws:
                print(name)
        return
                
    prefix = input("请输入重命名前缀，如 changsha20250500:\n")
    # 动态生成目标文件夹名称：原文件夹名称加下划线加 raw
    raw_folder_name = f"{folder.name}_raw"
    raw_folder = folder / raw_folder_name
    raw_folder.mkdir(exist_ok=True)

    # 重命名并移动文件
    index = 1
    for jpg_file, raw_file in zip(jpg_files, raw_files):
        new_name = f"{prefix}_{index:03d}"

        # 重命名 JPG（保留在原位置）
        new_jpg_name = folder / f"{new_name}.JPG"
        jpg_file.rename(new_jpg_name)

        # 重命名并移动 RAW
        new_raw_name = raw_folder / f"{new_name}.NEF"
        shutil.move(str(raw_file), new_raw_name)

        print(f"已重命名并移动: {jpg_file.name} → {new_jpg_name.name}")
        print(f"已重命名并移动: {raw_file.name} → {new_raw_name.name}")

        index += 1

    print(f"共移动 {index - 1} 对文件到 {raw_folder}")

if __name__ == "__main__":
    user_input = input("请输入文件夹路径:\n")
    move_and_rename_files(user_input)
    input("处理完成。按回车键退出...")
