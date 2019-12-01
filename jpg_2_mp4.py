# -*- coding=utf-8 -*-
import os
import cv2
from tqdm import tqdm
import subprocess


img_size = (3840, 2160)
img_det_dir = '../../mmsr_dest/'

assert os.path.exists(img_det_dir), "出错， 路径{}不存在。。。 ".format(img_det_dir)
# img_size = (960, 540)
# img_det_dir = '../../SDR_540p_jpg/'

dest_vids = '../../mmsr_dest_vids/'
if not os.path.exists(dest_vids):
    os.mkdir(dest_vids)
video_names = os.listdir(img_det_dir)

# first_file_name = file_name_list[0]
# temp_file_path = first_file_name[0:first_file_name.rfind("_")] + ".txt"
# merge_file_path = first_file_name[0:first_file_name_rfind("_")] + ".mp4"
#
# cmd = "ffmpeg -f concat -loglevel error -safe 0 -i " + \
#       temp_file_path + " -g 10 -s 640*340 -q 20 -c -copy " + merge_file_path
# print(cmd)
# subprocess.call(cmd, shell=True)

fps = 30
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

for vid in tqdm(video_names):
    video_dir = os.path.join(dest_vids, vid) + '.mp4'
    file_names = os.listdir(os.path.join(img_det_dir, vid))
    file_names.sort()
    if len(file_names) == 100 and not os.path.isfile(video_dir):
        video_writer = cv2.VideoWriter(video_dir, fourcc, fps, img_size)
        for file_name in file_names:
            img_path = os.path.join(img_det_dir, vid, file_name)
            img = cv2.imread(img_path)
            # print("Loading img from: {}".format(img_path))
            video_writer.write(img)
            cmd = "ffmpeg - threads 4 -r 24000/1001 - i {}/%%d.jpg -vcodec libx265 -pix_fmt yuv422p -crf 10 {}{}.mp4" \
                .format(os.path.join(img_det_dir, vid), dest_vids, vid)
            # cmd = "ffmpeg - i {}/%%d.jpg  - c:v libx264 - preset veryslow - crf 18 -c:a copy D:\dest1.mp4"
            print(cmd)
            subprocess.call(cmd, shell=True)
        video_writer.release()
    else:
        print("{} already exsists, next....".format(video_dir))
        continue

#     "图像序列编码，组委会建议采用以下编码命令样例/参数：
# ffmpeg -r 24000/1001 -i pngs/out%4d.png -vcodec libx265 -pix_fmt yuv422p -crf 10 test.mp4
# 特此说明。"