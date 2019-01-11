import sys
import time
import tellopy

# Levantar y monitorizar servicios
# Crea a control, ml y gui y los comunica
# Si se caen los levanta de nuevo (Docker?)
sys.path += ["src"]

import control
import gui as g
import ml as m



def main():
    global dron, ctrl, gui, ml
    dron = tellopy.Tello()
    dron.connect()
    dron.start_video()

    ctrl = control.Control()
    gui = g.GUI()
    ml = m.ML()

    #Setup interconnections    
    ctrl.setDron(dron)
    ctrl.setGui(gui)
    ctrl.setMl(ml)   

    #Empieza La GUI
    gui.init()
    

def endProgram():
    global dron, ctrl, gui, ml
    print("Out!")
    ml.quit()
    gui.quit()
    dron.quit()
    ctrl.quit()
    exit(0)

if __name__ == '__main__':
    main()
