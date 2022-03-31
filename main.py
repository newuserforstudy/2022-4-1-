# coding:utf-8
# @time:2022/3/17上午11:12
# @author:sdh
import os

import six
import sys
import lmdb
import torch
import random
import numpy as np
from PIL import Image
from torch.utils.data import Dataset
from torch.utils.data import sampler
import torchvision.transforms as transforms


class lmdbDataset(Dataset):
    def __init__(self, root=None, transform=None):

        self.env = lmdb.open(
            root,
            max_readers=1,
            readonly=True,
            lock=False,
            readahead=False,
            meminit=False)

        if not self.env:
            print('cannot creat lmdb from %s' % (root))
            sys.exit(0)

        with self.env.begin(write=False) as txn:
            nSamples = int(txn.get('num-samples'.encode()))
            self.nSamples = nSamples

        self.transform = transform

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        if index > len(self):
            index = len(self) - 1
        assert index <= len(self), 'Error %d' % index
        index += 1
        with self.env.begin(write=False) as txn:
            img_key = 'image-%09d' % index
            imgbuf = txn.get(img_key.encode())

            buf = six.BytesIO()
            buf.write(imgbuf)
            buf.seek(0)
            try:
                img = Image.open(buf)
            except IOError:
                print('Corrupted image for %d' % index)
                return self[index + 1]

            label_key = 'label-%09d' % index
            label = str(txn.get(label_key.encode()).decode('utf-8'))

            if len(label) <= 0:
                return self[index + 1]

            label = label.lower()

            if self.transform is not None:
                img = self.transform(img)

        return (img, label)


class resizeNormalize(object):

    def __init__(self, size, interpolation=Image.BILINEAR):
        self.size = size
        self.interpolation = interpolation
        self.toTensor = transforms.ToTensor()

    def __call__(self, img):
        img = img.resize(self.size, self.interpolation)
        img = self.toTensor(img)
        img.sub_(0.5).div_(0.5)
        return img


if __name__ == '__main__':
    # root_dir = "/media/lessmart/data/sdh/22-03-16-add-mae/benchmark_dataset/"
    # dir_list = os.listdir(root_dir)  # ['web', 'document', 'hwdb', 'scene']
    #
    # for sub_dir in dir_list:
    #
    #     print("正在处理文件夹：", sub_dir)
    #     s_dir = root_dir+sub_dir   # /media/lessmart/data/sdh/22-03-16-add-mae/benchmark_dataset/web
    #     image_dir_list = os.listdir(s_dir)  # 每个子文件夹下有3个子文件夹 ['web_val', 'web_test', 'web_train'
    #
    #     num = 0
    #     for image_dir in image_dir_list:
    #         image_path = s_dir+"/"+image_dir  # /media/lessmart/data/sdh/22-03-16-add-mae/benchmark_dataset/web/web_val
    #         dataset = lmdbDataset(image_path)
    #         print(f'Length of dataset {len(dataset)}')
    #         # for data in dataset:
    #         for a in range(len(dataset)):
    #             i = '%06d' % num
    #             image, label = dataset[a]
    #             imgPath = f'image/{i}.jpg'
    #             image.save(f'/media/lessmart/data/sdh/22-03-16-add-mae/{sub_dir}/{imgPath}')
    #             with open(f'/media/lessmart/data/sdh/22-03-16-add-mae/{sub_dir}/label.txt', 'a+', encoding='utf-8') as f:
    #                 f.write(imgPath + '\t' + label + '\n')
    #             num += 1

    root_dir = "/media/lessmart/data/sdh/2022-03-18-add-mae/ST_spe"
    dataset = lmdbDataset(root_dir)
    num = 0
    for a in range(len(dataset)):
        if a == 30000:
            break
        else:
            print("处理第: %d 张图" % num)
            i = '%06d' % num
            image, label = dataset[a]
            image = image.convert("RGB")
            imgPath = f'images/{i}.jpg'
            image.save(f'/media/lessmart/data/sdh/2022-03-18-add-mae/{imgPath}')
            with open(f'/media/lessmart/data/sdh/2022-03-18-add-mae/label.txt', 'a+', encoding='utf-8') as f:
                f.write(imgPath + '\t' + label + '\n')
            num += 1
