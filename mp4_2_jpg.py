import os
import cv2

root_dir = '../'

# img_set = 'SDR_4K'
# dest_dir = '../SDR_4K_jpg'


img_set = 'test_SDR_540p'
dest_dir = '../test_SDR_540p_jpg'

temp_dir = root_dir + img_set
video_names = os.listdir(temp_dir)

def trans(vid):
    count = 1
    vc = cv2.VideoCapture(os.path.join(temp_dir, vid))
    while vc.isOpened():
        rval, frame = vc.read()
        if not rval:
            break
        dest_img = os.path.join(dest_dir, vid[:-4], "%03d" % count + '.jpg')
        cv2.imwrite(dest_img, frame)
        count += 1
        print(dest_img)
        # cv2.imshow("res", frame)
        # cv2.waitKey(1)
    vc.release()

for vid in video_names:
    second_folder = os.path.join(dest_dir, vid[:-4])
    if not os.path.exists(second_folder):
        os.mkdir(second_folder)
    trans(vid)
