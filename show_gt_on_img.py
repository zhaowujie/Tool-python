#coding=utf-8
'''
# TODO: 把 visdrone 中的sequence标注变成和图片相对应的2进制文件
'''
import os
import numpy as np
import cv2
import pickle


keys = ['frame_index',
        'target_id',
        'bbox_left', 'bbox_top', 'bbox_width', 'bbox_height',
        'score',
        'object_category',
        'truncation',
        'occlusion']
classes_map = ['ignored_regions',  # always index 0
                'pedestrian', 'person',
                'bicycle', 'car', 'van',
                'truck', 'tricycle',
                'awning-tricycle',
                'bus', 'motor', 'others']

num_classes = len(classes_map)
class_to_index = dict(zip(range(num_classes), classes_map))
data_dir = '/media/hp208/4t/zhaoxingjie/graduation_project/VisDrone/VisDrone2018-VID-train'

anno_dir = os.path.join(data_dir, 'annotations')

sequences_dir = os.path.join(data_dir, 'sequences')

anno_names = os.listdir(anno_dir)

def convert_line_to_dict(line):
    dest = {}
    new_line = line.strip().split(',')
    for k, v in enumerate(new_line):
        dest[keys[k]] = v
    return dest

def convert_to_pkl(temp, img_path):
    roi_rec = {}
    num_objs = len(temp)
    boxes = np.zeros((num_objs, 4), dtype=np.uint16)
    gt_classes = np.zeros((num_objs), dtype=np.int32)
    gt_trackid = np.zeros((num_objs), dtype=np.int32)
    overlaps = np.zeros((num_objs, num_classes), dtype=np.float32)
    valid_objs = np.zeros((num_objs), dtype=np.bool)
    occluded = np.zeros((num_objs), dtype=np.int32)
    # class_to_index = dict(zip(classes_map, range(num_classes)))
    roi_rec['image'] = img_path
    height, width, _ = cv2.imread(img_path).shape
    roi_rec['frame_id'] = int(img_path[-11:-4])
    roi_rec['height'] = height
    roi_rec['width'] = width
    for ix, obj in enumerate(temp):
        # 'bbox_left', 'bbox_top', 'bbox_width', 'bbox_height',
        # bbox = obj.find('bndbox')
        # Make pixel indexes 0-based
        x1 = np.maximum(float(obj['bbox_left']), 0)
        y1 = np.maximum(float(obj['bbox_top']), 0)
        x2 = np.minimum(x1 + float(obj['bbox_width']), roi_rec['width'] - 1)
        y2 = np.minimum(y1 + float(obj['bbox_height']), roi_rec['height'] - 1)
        # if not class_to_index.has_key(obj['object_category']):
        #     continue
        valid_objs[ix] = True
        cls = int(obj['object_category'])
        boxes[ix, :] = [x1, y1, x2, y2]
        gt_classes[ix] = cls

        occluded[ix] = obj['occlusion']
        gt_trackid[ix] = obj['truncation']

        overlaps[ix, cls] = 1.0

    boxes = boxes[valid_objs, :]
    gt_classes = gt_classes[valid_objs]
    gt_trackid = gt_trackid[valid_objs]
    overlaps = overlaps[valid_objs, :]
    occluded = occluded[valid_objs]

    assert (boxes[:, 2] >= boxes[:, 0]).all()

    roi_rec.update({'boxes': boxes,
                    'gt_classes': gt_classes,
                    'gt_trackid': gt_trackid,
                    'gt_overlaps': overlaps,
                    'max_classes': overlaps.argmax(axis=1),
                    'max_overlaps': overlaps.max(axis=1),
                    'occluded': occluded,
                    'flipped': False})
    return roi_rec

pkl = []
cache_file = os.path.join(os.path.abspath('.'), 'VisDrone-2018-VID-train_gt.pkl')
for anno_name in anno_names:
    # read annos
    annos = []
    try:
        with open((os.path.join(anno_dir, anno_name)), "r") as f:
            lines = f.readlines()
            for line in lines:
                # annos.append(line.strip().split(','))
                annos.append(convert_line_to_dict(line))
    except:
        continue
    # get images
    sequence_dir = os.path.join(sequences_dir, anno_name[:-4])
    image_names = os.listdir(sequence_dir)
    image_names.sort()
    # save dir
    new_anno_dir = os.path.join(anno_dir, anno_name[:-4])
    if not os.path.exists(new_anno_dir):
        os.mkdir(new_anno_dir)
    for image in image_names:
        temp = []
        img_path = os.path.join(sequence_dir, image)
        img = cv2.imread(img_path)
        for anno in annos:
            # if int(anno[0]) == int(image[:-4]):
            if int(anno['frame_index']) == int(image[:-4]):
                # temp.append(anno)
        # ------------put boxes on an image
                cv2.rectangle(img, (int(anno['bbox_left']), int(anno['bbox_top'])),
                                    (int(anno['bbox_left']) + int(anno['bbox_width']),
                                     int(anno['bbox_top']) + int(anno['bbox_height'])),
                                    (0, 255, 255), 1)
                cv2.putText(img, class_to_index[int(anno['object_category'])] ,
                            (int(anno['bbox_left']), int(anno['bbox_top'])),
                            cv2.FONT_ITALIC, 1, (0, 0, 255), 1)
        cv2.imshow('Detecting image...', img)
        cv2.waitKey(1)
        # ------------put boxes on an image
        pkl.append(convert_to_pkl(temp, img_path))
        print(img_path)
with open(cache_file, 'wb') as fid:
    pickle.dump(pkl, fid, pickle.HIGHEST_PROTOCOL)
print ('wrote gt roidb to {}'.format(cache_file))

