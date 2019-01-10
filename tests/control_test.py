#Archivo de testeo del módulo de control
import control

ctrl = control.Control()
# ctrl_ins cannot be tested.

# ctrl_outs
imagen = ctrl.ml_out()
video_stream, dron_status, ml_prediction = ctrl.gui_out()
ctrl_command = ctrl.dron_out()

#print(imagen, video_stream, dron_status, ml_prediction, ctrl_command)