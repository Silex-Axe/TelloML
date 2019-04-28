import sys
import time
import tellopy

# Levantar y monitorizar servicios
# Crea a control, ml y gui y los comunica
# Si se caen los levanta de nuevo (Docker?)
sys.path += ["src"]
from laptop_camera import LaptopCamera
#from data_out import Out
from game_controller import GameController
from autonomous_control import AutonomousControl
import gui as g
import ml as m

def main():
    data_in = LaptopCamera()
    data_out = GameController()
    gui = g.GUI()
    autonomous_control = m.ML()

    gui.setDataIn(data_in)
    gui.setDataOut(data_out)
    gui.setAutonomousControl(autonomous_control)

    autonomous_control.setDataIn(data_in)
    #Empieza La GUI
    gui.start()       

if __name__ == '__main__':
    main()
