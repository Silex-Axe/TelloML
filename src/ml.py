import threading
import time
import numpy as np
from tensorflow.python import keras
from tensorflow.python.keras.models import model_from_json
#Usamos resnet50 por ahora, así que hay que preprocesar la entrada con esto
from tensorflow.python.keras.applications.resnet50 import preprocess_input
import cv2
from autonomous_control import AutonomousControl

#ml stands for Machine Learning (Module)
class ML(AutonomousControl):
    def __init__(self):
        AutonomousControl.__init__(self)
        self.ctrl_in = "Imagen"
        self.driving = False
        self.ctrl=None
        self.model_path = "./model_data/"
        self.model = None
        self.prediction = None
        self.data_in = None

    def start(self):
        self.driving=True
        threading.Thread(target=self.mlThread, args=[]).start()
    
    def stop(self):
        self.driving=False
    def setDataIn(self,data_in):
        self.data_in = data_in
    def mlThread(self):
        print("Loading ML model")
        self.model = self.loadKerasModel(self.model_path)
        img_height,img_width=240,320
        current_frame = None

        while self.driving:
            time.sleep(0.01)
            if self.data_in is not None:
                frame = self.data_in.getFrame()
                if frame is not current_frame:
                    current_frame = frame
                    frame = cv2.resize(frame, dsize=(img_height, img_width), interpolation=cv2.INTER_CUBIC)
                    img_array = np.array([frame])
                    frame = preprocess_input(img_array)
                    # Dejar el frame ready para el modelo
                    prediction = self.model.predict(frame)
                    predictions=['backward','forward','left','right','stop']
                    self.prediction = predictions[prediction.argmax(axis=-1)[0]]
                    print("Prediction:",self.prediction)
              
    def predictionOut(self):
        return self.prediction
    
    def quit(self):
        print("quit ml")
        self.stop()
        pass

    def loadKerasModel(self,path):
        print("loadKeras model")
        try:
            json_file =  open(path+'model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
            loaded_model.load_weights(path+"model.h5")
            print("Loaded model from disk")
            loaded_model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
            self.model = loaded_model
            return loaded_model
        except Exception as e:
            print("Exception loading model:",e)
