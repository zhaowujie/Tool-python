# -*- coding
"""
TODO: 画出目标尺寸、宽高比散点图
"""
import os
import os.path as osp
import math
import cv2
import pickle
import scipy.io as scio
from tqdm import tqdm
import matplotlib.pyplot as plt
import random
fixed_size = [1024, 512]

cnames = [
            'darkred',
            'darksalmon',
            'darkseagreen',
            'darkslateblue',
            'darkslategray',
            'darkturquoise',
            'aqua',
            'aquamarine',

            'beige',
            'bisque',
            'black',
            'blanchedalmond',
            'blue',
            'blueviolet',
            ]
marker = [  '.',
            ',',
            '*',
            'v',
            '^',
            '>',
            '1',
            '2',
            '3',
            '4',
            's',
            'p',
            '*',
            'h',
            'H',
            '+' ]

class_names = [
                   'pedestrian', 'person',
                   'bicycle', 'car', 'van',
                   'truck', 'tricycle',
                   'awning_tricycle',
                   'bus', 'motor']

sizes_dic = {}
ratios_dic = {}

size_mat_file = '/media/hp208/4t/zhaoxingjie/graduation_project/SSD-multi-batch-eval_add_task/scripts/size.mat'
ratio_mat_file = '/media/hp208/4t/zhaoxingjie/graduation_project/SSD-multi-batch-eval_add_task/scripts/ratio.mat'

sizes = scio.loadmat(size_mat_file)
ratios = scio.loadmat(ratio_mat_file)

for k, v in sizes.items():
    try:
        width = [x[0] for x in v]
        height = [x[1] for x in v]
        plt.scatter(width, height, c=cnames[class_names.index(k)], marker='*', label=k)
        plt.legend(loc='best')
        plt.savefig(fname=k + '.png')
        # plt.show()
        plt.cla()
    except:
        continue
# plt.close()
# plt.savefig('all.jpg')
for k, v in ratios.items():
    try:
        ratio = [x for x in v]
        x = [i for i in range(len(ratio))]
        plt.scatter(x, ratio, c='r', marker='*', label=k)
        plt.legend(loc='best')
        plt.savefig(fname=k + '_ratio.png')
        # plt.show()
        plt.cla()
    except:
        continue