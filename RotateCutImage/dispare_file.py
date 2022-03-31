# coding:utf-8
# @time:2022/3/30下午1:47
# @author:sdh

import shutil
import os
import glob

import os
import shutil


def show_files(path, imgpaths):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            show_files(cur_path, imgpaths)
        else:
            if '/标注/' in cur_path:
                imgpaths.append(cur_path)

    return imgpaths


imgRoot = '/media/lessmart/data/sdh/22-3-30-add-mae/data'
imgpath = show_files(imgRoot, [])

for imgFile in imgpath:
    print(imgFile)
    if '-' in os.path.basename(imgFile):
        newPath = imgFile.replace(imgFile.split('/')[-2], 'P2')
        mk_dir = newPath.split("/")

        img_base_name = mk_dir[-1]
        del mk_dir[-1]
        P2_dir = "/".join(mk_dir)

        if not os.path.exists(P2_dir):
            os.mkdir(P2_dir)

        shutil.move(imgFile, P2_dir + "/" + img_base_name)
    else:
        newPath = imgFile.replace(imgFile.split('/')[-2], 'P1')
        mk_dir = newPath.split("/")

        img_base_name = mk_dir[-1]
        del mk_dir[-1]
        P1_dir = "/".join(mk_dir)

        if not os.path.exists(P1_dir):
            os.mkdir(P1_dir)

        shutil.move(imgFile, P1_dir+"/"+img_base_name)



#
# def separate_image_files(root_dir_path):
#     # 获取所有子文件夹
#     dir_path_list = os.listdir(root_dir_path)
#
#     # 遍历每一个子文件夹
#     for i, sub_dir_path in enumerate(dir_path_list):
#
#         # 获取自子文件夹中的所有图片
#         sub_file_path = glob.glob(root_dir_path + sub_dir_path + "/*.jpg")
#
#         # 遍历每一张图片
#         for each_image_path in sub_file_path:
#             image_base_name = os.path.basename(each_image_path)
#             # 根据图像名移动到对应的文件夹
#             image_identification = int(each_image_path.split(".")[0].split("_")[-1])
#
#             temp_dir = root_dir_path.split("/")
#             del temp_dir[-1]
#             del temp_dir[-1]
#
#             temp_dir_str = "/".join(temp_dir)
#
#             print(temp_dir_str)
#
#             if image_identification >= 0:
#                 save_dir = "/p1/"
#                 if not os.path.exists(temp_dir_str+save_dir):
#                     os.mkdir(temp_dir_str+save_dir)
#
#                 save_name = temp_dir_str+save_dir+image_base_name
#                 shutil.move(each_image_path, save_name)
#             else:
#                 save_dir = "/p2/"
#                 if not os.path.exists(temp_dir_str + save_dir):
#                     os.mkdir(temp_dir_str + save_dir)
#
#                 save_name = temp_dir_str + save_dir + image_base_name
#                 shutil.move(each_image_path, save_name)
#
#         print(len(sub_file_path))
#
#
# if __name__ == '__main__':
#     separate_image_files("/media/lessmart/data/sdh/22-3-30-add-mae/data/1111/标注/ch/")
