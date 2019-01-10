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

        pygame.init()
        screen_width,screen_height = 960,720
        self.screen = pygame.display.set_mode((screen_width,screen_height)) 
        # Abrimos un nuevo hilo para gestionar la GUI (entradas y salidas)
        threading.Thread(target=self.guiIO, args=[]).start()


    def setCtrl(self, ctrl):
        self.ctrl = ctrl

    def eventOut(self):
        events = []
        for e in  pygame.event.get():
            if e.type == pygame.locals.KEYDOWN:
                keyname = pygame.key.name(e.key)
                events+=[keyname]
        return events

    def guiIO(self):
        self.font = pygame.font.SysFont("dejavusansmono", 32)

        try:
         while True:
            time.sleep(0.01) # Slow down boy!
            self.screen.fill((0,0,0))
            self.updateVisibleFrame()            
            self.updateHUD()
            pygame.display.update()
        except Exception as e:
            print("Exception ",e)

    def updateHUD(self):
        # Update flight data
        # Show direction 

        #size: (960,720)
        screen_width,screen_height = self.screen.get_size()
        stroke_width = 10

        #Draw corners/movement/prediction 
        #tl
        #pygame.draw.rect(self.screen, (255,0,0),(0,0,stroke_width,stroke_width),0)    
        #tr
        #pygame.draw.rect(self.screen, (255,0,0),(screen_width-stroke_width,0,stroke_width,stroke_width),0)
        #br
        #pygame.draw.rect(self.screen, (255,0,0),(screen_width-stroke_width,screen_height-stroke_width,stroke_width,stroke_width),0)
        #bl
        #pygame.draw.rect(self.screen, (255,0,0),(0,screen_height-stroke_width,stroke_width,stroke_width),0)
        
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
        
        dron_status = self.ctrl.statusOut()
        #Draw HUD values
        #╔    ═    ╗
        #        
        #║         ║
        #  ALT BAT
        #╚ SPD═NET ╝
        #dron_status.height
        #dron_status.ground_speed
        #dron_status.battery_percentage
        #dron_status.wifi_strength
        #dron_status.camera_state
        #dron_status.fly_mode
        if dron_status is not None:
            blits = []
            # Columna 1
            (w,h) = (100,screen_height) 
            surface = self.font.render("Height: "+dron_status.height, True, (255,0,0))
            h -= surface.get_height()
            blits += [(surface, (w, h))]

            surface = self.font.render("Speed: "+dron_status.ground_speed, True, (255,0,0))
            h -= surface.get_height()
            blits += [(surface, (w, h))]

            surface = self.font.render("Fly mode: "+dron_status.fly_mode, True, (255,0,0))
            h -= surface.get_height()
            blits += [(surface, (w, h))]

            # Columna 2
            (w,h) = (580,screen_height)  
            surface = self.font.render("Battery: "+dron_status.battery_percentage, True, (255,0,0))
            h -= surface.get_height()
            blits += [(surface, (w, h))]

            surface = self.font.render("Wifi: "+dron_status.wifi_strength, True, (255,0,0))
            h -= surface.get_height()
            blits += [(surface, (w, h))]

            surface = self.font.render("Camera: "+dron_status.camera_state, True, (255,0,0))
            h -= surface.get_height()
            blits += [(surface, (w, h))]
            
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            for blit in blits:
                overlay.blit(*blit)
            pygame.display.get_surface().blit(overlay, (0,0))
            pygame.display.update(overlay.get_rect())

    def updateVisibleFrame(self):
        #if self.ctrl.frameOut() is not None: print("Frame size:",self.ctrl.frameOut().shape)
        if self.current_frame is not self.ctrl.frameOut():
            #Color correction for pygame
            frame = cv2.cvtColor(self.ctrl.frameOut(), cv2.COLOR_BGR2RGB)
            #rotation correction for pygame
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)                
            self.screen.blit(frame,(0,0))
            self.current_image = self.ctrl.frameOut()
    
    def quit(self):
        #Close threads ?
        print("quit gui")