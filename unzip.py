# -*- coding=utf-8 -*-
import os
import zipfile

def unzip(path, zfile):
    """
    TODO: 解压缩文件，默认解压到当前目录
    :param path:    zip文件所在路径
    :param zfile:   压缩包名称
    :return:        无
    """
    file_path = os.path.join(path, zfile)
    desdir = path  # +zfile[:zfile.index('.zip')]  这一步可以设置是否解压到当前文件夹还是新建一个和压缩文件同名的文件夹
    srcfile=zipfile.ZipFile(file_path)
    for filename in srcfile.namelist():
        srcfile.extract(filename,desdir)
        if filename.endswith('.zip'):
            # if zipfile.is_zipfile(filename):
            path = desdir
            zfile = filename
            unzip(path, zfile)

if __name__ == "__main__":
    path = os.getcwd()
    print(path)
    zfile = r'train_val.zip'
    unzip(path, zfile)
    print('unzip file {} to {} successfully!!!!!!!'.format(zfile, path))