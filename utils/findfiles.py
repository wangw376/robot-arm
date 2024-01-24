# Copyright: Peng
# Date: 20220818
# coding:utf-8

import os
import shutil
import argparse

def findfiles(src_files, index_files, save_root, suffix):
    index_list = os.listdir(index_files)
    for file in index_list:
            src_path = src_files + os.path.splitext(file)[0] + suffix
            dst_path = save_root + os.path.splitext(file)[0] + suffix
            shutil.copy(src_path, dst_path)
            print('Get file:', dst_path)

# python findfiles.py --s .\hole-images\ --i .\hole-projection\  --r .\hole-new\

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--src_files", "--s", help="src files path", type=str, required=True)
    parser.add_argument("--index_files", "--i", help="index files path", type=str, required=True)
    parser.add_argument("--save_root", "--r", help="save root", type=str, required=True)
    parser.add_argument("--type_files", "--t", help=".jpg,.json,.png", type=str, required=True)
    args = parser.parse_args()

    src_files = args.src_files
    index_files = args.index_files
    save_root = args.save_root
    suffix = args.type_files

    if not os.path.exists(save_root):
        os.makedirs(save_root)

    findfiles(src_files, index_files, save_root, suffix)
