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
    def __init__(self):
        
        #self.ctrl_in = "Video Stream/Frame", "Dron Status", "Prediction [, ?] "
        self.ctrl = None
        self.current_frame = None # "Old frame nparray"
        self.new_frame = None #"New frame nparray"
        self.screen = None
        self.event_key = None
        self.running = False
        self.window_name = "Dron controller"

    def init(self): 
        print("Init gui")
        pygame.init()
        self.font = pygame.font.SysFont("dejavusansmono", 32)
        self.running = True
        background_colour = (100,200,200)
        screen_width,screen_height = 960,720
        self.screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption(self.window_name) 
        pygame.display.update()
        try:
            print("Start gui bucle")
            while self.running:
                time.sleep(0.01)
                for e in  pygame.event.get():
                    if e.type == pygame.locals.KEYDOWN:
                        keyname = pygame.key.name(e.key)
                        if(keyname is not self.event_key):
                            self.event_key = keyname
                            
                    elif e.type == pygame.locals.KEYUP:
                        keyname = pygame.key.name(e.key)
                        keyname = "-"+keyname
                        if(keyname is not self.event_key):
                            self.event_key = keyname

                    elif e.type == pygame.QUIT:
                        self.running = False

                self.screen.fill(background_colour)
                self.updateVisibleFrame()            
                self.updateHUD()
                #Preservamos el último evento :/
                pygame.display.update()# Equal to flip() in this case
        except Exception as e:
            print("Exception ",e)

                

    def setCtrl(self, ctrl):
        self.ctrl = ctrl

    def eventOut(self):
        #Consume the stored event
        event = self.event_key
        self.event_key = None
        return event

    def updateHUD(self):
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
        
       
        #Draw HUD values
        #╔    ═    ╗
        #        
        #║         ║
        #  ALT BAT
        #╚ SPD═NET ╝
        if self.ctrl is not None: 
            dron_status = self.ctrl.statusOut()
        if dron_status is not None:
            blits = []
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
            blits += [(surface, (w, h))]

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
        if self.ctrl is not None:
            frame = self.ctrl.frameOut()
            if self.current_frame is not frame:
                #rotation correction for pygame
                frame = np.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)                
                self.screen.blit(frame,(0,0))
                self.current_image = frame
    
    def quit(self):
        #Close threads ?
        print("quit gui")