'''根据txt label创建新的图片，并resize hand_img''' 
import glob 
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import random
import os
from multiprocessing import Pool
import time
# import concurrent.futures

def img_resize(img, W, H, pbg=None, print_img=None):
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
    if print_img == 'True':
        bg = pbg
    else:
        bg = Image.new('RGB', (360,64), (255,255,255))

    # 随机贴在白色背景上的位置
    bg_arry = aug_rand_place(W, H)

    bg.paste(imgResize, bg_arry)
    return bg.convert('RGB')


# 印刷体随机字体大小，字体类型
def aug_rand_font(fontdir):
    a = random.randint(0,2)
    fontSize = random.randint(16,24)
    fontPath = os.path.join(fontdir, os.listdir(fontdir)[a])
    fontText_1 = ImageFont.truetype(fontPath, fontSize, encoding="utf-8")# "./font/msyh.ttf"
    return fontText_1, fontSize


# 印刷体随机背景
def aug_rand_bg(img_w, img_h, bgdir):
    a = random.randint(0,2)
    bgPath = os.path.join(bgdir, os.listdir(bgdir)[a])
    bg = Image.open(bgPath)
    bg_1 = bg.resize((img_w+3, img_h+6))
    return bg_1, bg


# 手写体印刷体随机字体图片贴在背景的位置
def aug_rand_place(W, H):
    arry_W = random.randint(0, int(360-W))
    arry_H = random.randint(0, int(64-H))
    bg_arry = (arry_W, arry_H)
    return bg_arry


# 印刷体随机尺寸再还原，改变分辨率
def aug_rand_pix(image, W, H):
    ratio = random.randint(2,4)
    if W >= 100 and H >= 80:
        imgResize = image.resize((int(W/ratio), int(H/ratio)))
        img = imgResize.resize((W, H))
    else:
        img = image
    return img


def print_data(imgDir, imgFile, n):
    txtData = open(f'{imgDir}.txt', 'r', encoding='utf-8')
    imgFile = imgFile.replace('./', '')
    # print('imgFile === ', imgFile)
    for line in txtData:
        line = line.strip()
        imgPath = line.split('\t')[0]
        if './' in imgPath:
            imgPath = imgPath.replace('./', '')
        if imgPath == imgFile:
            label = line.split('\t')[-1]

            # 随机字体
            fontText_1, fontSize = aug_rand_font('fontdir')

            img_w = fontSize*len(label)

            # 随机文字写入的背景
            img_1, bg = aug_rand_bg(img_w, fontSize, 'bg_dir')
            # img_1 = Image.new('RGB', (img_w+12,64), (255,255,255))

            draw_1 = ImageDraw.Draw(img_1)
            draw_1.text((2,0), label, fill='black', font=fontText_1)
            W, H = img_1.size
            img = img_resize(img_1, W, H, bg, print_img='True')

            # 随机分辨率
            img = aug_rand_pix(img, W, H)
            img.save(f'images/print/down_{imgDir}_{n}.jpg')


def process_image(args):
    imgFile, n = args
    imgDir = imgFile.split('/')[1]
    img = Image.open(imgFile)
    W, H = img.size
    if W <= 8*H:
        print_data(imgDir, imgFile, n)
        img = img_resize(img, W, H)
        img.save(f'images/hand/down_{imgDir}_{n}.jpg')


if __name__=='__main__':
    imgRoot = ['/media/lessmart/data/sdh/2022-03-18-add-mae/images']
    a = 0
    for imgDir in imgRoot:
        # with concurrent.futures.ProcessPoolExecutor() as executor:
        start = time.time()
        imgPath = sorted(glob.glob(f'{imgDir}/*g'))
        print(len(imgPath))
        num = 0
        name_space = []
        for i in range(len(imgPath)):
            n = '%07d'%num
            name_space.append(n)
            num += 1
        pool = Pool(16)
        print(imgPath)

        pool.map(process_image, zip(imgPath, name_space))
        pool.close()
        pool.join()
        end = time.time()
        print(f"processed_{a} sucess: time {end-start}")
            # for imgFile in tqdm(imgPath):
            # for processedimg in zip(imgPath, executor.map(process_image, imgPath, name_space)):
        print(imgDir)
        print(num)

