from PIL import Image
import numpy as np
import os
import time
import threading
class Sampler(object):
    '''
    This is an object that can save frames to meory for later usage.
    
    '''
    def __init__(self):
        self.base_path ="./model_data/samples/"
        self.class_name="default"
        self.num_samples=200
        self.take = 0
        self.ctrl = None    
    
    def startSampling(self):
        self.take +=1
        threading.Thread(target=self.sampleThread, args=[]).start()
    
    def sampleThread(self):
        self.askQuestions()
        try:
            self.createFolder()
            i = 0
            current_img = None
            while i < self.num_samples:
                time.sleep(0.05)# Para no petar los recursos TODO- Optimizar el uso de sleep Barreras/colas?
                np_img = self.getSample()
                if current_img is not np_img:
                    print("new image with shape: ",np_img.shape)
                    current_img = np_img
                    path = self.base_path+self.class_name+ str(self.take)+"/"+str(i)+".bmp"
                    self.saveImage(path,np_img)
                    i+=1
                else:
                    print("Same image")
        except Exception as ex:
            print("Sampler thread exception: ",ex)


    def askQuestions(self):
        print("Will save ",self.num_samples," samples in '"+self.folder_path()+"'")
        print("Will start recording samples in:")
        seconds = 5
        print(seconds,"seconds")
        while seconds > 0:
            time.sleep(1)
            seconds-=1
            print(seconds,"seconds")

    def getSample(self):
        #Obtener sample desde Control
        if self.ctrl is not None:
            return self.ctrl.dron_actual_frame
        else:
            return None

    def folder_path(self):
        return self.base_path+self.class_name+str(self.take)

    def createFolder(self):
        #TODO - Fix this shit
        if not os.path.exists(self.folder_path()):
            print("Generating folders: '"+self.folder_path()+"'")
            os.makedirs(self.folder_path())
        else:
            print("Unable to create folder", os.path.exists(self.folder_path()))

    def npToImage(self, nparray):
        img = Image.fromarray(nparray.astype('uint8'))
        return img

    def saveImage(self,path_name,nparray):
        self.npToImage(nparray).save(path_name)
