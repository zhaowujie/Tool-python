# -*- coding=utf-8 -*-
from PIL import Image
import numpy as np
from tqdm import tqdm

train_root = '/media/hp208/4t/zhaoxingjie/data/HUAWEIAI/train_val500/train'

def get_files(dir):
    import os
    if not os.path.exists(dir):
        return []
    if os.path.isfile(dir):
        return [dir]
    result = []
    for subdir in os.listdir(dir):
        sub_path = os.path.join(dir, subdir)
        result += get_files(sub_path)
    return result


r = 0  # r mean
g = 0  # g mean
b = 0  # b mean

r_2 = 0  # r^2
g_2 = 0  # g^2
b_2 = 0  # b^2

total = 0


files = get_files(train_root)
files.sort()
count = len(files)

for image_file in tqdm(files):
    # print('Process: %d/%d' % (i, count))
    img = Image.open(image_file)#.convert('RGB')
    img = img.resize((224, 224))
    img = np.asarray(img)
    img = img.astype('float32') / 255.
    total += img.shape[0] * img.shape[1]
    try:
        r += img[:, :, 0].sum()
        g += img[:, :, 1].sum()
        b += img[:, :, 2].sum()

        r_2 += (img[:, :, 0] ** 2).sum()
        g_2 += (img[:, :, 1] ** 2).sum()
        b_2 += (img[:, :, 2] ** 2).sum()
    except:
        print(image_file)
        continue

r_mean = r / total
g_mean = g / total
b_mean = b / total

r_var = r_2 / total - r_mean ** 2
g_var = g_2 / total - g_mean ** 2
b_var = b_2 / total - b_mean ** 2
print("R, G, B:")
print('Mean is %.3f, %.3f, %.3f' % (r_mean, g_mean, b_mean))
print('Var is %.3f, %.3f, %.3f' % (r_var, g_var, b_var))
print('Std is %.3f, %.3f, %.3f' % (np.sqrt(r_var), np.sqrt(g_var), np.sqrt(b_var)))
# R, G, B:
# Mean is 0.574, 0.510, 0.444
# Var is 0.091, 0.093, 0.105
# Std is 0.301, 0.306, 0.325