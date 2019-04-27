from data_in import In
from out import Out
import tellopy
class DronTello(In,Out):
    '''
     Specific class for the tello drone integration
    '''
    def __init__(self):    
        In.__init__(self)
        Out.__init__(self)        
        self.dron = tellopy.Tello()
        self.dron.connect()
        self.dron.start_video()
        self.capturing_video = True
        threading.Thread(target=self.videoThread, args=[]).start()
        dron.subscribe(dron.EVENT_FLIGHT_DATA, self.flightDataHandler)

    def videoThread(self):
        try:
            container = av.open(self.dron.get_video_stream())
            #Drop first frames (to catch up)
            frame_skip=300
            generator = container.decode(video=0)
            # This is infinite because the frames will be appearing continuously, 
            # the generator yields new frames as they are generated
            for frame in generator:
                #Break out if we stop capturing
                if(self.capturing_video==False):
                    break
                start_time = time.time()
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                image = frame.to_ndarray(format='rgb24')
                self.actual_frame = image
                time_base = max(1.0/60,frame.time_base)
                frame_skip = int((time.time()-start_time)/time_base)
        except Exception as ex:
            print("Video thread exception: ",ex)

    def flightDataHandler(self, event, sender, data):    
        self.status = data
    
    def quit(self):
        print("Quit DronTello")
        self.capturing_video = False