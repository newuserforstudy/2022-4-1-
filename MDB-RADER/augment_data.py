# coding:utf-8
# @time:2022/3/17下午2:11
# @author:sdh
"""
印刷体数据增强的几种方法：
1 添加背景：白色、随机背景(学生作业的背景)
           #D8D8D8、#F2F2F2、#FAFAFA、#FBEFF2、#FBFBEF、#F7F8E0、#CED8F6、#F8ECE0、#EFF5FB、#A4A4A4、#FF0000
2 设置不同的字体：中文字体、英文字体、数学公式字体
3 设置字体的大小：font-size
4 尺寸缩放：缩小放大、放大缩小


"""
from PIL import Image, ImageDraw, ImageFont
import random


def make_background(image_path):
    """

    :param image_path: image path
    :return: new image
    """
    img = Image.open(image_path)
    print(img.size)
    w, h = img.size[0], img.size[1]
    if w > 360 and h <= 64:
        ratio = 360 / w
    elif w <= 360 and h > 64:
        ratio = 64 / h
    else:
        ratio_w = 360 / w
        ratio_h = 64 / h
        ratio = min(ratio_w, ratio_h)

    w = int(ratio * w)
    h = int(ratio * h)
    resize_img = img.resize((w, h))

    for i in range(50):
        index = random.randint(0, 10)
        print(index)
        bg = Image.new('RGB', (360, 64), background_list[index])
        paste_into_region = (int((360 - w) / 2), int((64 - h) / 2))
        bg.paste(resize_img, paste_into_region)

        new_img = bg.convert('RGB')
        new_img.save(f"./{i}.jpg")


def read_text_make_images(txt_path):
    i = "%06d" % 0
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            image_path = line.split("\t")[0]
            line_content = line.split("\t")[-1]

            # 1 设置字体大小
            font_size = random.randint(16, 24)

            # 2 随机设置字体类型
            font_index = random.randint(0, len(font_type))
            fontText_1 = ImageFont.truetype(font_type[font_index], 24, encoding="utf-8")

            # 3 设置随机的背景
            back_ground_index = random.randint(0, len(background_list))
            bg = Image.new('RGB', (360, 64), background_list[back_ground_index])

            # 4 把文字写入图像
            img_h = font_size + 6
            img_w = len(line_content) * font_size
            if img_h > 64:
                img_h = 64
            if img_w > 360:
                img_h = 360
            img_1 = Image.new('RGB', (img_w, img_h), (255, 255, 255))
            draw_1 = ImageDraw.Draw(img_1)

            # 5 从最左边将文字写入到图像
            x, y = (3, 3)
            draw_1.text((x, y), line_content, fill='black', font=fontText_1)

            # 6 从随机位置开始贴图
            p_x = random.randint(0, 360 - img_w)
            p_y = random.randint(0, 64 - img_h)
            bg.paste(img_1, (p_x, p_y))

            # 7 进行缩放:先放再缩
            new_img1 = img_1.resize((int(2 * img_w), int(2 * img_h)))
            new_img2 = new_img1.resize((img_w, img_h))
            
            new_img2.save('1.jpg')


if __name__ == '__main__':

    background_list = ["#D8D8D8", "#F2F2F2", "#FAFAFA", "#FBEFF2", "#FBFBEF", "#F7F8E0", "#CED8F6", "#F8ECE0",
                       "#EFF5FB", "#A4A4A4", "#FFFFFF"]
    font_type = ["./font/msyh.ttf", ""]
    root_dir = "/media/lessmart/data/sdh/22-03-16-add-mae/document"

    make_background("images/00.jpg", )
