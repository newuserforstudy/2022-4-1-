from directions_predict import Direction
import numpy as np
import glob
from PIL import Image
import torch

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# rotate


def rotate(img):
    angle_ = direction.predict(img)
    print(angle_)
    if angle_:
        count = int(int(angle_)/90)


        for i in range(count):

            img = np.rot90(img)
    return img



if __name__ == '__main__':
    direction = Direction(model_path='./direction/shufflenet.pth')
    imgPath = glob.glob(f'/media/lessmart/data/student_do_answer_data/img-20211223/*g')

    print("images nums= ",len(imgPath))
    try:
        for i,imgfile in enumerate(imgPath):

                imga = np.array(Image.open(imgfile))
                imgb = rotate(imga)
                img = Image.fromarray(imgb)
                # img.save(imgfile)
    except Exception as e :
        print("skip-------------")

    print("===over!")


