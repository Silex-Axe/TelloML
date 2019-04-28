
class AutonomousControl(object):
    '''
    Basic automatic controller that keeps position and does nothing :)
    '''
    def __init__(self):
        self.data_in = None
        self.data_out = None
        self.prediction = 'stop'
    
    def setDataIn(self,data_in):
        self.data_in = data_in
        
    def start(self):
        pass
    
    def predictionOut(self):
        return self.prediction

    def quit(self):
        pass
    