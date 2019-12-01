import os

'''
# TODO: get train.txt
'''

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
data_dir = '/media/hp208/4t/zhaoxingjie/graduation_project/VisDrone/patches'

train_txt = os.path.join(data_dir, 'train.txt')

anno_dir = os.path.join(data_dir, 'annotations')

sequences_dir = os.path.join(data_dir, 'sequences')

with open(train_txt, 'w') as f:
    for path_name, dir_list, _ in os.walk(sequences_dir):
        # print (path_name, )
        dir_list.sort()
        for dir in dir_list:
            file_names = os.listdir(os.path.join(sequences_dir, dir))
            file_names.sort()
            for file in file_names:
                f.write(dir + '/' + file[0:-4] + '\n')
                print(file)
