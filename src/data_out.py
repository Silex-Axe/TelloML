class Out(object):
    '''
    This class handles the output to the device that's being controlled by the system.
    We assume that this is a Drone or a mobile system right now and so we have functions
    to move on a 3D space 
    '''
    BASE_SPEED = 30
    def __init__(self):
        self.speed = self.BASE_SPEED

    def up(self):
        pass
    def down(self):
        pass
    def left(self):
        pass
    def right(self):
        pass
    def forward(self):
        pass
    def backward(self):
        pass
    def clockwise_spin(self):
        print("clockwise_spin")
        pass
    def counter_clockwise_spin(self):
        print("counter_clockwise_spin")
        pass
    def take_off(self):
        pass
    def land(self):
        pass

    def speed_up(self,n):
        self.speed+=n

    def speed_down(self,n):
        self.speed-=n

    def set_speed(self,speed):
        self.speed = speed
    
    def quit(self):
        print("Quit Out")