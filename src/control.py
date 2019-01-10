import av
import numpy as np
import cv2
import threading
import time
class Control(object):
    '''
        Clase de control entre dron, gui y ml
    '''
    def __init__(self):

        self.ml = None
        self.dron = None
        self.gui = None
        self.quit_flag=False
        self.dron_actual_frame = None #Se obtiene del video_stream de dron_in
        self.dron_actual_status = None #
        self.ml_actual_prediction = None #

        self.speed = 40

        self.controls = {
            "p": lambda drone,speed: self.startMlProcess(),
            "t": lambda drone,speed: self.startSampleTake(),
            "escape": lambda drone,speed: self.quitFunction(),
            'w': 'forward',
            's': 'backward',
            'a': 'left',
            'd': 'right',
            'up': 'up',
            'down': 'down',
            'space': 'up',
            'left shift': 'down',
            'right shift': 'down',
            'q': 'counter_clockwise',
            'e': 'clockwise',
            # arrow keys for fast turns and altitude adjustments
            'left': lambda drone, speed: drone.counter_clockwise(speed*2),
            'right': lambda drone, speed: drone.clockwise(speed*2),

            'tab': lambda drone, speed: drone.takeoff(),
            'backspace': lambda drone, speed: drone.land(),
            #Modify overall speed
            '1': lambda drone,speed: self.increaseSpeed(1),
            '0': lambda drone,speed: self.decreaseSpeed(1)
        }
    
    def increaseSpeed(self,n):
        self.speed = self.speed+1
   
    def decreaseSpeed(self,n):
        self.increaseSpeed(-n)
        
    def startMlProcess(self):
        print("startMlProcess")
    
    def startSampleTake(self):
        print("startSampleTake")
    
    def frameOut(self):
        #return "Imagen"
        return self.dron_actual_frame

    def statusOut(self):
        return self.dron_actual_status

    def predictionOut(self):
        return self.ml_actual_prediction

    def setDron(self,dron):
        self.dron = dron
        #Setup listeners and threads
        threading.Thread(target=self.videoThread, args=[]).start()
        dron.subscribe(dron.EVENT_FLIGHT_DATA, self.flightDataHandler)

    def setGui(self,gui):
        self.gui = gui
        self.gui.ctrl = self
        threading.Thread(target=self.eventsThread,args=[]).start()
    
    def setMl(self,ml):
        self.ml = ml
        ml.ctrl = self
    
    def eventsThread(self):
        try:
            while True:
                for e in self.gui.eventOut():
                    time.sleep(0.01) #Slow down buddy
                    if e in self.controls:
                        key_handler = self.controls[e]
                        if type(key_handler) == str:
                            getattr(self.dron, key_handler)(self.speed)
                            #TODO - Remove in the future
                            self.ml_actual_prediction = key_handler
                        else:
                            key_handler(self.dron, self.speed)
                    else:
                        print("Unknown command: ", e)       
        except Exception as ex:
            print("event thread exception: ", ex )
    
    def videoThread(self):
        try:
            container = av.open(self.dron.get_video_stream())
            #Drop first frames (to catch up)
            frame_skip=500
            #This is infinite because the frames will be appearing continuously
            for frame in container.decode(video=0):
                if 0<frame_skip:
                    frame_skip = frame_skip - 1
                    continue                    
             
                start_time = time.time()
                image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)            
                self.dron_actual_frame=image
                if frame.time_base<1.0/60:
                    time_base = 1.0/60
                else:
                    time_base=frame.time_base
                frame_skip = int((time.time()-start_time)/time_base)
        except Exception as ex:
            print(ex)

    def flightDataHandler(self, event, sender, data):    
        #print("flightDataEvent: ",type(data),data)
        self.dron_actual_status = data

    def quit(self):
        #Close threads ?
        print("quit control")

    def quitFunction(self):
        self.quit_flag=True