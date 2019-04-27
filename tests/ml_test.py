
import numpy as np
from tensorflow.python.keras.preprocessing.image import load_img, img_to_array
import threading
import time
class ControlDummy(object):
    def __init__(self):
        pass
    def frameOut(self):
        img_height=240
        img_width=320
        img_path = './forward_144.bmp'
        img = load_img(img_path,target_size=(img_height,img_width))  
        img = img_to_array(img)
        print(type(img))
        return img

import ml as m
ml = m.ML()
ctrl = ControlDummy()
ml.ctrl = ctrl
ml.start()
