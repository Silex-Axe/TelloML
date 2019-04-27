from data_out import Out

from flask import Flask
from flask_cors import CORS, cross_origin
import threading
import time

class GameController(Out):
    '''
    Does nothing, is just a placeholder for when I don't have a Drone
    I will try to connect it to a little p5.js game or something of the likes
    '''
    def __init__(self):
        Out.__init__(self)
        self.state = 'stop'
        self.app=None
        answer_questions_thread = threading.Thread(target=self.setup_webservice)
        answer_questions_thread.start()

    def setup_webservice(self):
        self.app = Flask(__name__)
        cors = CORS(self.app)
        self.app.config['CORS_HEADERS'] = 'Content-Type'
        @self.app.route("/")
        def hello():
            print(self.state)
            return self.state
        self.app.run(port=9000)

    def up(self):
        self.state='up'

    def down(self):
        self.state='down'

    def left(self):
        self.state='left'

    def right(self):
        self.state='right'

    def forward(self):
        self.state='forward'

    def backward(self):
        self.state='backward'

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

    def quit():
        print("Quit GameController")