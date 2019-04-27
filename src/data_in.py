class In(object):
    '''
    This class handles input from different sources and is able to communicate it 
    to the rest of the system. For example, gets the video feed from a drone or 
    a camera.
    '''
    def __init__(self):
        self.video_feed = None
        self.actual_frame = None
        self.status = None

    def getFrame(self):
        return self.actual_frame

    def quit(self):
        print("Quit In")