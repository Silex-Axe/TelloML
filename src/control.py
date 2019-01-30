import av
import numpy as np
import cv2
import threading
import time
import fractions
import sampler
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
        self.dron_actual_status = None 
        self.ml_actual_prediction = None 
        self.speed = 30

        self.controls = {
            "p": lambda dron,speed: self.startMlProcess(speed),
            "t": lambda dron,speed: self.startSampleTake(speed),
            "escape": lambda dron,speed: self.quitFunction(),
            'w': 'forward',
            's': 'backward',
            'a': 'left',
            'd': 'right',
            'up': 'up',
            'down': 'down',
            'space': 'up',
            'left shift': 'down',
            'right shift': 'down',
            #Add and decrease speed
            '1': lambda dron,speed: self.increaseSpeed(1),
            '0': lambda dron,speed: self.decreaseSpeed(1),

            # arrow keys for fast turns and altitude adjustments
            'q': 'counter_clockwise',
            'e': 'clockwise',
            'left': lambda dron, speed: dron.counter_clockwise(speed*2),
            'right': lambda dron, speed: dron.clockwise(speed*2),
            'tab': lambda dron, speed: dron.takeoff(),
            'backspace': lambda dron, speed: dron.land(),
            #Modify overall speed
        }
        #Init sampler
        self.sampler = sampler.Sampler()
        self.sampler.ctrl=self
    
    def increaseSpeed(self,n):
        self.speed = self.speed+1
   
    def decreaseSpeed(self,n):
        self.increaseSpeed(-n)

    #TODO - speed tiene que ser un booleano o un int y cambiar de nombre >:(
    def startMlProcess(self, speed):
        if speed is not 0:
            self.ml.start()
        print("startMlProcess")
    
    def startSampleTake(self,speed):
        
        if speed is not 0:
            print("startSampleTake")
            self.sampler.startSampling()
    
    def frameOut(self):
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
                    time.sleep(0.01)
                    if self.ml is not None:
                        self.ml_actual_prediction = self.ml.predictionOut()
   
                    if self.gui.running:
                        e = self.gui.eventOut()
                        if e is not None:      
                            print("input:",e)  
                            if e[0]=='-':
                                speed=0
                                e = e[1:]
                            else:
                                speed=self.speed
                            if e in self.controls:
                                key_handler = self.controls[e]
                                if type(key_handler) == str:
                                    getattr(self.dron, key_handler)(speed)
                                    #TODO - Quitar en un futuro?
                                    self.ml_actual_prediction = key_handler
                                else:
                                    key_handler(self.dron, speed)
                    else:
                        print("control: gui not running")
                        time.sleep(0.2)
            except Exception as ex:
                print("event thread exception: ", ex )
    
    def videoThread(self):
        try:
            container = av.open(self.dron.get_video_stream())
            
            #Record stuff
            '''
            record_seconds=4
            record_start = None
            recording=True
            container_2 =  av.open('test.mp4',mode='w')
            record_stream = container_2.add_stream('mpeg4', rate=24)
            record_stream.width = 960
            record_stream.height = 720
            record_stream.pix_fmt = 'yuv420p'
            '''
            #Drop first frames (to catch up)
            frame_skip=300
            generator = container.decode(video=0)

            #This is infinite because the frames will be appearing continuously
            for frame in generator:
                start_time = time.time()
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                image = frame.to_ndarray(format='rgb24')
                self.dron_actual_frame = image
                #Recording
                '''
                if record_start is None:
                    record_start = time.time()
                    print("Start recording:", record_start)
                if (record_start-time.time())/1000 < record_seconds:
                    for packet in record_stream.encode(frame):
                        container_2.mux(packet)
                elif recording :
                    print("stop recording:", record_start)
                    container_2.close()
                    recording=False
                print("tick",(record_start-time.time())/1000)
                '''
                time_base = max(1.0/60,frame.time_base)
                frame_skip = int((time.time()-start_time)/time_base)






        except Exception as ex:
            print("Video thread exception: ",ex)

    def flightDataHandler(self, event, sender, data):    
        #print("flightDataEvent: ",type(data),data)
        self.dron_actual_status = data

    def quit(self):
        #Close threads ?
        print("quit control")

    def quitFunction(self):
        self.quit_flag=True