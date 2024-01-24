# Copyright: Chenshp
# Date: 20220718
# coding:utf-8

import os
import sys
import json
import shutil
import argparse

# 图像宽度
WIDTH = 1920
# 图像高度
HEIGHT = 1080


# 参数函数：输入文件地址，输出修改文件的保存路径，以及添加文件的排列起始序号
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_pth', '--j', help='json file', type=str, required=True)
    parser.add_argument('--save_pth', '--s', help='save file', type=str, required=True)
    parser.add_argument('--index', '--i', help='num index', type=str, required=True)
    args = parser.parse_args()
    return args


def operation_json(json_path, index_num):
    # 读入文件内容
    file_s = json.load(open(json_path, 'r', encoding='utf-8'))

    # 复制文件内容
    file_c = file_s

    shapes = file_c['shapes']

    # 删除文件副本['imageData']的内容
    del file_c['imageData']

    # 读取标签中bbox的脚点坐标
    file_c['shapes'][0]['label'] = 'hl'
    file_c['shapes'][0]['points'][0][0] = WIDTH - file_s['shapes'][0]['points'][0][0]
    file_c['shapes'][0]['points'][1][0] = WIDTH - file_s['shapes'][0]['points'][1][0]

    file_c['shapes'][1]['label'] = 'hr'
    file_c['shapes'][1]['points'][0][0] = WIDTH - file_s['shapes'][1]['points'][0][0]
    file_c['shapes'][1]['points'][1][0] = WIDTH - file_s['shapes'][1]['points'][1][0]

    if len(shapes) > 2:
        file_c['shapes'][2]['label'] = 'er'
        file_c['shapes'][2]['points'][0][0] = WIDTH - file_s['shapes'][2]['points'][0][0]
        file_c['shapes'][2]['points'][1][0] = WIDTH - file_s['shapes'][2]['points'][1][0]

        file_c['shapes'][3]['label'] = 'el'
        file_c['shapes'][3]['points'][0][0] = WIDTH - file_s['shapes'][3]['points'][0][0]
        file_c['shapes'][3]['points'][1][0] = WIDTH - file_s['shapes'][3]['points'][1][0]

    # 读取标签中图像尺寸
    file_c['imageHeight'] = HEIGHT
    file_c['imageWidth'] = WIDTH

    # 修改标签的图像名称，以及json文件的名称
    str_list = file_s['imagePath'].split(".")
    num_img = int(str_list[0]) + int(index_num)
    img_name = "%05d.jpg" % num_img
    file_name = "%05d.json" % num_img
    file_c['imagePath'] = img_name

    return file_c, file_name


if __name__ == '__main__':

    # 参数初始化
    args = parse_args()
    json_pth = args.json_pth
    save_pth = args.save_pth
    index_num = args.index

    # 新建文件保存路径
    if os.path.exists(save_pth):
        shutil.rmtree(save_pth)
    os.makedirs(save_pth)

    filelist = os.listdir(json_pth)

    for file in filelist:

        filename = os.path.splitext(file)[0]
        filename_suffix = os.path.splitext(file)[1]
        if filename_suffix == '.json':
            file_path = os.path.join(json_pth, file)
            json_file, file_name = operation_json(file_path, index_num)
            save_file = os.path.join(save_pth, file_name)
            json.dump(json_file, open(save_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
