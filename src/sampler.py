from PIL import Image
import numpy as np
import os
import time
import threading
class Sampler(object):
    def __init__(self):
        self.base_path ="./model_data/samples/"
        self.class_name="default"
        self.num_samples=100
        self.ctrl = None    
    
    def startSampling(self):

        threading.Thread(target=self.sampleThread, args=[]).start()
    
    def sampleThread(self):
        self.askQuestions()
        try:
            self.createFolder()
            i = 0
            current_img = None
            while i < self.num_samples:
                time.sleep(0.01)# Para no petar los recursos TODO- Optimizar el uso de sleep Barreras/colas?
                np_img = self.getSample()
                if current_img is not np_img:
                    print("new image with shape: ",np_img.shape)
                    current_img = np_img
                    path = self.base_path+self.class_name+"/"+str(i)+".bmp"
                    self.saveImage(path,np_img)
                    i+=1
                else:
                    print("Same image")
        except Exception as ex:
            print("Sampler thread exception: ",ex)


    def askQuestions(self):
        print("Will save ",self.num_samples," samples in '"+self.base_path+self.class_name+"'")

    def getSample(self):
        #Obtener sample desde Control
        if self.ctrl is not None:
            return self.ctrl.dron_actual_frame
        else:
            return None

    def createFolder(self):

        if not os.path.exists(self.base_path+self.class_name):
            print("Generating folders: '"+self.base_path+"'")
            os.makedirs(self.base_path+self.class_name)
        else:
            print("unable to create folder", os.path.exists(self.base_path+self.class_name))

    ## Debería hacer un modulo para estas funciones 'ImageUtils?'
    def npToImage(self, nparray):
        img = Image.fromarray(nparray.astype('uint8'))
        return img

    def saveImage(self,path_name,nparray):
        self.npToImage(nparray).save(path_name)
