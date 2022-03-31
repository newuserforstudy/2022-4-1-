# coding:utf-8
# @time:2022/3/15下午3:20
# @author:sdh

from paddleocr import PaddleOCR
from PIL import Image
import glob
import os
import random


# 印刷体随机尺寸再还原，改变分辨率
def aug_rand_pix(image, W, H):
    ratio = random.randint(2, 4)
    if W >= 100 and H >= 80:
        imgResize = image.resize((int(W / ratio), int(H / ratio)))
        img = imgResize.resize((W, H))
    else:
        img = image
    return img


def aug_rand_place(W, H):
    arry_W = random.randint(0, int(360 - W))
    arry_H = random.randint(0, int(64 - H))
    bg_arry = (arry_W, arry_H)
    return bg_arry


def img_resize(img, W, H):
    if W > 360 and H <= 64:
        ratio = 360 / W
    elif W <= 360 and H > 64:
        ratio = 64 / H
    else:
        ratio_W = 360 / W
        ratio_H = 64 / H
        ratio = min(ratio_W, ratio_H)

    W = int(ratio * W)
    H = int(ratio * H)

    imgResize = img.resize((W, H))
    bg = Image.new('RGB', (360, 64), (255, 255, 255))

    # 随机贴在白色背景上的位置
    bg_arry = aug_rand_place(W, H)

    bg.paste(imgResize, bg_arry)
    return bg.convert('RGB')


def DBNet(image_path, output_img_path, language="ch"):
    """
    :param language: 检测的语言
    :param output_img_path: 输出图像路径
    :param image_path: 图像路径
    :return: 新图像
    """

    images_list = sorted(glob.glob(image_path + "/*g"))
    print("image_nums: ", len(images_list))

    num = 0
    for i, each_image in enumerate(images_list):

        try:
            n1 = '%06d' % num
            ocr = PaddleOCR(use_angle_cls=True, lang=language)
            result = ocr.ocr(each_image, cls=True)
            nnn = 0
            for j, post_items in enumerate(result):
                n2 = '%04d' % nnn
                positions = post_items[0]
                # print(positions)

                pos_left_up, pos_right_down = positions[0], positions[2]
                x0, y0 = pos_left_up[0], pos_left_up[1]
                x1, y1 = pos_right_down[0], pos_right_down[1]
                x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

                img_content = Image.open(each_image).convert('RGB')
                cut_image = img_content.crop((x0, y0, x1, y1))

                w, h = cut_image.size

                if w <= 8 * h:

                    n_img = img_resize(cut_image, w, h)
                    n_img.save(output_img_path + 'card_' + str(n1) + "_" + str(n2) + ".jpg")
                else:

                    cut_image_1 = cut_image.crop((0, 0, int(w / 2), h))
                    w_1, h_1 = cut_image_1.size

                    n_img_1 = img_resize(cut_image_1, w_1, h_1)
                    n_img_1.save(output_img_path + 'card_' + str(n1) + "_" + str(n2) + '_1' + ".jpg")

                    cut_image_2 = cut_image.crop((int(w / 2), 0, w, h))

                    w_2, h_2 = cut_image_2.size
                    n_img_2 = img_resize(cut_image_2, w_2, h_2)
                    n_img_2.save(output_img_path + 'card_' + str(n1) + "_" + str(n2) + '_2' + ".jpg")

                nnn += 1
            num += 1
        except Exception as e:
            print("skip 第:%d张图像,名为: %s" % (i, each_image))


if __name__ == '__main__':
    imgs_path = "/media/lessmart/data/student_do_answer_data/img-20211223"
    output_path = "/media/lessmart/data/student_do_answer_data/re/"
    DBNet(imgs_path, output_path)
