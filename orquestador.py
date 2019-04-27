import sys
import time
import tellopy

# Levantar y monitorizar servicios
# Crea a control, ml y gui y los comunica
# Si se caen los levanta de nuevo (Docker?)
sys.path += ["src"]
import control
from laptop_camera import LaptopCamera
from data_out import Out
import gui as g
import ml as m

def main():
    global dron, ctrl, gui, ml
   
    data_in = LaptopCamera()
    data_out = Out()
    gui = g.GUI()
    ml = m.ML()
    #dron = tellopy.Tello()
    #dron.connect()
    #dron.start_video()
    #ctrl = control.Control()
    #Setup interconnections    
    #ctrl.setDron(dron)
    #ctrl.setGui(gui)
    #ctrl.setMl(ml)

    gui.setDataIn(data_in)
    gui.setDataOut(data_out)
    gui.setAutonomousControl(ml)

    ml.setDataIn(data_in)
    #Empieza La GUI
    gui.start()
    

def endProgram():
    global dron, ctrl, gui, ml
    print("Out!")
    ml.quit()
    gui.quit()
    dron.quit()
    ctrl.quit()
    exit(0)
    dron.start_video()

def main2():
    #dron = new DronTello()
    #data_in = dron
    #data_out = dron
    #gui.start()
    pass

if __name__ == '__main__':
    main()
