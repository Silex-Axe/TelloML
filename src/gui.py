import threading
import pygame
import pygame.display
import pygame.key
import pygame.locals
import pygame.font
import time
import cv2
import numpy as np
class GUI(object):
    BACKGROUND_COLOR=(100,200,200)
    

    def __init__(self):        
        #self.ctrl_in = "Video Stream/Frame", "Dron Status", "Prediction [, ?] "
        self.ctrl = None
        self.data_in = None
        self.data_out = None

        self.autonomous_control = None
        self.autonomous_control_activated=False
        
        self.current_frame = None # "Old frame nparray"
        self.new_frcurrent_frameame = None #"New frame nparray"
        self.screen = None
        self.event_key = None
        self.running = False
        self.window_name = "Dron controller"
        #Controls definition
        self.controls = {
            'p': lambda out: self.startMlProcess(),
            't': lambda out: self.startSampleTake(),
            'escape': lambda out: self.quit(),
            'w': lambda out: out.forward(),
            's': lambda out: out.backward(),
            'a': lambda out: out.left(),
            'd': lambda out: out.right(),
            'up': lambda out: out.up(),
            'down': lambda out: out.down(),
            'space': lambda out: out.up(),
            'left shift': lambda out: out.down(),
            'right shift':  lambda out: out.down(),
            #Add and decrease speed
            '1': lambda out: out.speed_up(),
            '0': lambda out: out.speed_down(),
            # arrow keys for fast turns and altitude adjustments
            'q': lambda out: out.counter_clockwise_spin(),
            'e': lambda out: out.clockwise_spin(),
            'left': lambda out: out.counter_clockwise_spin(),
            'right': lambda out: out.clockwise_spin(),
            'tab': lambda out: out.takeoff(),
            'backspace': lambda out: out.land(),
            #Modify overall speed
        }

    def start(self): 
        print("Init gui")
        pygame.init()
        self.font = pygame.font.SysFont("dejavusansmono", 32)
        self.running = True
        screen_width,screen_height = 960,720
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption(self.window_name) 
        pygame.display.update()
        
        #This takes up the main thread which makes sense because the whole program is controlled from the GUI
        self.guiMain()

    def guiMain(self):
        print("Start gui bucle")
        while self.running:
            try:
                #Sleep so we don't take up too much processor time(?) TODO - find a better way to manage this loop
                time.sleep(0.01)
                # Autonomous control
                if self.autonomous_control is not None and self.autonomous_control_activated:
                    self.ml_actual_prediction = self.autonomous_control.predictionOut()

                for e in pygame.event.get():
                    #Keydown (start action)
                    if e.type == pygame.locals.KEYDOWN:
                        print("+"+pygame.key.name(e.key))
                        key_handler = self.controls[pygame.key.name(e.key)]
                        if key_handler!=None:
                            key_handler(self.data_out)

                    #Keyup (Stop action)
                    elif e.type == pygame.locals.KEYUP:
                        print("-"+pygame.key.name(e.key))

                    #Quit
                    elif e.type == pygame.QUIT:
                        self.running = False
                      
                self.screen.fill(self.BACKGROUND_COLOR)
                self.updateVisibleFrame()            
                self.updateHUD()
                pygame.display.update()# Equal to flip() in this case
            except Exception as e:
                print("Exception ",e)

    def setCtrl(self, ctrl):
        self.ctrl = ctrl

    def setDataIn(self,data_in):
        self.data_in = data_in
        
    def setDataOut(self,data_out):
        self.data_out = data_out

    def setAutonomousControl(self,controller):
        self.auto_controller = controller

    def eventOut(self):
        #Consume the stored event
        event = self.event_key
        self.event_key = None
        return event

    def updateHUD(self):
        '''
        Draw HUD values
        ╔    ═    ╗
                
        ║         ║
          ALT BAT
        ╚ SPD═NET ╝
        '''
        screen_width,screen_height = self.screen.get_size()
        stroke_width = 10
        if self.ctrl is not None:
            #top
            if(self.ctrl.predictionOut()== "up"): pygame.draw.rect(self.screen, (255,0,0),(screen_width/2-stroke_width*1.5,0,stroke_width*3,stroke_width),0)
            #right
            if(self.ctrl.predictionOut()== "right"): pygame.draw.rect(self.screen, (255,0,0),(screen_width-stroke_width,screen_height/2-stroke_width*1.5,stroke_width,stroke_width*3),0)
            #bottom
            if(self.ctrl.predictionOut()== "down"): pygame.draw.rect(self.screen, (255,0,0),(screen_width/2-stroke_width*1.5,screen_height-stroke_width,stroke_width*3,stroke_width),0)
            #left
            if(self.ctrl.predictionOut()== "left"): pygame.draw.rect(self.screen, (255,0,0),(0,screen_height/2-stroke_width*1.5,stroke_width,stroke_width*3),0)

            #forward
            if(self.ctrl.predictionOut()== "forward"): pygame.draw.rect(self.screen, (255,0,0),(screen_width/2-stroke_width*1.5,screen_height/2-stroke_width*1.5,stroke_width*3,stroke_width*3),0)
            #backward
            if(self.ctrl.predictionOut()== "backward"): pygame.draw.rect(self.screen, (255,255,0),(screen_width/2-stroke_width*0.5,screen_height/2-stroke_width*0.5,stroke_width,stroke_width),0)
        
        blits = []
        if self.data_in is not None: 
            dron_status = self.data_in.status
            if dron_status is not None:
                # Columna 1
                (w,h) = (100,screen_height) 
                surface = self.font.render("Height: %3d" % dron_status.height, True, (255,0,0))
                h -= surface.get_height()
                blits += [(surface, (w, h))]

                surface = self.font.render("Speed: %3d"%dron_status.ground_speed, True, (255,0,0))
                h -= surface.get_height()
                blits += [(surface, (w, h))]

                surface = self.font.render("Fly mode: %s" % dron_status.fly_mode, True, (255,0,0))
                h -= surface.get_height()
                blits += [(surface, (w, h))]

                # Columna 2
                (w,h) = (580,screen_height)  
                surface = self.font.render("Battery: %3d"%dron_status.battery_percentage, True, (255,0,0))
                h -= surface.get_height()
                blits += [(surface,quit (w, h))]

                surface = self.font.render("Wifi: %3d"%dron_status.wifi_strength, True, (255,0,0))
                h -= surface.get_height()
                blits += [(surface, (w, h))]

                surface = self.font.render("Camera: %s"%dron_status.camera_state, True, (255,0,0))
                h -= surface.get_height()
                blits += [(surface, (w, h))]
            
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            for blit in blits:
                overlay.blit(*blit)
            pygame.display.get_surface().blit(overlay, (0,0))
            pygame.display.update(overlay.get_rect())

    def updateVisibleFrame(self):
        if self.data_in is not None:
            frame = self.data_in.getFrame()
            if self.current_frame is not frame:
                #rotation correction for pygame
                frame = cv2.resize(frame, dsize=(960,720), interpolation=cv2.INTER_CUBIC)
                frame = np.rot90(frame)
                frame = np.flip(frame, axis=0)
                frame = pygame.surfarray.make_surface(frame)                
                self.screen.blit(frame,(0,0))
                self.current_image = frame
        else:
            print("Unable to find data in")

    def eventsThread(self):
        '''
            Gets the events from user interaction and the autonomous control system.
        '''
        try:
            while True:
                time.sleep(0.01)
                # Autonomous control
                if self.autonomous_control is not None and self.autonomous_control_activated:
                    self.ml_actual_prediction = self.ml.predictionOut()
                # User control
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
    
    def quit(self):
        print("Quit gui")
        #Send quit to the other threads
        if self.data_out is not None: 
            self.data_out.quit()
        if self.data_in is not None:
            self.data_in.quit()
        if self.autonomous_control is not None: 
            self.autonomous_control.quit()

        pygame.quit()
        exit(0)

    