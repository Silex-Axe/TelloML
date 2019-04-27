from data_in import In
import threading
import cv2

class LaptopCamera(In):
    '''Gets the video feed from the computer's camera'''
    def __init__(self):
        In.__init__(self)
        self.capturing_video = True
        threading.Thread(target=self.videoThread, args=[]).start()

    def videoThread(self):    
        cap = cv2.VideoCapture(0)
        while(self.capturing_video):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Our operations on the frame come here
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.actual_frame = frame

    def quit(self):
        print("Quit laptop_camera")
        self.capturing_video = False
