"""
Copyright: mjt
Date: 20230421
coding:utf-8
function:rename file's name as '00001.jpg'
"""

import os
import re
import sys
import argparse
import shutil

from tqdm import tqdm


class Rename:
    def rename_files1(self, folder_path, save_path, index):
        num = index
        filelist = os.listdir(folder_path)
        # filelist.sort(key=lambda x: int(re.findall(r".*-(.*)\.", x)[0]))
        filelist.sort(key=lambda x: int(x.split('.')[0]))
        for file in tqdm(filelist):
            filename = os.path.join(folder_path, file)
            if os.path.splitext(filename)[-1] == '.jpg':
                # print(str(int(os.path.splitext(file_path)[0][8:])))
                index = '%05d' % num  # 前面补零占位，重新按0开始
                new_filename = os.path.join(save_path, str(index) + '.png')
                shutil.copy(filename, new_filename)
                num += 1

    def rename_files2(self, folder_path, save_path, index):
        num = index
        filelist = os.listdir(folder_path)
        filelist.sort(key=lambda x: int(x.split('.')[0]))
        for file in tqdm(filelist):
            filename = os.path.join(folder_path, file)
            if os.path.splitext(filename)[-1] == '.jpg':
                # print(str(int(os.path.splitext(file_path)[0][8:])))
                # num = int(os.path.splitext(filename)[0][23:])
                index = '%05d' % num  # 前面补零占位，按原文件顺序开始
                new_filename = os.path.join(save_path, str(index) + '.jpg')
                shutil.copy(filename, new_filename)
                num += 1

    def rename_files3(self, folder_path, save_path, index):
        num = index
        filelist = os.listdir(folder_path)
        # filelist.sort(key=lambda x: int(re.findall(r".*-(.*)\.", x)[0]))
        filelist.sort(key=lambda x: int(x.split('.')[0]))
        for file in tqdm(filelist):
            filename = os.path.join(folder_path, file)
            if os.path.splitext(filename)[-1] == '.json':
                index = '%05d' % num  # 前面补零占位，重新按0开始
                new_filename = os.path.join(save_path, str(index) + '.json')
                shutil.copy(filename, new_filename)
                num += 1

    def rename_files4(self, folder_path, save_path, index):
        num = index
        filelist = os.listdir(folder_path)
        # filelist.sort(key=lambda x: int(re.findall(r".*-(.*)\.", x)[0]))
        filelist.sort(key=lambda x: int(x.split('.')[0]))
        for file in tqdm(filelist):
            filename = os.path.join(folder_path, file)
            if os.path.splitext(filename)[-1] == '.png':
                index = '%05d' % num  # 前面补零占位，按原文件顺序开始
                new_filename = os.path.join(save_path, str(index) + '.png')
                shutil.copy(filename, new_filename)
                num += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", "--f", help="src files path", type=str, required=True)
    parser.add_argument("--choice", "--c", help="choice function", type=str, required=True)
    parser.add_argument("--save_path", "--s", help="save files path", type=str, required=True)
    parser.add_argument("--index_num", "--i", help="index num", type=str, required=True)

    args = parser.parse_args()

    folder_path = args.folder_path
    choice = args.choice
    save_path = args.save_path
    index_num = args.index_num
    index = int(index_num)

    rename = Rename()
    if choice == '1':
        rename.rename_files1(folder_path, save_path, index)
        print('rename all files successfully')
    elif choice == '2':
        rename.rename_files2(folder_path, save_path, index)
        print('rename all files successfully')
    elif choice == '3':
        rename.rename_files3(folder_path, save_path, index)
        print('rename all files successfully')
    elif choice == '4':
        rename.rename_files4(folder_path, save_path, index)
        print('rename all files successfully')
